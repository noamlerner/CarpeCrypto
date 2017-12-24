import math
import numpy as np
class state_comparator(object):
    '''
    this class should hold a method for every indicator we want to implement.
    The method should be named [indicator name]_compare and take in 3 parameters - the indicator tuple and two intances of a
    state
    it should then return the similarity of the two states. if state1==state2, the method should return 0. Max dissimilarity
    should return 99

    we need to think of a standard way to do this so that one comparison function doesnt outweigh the rest.
    '''
    def __init__(self):
        pass

    def bbands_compare(self, i, state1, state2):
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
        s1 = (int(state1_int / 3), state1_int % 3)
        s2 = (int(state2_int / 3), state2_int % 3)
        same_area = s1[0] == s1[1] and s2[0] == s2[1]
        if same_area:
            return 50
        return 99


    def rsi_compare(self, i, state1, state2):
        '''
            Calculates the normalized simliarity based on the sum of the following values:
                absolute value of difference in current rsi and last rsi for each state scaled by its deviation from the middle RSI value (5 if precision=1, 50 if precision=2, etc)
                difference of current state1 rsi and current state2 rsi, also scaled by their deviation from the middle RSI, but multiplied by 4 to increase its weight
                examples:
                    (case 1, reasonable difference)
                    precision = 1 (maxValue = 10, middleValue = 4.5, maxMagnitudeFromMiddle = 20.25)
                    state1 = 13 (current = 1, last = 3)
                    state2 = 57 (current = 5, last = 7)
                    state1Severity = (1 - 4.5) ** 2, preserving sign = -12.25
                    lastState1Severity = (3 - 4.5) ** 2, preserving sign = -2.25
                    state2Severity = (5 - 4.5) ** 2, preserving sign = 0.25
                    lastState2Severity = (7 - 4.5) ** 2, preserving sign = 6.25
                    stateMovementDifference = |(-12.25 - -2.25) - (0.25 - 6.25)| = 4
                    currentStateDifference = |-12.25 - 0.25| * 4 = 50
                    difference = int((4 + 50) * (99 / (12 * 20.25))) = 22

                    (case 2, max possible difference)
                    precision = 1 (maxValue = 9, middleValue = 4.5, maxMagnitudeFromMiddle = 20.25)
                    state1 = 90 (current = 9, last = 0)
                    state2 = 09 (current = 0, last = 9)
                    state1Severity = (9 - 4.5) ** 2, preserving sign = 20.25
                    lastState1Severity = (0 - 4.5) ** 2, preserving sign = -20.25
                    state2Severity = (0 - 4.5) ** 2, preserving sign = -20.25
                    lastState2Severity = (9 - 4.5) ** 2, preserving sign = 20.25
                    stateMovementDifference = |(20.25 - -20.25) - (-20.25 - 20.25)| = 81
                    currentStateDifference = |-20.25 - 20.25| * 4 = 162
                    difference = int((81 + 162) * (99 / (12 * 20.25))) = 99

                    (case 3, increased precision, slightly bigger difference than case 1)
                    precision = 2 (maxValue = 100, middleValue = 49.5, maxMagnitudeFromMiddle = 2450.25)
                    state1 = 8070 (current = 80, last = 70)
                    state2 = 2030 (current = 20, last = 30)
                    state1Severity = (80 - 49.5) ** 2, preserving sign = 930.25
                    lastState1Severity = (70 - 49.5) ** 2, preserving sign = 420.25
                    state2Severity = (20 - 49.5) ** 2, preserving sign = -870.25
                    lastState2Severity = (30 - 49.5) ** 2, preserving sign = -380.25
                    stateMovementDifference = |(930.25 - 420.25) - (-870.25 - -380.25)| = 1000
                    currentStateDifference = |930.25 - -870.25| * 4 = 7202
                    difference = int((1000 + 7202) * (99 / (12 * 2450.25))) = 27
        '''

        precision = 1
        if len(i) == 3 and 'precision' in i[2]:
            precision = i[2]['precision']
        # maxValue is one larger than the largest value a state can take. half of max value - 1 is the midpoint for RSI (corresponds to 50%)
        maxValue = 10 ** precision
        middleValue = (maxValue - 1) / 2.0
        maxMagnitudeFromMiddle = middleValue ** 2

        # # states are integers where the first [precision] integers are the current_rsi, and the last [precision] integers are the last_rsi
        state1 = int(state1 / maxValue)
        lastState1 = int(state1 % maxValue)
        state2 = int(state2 / maxValue)
        lastState2 = int(state2 % maxValue)

        # trying to magnify the difference from the middle value, while preserving the sign. these all range [-maxMagnitudeFromMiddle, maxMagnitudeFromMiddle]
        state1Severity = ((state1 - middleValue) ** 2) * (-1 if state1 < middleValue else 1)
        lastState1Severity = ((lastState1 - middleValue) ** 2) * (-1 if lastState1 < middleValue else 1)
        state2Severity = ((state2 - middleValue) ** 2) * (-1 if state2 < middleValue else 1)
        lastState2Severity = ((lastState2 - middleValue) ** 2) * (-1 if lastState2 < middleValue else 1)

        # get differences between the recent changes of each state
        state1Change = state1Severity - lastState1Severity # range [-2 * maxMagnitudeFromMiddle, 2 * maxMagnitudeFromMiddle]
        state2Change = state2Severity - lastState2Severity # range [-2 * maxMagnitudeFromMiddle, 2 * maxMagnitudeFromMiddle]
        stateMovementDifference = abs(state1Change - state2Change) # range [0, 4 * maxMagnitudeFromMiddle]

        # get increased difference between current states
        currentStateDifference = abs(state1Severity - state2Severity) * 4 # range [0, 8 * maxMagnitudeFromMiddle]

        # range of (stateMovementDifference + currentStateDifference) is [0, 12 * maxMagnitudeFromMiddle]
        # constrain to range [0, 99]
        return int((stateMovementDifference + currentStateDifference) * (99.0 / (12.0 * maxMagnitudeFromMiddle)))



