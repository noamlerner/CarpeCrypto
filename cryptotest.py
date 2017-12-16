from state.state import state
from crypto_learner import crypto_learner
from qlearner import qlearner
import pandas as pd
s = state([('rsi',5),('bbands',5),('rsi',10),('bbands',10),('rsi',20),('bbands',20)])
ql = qlearner(num_states=s.get_num_states(),num_actions=2,dyna=200)
cl = crypto_learner(qlearner=ql, state=s)
prices = pd.DataFrame.from_csv('./prices.csv')
cl.train(prices['vwap'],prices['high'],prices['low'])