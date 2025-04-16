# 🎣 Anti-Scam AI (Michel Casper Project)

Ce projet a pour but de **faire perdre du temps aux arnaqueurs téléphoniques** grâce à une intelligence artificielle vocale capable de tenir une conversation crédible, en simulant une fausse victime naïve.

---

## 🧠 Fonctionnalités

- 🎙️ Reconnaissance vocale de l'arnaqueur (Speech-to-Text via Google Cloud)
- 🤖 Génération de réponse crédible en streaming (LLM Nebius/Hugging Face)
- 🗣️ Synthèse vocale naturelle (Google Text-to-Speech)
- 🔁 Lecture audio en temps réel, phrase par phrase
- 🎭 Simulation de personnalité (Michel Casper : naïf, bavard, distrait)
- ⏱️ Objectif : retenir l’arnaqueur le plus longtemps possible sans éveiller de soupçons

---

## 👤 Personnage simulé

- **Nom** : Michel Casper  
- **Âge** : 45 ans  
- **Profil** : retraité naïf vivant à Paris, passionné par les timbres  
- **Caractère** : gentil, crédule, impatient, légèrement confus  
- **Langage** : hésitations, reformulations, digressions absurdes

---

## 📂 Fichiers du projet

- `anti-scam.py` ou `anti-scam-streaming.py` — Script principal
- `key.json` — Clé de service Google Cloud (ne pas partager publiquement)
- `requirements.txt` — Dépendances Python à installer

---

## 💻 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/anti-scam-ai.git
cd anti-scam-ai
