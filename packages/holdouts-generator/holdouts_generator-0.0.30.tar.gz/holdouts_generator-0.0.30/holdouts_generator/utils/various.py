from typing import List, Tuple, Dict

def odd_even_split(data:List)->Tuple[List, List]:
    """Return given list split into even and odds elements.
        data:List, list of data to split.
    """
    return data[::2], data[1::2]

def build_query(parameters:Dict, join=" & ")->str:
    return join.join([
        "{key} == {value}".format(
            key=key,
            value="'{v}'".format(v=value) if isinstance(value, str) else value
        ) for key, value in parameters.items()
    ])