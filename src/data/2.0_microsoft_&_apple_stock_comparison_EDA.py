# Import necessary libraries
import sys
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

sys.path.append("../../src/data")
# Import API Stock data using the class in the stock_data_processor.py file
from stock_data_processor import APIStockProcessor

# ----------------------------------------------------------------------------------------------
# 1. Load the data from the API
# ----------------------------------------------------------------------------------------------
# Create an instance of the APIStockProcessor class
asp = APIStockProcessor()

# Get the stock data for Microsoft (MSFT) using the get_stock_data method
# The outputsize is set to 'full' to return the full-length time series
df_microsoft = asp.get_stock_data(ticker="MSFT")
df_microsoft = df_microsoft.head(2501)  # Limit the number of rows to 2501
print(df_microsoft.head())
print("Microsoft Stock Shape", df_microsoft.shape)
print(df_microsoft.info())

# Get the stock data for Apple (AAPL) using the get_stock_data method
df_apple = asp.get_stock_data(ticker="AAPL", outputsize="full")
df_apple = df_apple.head(2501)  # Limit the number of rows to 2501
print(df_apple.head())
print("Apple Stock Shape", df_apple.shape)
print(df_apple.info())

# ----------------------------------------------------------------------------------------------

# Visualize the closing price changes for Microsoft and Apple over the last decade
# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Plot the closing price for Microsoft and Apple
df_microsoft["close"].plot(ax=ax, label="Microsoft", color="red")
df_apple["close"].plot(ax=ax, label="Apple", color="blue")

# Add labels and title with white color
plt.xlabel("Date", color="white")
plt.ylabel("Closing Price", color="white")

# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

# Set the legend to black text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")

# Show the plot
plt.show()

"""
By comparing the closing prices of Microsoft and Apple, we can see that while Apple's stock
price initially exceeded Microsoft's, it fell below Microsoft's after the peak in 2021
price is higher than Apple's stock price. But this might be misleading because the stock
prices are not adjusted for splits and dividends.
To enable a fair evaluation of their performance, calculating the returns for both stocks
is necessary. The 'extract_returns' method in the AlphaVantageStockProcessor class will be
used to calculate the daily returns for Microsoft and Apple.
The 'extract_returns' method computes the daily returns and limits the dataset to
the most recent data 'limit' (default is 2500).
"""
# ----------------------------------------------------------------------------------------------
# 2. Extract the returns for Microsoft and Apple
# ----------------------------------------------------------------------------------------------

# Check if the 'extract_returns' method exists in the AlphaVantageStockProcessor class
print(hasattr(asp, "extract_returns"))  # Should return True

# Get the returns for Microsoft and Apple using the 'extract_returns' method
msft_stock_returns = asp.extract_returns(df_microsoft)
aapl_stock_returns = asp.extract_returns(df_apple)

# Print the first five rows of the returns for Microsoft
print(msft_stock_returns.head())
print(msft_stock_returns.shape)
print(type(msft_stock_returns))

# Print the first five rows of the returns for Apple
print(aapl_stock_returns.head())
print(aapl_stock_returns.shape)
print(type(aapl_stock_returns))

# ----------------------------------------------------------------------------------------------

# Visualize the returns for Microsoft and Apple
# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Plot the closing price for Microsoft and Apple
msft_stock_returns.plot(ax=ax, label="Microsoft", color="red")
aapl_stock_returns.plot(ax=ax, label="Apple", color="blue")

# Add labels and title with white color
plt.xlabel("Date", color="white")
plt.ylabel("Daily Return", color="white")

# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

# Set the legend with white text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")

# Show the plot
plt.show()

"""
Both stocks display significant fluctuations around the zero line, indicating varied investor sentiment.
A sharp increase in returns occurs around early 2021, likely linked to major market events.
Instances of substantial losses, especially for Apple, highlight periods of risk.
However: Both stocks exhibit comparable volatility, with occasional divergence in performance.
"""

# ----------------------------------------------------------------------------------------------

# Explore the histogram distribution of the daily returns for Microsoft and Apple
# This volatitly distribution doesn't consider time (Unonditional Volatility)

# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Plot the histogram of daily returns for Microsoft
msft_stock_returns.hist(ax=ax, bins=50, color="red", alpha=0.9, label="Microsoft")

# Plot the histogram of daily returns for Apple
aapl_stock_returns.hist(ax=ax, bins=50, color="blue", alpha=0.5, label="Apple")

# Add labels and title with white color
plt.xlabel("Daily Return", color="white")
plt.ylabel("Frequency", color="white")

# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

# Set the legend to black text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")

# Show the plot
plt.show()

"""
The returns follow an almost normal distribution, centered on 0, with a few outliers.
The distribution of returns for Microsoft and Apple is similar, with Microsoft having a slightly wider spread.
"""
# ----------------------------------------------------------------------------------------------
# 3. Compute the daily volatility of the two stocks
# ----------------------------------------------------------------------------------------------

# Calculate the standard deviation of the daily return for Microsoft and Apple
microsoft_volatility = msft_stock_returns.std()
apple_volatility = aapl_stock_returns.std()
# Print the standard deviation of the daily return for Microsoft and Apple
print("Daily Volatility for Microsoft:", microsoft_volatility)
print("Daily Volatility for Apple:", apple_volatility)


# Calculate the mean daily return for Microsoft and Apple
mean_msft_return = msft_stock_returns.mean()
mean_aapl_return = aapl_stock_returns.mean()
# Print the mean daily return for Microsoft and Apple
print("Mean Daily Return for Microsoft:", mean_msft_return)
print("Mean Daily Return for Apple:", mean_aapl_return)

"""
The daily volatility of Apple is slightly higher than that of Microsoft, indicating that Apple's stock
returns fluctuate more significantly on a daily basis. However, the mean daily return for Apple
is lower than that of Microsoft, suggesting that Apple's stock has a lower average return per day.
"""

# ----------------------------------------------------------------------------------------------

# Calculate the annualized volatility for Microsoft and Apple
annualized_microsoft_volatility = microsoft_volatility * (252**0.5)
annualized_apple_volatility = apple_volatility * (252**0.5)

# Print the annualized volatility for Microsoft and Apple
print("Annualized Volatility for Microsoft:", annualized_microsoft_volatility)
print("Annualized Volatility for Apple:", annualized_apple_volatility)

"""
The annualized volatility provides a better understanding of the risk associated with each stock over a year.
Microsoft has an annualized volatility of 27, while Apple has an annualized volatility of 37. This indicates
that Apple's stock is riskier than Microsoft's stock over a year, as it has a higher annualized volatility.
"""

# ----------------------------------------------------------------------------------------------

# Calculate the rolling 30-day volatility for Microsoft and Apple to see how they change over time
rolling_microsoft_volatility = msft_stock_returns.rolling(window=30).std().dropna()
rolling_apple_volatility = aapl_stock_returns.rolling(window=30).std().dropna()

# Print the rolling 30-day volatility for Microsoft and Apple
print(rolling_microsoft_volatility.head())
print(rolling_microsoft_volatility.shape)
print(rolling_apple_volatility.head())
print(rolling_apple_volatility.shape)

"""
The rolling 30-day volatility provides a more dynamic view of the risk associated with each stock.
By calculating the standard deviation of the daily returns over a 30-day window, is is observable how the
volatility changes over time which is a valuable information for investors looking to assess the risk.
"""

# ----------------------------------------------------------------------------------------------

# Visualize the rolling 30-day volatility for Microsoft
# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Plot the rolling 30-day volatility for Microsoft
msft_stock_returns.plot(ax=ax, label="Daily Return")
rolling_microsoft_volatility.plot(
    ax=ax, label="30 Days Rolling Volatility", color="red", linewidth=3
)
# Add labels and title with white color
plt.xlabel("Date", color="white")
plt.ylabel("Rolling 30-Day Volatility", color="white")
plt.title("Microsoft", color="white")
# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")
# Set the legend to black text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")
# Show the plot
plt.show()

# Visualize the rolling 30-day volatility for Apple
# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
# Plot the rolling 30-day volatility for Microsoft
aapl_stock_returns.plot(ax=ax, label="Daily Return")
rolling_apple_volatility.plot(
    ax=ax, label="30 Days Rolling Volatility", color="white", linewidth=3
)
# Add labels and title with white color
plt.xlabel("Date", color="white")
plt.ylabel("Rolling 30-Day Volatility", color="white")
plt.title("Apple", color="white")
# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")
# Set the legend to black text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")
# Show the plot
plt.show()

