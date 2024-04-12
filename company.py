from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
from backtesting import Backtest
# Make sure to correctly import your strategies
from backtestingExample import ThresholdVolumeStrategy, VolumeStrategy, MomentumStrategy,MovingAverageCrossover, SmaCross
import json

df_companies = pd.read_excel('Companies.xlsx')
# Create a dictionary mapping company names to tickers
company_to_ticker = df_companies.set_index('Name')['Symbol'].to_dict()



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



app = Flask(__name__)

def run_momentum(data, initial_cash):
    print("here")
    bt = Backtest(data, MomentumStrategy, cash=initial_cash, commission=.002)
    stats = bt.run()
    final_equity = round(stats['Equity Final [$]'],2)
    number_of_trades = stats['# Trades'] 
    return initial_cash, final_equity, number_of_trades\
    
def run_crossover(data, initial_cash):
    print("here")
    bt = Backtest(data, MovingAverageCrossover, cash=initial_cash, commission=.002)
    stats = bt.run()
    final_equity = round(stats['Equity Final [$]'],2)
    number_of_trades = stats['# Trades'] 
    return initial_cash, final_equity, number_of_trades

def run_threshold_volume_strategy(data, initial_cash):
    bt = Backtest(data, ThresholdVolumeStrategy, cash=initial_cash, commission=.002)
    stats = bt.run()
    final_equity = round(stats['Equity Final [$]'],2)
    number_of_trades = stats['# Trades'] 
    return initial_cash, final_equity, number_of_trades

def run_volume_strategy(data, initial_cash):
    bt = Backtest(data, VolumeStrategy, cash=initial_cash, commission=.002)
    stats = bt.run()
    print(stats)
    number_of_trades = stats['# Trades'] 
    final_equity = round(stats['Equity Final [$]'],2)
    #number_of_trades = stats['Trades'] 
    return initial_cash, final_equity, number_of_trades


def run_SMA_crossover(data, initial_cash):
    bt = Backtest(data, SmaCross, cash=initial_cash, commission=.002)
    stats = bt.run()
    print(stats)
    number_of_trades = stats['# Trades'] 
    final_equity = round(stats['Equity Final [$]'],2)
    #number_of_trades = stats['Trades'] 
    return initial_cash, final_equity, number_of_trades

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number_of_trades = 0
        selected_strategy = request.form.get('strategy')
        selected_company_name = request.form.get('company')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        # Read initial cash from form data, default to 10,000 if not provided
        initial_cash = int(request.form.get('initial_cash', 10000))

        selected_ticker = company_to_ticker.get(selected_company_name)
        if not selected_ticker:
            return "Ticker not found for the selected company", 404

        data = yf.download(selected_ticker, start=start_date, end=end_date)
        if data.empty:
            return "No data available for the selected ticker and date range."

        data['Volume_MA'] = data['Volume'].rolling(10).mean()

        # Call the appropriate strategy function with the initial cash
        if selected_strategy == 'movingcrossover':
            initial_cash, final_equity, number_of_trades = run_crossover(data, initial_cash)
        elif selected_strategy == 'volume':
            
            initial_cash, final_equity, number_of_trades= run_volume_strategy(data, initial_cash)
        elif selected_strategy == 'smacross':
            initial_cash, final_equity, number_of_trades= run_SMA_crossover(data, initial_cash)
        elif selected_strategy == 'momentum':
            # Fetch historical price data using run_backtest function
            print("hereeeeeeeeeeee")
            data = run_backtest(selected_ticker)
       
            
            # Call the backtest_run function with MomentumStrategy
            initial_cash, final_equity, number_of_trades = run_momentum(data, initial_cash)

            # Return the results to the template
            return render_template('results.html', initial_cash=initial_cash, final_equity=final_equity, number_of_trades=number_of_trades)

        return render_template('results.html', initial_cash=initial_cash, final_equity=final_equity, number_of_trades = number_of_trades)
    else:
        try:
            # Assuming the Excel file is in the same directory as this script
            df = pd.read_excel('Companies.xlsx')
            companies = df.iloc[:, 1].tolist()  # Adjust column index based on your Excel file
            return render_template('template.html', companies=companies)
        except Exception as e:
            print(e)
            return "An error occurred while fetching the company names."

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
