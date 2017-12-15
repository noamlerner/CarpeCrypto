class state_length(object):
    '''
    this class should hold a method for every indicator we want to implement.
    The method should be named [indicator name]_num_states and take in one parameters - the indicator tuple
    it should then return the amount of states this indicator tuple needs as a string.
    '''
    def __init__(self):
        pass

    def example_indicator_num_states(self,i):
        return "4"
    def bbands_num_states(self,i):
        return "8"