# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np


class BasePositioner:
    def __init__(self, epsilon=1):
        self.epsilon = epsilon

        self.pos_new = None
        self.score_new = -1000

        self.pos_current = None
        self.score_current = -1000

        self.pos_best = None
        self.score_best = -1000

    def move_climb(self, _cand_, pos, epsilon_mod=1):

        sigma = (_cand_._space_.dim / 33) * self.epsilon / epsilon_mod + 1
        pos_new = np.random.normal(pos, sigma, pos.shape)
        pos_new_int = np.rint(pos_new)

        n_zeros = [0] * len(_cand_._space_.dim)
        pos = np.clip(pos_new_int, n_zeros, _cand_._space_.dim)

        # if np.array_equal(_cand_.pos_best, pos):
        # pos_new = np.random.uniform(pos - 1, pos + 1, pos.shape)

        return pos

    def move_random(self, _cand_):
        return _cand_._space_.get_random_pos()
