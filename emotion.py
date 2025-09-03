from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

_sid = SentimentIntensityAnalyzer()
_emotion = pipeline("text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    return_all_scores=True)

def predict(text: str):
    sentiment = _sid.polarity_scores(text)["compound"]
    scores = _emotion(text)[0]
    scores_sorted = sorted(scores, key=lambda x: x["score"], reverse=True)
    top = scores_sorted[0]["label"]
    probs = {d["label"]: float(d["score"]) for d in scores_sorted}
    return {"sentiment": sentiment, "emotion": top, "probs": probs}
