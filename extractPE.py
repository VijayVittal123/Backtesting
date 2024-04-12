# import json

# # Load the JSON file
# with open('pe_ratios.json', 'r') as file:
#     data = json.load(file)

# # Access data for a specific company
# company_code = 'MMM'  # For example, to get data for company 'MMM'
# company_data = data['stocks'][company_code]

# # Print PE ratio data for 'MMM' for February 2023
# for date, pe_info in company_data.items():
#     if date.startswith('2023-02'):
#         print(f"Date: {date}, PE Ratio: {pe_info['pe_ratio']}")



# from backtesting import Backtest, Strategy
# from backtesting.lib import SignalStrategy, TrailingStrategy
# from backtesting.test import SMA, GOOG

# import json

# # Load the JSON file containing P/E ratio data
# with open('pe_ratios.json', 'r') as file:
#     data = json.load(file)


# # Define the trading strategy class
# class MomentumStrategy(Strategy):
#     def init(self):
#         self.buy_signal_triggered = False

#     def next(self):
#         # Iterate over the keys (stock symbols) in the data dictionary
#         company_data = data['stocks']['MMM']
#         for pe_info in company_data.items():
            
#             # Extract P/E ratio data for the current stock symbol
#             pe_ratio = pe_info['pe_ratio']

#             # Check if the P/E ratio is trending upwards or downwards
#             if self.buy_signal_triggered and pe_ratio > self.buy_signal_price:
#                 self.position.close()
#                 self.buy_signal_triggered = False
#             elif not self.buy_signal_triggered and pe_ratio < data['stocks']['MMM']['pe_ratio']:
#                 self.buy_signal_triggered = True
#                 self.buy_signal_price = pe_ratio
#                 self.buy()

# # Define the backtest parameters
# stock_data = GOOG  # Example stock data (replace with actual data)
# initial_cash = 10000  # Initial cash for trading
# commission = 0.001  # Commission rate

# # Run the backtest with the defined strategy
# bt = Backtest('MMM', MomentumStrategy,
#               cash=initial_cash, commission=commission)
# stats = bt.run()

# # Print the backtest statistics
# print(stats)


# # MOSTT RECENT
# from backtesting import Backtest, Strategy
# import pandas as pd
# import json

# # Load the JSON file containing P/E ratio data
# with open('pe_ratios.json', 'r') as file:
#     data = json.load(file)

# # Define the company symbol
# company_symbol = 'MMM'  # Replace with the desired company symbol

# # Create a pandas DataFrame with the P/E ratio data
# pe_ratios = pd.DataFrame(data['stocks'][company_symbol])

# print(pe_ratios)
# print(company_symbol)

# pe_ratios = pe_ratios.transpose()

# # Rename the column to 'Close'
# pe_ratios.columns = ['Close']

# # Since P/E ratio data doesn't have OHLC values, we'll use the same value for all
# # OHLC columns. You can replace '10.0' with the actual P/E ratio value.
# pe_ratios['Open'] = pe_ratios['High'] = pe_ratios['Low'] = pe_ratios['Close']

# # Create a dummy DataFrame with Volume column (set to 0)
# pe_ratios['Volume'] = 0


# print(pe_ratios['Open'])



# # Define the trading strategy class

# pe_ratios['Open'] = pd.to_numeric(pe_ratios['Open'], errors='coerce')
# pe_ratios['Close'] = pd.to_numeric(pe_ratios['Close'], errors='coerce')
# pe_ratios['High'] = pd.to_numeric(pe_ratios['High'], errors='coerce')
# pe_ratios['Low'] = pd.to_numeric(pe_ratios['Low'], errors='coerce')

#  # Sort the index in ascending order
# pe_ratios.sort_index(inplace=True)

# # Convert the index to datetime
# pe_ratios.index = pd.to_datetime(pe_ratios.index)


