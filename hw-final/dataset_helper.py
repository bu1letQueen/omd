def calculate_total_laureates(data):
    """
    Вернуть количество записей в датасете
    """
    return len(data)


def get_all_field_names(data):
    """
    Вернуть множество всех ключей во всех словарях
    """
    all_keys = set()
    for laureate in data:
        for key in laureate:
            if key in all_keys:
                continue
            else:
                all_keys.add(key)
    return all_keys


def count_all_missing_values(data):
    """
    Посчитать пропуски в целом и по каждому полю
    """
    missing_count = 0
    missing_by_field = {}

    for laureate in data:
        for field, value in laureate.items():

            is_missing = (
                value is None
                or value == ""
                or value == []
                or value == {}
            )

            if is_missing:
                missing_count += 1
                missing_by_field[field] = missing_by_field.get(field, 0) + 1

    return missing_count, missing_by_field


def get_field_values(data, field_name):
    """
    Вернуть список значений одного поля field_name
    из всех словарей data.
    Если в словаре нет этого поля — добавляем None
    """
    values = []

    for laureate in data:
        if field_name in laureate:
            values.append(laureate[field_name])
        else:
            values.append(None)

    return values


def filter_records(data, predicate):
    """
    Вернуть только те словари, для которых predicate(record) == True
    """
    return [record for record in data if predicate(record)]


def group_by_attributes(data, attributes):
    """
    Сгруппировать список словарей по нескольким атрибутам.
    Возвращает {tuple(key_values): [records]}
    """
    if isinstance(attributes, str):
        attributes = [attributes]

    groups = {}
    for record in data:
        key = tuple(record.get(attr) for attr in attributes)
        groups.setdefault(key, []).append(record)
    return groups


def apply_aggregation_to_groups(groups, field_name, aggregation_func):
    """
    Применить агрегацию к указанному полю в каждой группе.
    Возвращает {group_key: aggregated_value}
    """
    results = {}
    for key, records in groups.items():
        values = [record.get(field_name) for record in records]
        results[key] = aggregation_func(values)
    return results


def add_derived_field(data, field_name, build_func):
    """
    Вернуть копию списка словарей с добавленным вычисляемым полем.
    build_func принимает record и возвращает значение нового поля.
    """
    return [{**record, field_name: build_func(record)} for record in data]


# Базовые тесты
_demo = [
    {"id": 1, "a": 1, "b": None},
    {"id": 2, "a": None, "b": 3},
]
assert calculate_total_laureates(_demo) == 2
assert "a" in get_all_field_names(_demo)
_miss_total, _miss_by_field = count_all_missing_values(_demo)
assert _miss_total == 2 and _miss_by_field["a"] == 1
assert get_field_values(_demo, "missing") == [None, None]
assert filter_records(_demo, lambda r: r["id"] == 1)[0]["a"] == 1

_grouped = group_by_attributes(_demo, ["b"])
assert tuple(_grouped.keys())[0] == (None,)
_agg = apply_aggregation_to_groups(_grouped, "a", lambda vals: len(vals))
assert set(_agg.values()) == {1}

_extended = add_derived_field(_demo, "double", lambda r: (r.get("a") or 0) * 2)
assert _extended[0]["double"] == 2
