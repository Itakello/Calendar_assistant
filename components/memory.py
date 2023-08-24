import json
import re
from datetime import datetime

from langchain.schema import AgentAction, BaseMemory

from classes.calendar import Calendar, CalendarCollection
from classes.event import EventCollection


class CalendarMemory(BaseMemory):
    
    calendars: CalendarCollection = CalendarCollection()
    
    memory_key: str = "calendars"
    
    def clear(self) -> None:
        """Clear memory contents."""
        super().clear()
        self.calendars = CalendarCollection()
        
    @property
    def memory_variables(self) -> list[str]:
        """Define the variables we are providing to the prompt."""
        return [self.memory_key]
    
    def load_memory_variables(self, inputs: dict[str, any]) -> dict[str, str]:
        """Load the memory variables"""
        content = f'Current time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        if len(self.calendars) == 0:
            content += 'Warning! You have to download the calendars first!'
        else:
            content += 'Here are the available calendars and events:\n' + str(self.calendars)
        return {self.memory_key: content}
        
    def save_context(self, inputs: dict[str, any], outputs: dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if 'intermediate_steps' not in inputs or len(inputs['intermediate_steps']) == 0:
            return
        for step in inputs['intermediate_steps'][0]:
            if isinstance(step, AgentAction):
                continue
            if 'DELETE' in step: # No content
                self.remove_calendar(step)
            else:
                self.update_calendars(step)
        return
    
    def remove_calendar(self, output: str) -> None:
        pattern = r'/calendars/(?P<calendar_id>[^/\n]+)'
        match = re.search(pattern, output)
        if match:
            calendar_id = match.group('calendar_id')
            self.calendars.remove_calendar(calendar_id)
    
    def update_calendars(self, output: str) -> None:
        data = json.loads(output)
        if 'value' in data.keys():
            for calendar in data['value']:
                new_calendar = Calendar.from_microsoft_graph(calendar)
                self.calendars.add_calendar(new_calendar)
        else:
            new_calendar = Calendar.from_microsoft_graph(data)
            self.calendars.add_calendar(new_calendar)
            
                        