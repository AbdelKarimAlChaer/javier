# Javier — KI-Assistent für Gedanken

Javier ist ein KI-Assistent, der Notizen und Gedanken automatisch sortiert, kategorisiert und strukturiert. Die Web-App nutzt ein LLM (Anthropic Claude) als Verarbeitungs-Pipeline und speichert Einträge in MongoDB.

## Features

- Notizen eingeben und automatisch per KI kategorisieren lassen
- Automatisches Tagging via `tag_manager`
- Persistenz in MongoDB
- Einfache Web-UI (Flask + HTML/CSS/JS)

## Tech Stack

Python · Flask · Anthropic Claude API · MongoDB · python-dotenv

## Setup

### Voraussetzungen

- Python 3.10+
- MongoDB (lokal oder Atlas)
- Anthropic API Key ([console.anthropic.com](https://console.anthropic.com))

### Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/AbdelKarimAlChaer/javier.git
   cd javier
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env`-Datei erstellen:
   ```bash
   cp .env.example .env
   ```
   Dann `.env` befüllen:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   MONGO_URI=mongodb://localhost:27017/
   ```

5. App starten:
   ```bash
   python app.py
   ```
   Im Browser öffnen: `http://localhost:5000`

## Projektstruktur

```
javier/
├── app.py          # Flask-App & Routen
├── main.py         # Einstiegspunkt
├── llm.py          # Anthropic-Integration
├── pipeline.py     # Verarbeitungs-Pipeline
├── tag_manager.py  # Automatisches Tagging
├── writer.py       # Persistenz (MongoDB)
├── config.py       # Konfiguration
├── templates/      # HTML-Templates
├── Static/         # CSS & JS
└── requirements.txt
```
