# app.py
import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Create or load CSV
DATA_FILE = "journal.csv"
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp", "entry", "sentiment"])

st.title("Conversational Mood Historian (MVP)")

# Input box
entry = st.text_area("Write today's journal:", height=150)

if st.button("Save Entry"):
    if entry.strip():
        score = analyzer.polarity_scores(entry)["compound"]
        new_row = {"timestamp": datetime.now().isoformat(), "entry": entry, "sentiment": score}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Saved! Sentiment score: {score:.2f}")
    else:
        st.warning("Please write something before saving.")

# Show past entries
st.subheader("Past Entries")
st.dataframe(df)

# Show sentiment trend
if not df.empty:
    st.line_chart(df.set_index("timestamp")["sentiment"])
