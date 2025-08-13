import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
THRESHOLD = 2

load_dotenv()

STOCK_API_KEY = os.getenv("api")
NEWS_API_KEY = os.getenv("apiKey")
ACCOUNT_SID = os.getenv("account_sid")
AUTH_TOKEN = os.getenv("auth_token")
TWILIO_FROM = os.getenv("from_")
TWILIO_TO = os.getenv("to")


print("🔍 Fetching stock data...")

try:
    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK,
            "apikey": STOCK_API_KEY
        },
        timeout=10
    )
    response.raise_for_status()
    stock_data = response.json().get("Time Series (Daily)", {})

    if not stock_data:
        print("⚠ No stock data returned from API, using fallback test values.")
        today_price, yesterday_price = 350, 300  # Test data
    else:
        dates = list(stock_data.keys())
        today_price = float(stock_data[dates[0]]["4. close"])
        yesterday_price = float(stock_data[dates[1]]["4. close"])
except Exception as e:
    print(f"❌ Error fetching stock data: {e}")
    today_price, yesterday_price = 350, 300  # Fallback values

print(f"📊 Today's Close: {today_price}")
print(f"📊 Yesterday's Close: {yesterday_price}")


difference = today_price - yesterday_price
diff_per = round((difference / yesterday_price) * 100, 2)
updown = "📈" if diff_per > 0 else "📉"

print(f"📈 Change: {diff_per}% {updown}")


if abs(diff_per) >= THRESHOLD:
    print("📰 Significant change detected — fetching news...")

    try:
        news_params = {
            "q": COMPANY_NAME,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 3
        }
        news_response = requests.get("https://newsapi.org/v2/everything", params=news_params, timeout=10)
        news_response.raise_for_status()
        articles = news_response.json().get("articles", [])

        if not articles:
            print("⚠ No news articles found.")
        else:
            for article in articles:
                headline = article["title"]
                description = article.get("description", "No description available.")
                print(f"📰 {headline} — {description}")

                try:
                    client = Client(ACCOUNT_SID, AUTH_TOKEN)
                    message = client.messages.create(
                        from_=TWILIO_FROM,
                        body=f"{STOCK}: {diff_per}% {updown}\nHeadline: {headline}\nBrief: {description}",
                        to=TWILIO_TO
                    )
                    print(f"✅ SMS sent (SID: {message.sid})")
                except Exception as sms_error:
                    print(f"❌ Failed to send SMS: {sms_error}")
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
else:
    print("ℹ Change below threshold — no news fetched.")


