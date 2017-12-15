from state.state import state
import pandas as pd
prices = pd.DataFrame.from_csv('./prices.csv')
indicators = [('rsi',5,{'precision':2}),('bbands',10)]
s = state(indicators=indicators)

print(s.get_num_states())
state1 = s.get_state(prices)
state2 = s.get_state(prices[:-10])
print(s.compare(state1,state2))
