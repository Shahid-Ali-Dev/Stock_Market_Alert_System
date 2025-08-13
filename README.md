# 📊 Stock Market Alert System

This Python script monitors the stock price of a chosen company (default: Tesla Inc) using the **Alpha Vantage API**.  
If the stock price changes by more than a set threshold percentage, it fetches the latest related news from the **NewsAPI** and sends an **SMS alert** via **Twilio**.

---

## 🚀 Features
- **Live stock data** from Alpha Vantage.
- **Automatic percentage change calculation** between yesterday and today's closing prices.
- **News fetching** from NewsAPI when price movement exceeds a threshold.
- **SMS notifications** using Twilio API.
- **Fallback mode** with test data if APIs fail.
- **Environment variable support** for API keys and credentials.

---

## 🛠 Requirements
- Python 3.7+
- Alpha Vantage API key
- NewsAPI API key
- Twilio account & credentials
- Required Python packages:
  ```bash
  pip install python-dotenv requests twilio
