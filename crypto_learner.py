from state.state import state
from portfolio import portfolio
class crypto_learner(object):
    def __init__(self, qlearner, state):
        self.qlearner = qlearner
        self.state = state
        self.initial_value = 1000

    def train(self, prices, highs, lows):
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
        return self.portfolio.value(lows) / self.initial_value -1

    def test(self,prices,highs,lows):
        self.portfolio = portfolio(self.initial_value)
        self.last_value = self.initial_value
        start_index = self.state.minimum_datapoints_required()
        for i in range(start_index,len(prices)):
            state = self.state.get_state(prices[:i])
            if not self.qlearner.has_seen_state(int(state)):
                print("Havent seen state: " + state)
                scores = self.state.get_similarity_scores(self.qlearner.get_states_seen(),state)
                action = self.qlearner.act_based_on_similarity_scores(scores)
            else:
                action = self.qlearner.query_state(int(state))
            self._get_reward(highs[:i], lows[:i], self.portfolio, action)
        return self.portfolio.value(lows) / self.initial_value -1

    def _get_reward(self, highs, lows, portfolio, action):
        '''
        :param highs: high prices as a dataframe. action should have been taken on second to last data point
        :param lows:  low prices as a dataframe. action should have been taken on the second to last datapoint
        :param portfolio: the portfolio represnting this traders holdings
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