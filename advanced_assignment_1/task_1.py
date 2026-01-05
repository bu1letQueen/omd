# ISSUE 1
import keyword


class Wrapper:
    def __init__(self):
        self._data = {}

    def fill_data(self, vocab):
        for key, value in vocab.items():
            if type(value) == dict:
                inner_wrapper = Wrapper()
                inner_wrapper.fill_data(value)
                self._data[key] = inner_wrapper
            else:
                self._data[key] = value

    def __getattr__(self, item):
        if item[-1] == '_' and keyword.iskeyword(item[:-1]):
            item = item[:-1]
        if item in self._data:
            return self._data[item]
        else:
            raise AttributeError('Такого ключа нет в словаре')


class ColorizeMixin:
    repr_color_code = 33


class Advert(ColorizeMixin, Wrapper):
    def __init__(self, mapping):
        if 'title' not in mapping:
            raise ValueError
        if 'price' in mapping and mapping['price'] < 0:
            raise ValueError('Цена не может быть отрицательной!')

        super().__init__()
        self.fill_data(mapping)

    @property
    def price(self):
        if 'price' not in self._data:
            return 0
        return self._data['price']

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('Цена не может быть отрицательной!')
        else:
            self._data['price'] = new_price

    def __str__(self):
        base = f'{self.title} | {self.price} ₽'
        return f'\033[{self.repr_color_code}m{base}\033[0m'
