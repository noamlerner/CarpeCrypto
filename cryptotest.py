from state.state import state
from crypto_learner import crypto_learner
from qlearner import qlearner
import pandas as pd
s = state([('rsi',5,{'precision':2}),('bbands',7),('rsi',10,{'precision':2}),('bbands',3)])
ql = qlearner(num_states=s.get_num_states(),num_actions=2,dyna=100)
cl = crypto_learner(qlearner=ql, state=s)
prices = pd.DataFrame.from_csv('./prices.csv')
converged = False
last_cr = 199000
num_converged = 0
while not converged:
    cr = cl.train(prices['vwap'],prices['high'],prices['low'])
    converged = abs(last_cr - cr) < 0.0000000001 and cr > 0
    print("CR:" + str(cr))
    last_cr = cr
