import os
import pickle


def load_from_pickle(path: str, fnc):
    if os.path.exists(path):
        print('Loading pkl at {}.'.format(path))
        with open(path, 'rb') as f:
            res = pickle.load(f)
    else:
        res = fnc()
        with open(path, 'wb') as f:
            pickle.dump(res, f)
    return res
