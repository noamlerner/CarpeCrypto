'''

This should contain helper methods to retrieve indicators for a give dataframe
Each indicator should have two parameters - dataframe and timeperiod
:dataframe being the pandas dataframe with vwap data and at least timeperiod values
:timeperiod is the int which how many values to go back in the dataframe - so if the dataframe is in hours
5 would be 5 hours
'''

import numpy as np
import pandas as pd

def bollinger_bands(prices, window=20):
    sma = pd.rolling_mean(prices, window=window)
    std = pd.rolling_std(prices,window=window)
    bands_df = pd.DataFrame(index=sma.index, columns=['LOWER_BAND', 'UPPER_BAND'])
    bands_df['UPPER_BAND'] = sma + 2 * std
    bands_df['LOWER_BAND'] = sma - 2 * std
    bands_df.dropna()
    return bands_df

def normalized_prices(prices):
    return prices/prices[0]

def _rsi_for_window(window):
    gains = []
    losses = []
    for i in range(1, len(window)):
        delta = window[i] - window[i - 1]
        if delta > 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))
    RS = (np.sum(gains)/len(window)) / (np.sum(losses)/len(window))

    return 100 - 100 / (1 +RS)

def rolling_rsi(prices, window=10):
    return pd.rolling_apply(prices, window, _rsi_for_window)

def rolling_momentum(prices, window=20):
    rm = pd.rolling_apply(prices, window, lambda arr: arr[-1]/arr[0] - 1)
    return rm

