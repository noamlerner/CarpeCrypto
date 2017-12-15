class state_comparator(object):
    '''
    this class should hold a method for every indicator we want to implement.
    The method should be named [indicator name]_compare and take in 3 parameters - the indicator tuple and two intances of a
    state
    it should then return the similarity of the two states. if state1==state2, the method should return 0.

    we need to think of a standard way to do this so that one comparison function doesnt outway the rest.
    '''
    def __init__(self):
        pass

    def example_indicator_compare(self, i, state1, state2):
        comparison = 0
        for i in range(4):
            comparison += int(state1[i]) - int(state2)
        return comparison

