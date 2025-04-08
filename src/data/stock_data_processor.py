# Import necessary libraries
from arch import arch_model
import pandas as pd
import requests
import time

# Import settings from the config file
from config import settings

# ----------------------------------------------------------------------------------------------
# 1. Modularization: Save the wrangle function in a separate file for future importation
# ----------------------------------------------------------------------------------------------

"""
Save this function in a separate file (e.g., stock_data_processor.py) for reproducibility.

This process is called modularization. It helps in organizing code into reusable modules.
"""

# ----------------------------------------------------------------------------------------------
# 2. Create a class with the get_stock_data function as a method
# ----------------------------------------------------------------------------------------------


# Create a class to hold the get_stock_data method
class APIStockProcessor:
    """
    A class used to get stock data from the AlphaVantage API.

    Methods:
    --------
    - get_stock_data: Fetches stock data from the AlphaVantage API.
    - extract_returns: Computes daily returns and limits the dataset.
    - volatility_forecaster: Forecasts stock volatility using a GARCH model.
    """

    def __init__(self, api_key=settings.alpha_api_key):
        self.__api_key = api_key
        self.session = requests.Session()

    def get_stock_data(
        self,
        ticker: str,
        outputsize: str = "full",
        data_type: str = "json",
        limit: int = None,
    ) -> pd.DataFrame:
        """
        Fetch stock data from the AlphaVantage API.

        Parameters:
        ----------
        ticker : str
            The ticker symbol of the stock.
        outputsize : str, optional
            "compact" returns the latest 100 data points, "full" returns all available data.
        data_type : str, optional
            The format of the output data, defaults to "json".
        limit : int, optional
            The number of most recent records to retain.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing stock data with columns: open, high, low, close, volume.
        """
        # Create the URL
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY&"
            f"symbol={ticker}&"
            f"outputsize={outputsize}&"
            f"datatype={data_type}&"
            f"apikey={self.__api_key}"
        )
        # Make a GET request to the URL
        response = requests.get(url=url)

        # Check for HTTP errors
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Extract the data from the response
        response_data = response.json()
        stock_data = response_data.get("Time Series (Daily)", {})

        # Check if there is an error message in the response
        if "Error Message" in response_data:
            raise ValueError(
                f"Error encountered while fetching data: {response_data['Error Message']}"
            )

        # Check if the response contains valid data
        if not stock_data:
            raise ValueError(
                f"Invalid API call for {ticker}. Please enter a valid ticker symbol."
            )

        if "Note" in response_data:
            raise ValueError("Rate limit exceeded. Please wait and try again.")

        # Convert the data to a DataFrame and clean it
        df_stock = pd.DataFrame.from_dict(stock_data, orient="index", dtype=float)
        df_stock.index = pd.to_datetime(df_stock.index)  # Convert the index to datetime
        df_stock.index.name = "date"
        df_stock.columns = [
            col.split(". ")[1] for col in df_stock.columns
        ]  # Clean the headers
        # Apply limit if provided
        if limit:
            df_stock = df_stock.head(limit)

        return df_stock

    def extract_returns(self, df: pd.DataFrame, limit: int = 2500) -> pd.Series:
        """
        Calculate daily returns and return the most recent `limit` observations.

        Parameters:
        ----------
        df : pd.DataFrame
            DataFrame containing stock price data.
        limit : int, optional
            The number of most recent observations to retain (default is 2500).

        Returns:
        -------
        pd.Series
            Series containing daily percentage returns.
        """
        df = df.copy()  # Avoid modifying the original DataFrame

        # Sort DataFrame in ascending order by date
        df.sort_index(ascending=True, inplace=True)
        df["returns"] = df["close"].pct_change() * 100  # Calculate daily returns

        # Drop NaN values and retain only the last `n_observations`
        return df["returns"].dropna().iloc[-limit:]

    def volatility_forecaster(self, stock_data: pd.Series, n_days: int) -> dict:
        """
        Forecast the volatility of a stock for the next 'n' business days.

        Parameters:
        ----------
        stock_data (pd.Series): Time series of stock returns.
        n_days (int): Number of business days to forecast.

        Returns:
        -------
        dict
            Dictionary where each key is a business date in ISO 8601 format
            and each value is the predicted volatility.
        """
        # Fit the GARCH model
        model = arch_model(stock_data, p=1, q=1, rescale=False).fit(disp=0)

        # Generate forecasts
        forecasts = model.forecast(horizon=n_days, reindex=False).variance

        # Calculate forecast start date
        start_date = stock_data.index[-1] + pd.DateOffset(
            days=1
        )  # Get the last date in the stock data and add one day

        # Create date range for business days
        predicted_dates = pd.bdate_range(start=start_date, periods=n_days)

        # Extract predictions and take square root to get volatility
        volatility = forecasts.iloc[-1].values ** 0.5

        # Combine into a pandas Series
        predicted_output = pd.Series(
            volatility, index=[d.isoformat() for d in predicted_dates]
        )

        # Return as dictionary
        return predicted_output.to_dict()
