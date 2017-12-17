"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand
import pandas as pd
class qlearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.9, \
        radr = 0.999, \
        dyna = 0):
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.s = 0
        self.a = 0
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        # policy
        self.Q = np.zeros((num_states, num_actions))
        # this represents our model of which state follows a particular state and action. so self.Model[s,a] will return a
        # two values np array with (s_prime, r), the new state and the reward for that state.
        self.model = np.zeros((num_states, num_actions, 2))
        self._states_seen = pd.DataFrame(columns=['state', 'actions'])
        self._states_seen = self._states_seen.set_index('state')

    def query_state(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        self.a = self._best_action(actions=self.Q[s])
        return self.a
    def get_states_seen(self):
        return self._states_seen.index

    def take_action_based_on_similarity_scores(self, scores):
        '''
        pass in an array that tells you the similarity states to a given state and this will return a boosted/weighted action
        to take
        :param scores: retrieved from state.get_similarity_scores
        :return: action
        '''
        actions = np.zeros(self.num_actions)
        num_voted = np.zeros(self.num_actions)
        # they get to vote :P
        electoral_college = scores.nsmallest(int(len(scores)/ 10),columns="score")
        for s in electoral_college.index:
            a = self._best_action(self.Q[s])
            actions[a] += scores.loc[s] ** 2
            num_voted[a]+=1
        no_votes = np.where(num_voted == 0)[0]
        actions[no_votes] = np.inf
        num_voted[no_votes] = 1
        actions /= num_voted ** 2
        return np.argmin(actions)

    def has_seen_state(self, state):
        '''
        For a given state, this will return whether or not the state has been trained on.
        '''
        return state in self._states_seen.index

    def _should_take_random_action(self):
        should_rand = np.random.choice(2,p=[1-self.rar, self.rar])
        self.rar *= self.radr
        return should_rand

    def _best_action(self, actions):
        return np.argmax(actions)

    def _random_action(self, actions):
        '''
        takes any action that is NOT the best action
        '''
        best_action = self._best_action(actions)
        possible = [i for i in range(self.num_actions) if i != best_action]
        return rand.choice(possible)

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        # record keeping
        self.model[self.s, self.a] = np.array([s_prime, r])
        self._see_state_action(self.s, self.a)
        self.Q[self.s, self.a] = self._new_Q_value(self.s, self.a, r, s_prime)
        # dyna
        self._hallucinate()
        # action
        self.s = s_prime
        if self._should_take_random_action():
            self.a = self._random_action(self.Q[s_prime])
        else:
            self.a = self._best_action(actions=self.Q[s_prime])
        return self.a

    def _see_state_action(self,s,a):
        if s not in self._states_seen.index:
            self._states_seen.loc[s] = [np.array([a])]
            # self.states_seen['l'].append(s)
        elif a not in self._states_seen.loc[s]:
            self._states_seen.loc[s] = [np.append(self._states_seen.loc[s]['actions'], [a])]

    def _new_Q_value(self, s, a, r, s_prime):
        old_value = (1 - self.alpha) * self.Q[s,a]
        next_best_action = self._best_action(self.Q[s_prime])
        new_value = self.alpha * (r + self.gamma * self.Q[s_prime, next_best_action])
        return old_value + new_value

    def _hallucinate(self):
        if self.dyna == 0:
            return
        # if dyna isnt doing anything we can end early
        unchanged_iterations = 0
        d = self._states_seen.sample(self.dyna, replace=True)
        for s in d.index:
            actions_taken = self._states_seen.loc[s]['actions']
            a = np.random.choice(actions_taken)
            hallucination = self.model[s, a]
            old_value = self.Q[s,a]
            self.Q[s,a] = self._new_Q_value(s, a, int(hallucination[1]), int(hallucination[0]))
            if old_value == self.Q[s,a]:
                unchanged_iterations += 1
            else:
                unchanged_iterations = 0
            if unchanged_iterations >= 10:
                break
