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
        state = self.state.get_state(prices[:start_index], self.portfolio.is_holding())
        action = self.qlearner.query_state(int(state))
        # iterative loop
        for i in range(start_index+1,len(prices)):
            reward = self._get_reward(highs, lows, self.portfolio, action)
            state = self.state.get_state(prices[:i], self.portfolio.is_holding())
            action = self.qlearner.query(int(state), reward)
        return self.portfolio.value(lows.iloc[-1]) / self.initial_value -1

    def test(self,prices,highs,lows):
        self.portfolio = portfolio(self.initial_value)
        self.last_value = self.initial_value
        start_index = self.state.minimum_datapoints_required()
        for i in range(start_index,len(prices)):
            action = self.get_action(prices[:i], self.portfolio.is_holding())
            self._get_reward(highs, lows, self.portfolio, action)
        return self.portfolio.value(lows.iloc[-1]) / self.initial_value -1
    def get_action(self, prices, is_holding):
        state = self.state.get_state(prices, is_holding)
        if not self.qlearner.has_seen_state(int(state)):
            print("Havent seen state: " + state)
            scores = self.state.get_similarity_scores(self.qlearner.get_states_seen(), state)
            action = self.qlearner.act_based_on_similarity_scores(scores)
        else:
            action = self.qlearner.query_state(int(state))
        return action

    def _get_reward(self, highs, lows, portfolio, action):
        '''
        Highs and lows should be a dataframe where a trade was taken at index -2.
        :param portfolio: the portfolio represnting this traders holdings
        :param action: action taken, 1 = hold max, 0 = hold none
        :return: reward based on 1,000 dollars
        '''
        if action == 0:
            portfolio.sell(lows.iloc[-2])
        if action == 1:
            portfolio.buy(highs.iloc[-2])
        value = portfolio.value(lows.iloc[-1])
        reward = value - self.last_value
        self.last_value = value
        return reward