def find_nested_key_fn(data, target_key):
    """
    Recursively searches for a key in a nested JSON object.

    :param data: The JSON object (dictionary or list).
    :param target_key: The key you are searching for.
    :return: The value associated with the key if found, otherwise None.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_nested_key_fn(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_nested_key_fn(item, target_key)
            if result is not None:
                return result
    return None