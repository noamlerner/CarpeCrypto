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
        This will return a sliced dataframe which contained enough values to generate values_needed values with the specified
        window.
        As an example, if you have a window of 5 and you only need the  current rolling value and yesterdays rolling value,
        you would pass in (5,2) and this would return a slice of the prices that is of size 7 which would allow for the
        calculation of both rolling values. Giving more datapoints causes needless calculation of extra rolling values
        '''
        return prices[-(window+values_needed-1):]

    def bbands_state(self, i, prices):
        '''
        returns a state from [0..6] representing the current price relative to the current bollinger bands and the last price
        relative to the last bollinger bands.
        The current bollinger band can have the values 0,1 or 2 representing
            0=price is below lower band
            1=price is between lower and upper band
            2=price is above upper band.
        the last bollinger band works in the same way working to the last price.
        the final state returns is the state of the current bollinger band multiplied by 3, summed with the last bollinger
        band's state.
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
        returns a string representing num and adds 0s at the front until the length is of the passed in int l
        '''
        s = str(num)
        delta = l - len(s)
        return "0"*delta + s

    def rsi_state(self, i, prices):
        '''
        this will return a state s consisting of two values s0 and s1 such that s=s0+s1 (s,s0 and s1 are all strings).
        s0 represents the rsi for the most recent data point, s1 represents the rsi for the data point right before the
        current one.
        by default, the "precision" of this function is 1, meaning s0 and s1 will each occupy one digit, and can be a number
        between 0 and 9.
        the precision can be changed in the indicator tuple by passing in a dictionary which contains a key named "precision"
        which holds an int as a value. The int will represent the new preceision, or how many digits each state will contain.
        For example, if the third argument of i was {"precision":2}, s0 and s2 would both be between 0 and 99, making the
        final state take up 4 digits.
        :param i: indicator tuple: ("rsi",window (int), params(optional, {"precision":int})
        :param prices: dataframe of prices
        :return: string, int.
        '''
        window = i[1]
        rsi = indicators.rolling_rsi(self._slice_for_window(prices,window,2),window)
        current_rsi = rsi.iloc[-1]
        last_rsi = rsi.iloc[-2]
        precision = 1
        if len(i) == 3 and 'precision' in i[2]:
            precision = i[2]['precision']

        rsi_0 = self._num_to_precision(current_rsi,precision)
        rsi_1 = self._num_to_precision(last_rsi,precision)
        # essentially elimating 10/100/1000... and rounding to 9/99/999
        s0 = self._with_length(rsi_0,precision) * (((10 ** precision) - 1) / (10 ** precision))
        s1 = self._with_length(rsi_1,precision) * (((10 ** precision) - 1) / (10 ** precision))
        return s0 + s1

