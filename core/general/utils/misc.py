import yaml


def yaml_coerce(value):
    """
    Pass in a string dictionary
    and convert it to a Python dictionary
    """
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']

    return value
