import krakenex
from pykrakenapi import KrakenAPI
# instantiate API
api = krakenex.API()
# load the API key
api.load_key('kraken.key')
# instantiate API wrapper
k = KrakenAPI(api, tier=2,retry=.5)
'''
BCHUSD is the pair BCH, USD.
since = 0 means since the beginning of time. I.E, as much data as we can get
interval=60 means every 60 minutes, other options: 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600

with interval=60 we can get at most a month of data as of the time this comment is written.
'''
ohlc, last = k.get_ohlc_data("BCHUSD",since=0,interval=60)
# reverse data frame so that newest date at the end
ohlc = ohlc.iloc[::-1]

print(ohlc)
'''
ohlc returns a pandas dataframe with columns:
time
open
high
low
close
vwap (?)
volume
count
'''
