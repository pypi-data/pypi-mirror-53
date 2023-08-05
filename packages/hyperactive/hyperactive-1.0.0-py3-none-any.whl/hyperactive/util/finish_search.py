# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


def finish_search_(_config_, _cand_, X, y):
    _cand_._model_.cv = 1
    _cand_.eval_pos(_cand_.pos_best, X, y, force_eval=True)
    _config_.close_p_bar()

    return _cand_
