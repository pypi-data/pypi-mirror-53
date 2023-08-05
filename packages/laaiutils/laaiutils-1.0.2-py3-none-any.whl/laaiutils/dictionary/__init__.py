# -*- coding: utf-8 -*-


def convert_dict_value(values: dict, mapper: dict or None = None):
    if not mapper:
        return values

    for k, v in values.items():

        if k in mapper:
            converter = mapper.get(k)
            if callable(converter):
                values[k] = converter(v)
            else:
                values[k] = converter
    return values


def exchange_dict_key(values: dict, mapper: dict or None = None):
    if not mapper:
        return values
    data = {}
    for k, v in values.items():
        new_key = mapper.get(k, None)
        if new_key:
            data[new_key] = v
    return data
