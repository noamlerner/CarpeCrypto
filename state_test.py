from state.state import state
import pandas as pd
prices = pd.DataFrame.from_csv('./prices.csv')
indicators = [('rsi',5,{'precision':3})]
s = state(indicators=indicators)

print(s.get_num_states())
print(s.get_state(prices))
