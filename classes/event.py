from datetime import datetime

from intervaltree import Interval, IntervalTree


class Event:
    
    def __init__(self, id: str, start_time: datetime, end_time: datetime, name: str, is_all_day: bool, body: str = None):#recurrence: str = None):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.is_all_day = is_all_day
        self.body = body
        #self.recurrence = recurrence
        
    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.start_time} - {self.end_time})"

    @classmethod
    def from_microsoft_graph(cls, data: dict[str, any]) -> 'Event':
        id = data.get('id')
        start_time = datetime.fromisoformat(data.get('start').get('dateTime'))
        end_time = datetime.fromisoformat(data.get('end').get('dateTime'))
        name = data.get('subject')
        is_all_day = data.get('isAllDay')
        body = data.get('bodyPreview')
        #recurrence = data.get('recurrence')
        return cls(id, start_time, end_time, name, is_all_day, body,) #recurrence)
    
    def to_microsoft_graph(self) -> dict[str, any]:
        return {
            "id": self.id,
            "start": {
                "dateTime": self.start_time.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": self.end_time.isoformat(),
                "timeZone": "UTC"
            },
            "subject": self.name,
            "isAllDay": self.is_all_day,
            "bodyPreview": self.body,
            #"recurrence": self.recurrence
        }

class EventCollection:
    
    def __init__(self):
        self.events_by_id = {}
        self.events_by_time = IntervalTree()
        
    def __str__(self) -> str:
        return "\n".join([f"\t{interval.data}" for interval in self.events_by_time])
        
    def __len__(self) -> int:
        return len(self.events_by_id)

    def add_event(self, event: Event) -> None:
        if event.id in self.events_by_id:
            raise ValueError(f"An event with ID {event.id} already exists.")
        self.events_by_id[event.id] = event
        interval = Interval(event.start_time, event.end_time, event)
        self.events_by_time.add(interval)

    def remove_event(self, event_id: str) -> Event:
        if event_id not in self.events_by_id:
            raise ValueError(f"No event with ID {event_id} exists.")
        event = self.events_by_id[event_id]
        del self.events_by_id[event_id]
        intervals = self.events_by_time[event.start_time:event.end_time]
        for interval in intervals:
            if interval.data.id == event_id:
                self.events_by_time.remove(interval)
                break
        return event

    def get_event(self, event_id: str) -> Event:
        if event_id not in self.events_by_id:
            raise ValueError(f"No event with ID {event_id} exists.")
        return self.events_by_id[event_id]

    def get_events_by_datetime(self, start: datetime, end: datetime) -> 'EventCollection':
        intervals = self.events_by_time[start:end]
        selected_events =  [interval.data for interval in intervals]
        event_collection = EventCollection()
        for event in selected_events:
            event_collection.add_event(event)
        return event_collection

if __name__ == "__main__":
    event = Event("1", datetime(2021, 1, 1, 12, 0), datetime(2021, 1, 1, 13, 0), "Test Event 1", False)
    event2 = Event("2", datetime(2021, 1, 1, 13, 0), datetime(2021, 1, 1, 14, 0), "Test Event 2", False)
    print(event)
    print(event.to_microsoft_graph())
    print(Event.from_microsoft_graph(event.to_microsoft_graph()))
    event_collection = EventCollection()
    event_collection.add_event(event)
    event_collection.remove_event("1")
    event_collection.add_event(event)
    event_collection.add_event(event2)
    event_collection.update_event("1", event)
    print("Full event collection")
    print(event_collection)
    print(event_collection.get_events_by_datetime(datetime(2021, 1, 1, 12, 0), datetime(2021, 1, 1, 14, 0)))
    print("Removing event 1")
    event_collection.remove_event("1")
    print(event_collection.get_events_by_datetime(datetime(2021, 1, 1, 12, 0), datetime(2021, 1, 1, 14, 0)))