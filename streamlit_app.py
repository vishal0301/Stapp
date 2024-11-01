import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the moving average crossover strategy
def moving_average_strategy(data, short_window, long_window):
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data

# Simulate trades based on the strategy
def simulate_trades(data, initial_capital):
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    positions['Position'] = data['Signal'] * initial_capital / data['Close']  # Number of shares

    portfolio = positions.multiply(data['Close'], axis=0)
    portfolio['Holdings'] = positions['Position'] * data['Close']
    portfolio['Cash'] = initial_capital - (positions.diff() * data['Close']).cumsum()
    portfolio['Total'] = portfolio['Holdings'] + portfolio['Cash']
    portfolio['Returns'] = portfolio['Total'].pct_change()

    return portfolio

# Streamlit UI
st.title("Algorithmic Trading App")
st.write("Simulate trading strategies on historical data.")

# User inputs
stock = st.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))
short_window = st.number_input("Short Moving Average Window", min_value=1, max_value=50, value=40)
long_window = st.number_input("Long Moving Average Window", min_value=1, max_value=200, value=100)
initial_capital = st.number_input("Initial Capital ($)", min_value=1000, value=10000)

if st.button("Run Strategy"):
    # Load historical data
    data = yf.download(stock, start=start_date, end=end_date)
    
    if not data.empty:
        # Apply strategy and simulate trades
        strategy_data = moving_average_strategy(data, short_window, long_window)
        portfolio = simulate_trades(strategy_data, initial_capital)

        # Plot results
        st.subheader("Stock Price and Moving Averages")
        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label="Close Price")
        plt.plot(strategy_data['Short_MA'], label=f"Short MA ({short_window} days)")
        plt.plot(strategy_data['Long_MA'], label=f"Long MA ({long_window} days)")
        plt.scatter(strategy_data.index, strategy_data['Position'] == 1, color='green', marker='^', alpha=1, label="Buy Signal", lw=3)
        plt.scatter(strategy_data.index, strategy_data['Position'] == -1, color='red', marker='v', alpha=1, label="Sell Signal", lw=3)
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Price")
        st.pyplot(plt)

        st.subheader("Portfolio Value Over Time")
        plt.figure(figsize=(14, 7))
        plt.plot(portfolio['Total'], label="Portfolio Value")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.legend()
        st.pyplot(plt)

        # Show performance metrics
        total_return = (portfolio['Total'][-1] - initial_capital) / initial_capital
        st.write(f"**Total Return:** {total_return * 100:.2f}%")
        st.write(f"**Final Portfolio Value:** ${portfolio['Total'][-1]:.2f}")

    else:
        st.error("No data found. Please check the stock ticker and date range.")
