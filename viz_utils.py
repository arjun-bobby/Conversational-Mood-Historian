import matplotlib.pyplot as plt
import pandas as pd

def sentiment_line(df: pd.DataFrame):
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    grouped = df.groupby('date')['sentiment'].mean()
    fig, ax = plt.subplots()
    grouped.plot(ax=ax, marker="o")
    ax.set_title("Sentiment Trend")
    ax.set_ylabel("Sentiment (-1 to 1)")
    return fig

def emotion_bar(df: pd.DataFrame):
    counts = df['emotion'].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Emotion Distribution")
    return fig
