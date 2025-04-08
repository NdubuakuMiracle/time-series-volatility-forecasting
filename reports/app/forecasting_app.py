# Import necessary libraries
import streamlit as st  # For building the interactive web app
import plotly.express as px  # For data visualization
import sys
import os

# Append the absolute path of the `src/data` directory to system path
# This allows importing modules from that directory
sys.path.append(os.path.abspath("../../src/data"))
from stock_data_processor import (
    APIStockProcessor,
)  # Import the stock data processor class


class StockVolatilityApp:
    def __init__(self):
        """Initialize the application by creating an instance of APIStockProcessor."""
        self.processor = (
            APIStockProcessor()
        )  # Object for handling stock data processing
        self.df_stock = None  # Placeholder for stock price data
        self.returns = None  # Placeholder for stock returns data

    def get_stock_data(self, ticker: str, limit):
        """Fetch stock price data for a given ticker symbol."""
        with st.spinner("Fetching stock data..."):  # Display a loading spinner
            # If 'full' is selected, fetch all available data; otherwise, use the specified limit
            limit_value = None if limit == "full" else int(limit)
            self.df_stock = self.processor.get_stock_data(ticker, limit=limit_value)

            # Store the fetched data in Streamlit's session state for later use
            st.session_state["df_stock"] = self.df_stock

    def compute_returns(self):
        """Calculate stock returns based on the fetched stock data."""
        if self.df_stock is not None:
            self.returns = self.processor.extract_returns(self.df_stock)
            return self.returns
        return None  # Return None if no stock data is available

    def forecast_volatility(self, n_days: int, annualized: bool):
        """Forecast stock volatility over a given number of days."""
        if self.returns is not None:
            try:
                volatility = self.processor.volatility_forecaster(self.returns, n_days)

                # If annualization is selected, scale daily volatility using sqrt(252)
                if annualized:
                    return {
                        date: (vol * (252**0.5)) for date, vol in volatility.items()
                    }
                return volatility  # Return daily volatility otherwise
            except Exception as e:
                st.error(f"Error forecasting volatility: {str(e)}")
        return {}  # Return empty dictionary if returns data is unavailable

    def run(self):
        """Main method to run the Streamlit application."""
        st.set_page_config(page_title="Stock Volatility Forecasting", layout="wide")

        # === Sidebar Inputs ===
        st.sidebar.header("Stock Data Input")  # Sidebar section header

        # User input: Stock ticker symbol (default: AAPL)
        ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")

        # User selection for data amount (full dataset or custom limit)
        data_limit_option = st.sidebar.radio("Select Data Amount:", ["full", "custom"])

        # If 'custom' is selected, allow user to enter a numeric limit
        limit = (
            st.sidebar.number_input(
                "Enter Data Limit", min_value=50, max_value=5000, value=500, step=50
            )
            if data_limit_option == "custom"
            else "full"
        )

        # User selects number of forecast days (1 to 30 days)
        n_days = st.sidebar.slider("Forecast Days", min_value=1, max_value=30, value=5)

        # Checkbox for annualizing the volatility forecast
        annualized = st.sidebar.checkbox("Annualize Volatility", value=False)

        # Fetch data button
        if st.sidebar.button("Fetch Data"):
            self.get_stock_data(ticker, limit)

        # === Main App Content ===
        st.title("Alpha Vantage Stock Volatility Forecasting")  # Main title

        if (
            "df_stock" in st.session_state and not st.session_state["df_stock"].empty
        ):  # Check if stock data is available
            self.df_stock = st.session_state["df_stock"]

            # Display stock price data (last 10 records)
            st.subheader("Stock Price Data")
            st.dataframe(self.df_stock.head(10))

            # Plot the stock closing price trend using Plotly
            fig = px.line(
                self.df_stock,
                x=self.df_stock.index,
                y="close",
                title=f"Closing Prices of {ticker}",
            )
            st.plotly_chart(fig, use_container_width=True)

            # === Compute and Display Stock Returns ===
            st.subheader("Stock Returns")
            self.compute_returns()  # Calculate returns

            if self.returns is not None:
                st.line_chart(self.returns)  # Display returns as a line chart

            # === Forecast Volatility ===
            st.subheader("Volatility Forecast")
            with st.spinner(
                "Calculating volatility forecast..."
            ):  # Show loading spinner
                forecasted_volatility = self.forecast_volatility(n_days, annualized)

                # Define the appropriate label based on user selection
                unit_label = (
                    "Annualized Volatility (% change per year)"
                    if annualized
                    else "Daily Volatility (% change per day)"
                )

                # Display the forecasted volatility in JSON format
                st.write(f"### Forecasted {unit_label}")
                st.json(forecasted_volatility)

        # === Footer Section ===
        st.sidebar.subheader("Developed by:")
        st.sidebar.write("Ndubuaku Miracle Oluebube")  # Developer credit


# Run the app when the script is executed
if __name__ == "__main__":
    app = StockVolatilityApp()
    app.run()
