# 📌 Stock Data Source: Alpha Vantage  

Stock price data in this project is sourced from **Alpha Vantage**, a widely used financial market data provider. The **Alpha Vantage API** allows access to real-time and historical stock data, including:  

- **Time-series stock prices** (daily, weekly, monthly)  
- **Intraday price data**  
- **Technical indicators**  
- **Fundamental data**  

## 🔗 API Access  
To use Alpha Vantage, an **API key** is required. A free API key can be obtained from:  
🔗 [Alpha Vantage API](https://www.alphavantage.co/support/#api-key)  

## 📥 Example API Request  
Stock data can be fetched via a simple HTTP request:  

```bash
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=YOUR_API_KEY
