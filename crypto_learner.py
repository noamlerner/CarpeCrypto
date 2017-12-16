from state.state import state
from portfolio import portfolio
class crypto_learner(object):
    def __init__(self, qlearner, state):
        self.qlearner = qlearner
        self.state = state
        self.initial_value = 1000

    def train(self, prices, highs, lows):
        for i in range(20):
            self.portfolio = portfolio(self.initial_value)
            self.last_value = self.initial_value
            start_index = self.state.minimum_datapoints_required()
            # set_state
            state = self.state.get_state(prices[:start_index])
            action = self.qlearner.query_state(int(state))
            # iterative loop
            for i in range(start_index+1,len(prices)):
                reward = self._get_reward(highs[:i],lows[:i],self.portfolio,action)
                state = self.state.get_state(prices[:i])
                action = self.qlearner.query(int(state), reward)
            cr = self.portfolio.value(lows) / self.initial_value -1
            print("CR: " + str(cr))
            print("rar: " + str(self.qlearner.rar))

    def _get_reward(self, highs, lows, portfolio, action):
        '''
        :param highs: high prices as a dataframe. action should have been taken on second to last data point
        :param lows:  low prices as a dataframe. action should have been taken on the second to last datapoint
        :param holding: the state of the portfolio at the time of the action. 2 = not holding, 1 = long, 0 short
        :param action: action taken, 1 = hold max, 0 = hold none
        :return: reward based on 1,000 dollars
        '''
        if action == 0:
            portfolio.sell(lows[:-1])
        if action == 1:
            portfolio.buy(highs[:-1])
        value = portfolio.value(lows)
        reward = value - self.last_value
        self.last_value = value
        return reward