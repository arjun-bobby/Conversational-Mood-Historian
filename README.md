# Conversational Mood Historian

AI-powered personal mood tracker that records daily text/voice journals, detects emotions, and generates weekly "emotional weather reports."

## Features
- Log daily journal entries (text or voice-to-text)
- Sentiment & emotion detection (NLP)
- Trend charts (weekly/monthly)
- Automatic weekly mood summaries
- Data stored locally (CSV by default)

## Setup
```bash
git clone <repo-url>
cd conversational-mood-historian
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```
