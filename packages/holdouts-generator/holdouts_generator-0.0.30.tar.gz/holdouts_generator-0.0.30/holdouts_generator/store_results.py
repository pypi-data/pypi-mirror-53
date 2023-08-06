from typing import Dict, List, Tuple
import os
import pandas as pd
import numpy as np
from .utils import results_path, hyper_parameters_path, parameters_path, history_path, trained_model_path, true_labels_path, predictions_labels_path
from .utils import build_keys, build_query, load_cache, is_valid_holdout_key, get_path_from_key
from keras import Model
import shutil
from json import dump
import humanize
from auto_tqdm import tqdm
from multiprocessing import cpu_count, Pool


def store_result(key: str, new_results: Dict, time: int, hyper_parameters: Dict = None, parameters: Dict = None, results_directory: str = "results"):
    """Store given results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        new_results: Dict, results to store.
        hyper_parameters: Dict, hyper parameters to check for.
        parameters: Dict, parameters used for tuning the model.
        results_directory: str = "results", directory where to store the results.
    """
    if result_exists(key, hyper_parameters, results_directory):
        raise ValueError("Given key {key} and hyper_parameters {hyper_parameters} map already to a result in directory {results_directory}!".format(
            key=key,
            hyper_parameters=hyper_parameters,
            results_directory=results_directory
        ))
    os.makedirs(results_directory, exist_ok=True)
    hppath = None if hyper_parameters is None else hyper_parameters_path(
        results_directory, hyper_parameters)
    ppath = None if parameters is None else parameters_path(
        results_directory, parameters)
    new_row = pd.DataFrame({
        **new_results,
        **build_keys(key, hyper_parameters),
        "hyper_parameters_path": hppath,
        "parameters_path": ppath,
        "required_time": time,
        "human_required_time": humanize.naturaldelta(time)
    }, index=[0])
    if hyper_parameters is not None:
        with open(hppath, "w") as f:
            dump(hyper_parameters, f)
    if parameters is not None:
        with open(ppath, "w") as f:
            dump(parameters, f)
    try:
        results = pd.concat([load_results(results_directory), new_row])
    except FileNotFoundError:
        results = new_row
    store_results_csv(results, results_directory)


def is_result_directory(results_directory: str) -> bool:
    """Return boolean representing if given directory contains results.
        results_directory: str, directory to determine if contains results.
    """
    return os.path.isfile(results_path(results_directory))


def result_exists(key: str, hyper_parameters: Dict = None, results_directory: str = "results") -> bool:
    """Return boolean representing if given key is work completed for given results directory.
        key: str, key identifier of holdout.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where results are stored.
    """
    return is_result_directory(results_directory) and not load_results(results_directory).query(
        build_query(build_keys(key, hyper_parameters))
    ).empty


def get_all_results_directories(rootdir: str):
    """Return list of all result directories under rootdir, including rootdir if contains results.
        rootdir:str, directory from which to start.
    """
    return [
        os.path.join(root, subdir)
        for root, subdirs, files in os.walk(rootdir) for subdir in subdirs
        if is_result_directory(os.path.join(root, subdir))
    ] + ([rootdir] if is_result_directory(rootdir) else [])


def store_results_csv(results: pd.DataFrame, results_directory: str = "results"):
    """Store results csv from given results directory.
        results: pd.DataFrame, standard dataframe of results to store.
        results_directory: str = "results", directory where to store the results.
    """
    results.to_csv(results_path(results_directory), index=False)


def store_keras_result(key: str, history: Dict, x_test: np.ndarray, y_test_true: np.ndarray, model: Model, time: int, informations: Dict = None, hyper_parameters: Dict = None, parameters: Dict = None, save_model: bool = True, results_directory: str = "results"):
    """Store given keras model results in a standard way, so that the skip function can use them.
        key: str, key identifier of holdout to be skipped.
        history: Dict, training history to store.
        x_test:np.ndarray, input test values for the model.
        y_test_true:np.ndarray, true output test values.
        model:Model, model to save if save_model is True, used to predict the value.
        hyper_parameters: Dict, hyper parameters to check for.
        parameters: Dict, parameters used for tuning the model.
        save_model:bool=True, whetever to save or not the model.
        results_directory: str = "results", directory where to store the results.
    """
    if result_exists(key, hyper_parameters, results_directory):
        raise ValueError("Given key {key} and hyper_parameters {hyper_parameters} map already to a result in directory {results_directory}!".format(
            key=key,
            hyper_parameters=hyper_parameters,
            results_directory=results_directory
        ))
    y_pred = model.predict(x_test)
    hpath = history_path(results_directory, history)
    mpath = trained_model_path(results_directory, key, hyper_parameters)
    plpath = predictions_labels_path(results_directory, y_pred)
    tlpath = true_labels_path(results_directory, y_test_true)

    informations = {} if informations is None else informations
    dfh = pd.DataFrame(history)
    store_result(key, {
        **dfh.iloc[-1].to_dict(),
        **informations,
        "history_path": hpath,
        "model_path": mpath if save_model else None,
        "predictions_labels_path": plpath,
        "true_labels_path": tlpath
    }, time, hyper_parameters, parameters, results_directory)
    dfh.to_csv(hpath, index=False)
    pd.DataFrame(y_pred).to_csv(plpath, index=False)
    pd.DataFrame(y_test_true).to_csv(tlpath, index=False)
    if save_model:
        model.save(mpath)


