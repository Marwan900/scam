from huggingface_hub import InferenceClient
from google.cloud import texttospeech, speech
import os
import sounddevice as sd
import soundfile as sf
import pyaudio
import io
import wave

# LLM client setup (streaming LLM)
llm_client = InferenceClient(
    provider="nebius",
    api_key="YOUR_API_KEY",
)

# Authentification GCP
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Setup client TTS
tts_client = texttospeech.TextToSpeechClient()
voice_params = texttospeech.VoiceSelectionParams(
    language_code='fr-FR',
    name='fr-FR-Chirp-HD-O',
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

# Fonction de lecture audio WAV avec PyAudio
def play_audio(audio_bytes):
    with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()

# Contexte initial
context = "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur..."
messages = [
    {"role": "system", "content": context}
]

while True:
    # 1. Enregistrement de la voix
    duration = 5  # secondes
    sample_rate = 44100
    print("🎤 Enregistrement...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    sf.write('voice.flac', audio_data, sample_rate)
    print("✅ Enregistrement terminé.")

    # 2. Transcription vocale avec Google STT
    speech_client = speech.SpeechClient()
    with open("voice.flac", "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(sample_rate_hertz=44100, language_code="fr-FR")
    result = speech_client.recognize(config=config, audio=audio)

    if len(result.results) == 0:
        print("⚠️ Aucune voix détectée.")
        continue

    user_input = result.results[0].alternatives[0].transcript
    print("👤 Escroc :", user_input)
    messages.append({"role": "user", "content": user_input})

    # 3. Réponse en streaming du LLM + TTS phrase par phrase
    completion = llm_client.chat.completions.create(
        model="Qwen/Qwen2.5-32B-Instruct",
        messages=messages,
        max_tokens=1512,
        stream=True,
        temperature=0.9
    )

    print("🤖 Michel : ", end="", flush=True)
    reponse = ""
    buffer = ""

    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            reponse += content
            buffer += content

            if any(p in buffer for p in [".", "!", "?", "\n"]):
                synthesis_input = texttospeech.SynthesisInput(text=buffer.strip())
                tts_response = tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice_params,
                    audio_config=audio_config
                )
                play_audio(tts_response.audio_content)
                buffer = ""

    print()
    messages.append({"role": "assistant", "content": reponse})
