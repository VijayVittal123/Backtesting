from flask import Flask, render_template
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import talib
from backtesting.lib import crossover
import yfinance as yf
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Assuming the Excel file is in the same directory as this script
        df = pd.read_excel('Companies.xlsx')
        companies = df.iloc[:, 1].tolist()  # Adjust the index if necessary
        print(companies)
        return render_template('template.html', companies=companies)
    except Exception as e:
        # For debug purposes, print the exception
        print(e)
        return "An error occurred while fetching the company names."

if __name__ == '__main__':
    app.run(debug=True)


def run_threshold_volume_strategy(data):
    bt = Backtest(data, ThresholdVolumeStrategy, cash=10_000, commission=.002)
    stats = bt.run()
    return stats

def run_volume_strategy(data):
    bt = Backtest(data, VolumeStrategy, cash=10_000, commission=.002)
    stats = bt.run()
    return stats

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected strategy and company from form submission
        selected_strategy = request.form.get('strategy')
        selected_company = request.form.get('company')

        # Fetch the data for the selected company
        data = yf.download(selected_company, start="2023-02-01", end="2024-03-01")
        data['Volume_MA'] = data['Volume'].rolling(10).mean()

        # Run the selected strategy backtest
        if selected_strategy == 'threshold_volume':
            results = run_threshold_volume_strategy(data)
        elif selected_strategy == 'volume':
            results = run_volume_strategy(data)

        # Render a template to show the results or handle them as needed
        return render_template('results.html', results=results)
    else:
        # The GET request logic remains the same
        ...
