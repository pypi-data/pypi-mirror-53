# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import random
import numpy as np


class SearchSpace:
    def __init__(self, _config_, model_nr):
        self.search_config = _config_.search_config
        self.warm_start = _config_.warm_start
        self.scatter_init = _config_.scatter_init
        self.model_nr = model_nr

        self.memory = {}

    def pos_space_limit(self):
        dim = []

        for pos_key in self.para_space:
            dim.append(len(self.para_space[pos_key]) - 1)

        self.dim = np.array(dim)

    def create_kerasSearchSpace(self):
        """
        para_space = {}

        for para_key in search_config_temp.keys():

            for param_str in search_config_temp[para_key].keys():
                new_param_str = para_key + "." + param_str

                para_space[new_param_str] = search_config_temp[para_key][param_str]

        """

        self.para_space = self.search_config[list(self.search_config)[self.model_nr]]

        self.pos_space_limit()

    def get_random_pos(self):
        pos_new = np.random.uniform(np.zeros(self.dim.shape), self.dim, self.dim.shape)
        pos = np.rint(pos_new)

        # n_zeros = [0] * len(self.dim)
        # pos = np.clip(pos_new_int, n_zeros, self.dim)
        return pos

    def get_random_pos_scalar(self, hyperpara_name):
        n_para_values = len(self.para_space[hyperpara_name])
        pos = random.randint(0, n_para_values - 1)

        return pos

    def pos2para(self, pos):
        if len(self.para_space.keys()) == pos.size:
            values_dict = {}
            for i, key in enumerate(self.para_space.keys()):
                pos_ = int(pos[i])
                values_dict[key] = list(self.para_space[key])[pos_]

            return values_dict
