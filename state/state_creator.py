from state import indicators
import math

class state_creator(object):
    '''
    this class should hold a method for every indicator we want to implement.
    The method should be named [indicator name]_state and take in two parameters - the indicator tuple and the prices dataframe
    it should then return that given indicators state
    '''
    def __init__(self):
        pass
    def _slice_for_window(self, prices, window, values_needed):
        '''
        this will return a sliced dataframe that has just enough values to the amount of values you need at the specified window.
        As an example, if you have a window of 5 and you only need the last current rolling value and yesterdays rolling value,
        you would pass in (5,2) and this would return a slice of the prices that is of size 7 since we do not need more values
        than that in the rolling calculation, and more values would waste performance
        '''
        return prices[-(window+values_needed-1):]
    def example_indicator_state(self, i, prices):
        return "1111"

    def bbands_state(self, i, prices):
        '''
        returns a state from [0..8] representing the current price relative to the current bollinger bands and the last price
        relative to the last bollinger bands.
        '''
        window = i[1]
        roling_band = indicators.bollinger_bands(self._slice_for_window(prices,window,2), window)
        current_price = prices.iloc[-1]
        last_price = prices.iloc[-2]
        current_band = roling_band.iloc[-1]
        last_band = roling_band.iloc[-2]
        current_price_state = 1
        last_price_state = 1
        if current_price > current_band['UPPER_BAND']:
            current_price_state += 1
        if current_price < current_band['LOWER_BAND']:
            current_price_state -= 1
        if last_price > last_band['UPPER_BAND']:
            last_price_state += 1
        if last_price < last_band['LOWER_BAND']:
            last_price_state -= 1
        return str(current_price_state * 3 + last_price_state)

    def _num_to_precision(self, num, precision):
        '''
        takes in a number, rounds it to the the number of places specified by precision and returns an int.
        examples: input => output
            (62.5, 1) => 6
            (62.5, 2) => 63
            (62.5, 4) => 625
        '''
        if num == 0:
            return  0
        in_front_of_decimal = int(math.log(num,10)) + 1
        n = num / 10 ** in_front_of_decimal
        return int(round(n,precision) * 10**precision)


    def _with_length(self, num, l):
        '''
        returns a string representing num and adds 0s at the front until the length is len
        '''
        s = str(num)
        delta = l - len(s)
        return "0"*delta + s
    def rsi_state(self, i, prices):
        window = i[1]
        rsi = indicators.rolling_rsi(self._slice_for_window(prices,window,2),window)
        current_rsi = rsi.iloc[-1]
        last_rsi = rsi.iloc[-2]
        precision = 1
        if len(i) == 3 and 'precision' in i[2]:
            precision = i[2]['precision']

        rsi_0 = self._num_to_precision(current_rsi,precision)
        rsi_1 = self._num_to_precision(last_rsi,precision)
        s0 = self._with_length(rsi_0,precision)
        s1 =self._with_length(rsi_1,precision)
        # essentially elimating 10/100/1000... and rounding to 9/99/999
        if len(s0) > precision:
            s0 = "9" * precision
        if len(s1) > precision:
            s1 = "9" * precision
        return s0 + s1