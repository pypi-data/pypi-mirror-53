from dict_hash import sha256
from typing import Dict

def build_keys(holdouts_key: str, hyper_parameters: Dict)->Dict[str, str]:
    """Return formatted keys for given holdouts and hyper_parameters.
        holdouts_key: str, key of a valid holdout.
        hyper_parameters: Dict, dictionary of hyper-parameters.
    """
    return {
        "holdouts_key": holdouts_key,
        "hyper_parameters_key": sha256({} if hyper_parameters is None else hyper_parameters)
    }