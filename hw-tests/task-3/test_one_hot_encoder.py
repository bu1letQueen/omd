import unittest
from one_hot_encoder import fit_transform

class TestOneHotEncoder(unittest.TestCase):

    def test_two_categories(self):
        """
        Два разных значения -- два разных вектора
        """
        result = fit_transform('biba', 'boba')
        self.assertEqual(result[0][0], 'biba')
        self.assertEqual(result[1][0], 'boba')

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0][1]), 2)
        self.assertEqual(len(result[1][1]), 2)

        self.assertEqual(result[0][1], [0, 1])
        self.assertEqual(result[1][1], [1, 0])

    def test_duplicates_same_vector(self):
        """
        Повторяющиеся категории кодируются одинаково
        """
        result = fit_transform('biba', 'boba', 'biba')
        first_biba_vec = result[0][1]
        second_biba_vec = result[2][1]

        self.assertEqual(first_biba_vec, second_biba_vec)

        self.assertNotEqual(first_biba_vec, result[1][1])
        self.assertEqual(result[1][0], 'boba')
        self.assertEqual(result[1][1], [1, 0])

    def test_iterable_arguments(self):
        """
        Поддержка вызова fit_transform([a, b, c])
        """
        humans = ['biba', 'boba', 'buba']
        result = fit_transform(humans)
        decoded_labels = [name for name, _ in result]

        self.assertEqual(decoded_labels, humans)

        self.assertEqual(len(result[0][1]), 3)
        self.assertEqual(len(result[1][1]), 3)
        self.assertEqual(len(result[2][1]), 3)

        self.assertEqual(result[0][1], [0, 0, 1])
        self.assertEqual(result[1][1], [0, 1, 0])
        self.assertEqual(result[2][1], [1, 0, 0])

    def test_no_arguments(self):
        """
        Передача нуля аргументов должна приводить к TypeError
        """
        with self.assertRaises(TypeError):
            fit_transform()


if __name__ == '__main__':
    unittest.main()
