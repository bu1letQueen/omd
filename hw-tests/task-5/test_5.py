import unittest
from unittest.mock import patch
import io
import json

from what_is_year_now import what_is_year_now, API_URL

class TestWhatIsYearNow(unittest.TestCase):

    @patch('what_is_year_now.urllib.request.urlopen')
    def test_ymd_format(self, mock_urlopen):
        """
        Формат YYYY-MM-DD -- все работает
        """
        data = {'currentDateTime': '2005-05-18'}
        fake_response = io.BytesIO(json.dumps(data).encode('utf-8'))

        mock_urlopen.return_value.__enter__.return_value = fake_response

        year = what_is_year_now()
        self.assertEqual(year, 2005)
        mock_urlopen.assert_called_once_with(API_URL)

    @patch('what_is_year_now.urllib.request.urlopen')
    def test_dmy_format(self, mock_urlopen):
        """
        Формат DD.MM.YYYY -- год извлекается корректно
        """
        data = {'currentDateTime': '27.03.2011'}
        fake_response = io.BytesIO(json.dumps(data).encode('utf-8'))

        mock_urlopen.return_value.__enter__.return_value = fake_response

        year = what_is_year_now()
        self.assertEqual(year, 2011)
        mock_urlopen.assert_called_once_with(API_URL)

    @patch('what_is_year_now.urllib.request.urlopen')
    def test_invalid_format(self, mock_urlopen):
        """
        Не совпадает с двумя форматами выше, выдаем ValueError
        """
        data = {'currentDateTime': '1988/01/01'}
        fake_response = io.BytesIO(json.dumps(data).encode('utf-8'))

        mock_urlopen.return_value.__enter__.return_value = fake_response

        with self.assertRaises(ValueError):
            what_is_year_now()

    @patch('what_is_year_now.urllib.request.urlopen')
    def test_invalid_format_no_separators(self, mock_urlopen):
        """
        Строка без разделителей должна вызвать ValueError
        (проверяет else-ветку)
        """
        data = {"currentDateTime": "20190301"}
        fake_response = io.BytesIO(json.dumps(data).encode('utf-8'))

        mock_urlopen.return_value.__enter__.return_value = fake_response

        with self.assertRaises(ValueError):
            what_is_year_now()


if __name__ == '__main__':
    unittest.main()
