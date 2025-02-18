from typing import Dict


def try_to_state(status_id: str, mapping: Dict[str, str]) -> str:
    for (key, val) in mapping.items():
        if status_id == key:
            return key
        if status_id.lower() == val.lower():
            return key
    raise ValueError(f"非法状态: {status_id}")
