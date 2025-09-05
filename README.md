# 🎤 AI Mood Journal (Streamlit)

An AI-powered mood journal that allows users to **speak their thoughts** 🎙️,  
analyzes them using **NLP emotion detection**, stores them in a database,  
and generates **reports & suggestions** 📊✨.

---

## 🚀 Features
- 🎤 Speech input (no typing required!)
- 🤖 Emotion analysis with Hugging Face Transformers
- 🗄️ Data stored in SQLite
- 📊 Interactive mood trends visualization
- 💡 Personalized well-being suggestions

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python (SQLite database)
- **AI Model:** `j-hartmann/emotion-english-distilroberta-base`
- **Deployment:** Hugging Face Spaces

---

## ▶️ Run Locally
```bash
git clone https://huggingface.co/spaces/YourUsername/mood-journal
cd mood-journal
pip install -r requirements.txt
streamlit run app.py
