from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import talib
from backtesting.lib import crossover
import yfinance as yf
import pandas as pd



# symbol = "AAPL"
# data = yf.download(symbol, start="2023-02-01", end="2024-03-01")

# # Preparing the data for backtesting
# data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
# data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# # # Calculate the 10-day moving average of volume and add it to the DataFrame
# n1 = 10  # Number of days for moving average of volume
# data['Volume_MA'] = data['Volume'].rolling(n1).mean()

class ThresholdVolumeStrategy(Strategy):
    def init(self):
        # Calculate the rolling mean outside of self.I() using pandas directly
        volume_ma = self.data.Volume.rolling(10).mean()
        
        # Now, use self.I() to properly integrate the pre-calculated indicator
        self.volume_ma = self.I(lambda x: x, volume_ma)

    def next(self):
        if self.data.Volume[-1] > 1.5 * self.volume_ma[-1]:
            # Volume significantly above average, might indicate a selling opportunity
            if self.position:
                self.position.close()  # Here you could adjust to sell a certain amount instead
        elif self.data.Volume[-1] < 0.5 * self.volume_ma[-1]:
            # Volume significantly below average, might indicate a buying opportunity
            self.buy(size=3)  # X is the number of shares you decide to buy

# bt0 = Backtest(data, ThresholdVolumeStrategy, cash=10_000, commission=.002)

# find the last 10 days of volume and average itxqx

# if today is greater than the average then buy but if lower then sell

class VolumeStrategy(Strategy):
    def init(self):
        # The moving average of volume is already pre-calculated and included in the data
        self.volume_ma = self.data.Volume_MA
        
    def next(self):
        if self.data.Volume[-1] > self.volume_ma[-1]:
            # If today's volume is greater than the moving average, we buy
            if not self.position:
                self.buy()
        elif self.data.Volume[-1] < self.volume_ma[-1]:
            # If today's volume is less than the moving average, we sell
            if self.position:
                self.position.close()

# # Running the backtest
# bt1 = Backtest(data, VolumeStrategy, cash=10_000, commission=.002)
# output1 = bt1.run()
# print(output1)

# # Plot the backtest result
# bt1.plot()
# print(GOOG)

# class RsiOscillator(Strategy):
#     upper_bound = 70
#     lower_bound = 30
#     rsi_window = 14

#     def init(self): #runs one time at initialization
#         self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)#i is how we build indicators. into this rsi we pass close and 14

#     def next(self): # goes through each candle individually
#         # when rsi is above a certain value it sells
#         if crossover(self.rsi,self.upper_bound):
#             # if rsi is greater than upper bound

#             self.position.close() # sell everything
#         elif crossover(self.lower_bound,self.rsi):
#             self.buy()

# bt2 = Backtest(GOOG, RsiOscillator, cash = 20_000)
# # stats = bt2.optimize(
# #     upper_bound = range(50,85,5),
# #     lower_bound = range(10,45,5),
# #     rsi_window = range(10,30,2), 
# #     maximize='Sharpe Ratio'
# #     #max_tries = 100 does 100 random tests instead of the thousands because that could take a while
# #     #constraint= lambda param: param.upper_bound > param.lower_bound)
# # )
# #stats = bt.run()
# #print(stats)
# #bt2.plot()

# # Assuming 'bt' is your Backtest object and you've already run a backtest:
# # Assuming you've already set up and run your backtest like this:
# # Assuming you've set up your Backtest object as `bt2`

# initial_cash = 10_000

# bt2 = Backtest(data, VolumeStrategy, cash=initial_cash, commission=.002)

# # Now, you must run the backtest to obtain the results
# results = bt2.run()


# # Only after running the backtest, you print the initial and final portfolio values
# print(f"Initial Portfolio Value: {initial_cash}")
# print(f"Final Portfolio Value: {results['Equity Final [$]']}")

# # Now that you've run the backtest, you can safely plot the results
# bt2.plot()
