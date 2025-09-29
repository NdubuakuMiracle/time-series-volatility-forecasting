# Import necessary libraries
from arch import arch_model
import pandas as pd
import requests
import os

# ----------------------------------------------------------------------------------------------
# APIStockProcessor Class
# ----------------------------------------------------------------------------------------------

class APIStockProcessor:
    """
    A class used to get stock data from the AlphaVantage API.

    Methods:
    --------
    - get_stock_data: Fetches stock data from the AlphaVantage API.
    - extract_returns: Computes daily returns and limits the dataset.
    - volatility_forecaster: Forecasts stock volatility using a GARCH model.
    """

    def __init__(self, api_key=None):
        # First try env variable (Render)
        self.__api_key = api_key or os.getenv("ALPHA_API_KEY")
        if not self.__api_key:
            raise ValueError("Alpha Vantage API key not found. Please set ALPHA_API_KEY.")
        self.session = requests.Session()

    def get_stock_data(
        self,
        ticker: str,
        outputsize: str = "full",
        data_type: str = "json",
        limit: int = None,
    ) -> pd.DataFrame:
        """Fetch stock data from Alpha Vantage API."""
        
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY&"
            f"symbol={ticker}&"
            f"outputsize={outputsize}&"
            f"datatype={data_type}&"
            f"apikey={self.__api_key}"
        )

        # Debugging (optional: logs show in Render)
        print(f"DEBUG: Fetching {ticker} with API key {self.__api_key[:4]}...")

        response = requests.get(url=url)
        response.raise_for_status()

        response_data = response.json()

        if "Error Message" in response_data:
            raise ValueError(f"Error encountered while fetching data: {response_data['Error Message']}")
        if "Note" in response_data:
            raise ValueError("Rate limit exceeded. Please wait and try again.")
        if "Time Series (Daily)" not in response_data:
            raise Exception(f"Invalid API call for {ticker}. Please enter a valid ticker symbol.")

        stock_data = response_data["Time Series (Daily)"]

        df_stock = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)
        df_stock.index = pd.to_datetime(df_stock.index)
        df_stock.index.name = "date"
        df_stock.columns = [col.split(". ")[1] for col in df_stock.columns]

        if limit:
            df_stock = df_stock.head(limit)

        return df_stock

    def extract_returns(self, df: pd.DataFrame, limit: int = 2500) -> pd.Series:
        df = df.copy()
        df.sort_index(ascending=True, inplace=True)
        df["returns"] = df["close"].pct_change() * 100
        return df["returns"].dropna().iloc[-limit:]

    def volatility_forecaster(self, stock_data: pd.Series, n_days: int) -> dict:
        model = arch_model(stock_data, p=1, q=1, rescale=False).fit(disp=0)
        forecasts = model.forecast(horizon=n_days, reindex=False).variance
        start_date = stock_data.index[-1] + pd.DateOffset(days=1)
        predicted_dates = pd.bdate_range(start=start_date, periods=n_days)
        volatility = forecasts.iloc[-1].values ** 0.5
        predicted_output = pd.Series(volatility, index=[d.isoformat() for d in predicted_dates])
        return predicted_output.to_dict()
