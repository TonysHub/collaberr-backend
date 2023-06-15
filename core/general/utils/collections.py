def deep_update(base_dict, update_with):
    """
    Recursively update a dictionary with another dictionary.

    base_dict: The dictionary to update.
    update_with: The dictionary to update with.
    """
    for key, value in update_with.items():
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            else:
                base_dict[key] = value
        else:
            base_dict[key] = value

    return base_dict
