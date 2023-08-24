import unittest
from unittest.mock import patch

import main


class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['hi', 'quit'])
    @patch('builtins.print')
    def test_hi(self, mock_print, mock_input):
        main.main()
        args, _ = mock_print.call_args
        output = args[0].lower()
        self.assertTrue('hi' in output or 'hello' in output)

    @patch('builtins.input', side_effect=['hi, list my calendars', 'quit'])
    @patch('builtins.print')
    def test_list_calendars(self, mock_print, mock_input):
        main.main()
        args, _ = mock_print.call_args
        self.assertTrue('University' in args[0] and 'Work' in args[0])

    @patch('builtins.input', side_effect=['hi, list my events', 'quit'])
    @patch('builtins.print')
    def test_list_events(self, mock_print, mock_input):
        main.main()
        args, _ = mock_print.call_args
        self.assertTrue('Lecture' in args[0] and 'Dentist' in args[0])

if __name__ == "__main__":
    unittest.main()
