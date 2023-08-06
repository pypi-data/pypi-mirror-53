# -*- coding: utf-8 -*-
"""Jasm will find the best json around!

This ripped from my package pupy (AKA Pretty Useful Python)

If you need a whole mess of utils check pupy out!
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Union

JSONish = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
BETTER_JSONS = ("rapidjson", "orjson", "ujson", "simplejson")


def _import_json():
    """Import the best possible json

    Ripped from pupy (Pretty Useful Python)
    """

    for mod in BETTER_JSONS:
        try:
            res = __import__(mod)
            return res
        except ImportError:
            pass
    import json

    return json
    raise ImportError(
        "Ya need one of the following:\n"
        "   ~ ujson; 'pip install ujson'\n"
        "   ~ ujson; 'pip install python-rapidjson'\n"
        "   ~ json; this should have come with python\n"
    )


json = _import_json()


def sjson(filepath: str, data: JSONish, *args, **kwargs) -> None:
    """Save/Write json-serial-ize-able data to a filepath

    Ripped from pupy (Pretty Useful Python)

    Args:
        filepath (str): filepath to write to
        data (JSONish): json-serial-ize-able data
        minify (bool): If the data should be minified (default=False)
        sort_keys (bool): Sort the data keys if the data is a dictionary.

    Returns:
        None

    """
    try:
        json_string = json.dumps(data, ensure_ascii=True, **kwargs)
    except:
        data = {k: str(v, encoding="utf-8") for k, v in data.items()}
        json_string = json.dumps(data, ensure_ascii=True, **kwargs)

    with open(filepath, "w") as f:
        f.write(json_string)


def ljson(filepath: str) -> JSONish:
    """Load/Read-&-parse json data given a filepath
    
    Ripped from pupy (Pretty Useful Python)

    Args:
        filepath (str): Filepath to load/read data from

    Returns:
        Parsed JSON data

    """
    with open(filepath, "r") as f:
        return json.loads(f.read())
