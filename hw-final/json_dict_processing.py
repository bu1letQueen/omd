"""
Инструменты сделать вложенный словарь плоским
"""


def extract_nested_value(obj, keys):
    """
    Достать значение из вложенного словаря по списку ключей
    """
    current = obj
    for key in keys:
        if not isinstance(current, dict):
            return None
        if key in current.keys():
            current = current[key]
        else:
            return None
    return current


def process_dictionary_with_config(dictionary, config):
    """
    :param dictionary: nested initial dict
    :param config: dict, keys -- name of output, vals -- path + func
    """
    result = {}
    for name, config_value in config.items():
        processing_function = None

        if isinstance(config_value, list):
            path = config_value
        elif isinstance(config_value, tuple):
            path = config_value[0]
            processing_function = config_value[1]
        else:
            continue

        raw_value = extract_nested_value(dictionary, path)

        if processing_function:
            processed_value = processing_function(raw_value)
        else:
            processed_value = raw_value

        result[name] = processed_value

    return result


def process_list_of_dicts_with_config(list_of_dicts, config):
    """
    Обработать список словарей согласно конфигу
    """
    flatten_dicts = []

    for dictionary in list_of_dicts:
        flatten_dict = process_dictionary_with_config(dictionary, config)
        flatten_dicts.append(flatten_dict)

    return flatten_dicts


def create_processor(config, list_processor=False):
    """
    Создать функцию-процессор, которая уже знает, какой конфиг применять
    """
    def processor(data):
        if list_processor:
            return process_list_of_dicts_with_config(data, config)
        else:
            return process_dictionary_with_config(data, config)
    return processor


# Базовые тесты
_obj = {"a": {"b": {"c": 3}}}
assert extract_nested_value(_obj, ["a", "b", "c"]) == 3
assert extract_nested_value(_obj, ["a", "x"]) is None

_config = {"leaf": (["a", "b", "c"], lambda x: x + 1)}
assert process_dictionary_with_config(_obj, _config)["leaf"] == 4

_list_config = {"leaf": ["key"]}
_list_processed = process_list_of_dicts_with_config([{"key": 1}, {}], _list_config)
assert _list_processed[0]["leaf"] == 1 and _list_processed[1]["leaf"] is None
