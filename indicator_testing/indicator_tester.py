from state.state import state
import numpy as np
import pandas as pd
from qlearner import qlearner
import datetime as dt
from crypto_learner import crypto_learner
class indicator_tester(object):
    '''
    Indicator tester takes in an indicators array
    It uses the same price data every time
    It splits this data into 3 sets  -->   [training data] [ testing data] [ training data]
    Testing data is always the same size (currently 10% of the data)
    it trains on the training data until it converges. It tests how long it takes to converge
    It then tests on the 10% of data and keeps track of the CR
    it will output the times and CR along the way and the averages at the end.
    '''
    def __init__(self, indicators):
        self.indicators=indicators
        print("Starting test for " + str(self.indicators))
        self.state = state(indicators, with_holding=True)
        self.prices = pd.read_csv("./test_prices.csv")
        self.prices.set_index("dtime",inplace=True)
        self.trial_times = []
        self.CRs = []
        self.test()
        print("Average CR: " + str(np.mean(self.CRs)))
        print("Average Time To Run: " + str(np.mean(self.trial_times)))

    def test(self):
        at_index = 0
        slice_size = int(len(self.prices) / 10)
        while at_index * slice_size + slice_size < len(self.prices):
            testing_slice_start = at_index * slice_size
            testing_slice = self.prices.iloc[testing_slice_start:testing_slice_start+slice_size]
            training_slices = [self.prices.iloc[0:testing_slice_start], self.prices.iloc[testing_slice_start+slice_size:]]
            self.run_trial(testing_slice, training_slices)
            at_index+=1
    def run_trial(self,testing_slice, training_slices):
        ql = qlearner(num_states=self.state.get_num_states(), num_actions=2, dyna=100)
        cl = crypto_learner(qlearner=ql, state=self.state)
        print("Starting Training for Trial")
        converged = False
        cr = 0
        last_cr = 9999
        start_time = dt.datetime.now()
        while not converged:
            for training_slice in training_slices:
                if len(training_slice):
                    cr = cl.train(training_slice['vwap'],training_slice['high'],training_slice['low'])
            converged = abs(last_cr - cr) < 0.00000001
            print("Trying to converge, current CR:" + str(cr))
            last_cr = cr
        end_time = dt.datetime.now()
        delta = end_time - start_time
        print("Time To Converge : " + str(delta))
        self.trial_times.append(delta)

        print("Starting Testing for trial")
        cr = cl.train(testing_slice['vwap'],testing_slice['high'],testing_slice['low'])
        print("Cumulative Return: "+ str(cr))
        self.CRs.append(cr)
