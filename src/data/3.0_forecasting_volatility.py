# Import necessary libraries
import sys
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model

sys.path.append("../../src/data")
# Import API Stock data using the class in the stock_data_processor.py file
from stock_data_processor import APIStockProcessor

# ----------------------------------------------------------------------------------------------
# 1. Use the APIStockProcessor class to prepare the stock for Microsoft
# ----------------------------------------------------------------------------------------------
# Create an instance of the APIStockProcessor class
asp = APIStockProcessor()

# Get the stock data for Microsoft (MSFT) using the get_stock_data method
df_microsoft = asp.get_stock_data(ticker="MSFT")
print(df_microsoft.head())
print("Full MSFT stock data", df_microsoft.shape)
# Get the returns for Microsoft using the 'extract_returns' method
msft_stock_returns = asp.extract_returns(df_microsoft)

# Print the first five rows of the returns for Microsoft
print(msft_stock_returns.head())
print(msft_stock_returns.shape)
print(type(msft_stock_returns))

# ----------------------------------------------------------------------------------------------
# 2. Split the data into training set that contains the first 80% of the data
# ----------------------------------------------------------------------------------------------

# Calculate the index for the training set
int(0.8 * len(msft_stock_returns))

# Create the training set
msft_train = msft_stock_returns[: int(0.8 * len(msft_stock_returns))]
print(msft_train.shape)
print(msft_train.head())
print(msft_train.tail())

# ----------------------------------------------------------------------------------------------
# 3. Build and Iterate on the Model
# ----------------------------------------------------------------------------------------------

# Initialize the model parameters and fit the model
model = arch_model(
    msft_train,
    p=1,
    q=1,
    rescale=False,  # Avoid rescaling the data for easier interpretation
).fit(
    disp="off"
)  # Turn off the convergence output to suppress the fiting output

# Print the model summary to understand the model parameters
print(model.summary())

"""
The model summary provides the following information:

- The mean return (mu) is positive and statistically significant,
indicating that the average return is significantly different from zero.
- The GARCH model parameters (omega, alpha[1], and beta[1]) describe the volatility dynamics of the returns:
  - **omega** is not statistically significant, meaning that
  the constant term in the volatility equation may not be necessary.
  - **alpha[1]** is statistically significant, indicating that past
  squared residuals (shocks) have a significant impact on current volatility.
  - **beta[1]** is highly statistically significant, indicating that 
  past volatility has a strong influence on current volatility.
- The high value of **beta[1]** (0.8106) suggests that volatility is persistent,
meaning that high volatility periods tend to be followed by high volatility periods.

Overall, the model captures the volatility clustering commonly observed in financial time series, where 
periods of high volatility are followed by high volatility and periods of low volatility are followed by low volatility.
"""

# ----------------------------------------------------------------------------------------------
# 4. Plot the model diagnostics
# ----------------------------------------------------------------------------------------------

# Plot the time series of the msft_train data and the model's conditional volatility
fig = plt.figure(figsize=(15, 8))
fig.patch.set_facecolor("black")
plt.style.use("dark_background")

plt.plot(msft_train, label="MSFT Returns", color="Orange")
plt.plot(
    2 * model.conditional_volatility, label="2 SD Conditional Volatility", color="blue"
)  # Multiply by 2 for better visualization
plt.plot(
    -2 * model.conditional_volatility.rename(), color="blue"
)  # Multiply by -2 for better visualization
plt.title("MSFT Returns and Conditional Volatility")
plt.legend()
plt.show()

# Plot the model diagnostics
model.plot()
plt.show()

"""
The plot shows the following diagnostics:
- The standardized residuals are normally distributed with a mean close to zero.
- The model performs well in capturing the volatility clustering in the data.
"""

# ----------------------------------------------------------------------------------------------

# Plot a histogram of the standardized residuals to better understand the normality assumption
plt.figure(figsize=(15, 8))
fig.patch.set_facecolor("black")
plt.style.use("dark_background")

plt.hist(model.resid, bins=25, color="skyblue", edgecolor="black")
plt.title("Distribution of Standardized Residuals")
plt.show()

