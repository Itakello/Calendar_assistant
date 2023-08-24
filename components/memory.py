import json
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
            # TODO find a way to add/update/remove calendars and events based on the step content
            if (not isinstance(step, AgentAction)) and '"value":' in step:
                data = json.loads(step)
                for calendar in data['value']:
                    new_calendar = Calendar.from_microsoft_graph(calendar)
                    self.calendars.add_calendar(new_calendar)
        return
                        