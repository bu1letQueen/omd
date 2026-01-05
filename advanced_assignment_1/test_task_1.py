# test_task_1.py
import pytest
from task_1 import Advert

def test_basic_fields_and_keyword():
    ad = Advert({"title": "Xiaomi Redmi 10000 Ultra Pro Max", "price": 666, "class": "trubka"})
    assert ad.title == "Xiaomi Redmi 10000 Ultra Pro Max"
    assert ad.price == 666
    assert ad.class_ == "trubka"

def test_nested_location_access():
    ad = Advert({"title": "x", "location": {"address": "Dagestan"}})
    assert ad.location.address == "Dagestan"

def test_price_default_zero():
    ad = Advert({"title": "jija veipa"})
    assert ad.price == 0

def test_price_negative_on_init_raises():
    with pytest.raises(ValueError):
        Advert({"title": "bad", "price": -1})

def test_price_negative_on_set_raises():
    ad = Advert({"title": "ok", "price": 1})
    with pytest.raises(ValueError):
        ad.price = -10

def test_str_contains_title_price_ruble_and_ansi():
    ad = Advert({"title": "Xiaomi Redmi 10000 Ultra Pro Max", "price": 666})
    s = str(ad)
    assert "Xiaomi Redmi 10000 Ultra Pro Max | 666 ₽" in s
    assert s.startswith("\033[")
    assert s.endswith("\033[0m")
