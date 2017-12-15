from state.state import state
import pandas as pd
prices = pd.DataFrame.from_csv('./prices.csv')
indicators = [('bbands',5)]
s = state(indicators=indicators)

print(s.get_num_states())
print(s.get_state(prices))
