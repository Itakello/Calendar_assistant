import unittest

from classes.calendar import Calendar, CalendarCollection


class TestCalendarAndCalendarCollection(unittest.TestCase):
    
    def setUp(self):
        self.calendar_data = {
            "id": "AQMkADAwATNiZmYAZC02MzZmLTQ5NGQtMDACLTAwCgBGAAADAv5s9h_DaUmJsy3FoKN6uwcArHwGZMKHqEqIEJPyj6KTZAAAAgEGAAAArHwGZMKHqEqIEJPyj6KTZAAAAixuAAAA",
            "name": "Calendar",
            "color": "lightOrange",
            "hexColor": "#f7630c",
            "isDefaultCalendar": True,
            "changeKey": "rHwGZMKHqEqIEJPyj6KTZAAAD09U/w==",
            "canShare": True,
            "canViewPrivateItems": True,
            "canEdit": True,
            "allowedOnlineMeetingProviders": [
                "skypeForConsumer"
            ],
            "defaultOnlineMeetingProvider": "skypeForConsumer",
            "isTallyingResponses": True,
            "isRemovable": False,
            "owner": {
                "name": "Ita Kello",
                "address": "test_itakello@outlook.com"
            }
        }
        self.calendar = Calendar.from_microsoft_graph(self.calendar_data)
        self.collection = CalendarCollection()

    def test_add_calendar(self):
        self.collection.add_calendar(self.calendar)
        self.assertEqual(self.collection.get_calendar(self.calendar.id), self.calendar)

    def test_remove_calendar(self):
        self.collection.add_calendar(self.calendar)
        self.collection.remove_calendar(self.calendar.id)
        with self.assertRaises(ValueError):
            self.collection.get_calendar(self.calendar.id)

    def test_get_calendar(self):
        self.collection.add_calendar(self.calendar)
        self.assertEqual(self.collection.get_calendar(self.calendar.id), self.calendar)

if __name__ == "__main__":
    unittest.main()