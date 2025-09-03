import pandas as pd

def weekly_report(df: pd.DataFrame) -> str:
    if df.empty:
        return "No entries yet."
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    last7 = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=7))]
    prev7 = df[(df['date'] < last7['date'].min()) & 
               (df['date'] >= (df['date'].max() - pd.Timedelta(days=14)))]
    msg = []
    if not last7.empty:
        msg.append(f"Average sentiment last 7 days: {last7['sentiment'].mean():.2f}")
        top_emotion = last7['emotion'].mode()[0]
        msg.append(f"Most common emotion: {top_emotion}")
    if not prev7.empty:
        change = last7['sentiment'].mean() - prev7['sentiment'].mean()
        msg.append(f"Change vs previous week: {change:+.2f}")
    return "\n".join(msg)
