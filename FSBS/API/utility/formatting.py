from typing import Any


def stringify_params(param_map: dict[Any, Any]) -> str:
    pairs = []
    for key in param_map:
        pairs.append('='.join([str(key), str(param_map[key])]))

    return ','.join(str(pair) for pair in pairs)