# print(pe_ratios['Open'].dtype)
# print(pe_ratios['Open'].unique())
# class MomentumStrategy(Strategy):
#     def init(self):
#         self.buy_signal_triggered = False
#         self.buy_signal_price = 1000000 
#         print("hi")

#     def next(self):
#         pe_ratio = self.data['Open']  # Use the 'Open' column as the P/E ratio
#         print("pe_ratio:", pe_ratio)
#         print("buy_signal_price:", self.buy_signal_price)
       
#         # Check if the P/E ratio is trending upwards or downwards
#         if self.buy_signal_triggered and pe_ratio > self.buy_signal_price:
#             print("here")
#             self.position.close()
#             self.buy_signal_triggered = False
#         elif not self.buy_signal_triggered and pe_ratio < self.buy_signal_price:
#             print("here2")
#             print()
#             self.buy_signal_triggered = True
#             self.buy_signal_price = pe_ratio
#             self.buy()


# # Define the backtest parameters
# initial_cash = 10000  # Initial cash for trading
# commission = 0.001  # Commission rate

# # Run the backtest with the defined strategy
# bt = Backtest(pe_ratios, MomentumStrategy,
#               cash=initial_cash, commission=commission)
# stats = bt.run()

# # Print the backtest statistics
# print(stats)

from backtesting import Backtest, Strategy
import pandas as pd
import json

def run_backtest(company_symbol):
    print("here")
    # Load the JSON file containing P/E ratio data
    with open('pe_ratios.json', 'r') as file:
        data = json.load(file)

    # Create a pandas DataFrame with the P/E ratio data for the specified symbol
    pe_ratios = pd.DataFrame(data['stocks'][company_symbol])

    pe_ratios = pe_ratios.transpose()

    # Rename the column to 'Close'
    pe_ratios.columns = ['Close']

    # Since P/E ratio data doesn't have OHLC values, we'll use the same value for all
    # OHLC columns. You can replace '10.0' with the actual P/E ratio value.
    pe_ratios['Open'] = pe_ratios['High'] = pe_ratios['Low'] = pe_ratios['Close']

    # Create a dummy DataFrame with Volume column (set to 0)
    pe_ratios['Volume'] = 0

    # Convert the OHLC columns to numeric
    pe_ratios['Open'] = pd.to_numeric(pe_ratios['Open'], errors='coerce')
    pe_ratios['Close'] = pd.to_numeric(pe_ratios['Close'], errors='coerce')
    pe_ratios['High'] = pd.to_numeric(pe_ratios['High'], errors='coerce')
    pe_ratios['Low'] = pd.to_numeric(pe_ratios['Low'], errors='coerce')

    # Sort the index in ascending order
    pe_ratios.sort_index(inplace=True)

    # Convert the index to datetime
    pe_ratios.index = pd.to_datetime(pe_ratios.index)
    return pe_ratios

class MomentumStrategy(Strategy):

    def init(self):
        self.buy_signal_triggered = False
        self.buy_signal_price = [1000000] 

    def next(self):
        pe_ratio = self.data['Open']  # Use the 'Open' column as the P/E ratio
     

        # Check if the P/E ratio is trending upwards or downwards
        if self.buy_signal_triggered and pe_ratio[-1] > self.buy_signal_price[-1]:
            self.position.close()
            self.buy_signal_triggered = False
        elif not self.buy_signal_triggered and pe_ratio[-1] < self.buy_signal_price[-1]:
            self.buy_signal_triggered = True
            self.buy_signal_price = pe_ratio
            self.buy()

# Define the backtest parameters
initial_cash = 10000  # Initial cash for trading
commission = 0.001  # Commission rate

# Fill missing values with interpolation
pe_ratios = run_backtest("AAPL")
pe_ratios.interpolate(inplace=True)

# Run the backtest with the defined strategy
bt = Backtest(pe_ratios, MomentumStrategy, cash=initial_cash, commission=commission)
stats = bt.run()

# Print the backtest statistics
print(stats)
