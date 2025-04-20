import streamlit as st
import requests
from textblob import TextBlob
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Stock News Sentiment Analyzer", layout="centered")

st.title("Stock Market News Sentiment Analyzer")

# COMPANY AND DATE INPUTS
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, INFY)", value="AAPL").upper()
start_date = st.date_input("Start Date", datetime(2024, 3, 1))
end_date = st.date_input("End Date", datetime(2024, 4, 1))

if st.button("Analyze"):
    company_name = ticker
    API_KEY = "964891c96bfc484393ba18e558b7488f"  # Replace with your NewsAPI key

    # === FETCH NEWS ===
    st.subheader("📰 News Sentiment")
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok" or not data["articles"]:
        st.error("Failed to fetch news or no news available.")
        st.stop()

    articles = data["articles"]
    positive, negative, neutral = 0, 0, 0
    rows = []

    for article in articles[:10]:
        headline = article["title"]
        sentiment_score = TextBlob(headline).sentiment.polarity

        if sentiment_score > 0.1:
            sentiment_label = "Positive"
            positive += 1
        elif sentiment_score < -0.1:
            sentiment_label = "Negative"
            negative += 1
        else:
            sentiment_label = "Neutral"
            neutral += 1

        rows.append({"Headline": headline, "Sentiment": sentiment_label, "Score": sentiment_score})

    # DISPLAY SENTIMENT SUMMARY 
    st.write(f"**Total Articles Analyzed:** {len(rows)}")

    sentiment_counts = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [positive, negative, neutral]
    })

    st.bar_chart(sentiment_counts.set_index("Sentiment"))

    # DISPLAY TABLE OF HEADLINES 
    df = pd.DataFrame(rows)
    st.subheader("🗞️ Headlines Analyzed")
    st.dataframe(df)

    #FETCH STOCK DATA 
    st.subheader("📉 Stock Price Trend")
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.warning("No stock data available for the selected date range.")
    else:
        st.line_chart(stock_data["Close"])
        st.caption(f"Closing prices for {ticker} from {start_date} to {end_date}")
