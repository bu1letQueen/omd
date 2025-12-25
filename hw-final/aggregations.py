"""Функции агрегации игнорирующие пустые значения"""

from statistics import mean, median


def min_value(values):
    """
    Минимум по непустым значениям.
    Игнорируем None
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return min(clean)


def max_value(values):
    """
    Максимум по непустым значениям
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return max(clean)


def avg_value(values):
    """
    Среднее по непустым значениям.
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return mean(clean)


def median_value(values):
    """
    Медиана по непустым значениям.
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return median(clean)


def top_n_by_key(data, key, n):
    """
    Возвращает топ-N записей по значению поля key.
    None считаем минимальным.
    """

    # Создаём копию, чтобы не портить исходный список
    remaining = data[:]  
    result = []

    for _ in range(n):
        best_record = None
        best_value = None

        # Находим лучший элемент
        for record in remaining:
            value = record.get(key)

            # None считаем самым маленьким — просто пропускаем
            if value is None:
                continue

            if best_value is None or value > best_value:
                best_value = value
                best_record = record

        # если не нашли (например, всё None)
        if best_record is None:
            break

        # добавляем в результат
        result.append(best_record)

        # удаляем из оставшихся
        remaining.remove(best_record)

    return result


def sum_value(values):
    """Сумма по непустым значениям; если нет данных, вернем None."""
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return sum(clean)


def count_non_null(values):
    """Количество элементов, отличных от None."""
    return len([v for v in values if v is not None])


def aggregate_field(dicts, key, aggregator):
    """
    Применить агрегатор (например, avg_value) к полю key в списке словарей.
    """
    values = [d.get(key) for d in dicts]
    return aggregator(values)


# Базовые тесты
_sample_numbers = [None, 3, 10, None, 5]
assert min_value(_sample_numbers) == 3
assert max_value(_sample_numbers) == 10
assert avg_value(_sample_numbers) == mean([3, 10, 5])
assert median_value([None, 1, 2, 10]) == median([1, 2, 10])
assert sum_value(_sample_numbers) == 18
assert count_non_null(_sample_numbers) == 3

_sample_dicts = [
    {"value": 2, "name": "a"},
    {"value": None, "name": "b"},
    {"value": 5, "name": "c"},
]
assert aggregate_field(_sample_dicts, "value", max_value) == 5
assert top_n_by_key(_sample_dicts, "value", 1)[0]["name"] == "c"
