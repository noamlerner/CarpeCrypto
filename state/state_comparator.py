import math
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




