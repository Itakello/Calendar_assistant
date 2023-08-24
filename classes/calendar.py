from datetime import datetime

from intervaltree import Interval, IntervalTree

from .event import Event, EventCollection


class Calendar():
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.events = EventCollection()
        self.download_periods = IntervalTree()
        self.start_time : datetime = None
        self.end_time : datetime = None
        
    def __str__(self) -> str:
        if self.start_time is None or self.end_time is None:
            return f"[{self.id}] {self.name} (No events downloaded yet)"
        return f"[{self.id}] {self.name} (Events downloaded for the following periods: {self._download_periods_to_string()}):\n{self.events}"
    
    def _download_periods_to_string(self) -> str:
        return str([f"[{interval.begin} - {interval.end}]" for interval in self.download_periods])
    
    def add_events(self, start: datetime, end: datetime, events: list[Event]) -> None:
        self.download_periods.add(Interval(start, end))
        self.download_periods.merge_overlaps()
        self.download_periods = sorted(self.download_periods)
        for event in events:
            self.events.add_event(event)
    
    @classmethod
    def from_microsoft_graph(cls, data: dict[str, any]) -> 'Calendar':
        id = data.get('id')
        name = data.get('name')
        return cls(id, name)
    
    def to_microsoft_graph(self) -> dict[str, any]:
        return {
            "id": self.id,
            "name": self.name
        }

class CalendarCollection:
    
    def __init__(self):
        self.calendars = {}
        
    def __str__(self) -> str:
        return "\n".join([str(calendar) for calendar in self.calendars.values()])

    def __len__(self) -> int:
        return len(self.calendars)
    
    def add_calendar(self, calendar: Calendar):
        self.calendars[calendar.id] = calendar

    def remove_calendar(self, calendar_id: str):
        if calendar_id not in self.calendars:
            raise ValueError(f"No calendar with ID {calendar_id} exists.")
        del self.calendars[calendar_id]

    def get_calendar(self, calendar_id: str) -> Calendar:
        if calendar_id not in self.calendars:
            raise ValueError(f"No calendar with ID {calendar_id} exists.")
        return self.calendars[calendar_id]
    
if __name__ == "__main__":
    calendar1 = Calendar("id1", "name1")
    calendar2 = Calendar("id2", "name2")
    print(calendar1)
    print(calendar1.to_microsoft_graph())
    print(Calendar.from_microsoft_graph(calendar1.to_microsoft_graph()))
    calendar_collection = CalendarCollection()
    calendar_collection.add_calendar(calendar1)
    calendar_collection.remove_calendar("id1")
    calendar_collection.add_calendar(calendar1)
    calendar_collection.add_calendar(calendar2)
    calendar_collection.update_calendar("id1", calendar1)
    print("Full calendar collection:")
    print(calendar_collection)
    print("Test add event")
    event = Event("1", datetime(2021, 1, 1, 12, 0), datetime(2021, 1, 1, 13, 0), "Test Event 1", False)
    calendar1.events.add_event(event)
    print(calendar1.events)