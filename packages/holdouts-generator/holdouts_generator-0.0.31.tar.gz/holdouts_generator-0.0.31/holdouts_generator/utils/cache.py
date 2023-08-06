from typing import Callable, List, Dict
from .paths import pickle_path, info_path
from .various import odd_even_split, build_query
from .hash import hash_file
import os
import pandas as pd
import zlib
import pickle
import compress_pickle


def uncached(generator: Callable, dataset: List, *args, **kwargs):
    return odd_even_split(generator(dataset)), None


def cached(generator: Callable, dataset: List, cache_dir: str, **parameters: Dict):
    path = pickle_path(cache_dir, **parameters)
    try:
        holdouts = load_cache(cache_dir)
        key = get_key_from_path(holdouts, path)
        if not is_valid_holdout_key(path, key):
            raise ValueError("Holdout has been tempered with!")
        return compress_pickle.load(path), key
    except (pickle.PickleError, FileNotFoundError, AttributeError,  EOFError, ImportError, IndexError, zlib.error):
        data = odd_even_split(generator(dataset))
    key = dump(data, cache_dir, path, **parameters)
    return (data, key)


def get_key_from_path(holdouts: pd.DataFrame, path: str) -> str:
    """Return holdout's key matched to given holdout's path.
        holdouts:pd.DataFrame, dataframe of the holdouts' cache.
        path:str, the holdout's path.
    """
    return holdouts.query(
        build_query({"path": path})
    )["key"].values[0]


def get_path_from_key(holdouts: pd.DataFrame, key: str) -> str:
    """Return holdout's path matched to given holdout's key.
        holdouts:pd.DataFrame, dataframe of the holdouts' cache.
        key:str, the holdout's key.
    """
    return holdouts.query(
        build_query({"key": key})
    )["path"].values[0]


def is_cache_directory(cache_dir: str) -> bool:
    """Return boolean representing if given directory contains holdout caches.
        cache_dir: str, directory to determine if contains caches.
    """
    return os.path.isfile(info_path(cache_dir))


def is_valid_holdout_key(path: str, key: str) -> bool:
    """Return bool representing if given key is correct sign for given holdout's path.
        path:str, the holdout's path.
        key:str, the holdout's key.
    """
    try:
        return hash_file(path) == key
    except FileNotFoundError:
        return False


def build_info(path: str, parameters: Dict, key: str) -> pd.DataFrame:
    return pd.DataFrame({
        "path": path,
        "key": key,
        **parameters
    }, index=[0])


def dump(data, cache_dir: str, path: str, **parameters: Dict) -> str:
    compress_pickle.dump(data, path)
    key = hash_file(path)
    new_row = build_info(path, parameters, key)
    try:
        holdouts = pd.concat([load_cache(cache_dir), new_row])
    except FileNotFoundError:
        holdouts = new_row
    store_cache(holdouts, cache_dir)
    return key


def get_holdout_key(cache_dir: str, **parameters: Dict) -> str:
    """Return key, if cached, for given holdout else return None.
        cache_dir:str, cache directory to load data from
        parameters:Dict, parameters used to generated the holdout.
    """
    try:
        return pd.read_csv(info_path(cache_dir)).query(build_query(parameters))["key"].values[0]
    except (FileNotFoundError, IndexError):
        return None


def load_cache(cache_dir: str) -> pd.DataFrame:
    """Load the holdouts cache.
        cache_dir:str=".holdouts", the holdouts cache directory.
    """
    return pd.read_csv(info_path(cache_dir))


def store_cache(holdouts: pd.DataFrame, cache_dir: str):
    """Store the holdouts cache.
        holdouts:pd.DataFrame, dataframe of the holdouts' cache.
        cache_dir:str=".holdouts", the holdouts cache directory.
    """
    holdouts.to_csv(info_path(cache_dir), index=False)


def delete_deprecated_cache(cache_dir: str = ".holdouts"):
    """Delete the cache which do not map anymore to a valid holdout.
        cache_dir:str=".holdouts", the holdouts cache directory to be removed.
    """
    holdouts = load_cache(cache_dir)
    for path, key in zip(holdouts.path, holdouts.key):
        if not is_valid_holdout_key(path, key):
            delete_holdout_by_key(key, cache_dir)


def delete_holdout_by_key(key: str, cache_dir: str = ".holdouts"):
    """Delete holdout with given key.
        cache_dir:str=".holdouts", the holdouts cache directory.
        key:str, the holdout's key.
    """
    holdouts = load_cache(cache_dir)
    path = get_path_from_key(holdouts, key)
    if os.path.exists(path):
        os.remove(path)
    store_cache(holdouts[holdouts.key != key], cache_dir)


def get_all_cache_directories(rootdir: str):
    """Return list of all result directories under rootdir, including rootdir if contains cache.
        rootdir:str, directory from which to start.
    """
    return [
        os.path.join(root, subdir)
        for root, subdirs, files in os.walk(rootdir) for subdir in subdirs
        if is_cache_directory(os.path.join(root, subdir))
    ] + ([rootdir] if is_cache_directory(rootdir) else [])


def delete_all_deprecated_cache(root_cache_dir: str):
    """Delete the cache which do not map anymore to a valid holdout recursively.
        cache_dir:str=".holdouts", the holdouts cache directory to be removed.
    """
    for results_directory in get_all_cache_directories(root_cache_dir):
        delete_deprecated_cache(results_directory)
