'''
The state class will hold the current state for any given time period,
It should be able to retrieve pairs of data ('indicator name', value) which it will store in an array
it should then take the indicators and transform them into a state
Any time it gets the same values, the same state should be given

Find a way to keep order, possibly pass in an array of indicator names on init which it can use to keep track of the order

should also contain a similarity scoring method for any two states.

should return an int based on the indicators it gets that tells you how large the state space is

(name, window, parameters)
'''

class state(object):
    def __init__(self, indicators_used = [('bbands',5,None),('bbands',2, None),('rsi',6, None)]):
        pass