"""
The volatility for Microsoft is relatively stable, with occasional spikes,
while Apple's volatility is more erratic, with frequent fluctuations.
"""

# ----------------------------------------------------------------------------------------------

# Visualize the squared returns for Microsoft and Apple
# Create a figure and axis with a dark background
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Plot the closing price for Microsoft and Apple
(msft_stock_returns**2).plot(ax=ax, label="Microsoft", color="red")
(aapl_stock_returns**2).plot(ax=ax, label="Apple", color="blue")

# Add labels and title with white color
plt.xlabel("Date", color="white")
plt.ylabel("Daily Return", color="white")

# Set the color of the tick labels to white
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

# Set the legend to black text
legend = plt.legend()
for text in legend.get_texts():
    text.set_color("black")

# Show the plot
plt.show()

"""
The squared returns provide a measure of the volatility of the stock, with higher values indicating
greater volatility. By squaring the returns, the negative values are removed, allowing for a clearer view
of the volatility patterns.
"""
# ----------------------------------------------------------------------------------------------

# Create an ACF plot for the squared returns of Microsoft and Apple to determine the ideal number
# of lags for the ARCH model
# Create a figure and axis with a dark background
fig, ax = plt.subplots(2, 1, figsize=(15, 10))
fig.patch.set_facecolor("black")
ax[0].set_facecolor("black")
ax[1].set_facecolor("black")

# Plot the ACF for the squared returns of Microsoft
plot_acf(msft_stock_returns**2, ax=ax[0])
ax[0].set_title("ACF - Microsoft Squared Returns", color="white")
ax[0].tick_params(axis="x", colors="white")
ax[0].tick_params(axis="y", colors="white")

# Plot the ACF for the squared returns of Apple
plot_acf(aapl_stock_returns**2, ax=ax[1])
ax[1].set_title("ACF - Apple Squared Returns", color="white")
ax[1].tick_params(axis="x", colors="white")
ax[1].tick_params(axis="y", colors="white")

# Add labels and title with white color
fig.text(0.5, 0.04, "Lag [Days]", ha="center", color="white")
fig.text(
    0.04,
    0.5,
    "Correlation Coefficient",
    va="center",
    rotation="vertical",
    color="white",
)

# Show the plot
plt.show()

# ----------------------------------------------------------------------------------------------

# Create a PACF plot for the squared returns of Microsoft and Apple to determine the ideal number
# of lags for the ARCH model
# Create a figure and axis with a dark background
fig, ax = plt.subplots(2, 1, figsize=(15, 10))
fig.patch.set_facecolor("black")
ax[0].set_facecolor("black")
ax[1].set_facecolor("black")

# Plot the PACF for the squared returns of Microsoft
plot_pacf(msft_stock_returns**2, ax=ax[0])
ax[0].set_title("PCF - Microsoft Squared Returns", color="white")
ax[0].tick_params(axis="x", colors="white")
ax[0].tick_params(axis="y", colors="white")

# Plot the PACF for the squared returns of Apple
plot_pacf(aapl_stock_returns**2, ax=ax[1])
ax[1].set_title("PACF - Apple Squared Returns", color="white")
ax[1].tick_params(axis="x", colors="white")
ax[1].tick_params(axis="y", colors="white")

# Add labels and title with white color
fig.text(0.5, 0.04, "Lag [Days]", ha="center", color="white")
fig.text(
    0.04,
    0.5,
    "Correlation Coefficient",
    va="center",
    rotation="vertical",
    color="white",
)

# Show the plot
plt.show()

"""
ACF: Both companies demonstrate volatility clustering, indicated by the significant spikes at lag 0,
but Microsoft shows a more prolonged correlation pattern, suggesting higher persistence
in its volatility compared to Apple.
PACF: Both stocks exhibit a short memory in their volatility, with the majority of
correlation diminishing quickly after the first lag.
But Microsoft's shows that a lag of 3 days is possible.
"""
