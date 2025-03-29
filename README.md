# Time-Series Volatility Forecasting 

## Project Overview  
This project performs a **comprehensive financial time series analysis and volatility forecasting** for stocks, specifically **Microsoft (MSFT) and Apple (AAPL)**. It includes:  
- **Volatility modeling** using **GARCH**  
- An **interactive Streamlit web application** for real-time forecasting  
- **Exploratory Data Analysis (EDA)** to compare price trends and risk characteristics  
- **Dynamic visualizations** to analyze stock performance  

The **forecasting web application is hosted on Render**, providing an accessible platform for users to interactively forecast stock volatility and explore historical trends.  

---

## Project Structure  

### 1️⃣ Data Import & Processing  
- **Data Source**: Stock price data is **fetched dynamically** from the **Alpha Vantage API**.  
- **Processor**: The `APIStockProcessor` class handles:  
  - Retrieving stock data  
  - Data cleaning and transformation  
  - Computation of **daily returns**  

### 2️⃣ Exploratory Data Analysis (EDA) - Microsoft vs. Apple  
A comparative **EDA** is performed to understand the differences in price movement, risk exposure, and volatility characteristics between **Microsoft (MSFT) and Apple (AAPL)** stocks.  

- **Price Trends & Returns**:  
  - **Closing Prices**: Visual comparison of long-term stock performance.  
  - **Daily Returns Distribution**: Analysis of risk and return profiles.  

- **Volatility & Risk Assessment**:  
  - **Rolling 30-Day Volatility**: Measures fluctuations over time.  
  - **Squared Returns Plot**: Identifies **volatility clustering** (essential for GARCH modeling).  
  - **Autocorrelation Analysis (ACF & PACF)**: Detects patterns in stock volatility.  
  - **Annualized Volatility Calculation**:  
    - Apple stock demonstrates **higher annualized volatility**, implying **greater risk exposure**.  
    - Microsoft stock exhibits **more stable return patterns**.  

### 3️⃣ Volatility Forecasting - GARCH Model  
The **GARCH (Generalized Autoregressive Conditional Heteroskedasticity) model** is employed to model and forecast Microsoft's (MSFT) stock price volatility.  

- **Model Insights**:  
  - The **mean return (μ)** is statistically significant, confirming **non-zero expected returns**.  
  - **GARCH Parameters**:  
    - **ω (Omega)**: Baseline volatility (not significant).  
    - **α (Alpha[1])**: Past stock shocks **strongly influence** current volatility.  
    - **β (Beta[1])**: High persistence in volatility, meaning past fluctuations impact future volatility significantly.  

- **Practical Use**:  
  - Traders can use these insights to assess **risk periods**.  
  - Investors can incorporate **volatility predictions** into their trading strategies.  

---

## Deployment  

### 🌐 Interactive Forecasting App (Streamlit)  
A **fully interactive web app** built with **Streamlit** enables users to:  
✅ **Input a stock ticker** (e.g., AAPL, TSLA, MSFT).  
✅ **Choose data limit** (full dataset or a custom limit).  
✅ **Set forecast days** (1-30 days).  
✅ **Enable annualized volatility** (optional).  
✅ Fetch **live stock data**  
✅ Compute **returns & volatility**  
✅ Visualize **trend charts**, **returns**, and **forecasted volatility**.  

**App Deployment:** Hosted on **Render** for real-time access.  
[![Deployed on Render](https://img.shields.io/badge/Render-Live%20App-blue)](https://time-series-volatility-forecasting.onrender.com)

---

## 📁 Key Files & Scripts  

| File | Description |
|------|------------|
| `1.0_importing_stock_data_from_api.py` | Fetches stock data from **Alpha Vantage API** and processes it for analysis. |
| `2.0_microsoft_&_apple_stock_comparison_EDA.py` | **Exploratory Data Analysis (EDA)** comparing Microsoft & Apple stocks, including price trends, volatility, and autocorrelation. |
| `3.0_forecasting_volatility.py` | Implements **GARCH model** for stock volatility forecasting, with model evaluation and parameter analysis. |
| `stock_data_processor.py` | Defines the **APIStockProcessor** class for retrieving, processing, and analyzing stock data. |
| `forecasting_app.py` | The **Streamlit app** that provides an interactive interface for stock forecasting. |

---

## 📌 Installation & Setup  

To run the project locally, install the required dependencies:  

```bash
pip install pandas numpy matplotlib statsmodels arch streamlit plotly python-dotenv pydantic
