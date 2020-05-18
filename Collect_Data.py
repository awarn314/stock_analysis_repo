import pandas as pd
import os
from shutil import rmtree
from os import listdir
from os.path import isfile, join
from builtins import any as b_any
from pandas_datareader import data as pdr
import yfinance as yf
import datetime

yf.pdr_override()


def check_csv(csv_file):
    data_df = pd.read_csv(csv_file)
    columns = ['Symbol', 'Name', 'Dividend', 'Market Cap, Billions']

    for c in columns:
        if c in data_df.columns:
            print(f"{c} is in csv")
        else:
            print(f"{c} is NOT in csv")
            raise SystemExit


def main(*args):
    stock_path = 'Stock_Data'

    if args[0] == 1:
        rmtree(stock_path)

    if not os.path.exists(stock_path):
        os.makedirs(stock_path)

    start = str(datetime.date.today() - datetime.timedelta(days=int(args[1] * 365)))
    end = str(datetime.date.today())

    tickers = pd.read_csv(args[2])

    onlyfiles = [f for f in listdir(stock_path) if isfile(join(stock_path, f))]
    Doneticks = [i.split('.csv', 1)[0] for i in onlyfiles]

    skipticks = []

    for tick, comp, divi, mc in zip(tickers['Symbol'], tickers['Name'], tickers['Dividend'],
                                    tickers['Market Cap, Billions']):
        f_str = tick + '__' + comp
        if not b_any(f_str in x for x in Doneticks):
            try:
                df = pdr.get_data_yahoo(tick, start, end)
                if len(df) > 0:
                    df = df.reset_index()
                    df['Count'] = df.index
                    df['Week Day'] = -1
                    df['Change'] = ((df['Close'] / df['Open']) - 1) * 100
                    for index, row in df.iterrows():
                        date = row['Date']
                        wk_day = date.weekday()
                        df.at[index, 'Week Day'] = wk_day

                    period = 14
                    delta = df['Close'].diff()
                    dUp, dDown = delta.copy(), delta.copy()
                    dUp[dUp < 0] = 0
                    dDown[dDown > 0] = 0
                    RS = dUp.rolling(period).mean() / dDown.rolling(period).mean().abs()
                    df['RSI'] = 100.0 - (100.0 / (1.0 + RS))
                    df = df.fillna(df['Close'].min())
                    fname = stock_path + '/' + tick + '__' + comp + '.csv'
                    df.to_csv(fname, sep=',', encoding='utf-8', index=False)
                else:
                    tickers = tickers[tickers.Symbol != tick]

            except Exception:
                skipticks.append(tick)
                pass
    tickers.to_csv(args[2][:-4] + '-new.csv', sep=',', encoding='utf-8',
                   index=False)  # saves out csv with delisted tickers
    if len(listdir(stock_path)) < 7000:
        print(f'Missing some stocks (returned only {len(listdir(stock_path))} when there is likely more)')


if __name__ == "__main__":
    ## INPUTS ##
    RESET = 0  # Set to 1 to delete stock data
    years = 5  # how many past years data to collect
    csv_of_symbols = 'secwiki_tickers7.csv'
    ## INPUTS ##

    check_csv(csv_of_symbols)  # checking tickers input into main()

    main(RESET, years, csv_of_symbols)
