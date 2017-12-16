class minimum_datapoints_required(object):
    '''
    for each indicator this should implement [indicator name]_points_required which takes in the indicator tuple i
    for the given indicator tuple, this should return an int which represents the minimum data points required to
    get a state for this indicator.
    '''
    def __init__(self):
        pass
    def _slice_size_for_window(self, window, values_needed):
        '''
        this will return a sliced dataframe that has just enough values to the amount of values you need at the specified window.
        As an example, if you have a window of 5 and you only need the last current rolling value and yesterdays rolling value,
        you would pass in (5,2) and this would return a slice of the prices that is of size 7 since we do not need more values
        than that in the rolling calculation, and more values would waste performance
        '''
        return (window+values_needed)

    def bbands_points_required(self,i):
        window = i[1]
        return self._slice_size_for_window(window,2)

    def rsi_points_required(self,i):
        window = i[1]
        return self._slice_size_for_window(window,2)