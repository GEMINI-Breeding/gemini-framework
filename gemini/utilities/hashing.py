from hashlib import sha256, md5
from typing import Any, Dict, List, Union
import json
import os


def hash_dict(dictionary: Dict[str, Any]) -> str:
    """
    Hash a dictionary of values using SHA-256.

    Args:
        dictionary: The dictionary to hash.

    Returns:
        The SHA-256 hash of the dictionary.
    """
    # Sort the dictionary by key to ensure consistent hashing
    sorted_dict = json.dumps(dictionary, sort_keys=True)
    return sha256(sorted_dict.encode()).hexdigest()

def get_file_digest(file_path: str) -> str:
    # Get MD5 hash of file contents
    with open(file_path, 'rb') as f:
        file_contents = f.read()
    return md5(file_contents).hexdigest()