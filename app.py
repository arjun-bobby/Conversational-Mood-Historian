import streamlit as st
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import os

# Optional HuggingFace emotion model
try:
    from transformers import pipeline
    hf_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    HF_AVAILABLE = True
except:
    HF_AVAILABLE = False

# Voice recognition
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

# ---------------- File Setup ----------------
DATA_FILE = "data/mood_journal.csv"
os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["timestamp", "entry", "sentiment", "emotion"]).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])

# ---------------- App UI ----------------
st.set_page_config(page_title="Conversational Mood Historian", layout="wide")
st.title("📝 Conversational Mood Historian")
st.write("Track your daily mood, visualize emotional trends, and receive personalized insights.")

# ---------------- Journal Entry ----------------
st.header("➕ Add a New Journal Entry")
entry = st.text_area("Type your journal entry here", height=120)

# ---------------- Voice Entry ----------------
if VOICE_AVAILABLE:
    st.subheader("🎤 Add Entry by Voice")
    if st.button("🎙️ Record Voice"):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            st.write("Listening for ~5 seconds...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized: {text}")
            entry = text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Could not connect to recognition service.")

# ---------------- Save Entry ----------------
analyzer = SentimentIntensityAnalyzer()
if st.button("💾 Save Entry"):
    if entry.strip():
        scores = analyzer.polarity_scores(entry)
        sentiment = scores["compound"]
        emotion = "N/A"
        if HF_AVAILABLE:
            result = hf_model(entry)[0]
            emotion = max(result, key=lambda x: x["score"])["label"]

        new_row = {"timestamp": datetime.now(), "entry": entry, "sentiment": sentiment, "emotion": emotion}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Entry saved!")
    else:
        st.warning("Please write something before saving.")

# ---------------- Data Overview ----------------
st.header("📊 Mood Journal Overview")
if not df.empty:
    st.subheader("Recent Entries")
    st.dataframe(df.tail(10), use_container_width=True)

    fig = px.line(df, x="timestamp", y="sentiment", title="Sentiment Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Weekly Report ----------------
    st.header("📅 Weekly Mood Report")
    last_week = df[df["timestamp"] > (datetime.now() - pd.Timedelta(days=7))]
    if not last_week.empty:
        avg_sentiment = last_week["sentiment"].mean()
        positive_days = (last_week["sentiment"] > 0.05).sum()
        negative_days = (last_week["sentiment"] < -0.05).sum()

        report = f"""
**Your Weekly Emotional Weather Report** 🌤️  
- Average Sentiment: {avg_sentiment:.2f}  
- Positive Days: {positive_days}  
- Negative Days: {negative_days}  
"""

        if avg_sentiment > 0.3:
            suggestion = "🎉 Great job! You’ve been generally positive this week. Keep doing what works for you."
        elif avg_sentiment < -0.3:
            suggestion = "🌧️ Mood has been low this week. Consider journaling about gratitude or talking to a friend."
        else:
            suggestion = "⛅ Mixed week — try adding positive routines like hobbies or exercise."

        st.markdown(report)
        st.info(suggestion)

        st.download_button("📥 Download Weekly Report", data=report + "\n\n" + suggestion, file_name="weekly_mood_report.txt")
    else:
        st.write("No entries this week yet. Start journaling today!")
else:
    st.write("No entries yet. Add your first journal entry above!")

