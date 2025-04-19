import requests
from textblob import TextBlob
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# INPUT STOCK SYMBOL
ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple): ").upper()
company_name = ticker  # Use ticker as company name in News API search

# Get custom date range for stock data
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Validate date format
try:
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

# FETCHING NEWS FROM NEWSAPI 
print(f"\nFetching news for {company_name}...")

API_KEY = "964891c96bfc484393ba18e558b7488f"  # API key
url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

if data.get("status") != "ok":
    print("Failed to fetch news.")
    exit()

articles = data["articles"]
print(f"Fetched {len(articles)} news articles for {company_name}.\n")

# PERFORM SENTIMENT ANALYSIS
positive, negative, neutral = 0, 0, 0
rows = []

print("Analyzing sentiment for top 10 headlines:\n")

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

    print(f"[{sentiment_label}] {headline}")
    rows.append({"Headline": headline, "Sentiment": sentiment_label, "Score": sentiment_score})

#------
df = pd.DataFrame(rows)
csv_filename = f"{ticker}_news_sentiment.csv"
df.to_csv(csv_filename, index=False)
print(f"\nSaved sentiment results to {csv_filename}")

# === MATPLOTLIB ===
labels = ['Positive', 'Negative', 'Neutral']
counts = [positive, negative, neutral]
colors = ['green', 'red', 'gray']

plt.figure(figsize=(6, 4))
plt.bar(labels, counts, color=colors)
plt.title(f"Sentiment Breakdown for {company_name}")
plt.ylabel("Number of Articles")
plt.xlabel("Sentiment")
plt.tight_layout()
plt.show()

# === FETCH STOCK DATA ===
print(f"\nFetching stock price data for {ticker} from {start_date} to {end_date}...")

stock_data = yf.download(ticker, start=start_date, end=end_date)

if stock_data.empty:
    print("No stock data found for the given range.")
else:
    print("\nStock Price Preview:")
    print(stock_data[["Close"]].head())

    stock_data["Close"].plot(
        title=f"{ticker} Closing Prices ({start_date} to {end_date})",
        ylabel="Price (USD)",
        xlabel="Date",
        grid=True,
        figsize=(10, 5)
    )
    plt.tight_layout()
    plt.show()
