from state.state_comparator import state_comparator
from state.state_creator import state_creator
from state.state_length import state_length


class state(object):
    '''
    This acts as an api to handle state.
    On init, it expects a list of tuples, each with the format:
        (str, int, any...) = (indicator name, window, parameters...)
    Using this class one can:
        get the number of states for a given indicators array
        get the current state for a prices dataframe
        compare two states that were generated by the same indicator arrays
    '''
    def __init__(self, indicators = [('bbands',5,None),('bbands',2, None),('rsi',6, None)]):
        self._indicators = indicators
        self._num_states_for_indicator = {}
        self.state_creator = state_creator()
        self.state_length = state_length()
        self.state_comparator = state_comparator()

    def get_num_states(self):
        '''
        returns the number of states the list of indicators this class was initialized with will require
        :return: int
        '''
        num_states = ""
        for i in self._indicators:
            num_states += self._get_num_states_for_indicator(i)
        return  int(num_states)

    def _get_num_states_for_indicator(self,i):
        func_name = i[0] + "_num_states"
        return getattr(self.state_length, func_name)(i)

    def get_state(self,prices_to_date):
        '''
        returns a state for a given time period
        :param prices_to_date: prices up to the time of makes a decision
        :return: str that can be converted to an int
        '''
        states = []
        for i in self._indicators:
            func_name = i[0] + "_state"
            states.append(getattr(self.state_creator,func_name)(i, prices_to_date))
        return "".join(states)

    def compare(self, state1, state2):
        '''
        returns a score as to how similar two states are.
        If state1 == state2, this should return 0.
        :param state1: str, state
        :param state2: str, state
        :return: int, simlarity score
        '''
        score = 0
        at = 0
        for i in self._indicators:
            l = len(self._get_num_states_for_indicator(i))
            func_name = i[0] + "_compare"
            score += getattr(self.state_comparator,func_name)(i,state1[at:at+l], state2[at:at+l])
            at = l
        return score



