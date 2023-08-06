from dict_hash import sha256
from typing import Dict
import os
import numpy as np

def pickle_path(cache_directory: str, **hyper_parameters: Dict)->str:
    """Return path where to pickle an holdout created with given parameters.
        cache_directory: str, directory where to store the holdouts cache.
        hyper_parameters: Dict, hyper parameters used to create the holdouts.
    """
    root = "{cd}/holdouts".format(cd=cache_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{hash}.pickle.gz".format(
        root=root,
        hash=sha256(hyper_parameters)
    )

def info_path(cache_directory: str)->str:
    """Return path where to store the cache file, recording the created holdouts.
        cache_directory: str, directory where to store the holdouts cache.
    """
    return "{cache_directory}/cache.csv".format(
        cache_directory=cache_directory
    )

def hyper_parameters_path(results_directory: str, hyper_parameters: Dict)->str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        hyper_parameters: Dict, hyper parameters used to create and train the model.
    """
    root = "{rd}/hyper_parameters".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{hyper_parameters_key}.json".format(
        root=root,
        hyper_parameters_key=sha256(hyper_parameters)
    )

def parameters_path(results_directory: str, parameters: Dict)->str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        parameters: Dict, hyper parameters used to create and train the model.
    """
    root = "{rd}/parameters".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{parameters_key}.json".format(
        root=root,
        parameters_key=sha256(parameters)
    )

def history_path(results_directory: str, history: Dict)->str:
    """Return path where to store metrics tracked during history.
        results_directory: str, directory where to store the prediction_labels.
        history: Dict, training history.
    """
    root = "{rd}/histories".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{history_key}.csv".format(
        root=root,
        history_key=sha256(history)
    )

def trained_model_path(results_directory: str, holdouts_key:str, hyper_parameters: Dict)->str:
    """Return default path for storing the model trained with given holdout key and given parameters.
        results_directory: str, directory where to store the prediction_labels.
        holdouts_key:str, key that identifies the holdout used for training.
        hyper_parameters: Dict, hyperparameters used to train the model.
    """
    root = "{rd}/trained_models".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{holdouts_key}_{hyper_parameters}.h5".format(
        root=root,
        holdouts_key=holdouts_key,
        hyper_parameters=sha256(hyper_parameters)
    )

def results_path(results_directory: str)->str:
    """Return default path for storing the main results csv.
        results_directory: str, directory where to store the prediction_labels.
    """
    return "{results_directory}/results.csv".format(
        results_directory=results_directory
    )

def work_in_progress_path(results_directory: str)->str:
    """Return default path for storing the main work in progress csv.
        results_directory: str, directory where to store the prediction_labels.
    """
    return "{results_directory}/work_in_progress.csv".format(
        results_directory=results_directory
    )

def predictions_labels_path(results_directory: str, predictions_labels: np.ndarray)->str:
    """Return default path for prediction labels.
        results_directory: str, directory where to store the prediction_labels.
        predictions_labels: np.ndarray, array of prediction labels.
    """
    root = "{rd}/predictions_labels".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{hash}.csv".format(
        root=root,
        hash=sha256({
            "predictions_labels":predictions_labels
        })
    )

def true_labels_path(results_directory: str, true_labels: np.ndarray)->str:
    """Return default path for true labels.
        results_directory: str, directory where to store the true_labels.
        true_labels: np.ndarray, array of true labels.
    """
    root = "{rd}/true_labels".format(rd=results_directory)
    os.makedirs(root, exist_ok=True)
    return "{root}/{hash}.csv".format(
        root=root,
        hash=sha256({
            "true_labels":true_labels
        })
    )