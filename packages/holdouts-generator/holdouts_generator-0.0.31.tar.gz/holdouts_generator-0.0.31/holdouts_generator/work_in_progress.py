from .utils import work_in_progress_path, work_in_progress_directory
import pandas as pd
import os
from typing import Dict
from touch import touch
import shutil
from .store_results import load_results, is_result_directory, result_exists, get_all_results_directories


def skip(key: str, hyper_parameters: Dict, results_directory: str) -> bool:
    """Default function to choose to load or not a given holdout.
        key: str, key identifier of holdout to be skipped.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where to store the results.
    """
    return (
        is_work_in_progress(key, hyper_parameters, results_directory) or
        result_exists(key, hyper_parameters, results_directory)
    )


def add_work_in_progress(key: str, hyper_parameters: Dict = None, results_directory: str = "results"):
    """Sign given holdout key as under processing for given results directory.
        key: str, key identifier of holdout.
        hyper_parameters: Dict, hyper parameters to check for.
        results_directory: str = "results", directory where results are stored.
    """
    if skip(key, hyper_parameters, results_directory):
        raise ValueError("Given key {key} for given directory {results_directory} is already work in progress or completed!".format(
            key=key,
            results_directory=results_directory
        ))
    touch(work_in_progress_path(results_directory, key, hyper_parameters))


def is_work_in_progress(key: str, hyper_parameters: Dict = None, results_directory: str = "results") -> bool:
    """Return boolean representing if given key is under work for given results directory.
        key: str, key identifier of holdout.
        results_directory: str = "results", directory where results are stored.
    """
    return os.path.isfile(work_in_progress_path(results_directory, key, hyper_parameters))


def clear_work_in_progress(results_directory: str = "results"):
    """Delete work in progress log for given results directory.
        results_directory: str = "results", directory where results are stored.
    """
    if os.path.exists(work_in_progress_directory(results_directory)):
        shutil.rmtree(work_in_progress_directory(results_directory))


def clear_all_work_in_progress(root_results_directory: str = "results"):
    """Delete work in progress log for given results directory.
        root_results_directory: str = "results", directory where results are stored.
    """
    for results_directory in get_all_results_directories(root_results_directory):
        clear_work_in_progress(results_directory)