# ----------------------------------------------------------------------------------------------

# Plot the autocorrelation and partial autocorrelation functions of the standardized residuals
fig, ax = plt.subplots(2, 1, figsize=(15, 10))
fig.patch.set_facecolor("black")

plot_acf(model.resid, ax=ax[0], color="skyblue")
ax[0].set_title("Autocorrelation of Standardized Residuals")

plot_pacf(model.resid, ax=ax[1], color="skyblue")
ax[1].set_title("Partial Autocorrelation of Standardized Residuals")

plt.tight_layout()
plt.show()

"""
The plots show that the residuals are not correlated, which means that the model
adequately captures the information in the data.
The lack of significant autocorrelation suggests that the model has
adequately captured the volatility dynamics of the returns.
"""

# ----------------------------------------------------------------------------------------------
# 5. Forecasting Volatility
# ----------------------------------------------------------------------------------------------

# Forecast the volatility for the next 10 days
forecast_horizon = 10
forecasted_volatility = (
    model.forecast(
        horizon=forecast_horizon, reindex=False  # Avoid reindexing the data
    ).variance
    ** 0.5
)  # Take the square root of the variance to get the volatility
forecasted_volatility

# ----------------------------------------------------------------------------------------------

# Model walk-fforward validation forecast on the test set to evaluate the model's performance
# Create an empty list to store the forecasted volatility
forecasted_volatility = []
test_size = int(len(msft_stock_returns) * 0.2)

# Iterate over the test set to forecast the volatility
for i in range(test_size):
    # Create the test set
    msft_test = msft_stock_returns.iloc[
        : -(test_size + i)
    ]  # The +i includes the current day
    # Fit the model on the test set
    model = arch_model(
        msft_test,
        p=1,
        q=1,
        rescale=False,
    ).fit(disp=0)

    # Forecast the volatility for the next day
    forecasted_volatility.append(
        model.forecast(horizon=1, reindex=False).variance.iloc[0, 0]
        ** 0.5  # The [0, 0] index is used to extract the forecasted volatility
    )

# Convert the forecasted volatility to a Series
forecasted_volatility = pd.Series(
    forecasted_volatility, index=msft_stock_returns.tail(test_size).index
)
forecasted_volatility.head()
forecasted_volatility.shape

# ----------------------------------------------------------------------------------------------

# Plot the time series of the walk-forward predicted volatility and the returns
fig = plt.figure(figsize=(15, 8))
fig.patch.set_facecolor("black")
plt.style.use("dark_background")

# Plot the MSFT returns, the predicted volatility, and the 2 SD confidence interval
plt.plot(msft_stock_returns.tail(test_size), label="MSFT Returns", color="Orange")
plt.plot(
    2 * forecasted_volatility, label="2 SD Predicted Volatility", color="blue"
)  # Multiply by 2 SD for better visualization
plt.plot(
    -2 * forecasted_volatility.rename(), color="blue"
)  # Multiply by -2 for better visualization
plt.title("MSFT Returns and Predicted Volatility")
plt.xlabel("Date")
plt.ylabel("Return")
plt.legend()
plt.show()


# ----------------------------------------------------------------------------------------------
# 6. Communicate the Results
# ----------------------------------------------------------------------------------------------

# Create a function 'volatility_forecaster' that returns
# #the model's forecasted volatility for the next 'n' days


def volatility_forecaster(stock_data: pd.Series, n_days: int) -> dict:
    """
    Forecast the volatility of a stock for the next 'n' business days.

    Parameters:
    stock_data (pd.Series): A time series of stock returns.
    n_days (int): The number of business days to forecast.

    Returns:
    dict: A dictionary where each key is a business date
    in ISO 8601 format and each value is the predicted volatility.
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


# Forecast the volatility for the next 10 days using the 'volatility_forecaster' function
volatility_forecaster(msft_stock_returns, 10)

# ----------------------------------------------------------------------------------------------
# 7. Update the "APIStockProcessor class" in the "stock_data_processor.py"
# ----------------------------------------------------------------------------------------------

"""This will be used to build an interactive web app deployed for stock volatility forecasting.
"""
