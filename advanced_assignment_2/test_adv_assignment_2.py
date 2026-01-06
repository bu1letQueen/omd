from adv_assignment_2 import Color


def test_task1_print_color():
    red = Color(255, 0, 0)
    s = str(red)
    assert "●" in s


def test_task2_compare_colors():
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    assert (red == green) is False
    assert (red == Color(255, 0, 0)) is True


def test_task3_add_colors():
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    mixed = red + green
    assert isinstance(mixed, Color)
    assert "●" in str(mixed)


def test_task4_unique_colors_set():
    orange1 = Color(255, 165, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    orange2 = Color(255, 165, 0)
    color_list = [orange1, red, green, orange2]
    unique = set(color_list)
    assert len(unique) == 3


def test_task5_contrast_multiply():
    red = Color(255, 0, 0)
    half = 0.5 * red
    assert isinstance(half, Color)
    assert "●" in str(half)