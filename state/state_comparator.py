import math
import numpy as np
class state_comparator(object):
    '''
    this class should hold a method for every indicator we want to implement.
    The method should be named [indicator name]_compare and take in 3 parameters - the indicator tuple and two intances of a
    state
    it should then return the similarity of the two states. if state1==state2, the method should return 0. Max dissimilarity
    should return 99

    we need to think of a standard way to do this so that one comparison function doesnt outway the rest.
    '''
    def __init__(self):
        pass

    def example_indicator_compare(self, i, state1, state2):
        comparison = 0
        for i in range(4):
            comparison += int(state1[i]) - int(state2)
        return comparison

    def bbands_compare(self,i,state1,state2):
        '''
            0 if the same state,
            50 if movement is horizontal
            99 otherwise
        '''
        if state1 == state2:
            return 0
        state1_int = int(state1)
        state2_int = int(state2)
        # (current_price_state, last_price_state)
        s1 = (int(state1_int/3),state1_int % 3)
        s2 = (int(state2_int/3), state2_int % 3)
        same_area = s1[0] == s1[1] and s2[0] == s2[1]
        if same_area:
            return 50
        return 99


    def rsi_compare(self, i, state1, state2):
        '''
            Calculates simliarity based on the sum of the following values:
                absolute value of difference in current rsi and last rsi
                absolute value difference in the difference between the current rsi and the last rsi
                example:precision=1, state1=12 state2=34
                returns (3-1) + (4-2) + ( (2-1) - (4-3) ) = 2+ 2 + 0 = 4
        '''
        precision = 1
        if len(i) == 3 and 'precision' in i[2]:
            precision = i[2]['precision']
        #     (current_rsi,             last_rsi)
        r1 = (int(state1[:precision]),int(state1[precision:]))
        r2 = (int(state2[:precision]),int(state2[precision:]))
        diffs = []
        diffs.append(abs(r1[0] - r2[0]))
        diffs.append(abs(r1[1] - r2[1]))
        diff1 = r1[0] - r1[1]
        diff2 = r2[0] - r2[1]
        diffs.append(abs(diff1 - diff2))
        return np.sum(diffs)
