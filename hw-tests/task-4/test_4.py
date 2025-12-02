import pytest
from one_hot_encoder import fit_transform

def test_two_categories():
    """
    Два разных значения -- два разных вектора корректной длины
    """
    result = fit_transform('biba', 'boba')

    assert result[0][0] == 'biba'
    assert result[1][0] == 'boba'

    assert len(result) == 2
    assert len(result[0][1]) == 2
    assert len(result[1][1]) == 2

    assert result[0][1] != result[1][1]

def test_duplicates_same_vector():
    """
    Одинаковое кодирование повторяющихся категорий
    """
    result = fit_transform('biba', 'boba', 'biba')

    first_biba_vec = result[0][1]
    second_biba_vec = result[2][1]
    boba_vec = result[1][1]

    assert first_biba_vec == second_biba_vec
    assert first_biba_vec != boba_vec

def test_iterable_argument_list():
    """
    Поддержка вызова fit_transform([a, b, c])
    """
    humans = ['biba', 'boba', 'buba']
    result = fit_transform(humans)

    decoded_labels = [name for name, _ in result]
    assert decoded_labels == humans

    for _, vector in result:
        assert len(vector) == 3
        assert sum(vector) == 1

def test_no_arguments():
    """
    Вызов пустой функции ведет к TypeError
    """
    with pytest.raises(TypeError):
        fit_transform()