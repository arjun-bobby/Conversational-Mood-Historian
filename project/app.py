import streamlit as st
from models.emotion import predict
from utils.io_utils import save_entry, load_entries
from utils.analytics import weekly_report
from utils import viz_utils

st.title("🧠 Conversational Mood Historian")

text = st.text_area("Today's journal entry", height=150)

if st.button("Analyze & Save") and text.strip():
    result = predict(text)
    save_entry(text, result)
    st.success(f"Saved! Emotion: {result['emotion']} | Sentiment: {result['sentiment']:.2f}")

df = load_entries()
if not df.empty:
    st.header("📊 Dashboard")
    st.pyplot(viz_utils.sentiment_line(df))
    st.pyplot(viz_utils.emotion_bar(df))

    st.header("🌦 Emotional Weather Report")
    st.text(weekly_report(df))
