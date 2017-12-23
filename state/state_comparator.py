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

    def bbands_compare(self, i, state1, lastState1, state2, lastState2):
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


    def rsi_compare(self, i, state1, lastState1, state2, lastState2):
        '''
            Calculates the normalized simliarity based on the sum of the following values:
                absolute value of difference in current rsi and last rsi for each state scaled by its deviation from the middle RSI value (5 if precision=1, 50 if precision=2, etc)
                difference of current state1 rsi and current state2 rsi, also scaled by their deviation from the middle RSI, but multiplied by 4 to increase its weight
                examples:
                    (case 1, reasonable difference)
                    precision = 1 (maxValue = 10, middleValue = 5, maxMagnitudeFromMiddle = 25)
                    state1 = 2 4 (current = 2, last = 4)
                    state2 = 5 7 (current = 5, last = 7)
                    state1Severity = (2 - 5) ** 2, preserving sign = -9
                    lastState1Severity = (4 - 5) ** 2, preserving sign = -1
                    state2Severity = (5 - 5) ** 2, preserving sign = 0
                    lastState2Severity = (7 - 5) ** 2, preserving sign = 4
                    stateMovementDifference = |-9 - -1| + |0 - 4| = 12
                    currentStateDifference = |-9 - 0| * 4 = 36
                    difference = (12 + 18) * (99 / (8 * 25)) = 15

                    (case 2, max possible difference)
                    precision = 1 (maxValue = 10, middleValue = 5, maxMagnitudeFromMiddle = 25)
                    state1 = 10 0 (current = 10, last = 0)
                    state2 = 0 10 (current = 0, last = 10)
                    state1Severity = (10 - 5) ** 2, preserving sign = 25
                    lastState1Severity = (0 - 5) ** 2, preserving sign = -25
                    state2Severity = (10 - 5) ** 2, preserving sign = 25
                    lastState2Severity = (0 - 5) ** 2, preserving sign = -25
                    stateMovementDifference = |25 - -25| + |25 - -25| = 100
                    currentStateDifference = |-25 - 25| * 4 = 200
                    difference = (100 + 200) * (99 / (8 * 25)) = 99

                    (case 3, increased precision, slightly bigger difference than case 1)
                    precision = 2 (maxValue = 100, middleValue = 50, maxMagnitudeFromMiddle = 2500)
                    state1 = 80 70 (current = 80, last = 70)
                    state2 = 20 30 (current = 20, last = 30)
                    state1Severity = (80 - 50) ** 2, preserving sign = 900
                    lastState1Severity = (70 - 50) ** 2, preserving sign = 400
                    state2Severity = (20 - 50) ** 2, preserving sign = -900
                    lastState2Severity = (30 - 50) ** 2, preserving sign = -400
                    stateMovementDifference = |900 - 400| + |-900 - -400| = 2600
                    currentStateDifference = |900 - -900| * 4 = 7200
                    difference = (2600 + 7200) * (99 / (8 * 2500)) = 48
        '''

        precision = 1
        if len(i) == 3 and 'precision' in i[2]:
            precision = i[2]['precision']
        # maxValue is the largest value any state can take. half of max value is the midpoint for RSI (corresponds to 50%)
        maxValue = 10 ** precision
        middleValue = maxValue / 2.0
        maxMagnitudeFromMiddle = middleValue ** 2

        # # states are integers where the first [precision] integers are the current_rsi, and the last [precision] integers are the last_rsi
        # state1 = int(state1 / maxValue)
        # lastState1 = int(state1 % maxValue)
        # state2 = int(state2 / maxValue)
        # lastState2 = int(state2 % maxValue)

        # trying to magnify the difference from the middle value, while preserving the sign. these all range [-maxMagnitudeFromMiddle, maxMagnitudeFromMiddle]
        state1Severity = ((state1 - middleValue) ** 2) * (-1 if state1 < middleValue else 1)
        lastState1Severity = ((lastState1 - middleValue) ** 2) * (-1 if lastState1 < middleValue else 1)
        state2Severity = ((state2 - middleValue) ** 2) * (-1 if state2 < middleValue else 1)
        lastState2Severity = ((lastState2 - middleValue) ** 2) * (-1 if lastState2 < middleValue else 1)

        # get differences between the recent changes of each state
        state1Change = abs(state1Severity - lastState1Severity) # range [0, 2 * maxMagnitudeFromMiddle]
        state2Change = abs(state2Severity - lastState2Severity) # range [0, 2 * maxMagnitudeFromMiddle]
        stateMovementDifference = state1Change + state2Change # range [0, 4 * maxMagnitudeFromMiddle]

        # get increased difference between current states
        currentStateDifference = abs(state1Severity - state2Severity) * 4 # range [0, 8 * maxMagnitudeFromMiddle]

        # range of (stateMovementDifference + currentStateDifference) is [0, 12 * maxMagnitudeFromMiddle]
        # constrain to range [0, 99]
        return int((stateMovementDifference + currentStateDifference) * (99.0 / (12.0 * maxMagnitudeFromMiddle)))



