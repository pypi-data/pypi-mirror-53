from dict_hash import sha256
from typing import Dict, Callable
import os
import numpy as np


def mkdir(path_function: Callable) -> Callable:
    """Decorator for automatically create directory for path returned from given function."""
    def wrapper(*args, **kwargs):
        path = path_function(*args, **kwargs)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
    return wrapper


@mkdir
def pickle_path(cache_directory: str, **hyper_parameters: Dict) -> str:
    """Return path where to pickle an holdout created with given parameters.
        cache_directory: str, directory where to store the holdouts cache.
        hyper_parameters: Dict, hyper parameters used to create the holdouts.
    """
    return "{results_directory}/holdouts/{hash}.pickle.gz".format(
        results_directory=cache_directory,
        hash=sha256(hyper_parameters)
    )


@mkdir
def info_path(cache_directory: str) -> str:
    """Return path where to store the cache file, recording the created holdouts.
        cache_directory: str, directory where to store the holdouts cache.
    """
    return "{cache_directory}/cache.csv".format(
        cache_directory=cache_directory
    )


@mkdir
def hyper_parameters_path(results_directory: str, hyper_parameters: Dict) -> str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        hyper_parameters: Dict, hyper parameters used to create and train the model.
    """
    return "{results_directory}/hyper_parameters/{hyper_parameters_key}.json".format(
        results_directory=results_directory,
        hyper_parameters_key=sha256(hyper_parameters)
    )


@mkdir
def parameters_path(results_directory: str, parameters: Dict) -> str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        parameters: Dict, hyper parameters used to create and train the model.
    """
    return "{results_directory}/parameters/{parameters_key}.json".format(
        results_directory=results_directory,
        parameters_key=sha256(parameters)
    )


@mkdir
def history_path(results_directory: str, history: Dict) -> str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        history: Dict, training history.
    """
    return "{results_directory}/histories/{history_key}.csv".format(
        results_directory=results_directory,
        history_key=sha256(history)
    )


@mkdir
def trained_model_path(results_directory: str, holdouts_key: str, hyper_parameters: Dict) -> str:
    """Return default path for storing the model trained with given holdout key and given parameters.
        results_directory: str, directory where to store the prediction_labels.
        holdouts_key:str, key that identifies the holdout used for training.
        hyper_parameters: Dict, hyperparameters used to train the model.
    """
    return "{results_directory}/trained_models/{holdouts_key}_{hyper_parameters}.h5".format(
        results_directory=results_directory,
        holdouts_key=holdouts_key,
        hyper_parameters=sha256(hyper_parameters)
    )


@mkdir
def results_path(results_directory: str) -> str:
    """Return default path for storing the main results csv.
        results_directory: str, directory where to store the prediction_labels.
    """
    return "{results_directory}/results.csv".format(
        results_directory=results_directory
    )


@mkdir
def work_in_progress_directory(results_directory: str) -> str:
    """Return default path for storing work in progress temporary files.
        results_directory: str, directory where to store the prediction_labels.
    """
    return "{results_directory}/work_in_progress".format(
        results_directory=results_directory
    )

@mkdir
def work_in_progress_path(results_directory: str, holdouts_key: str, hyper_parameters: str = None) -> str:
    """Return default path for storing the main work in progress csv.
        results_directory: str, directory where to store the prediction_labels.
    """
    return "{wip}/{holdouts_key}_{hyper_parameters}".format(
        wip=work_in_progress_directory(results_directory),
        holdouts_key=holdouts_key,
        hyper_parameters=sha256(
            {} if hyper_parameters is None else hyper_parameters)
    )


@mkdir
def predictions_labels_path(results_directory: str, predictions_labels: np.ndarray) -> str:
    """Return default path for prediction labels.
        results_directory: str, directory where to store the prediction_labels.
        predictions_labels: np.ndarray, array of prediction labels.
    """
    return "{results_directory}/predictions_labels/{hash}.csv".format(
        results_directory=results_directory,
        hash=sha256({
            "predictions_labels": predictions_labels
        })
    )


@mkdir
def true_labels_path(results_directory: str, true_labels: np.ndarray) -> str:
    """Return default path for true labels.
        results_directory: str, directory where to store the true_labels.
        true_labels: np.ndarray, array of true labels.
    """
    return "{results_directory}/true_labels/{hash}.csv".format(
        results_directory=results_directory,
        hash=sha256({
            "true_labels": true_labels
        })
    )
