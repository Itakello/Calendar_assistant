import unittest
from datetime import datetime, timedelta

from intervaltree import Interval

from classes.event import Event, EventCollection


class TestEventAndEventCollection(unittest.TestCase):
    
    def setUp(self):
        self.event_data = {
            "id": "AQMkADAwATNiZmYAZC02MzZmLTQ5NGQtMDACLTAwCgBGAAADAv5s9h_DaUmJsy3FoKN6uwcArHwGZMKHqEqIEJPyj6KTZAAAAgENAAAArHwGZMKHqEqIEJPyj6KTZAAAAA9RFxUAAAA=",
            "start": {
                "dateTime": "2023-06-11T06:00:00.0000000",
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": "2023-06-11T06:30:00.0000000",
                "timeZone": "UTC"
            },
            "subject": "Test 1🧪",
            "isAllDay": False,
            "bodyPreview": "Test 1",
            "recurrence": {
                "pattern": {
                    "type": "daily",
                    "interval": 1,
                    "month": 0,
                    "dayOfMonth": 0,
                    "firstDayOfWeek": "sunday",
                    "index": "first"
                },
                "range": {
                    "type": "endDate",
                    "startDate": "2023-06-11",
                    "endDate": "2023-09-11",
                    "recurrenceTimeZone": "W. Europe Standard Time",
                    "numberOfOccurrences": 0
                }
            }
        }
        self.event = Event.from_microsoft_graph(self.event_data)
        self.collection = EventCollection()

    def test_add_event(self):
        self.collection.add_event(self.event)
        self.assertEqual(self.collection.get_event(self.event.id), self.event)

    def test_remove_event(self):
        self.collection.add_event(self.event)
        self.collection.remove_event(self.event.id)
        with self.assertRaises(ValueError):
            self.collection.get_event(self.event.id)

    def test_get_events_by_datetime(self):
        self.collection.add_event(self.event)
        start = datetime.fromisoformat(self.event_data['start']['dateTime'])
        end = start + timedelta(minutes=30)
        new_collection = self.collection.get_events_by_datetime(start, end)
        self.assertEqual([e.data for e in new_collection.events_by_time], [self.event])

    def test_get_events_by_datetime_no_events(self):
        start = datetime.fromisoformat(self.event_data['start']['dateTime'])
        end = start + timedelta(minutes=30)
        new_collection = self.collection.get_events_by_datetime(start, end)
        self.assertEqual([e.data for e in new_collection.events_by_time], [])

    def test_add_event_already_exists(self):
        self.collection.add_event(self.event)
        with self.assertRaises(ValueError):
            self.collection.add_event(self.event)

    def test_remove_event_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.collection.remove_event(self.event.id)

    def test_get_event_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.collection.get_event(self.event.id)

if __name__ == '__main__':
    unittest.main()