def load_results(results_directory: str = "results") -> pd.DataFrame:
    """Load standard results.
        results_directory: str = "results", directory where results are stored.
    """
    return pd.read_csv(results_path(results_directory))


def load_result(key: str, hyper_parameters: Dict = None, results_directory: str = "results"):
    """Load standard results corresponding at given key and hyper_parameters.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    return load_results(results_directory).query(
        build_query(build_keys(key, hyper_parameters))
    ).to_dict('records')[0]

def delete_results(results_directory: str = "results"):
    """Delete the results stored in a given directory.
        results_directory: str = "results", directory where results are stores.
    """
    if os.path.exists(results_directory):
        shutil.rmtree(results_directory)


def is_valid_path(path: str, results_directory: str) -> bool:
    """Return a boolean represing if the given path is valid.
        path:str, the path to be tested.
        results_directory: str, directory where results are stores.
    """
    return not pd.isna(path) and isinstance(path, str) and path.startswith(results_directory) and os.path.isfile(path)


def get_paths_columns(df: pd.DataFrame) -> List[str]:
    """Return columns deemed as paths from given dataframe.
        df:pd.DataFrame, dataframe to analyze.
    """
    return [path for path in df if path.endswith("_path")]


def delete_result_by_key(key: str, results_directory: str = "results"):
    """Delete the results stored in a given directory.
        results_directory: str = "results", directory where results are stores.
    """
    results = load_results(results_directory)
    paths = get_paths_columns(results)
    mask = results.holdouts_key == key
    for path in results[paths][mask].values.flatten():
        if is_valid_path(path, results_directory):
            os.remove(path)
    store_results_csv(results[~mask], results_directory)


def delete_deprecated_results(cache_dir: str = ".holdouts", results_directory: str = "results") -> List[str]:
    """Delete the results which do not map anymore to a valid holdout and return the list of deleted keys.
        cache_dir:str=".holdouts", the holdouts cache directory to be deleted.
        results_directory: str = "results", directory where results are stores.
    """
    results = load_results(results_directory)
    holdouts = load_cache(cache_dir)
    keys = []
    for key in np.unique(results.holdouts_key):
        if not holdouts.key.eq(key).any() or not is_valid_holdout_key(
            get_path_from_key(holdouts, key), key
        ):
            delete_result_by_key(key, results_directory)
            keys.append(key)
    return keys


def update_path(path: str, old_root: str, new_root: str) -> str:
    """Return path with old root string in path replaced with a new given one.
        path:str, the path to update.
        old_root:str, old root to delete.
        new_root:str, new root to apply.
    """
    return new_root + path[len(old_root):]


def copy_file_mkdir(job: Tuple[str, str]):
    source, destination = job
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copy(source, destination)


def merge_results(results_directories: List[str], target_results_directory: str):
    """Copies the results from the given results_directories into a given target directory.
        results_directories:List[str], list of directories to copy from.
        target_results_directory:str, target directory to copy to.
    """
    os.makedirs(target_results_directory, exist_ok=True)
    sources = [
        load_results(results_directory)
        for results_directory in results_directories
    ]
    targets = []
    for original, results_directory in zip(sources, results_directories):
        target = original.copy()
        paths = get_paths_columns(target)
        target[paths] = target[paths].applymap(lambda value: update_path(
            value,
            results_directory,
            target_results_directory
        ) if is_valid_path(value, results_directory) else value)
        targets.append(target)

    jobs = [
        (source_path, target_path) for ori, upd, results_directory in zip(
            sources, targets, results_directories
        ) for source_path, target_path in zip(
            ori.values.flatten(),
            upd.values.flatten()
        ) if is_valid_path(source_path, results_directory)
    ]
    with Pool(min(cpu_count(), len(jobs))) as p:
        list(tqdm(p.imap(copy_file_mkdir, jobs),
                  total=len(jobs), desc="Copying files"))
        p.close()
        p.join()
    store_results_csv(pd.concat(targets), target_results_directory)
    delete_duplicate_results(target_results_directory)


def merge_all_results(root_results_directory: str, target_results_directory: str):
    """Copies the results under given root_results_directory into a given target directory.
        root_results_directory:str, directory from which to start.
        target_results_directory:str, target directory to copy to.
    """
    merge_results(get_all_results_directories(
        root_results_directory), target_results_directory)


def delete_duplicate_results(results_directory: str = "results"):
    """Delete duplicate results from given results directory.
        results_directory: str = "results", directory where results are stores.
    """
    store_results_csv(load_results(results_directory).drop_duplicates([
        "holdouts_key", "hyper_parameters_key"
    ]), results_directory)


def delete_all_duplicate_results(root_results_directory: str):
    """Delete duplicate results under given root_results_directory into a given target directory.
        root_results_directory:str, directory from which to start.
    """
    for results_directory in get_all_results_directories(root_results_directory):
        delete_duplicate_results(results_directory)


def delete_all_deprecated_results(cache_dir: str, root_results_directory: str)->List[str]:
    """Delete the results which do not map anymore to a valid holdout and return the list of deleted keys.
        cache_dir:str=".holdouts", the holdouts cache directory to be deleted.
        root_results_directory:str, directory from which to start.
    """
    return [
        key for results_directory in get_all_results_directories(root_results_directory)
        for key in delete_deprecated_results(cache_dir, results_directory)
    ]