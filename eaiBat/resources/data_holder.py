from copy import deepcopy

import dpath.util
# Act as a singleton in order to access without update dataset


TEST_DATA = {}


def retrieve_data(path: str):
    """Access the data dictionary by its path and returns a deepcopy"""
    return deepcopy(dpath.util.get(TEST_DATA, path))
