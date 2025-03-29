# Import necessary libraries
import pandas as pd
import requests

# Import settings from the config file
from config import settings


# ----------------------------------------------------------------------------------------------
# 1. Load the data from the API
# ----------------------------------------------------------------------------------------------

# Create a dynamic URL using all the parameters listed in the AlphaVantge documentation
# https://www.alphavantage.co/documentation/#daily

ticker = "MSFT"  # ticker symbol for Microsoft
outputsize = (
    "compact"  # compact returns the latest 100 data points in the daily time series
)
data_type = "json"  # json format for the data

url = (
    "https://www.alphavantage.co/query?"
    "function=TIME_SERIES_DAILY&"
    f"symbol={ticker}&"
    f"outputsize={outputsize}&"
    f"data_type={data_type}&"
    f"apikey={settings.alpha_api_key}"
)  # Use the API key from the settings

print("url type:", type(url))  # Print the URL type to check if it is correct

# ----------------------------------------------------------------------------------------------

# Make a GET request to the URL
response = requests.get(url=url)
# Check the type of the response
print("response type:", type(response))

# Check the response
dir(response)

# Check the status code of the response
response_code = response.status_code
print("response code type:", type(response_code))
print(response_code)

# Check the response text
response_text = response.text
print("response_text type:", type(response_text))
print(response_text[:200])

# Check the response JSON
response_data = response.json()
print("response_data type:", type(response_data))


# Check the keys in the response data
print("response_data keys:", response_data.keys())


# Extract the "Time Series (Daily)" data from the response data
# This is the data we are interested in
stock_data = response_data["Time Series (Daily)"]
# Check the type of the stock_data
print("stock_data type:", type(stock_data))

# Check the data for one of the keys in the stock_data
print("stock_data['2025-03-21']:", stock_data["2025-03-21"])

# ----------------------------------------------------------------------------------------------
# 2. Read the data to a DataFrame
# ----------------------------------------------------------------------------------------------

# Convert the stock_data to a DataFrame
df_microsoft = pd.DataFrame.from_dict(
    stock_data, orient="index", dtype="float"
)  # Add dtypes="float" because the data is in string format
# Make the date headings the index

# Check the shape, head, and info of the DataFrame
df_microsoft.shape
df_microsoft.head()
df_microsoft.info()

# ----------------------------------------------------------------------------------------------

# Clean the data by converting the index to a datetime object
df_microsoft.index = pd.to_datetime(df_microsoft.index)

# Give the index a name
df_microsoft.index.name = "date"
# Check the head and info of the DataFrame
df_microsoft.head()
df_microsoft.info()

# Clean the headers by removing the "number" prefix from the columns names
df_microsoft.columns = [col.split(". ")[1] for col in df_microsoft.columns]
# Check the head and info of the DataFrame
df_microsoft.head()
df_microsoft.info()


# ----------------------------------------------------------------------------------------------
# 3. Incorporate the data cleaning steps into a function to get data from the AlphaVantage API
# ----------------------------------------------------------------------------------------------


# The function to get the stock data from the AlphaVantage API
def get_stock_data(ticker: str, outputsize: str, data_type="json") -> pd.DataFrame:
    """
    Get the stock data from the AlphaVantage API.

    Parameters:
    ticker (str): The ticker symbol of the stock.
    outputsize (str): The size of the output data (compact or full),
    where compact returns the latest 100 data points. Full returns the full-length time series.
    data_type (str): The format of the output data set to json by default.

    Returns:
    pd.DataFrame: A DataFrame containing the stock data.
    The columns are: open, high, low, close, volume.The index is the date.
    """
    # Create the URL
    url = (
        "https://www.alphavantage.co/query?"
        "function=TIME_SERIES_DAILY&"
        f"symbol={ticker}&"
        f"outputsize={outputsize}&"
        f"data_type={data_type}&"
        f"apikey={settings.alpha_api_key}"
    )

    # Make a GET request to the URL
    response = requests.get(url=url)

    # Extract the data from the response
    response_data = response.json()
    stock_data = response_data["Time Series (Daily)"]

    # Convert the data to a DataFrame and clean it
    df_stock = pd.DataFrame.from_dict(stock_data, orient="index", dtype="float")
    df_stock.index = pd.to_datetime(df_stock.index)
    df_stock.index.name = "date"
    df_stock.columns = [col.split(". ")[1] for col in df_stock.columns]

    return df_stock


# ----------------------------------------------------------------------------------------------
# 4. Use the function to get data for different stocks
# ----------------------------------------------------------------------------------------------

# Get the stock data for Apple (AAPL
df_apple = get_stock_data("AAPL", "compact")  # Get the latest 100 data points

# Check the shape, head, and info of the DataFrame
print("Apple Stock Shape:", df_apple.shape)
df_apple.head()
df_apple.info()


# Get the stock data for Google (GOOGL)
df_google = get_stock_data("GOOGL", "compact")  # Get the latest 100 data points

# Check the shape, head, and info of the DataFrame
print("Google Stock Shape:", df_google.shape)
df_google.head()
df_google.info()
