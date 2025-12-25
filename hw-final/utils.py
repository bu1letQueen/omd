def process_year(date_string):
    """
    Принимает строку формата 'YYYY-MM-DD' или None.
    Возвращает только год (int) или None, если данных нет.
    """
    if not date_string:
        return None

    return int(date_string.split("-")[0])


# Базовые тесты
assert process_year("2020-05-01") == 2020
assert process_year(None) is None
