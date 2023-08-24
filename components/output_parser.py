import json
import re
from typing import Union

from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish


class CustomOutputParser(AgentOutputParser):
    def parse(self, raw_output: str)  -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in raw_output:
            return AgentFinish(
                return_values={"output": raw_output.split("Final Answer:")[-1].strip()},
                log=raw_output,
            )
        # Parse out the action and action input
        action_pattern = r'Action:\s*(?P<action>\w+)'
        action_input_pattern = r'Action Input:\s*(?P<action_input>.*)'

        action_match = re.search(action_pattern, raw_output)
        action_input_match = re.search(action_input_pattern, raw_output, re.DOTALL)
        
        action_input = ""

        if action_match:
            action = action_match.group('action').strip()
        if action_input_match:
            action_input = action_input_match.group('action_input').strip()
            if action_input == 'None':
                action_input = ''
            elif '{' not in action_input:
                action_input = '{' + action_input + '}'
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input, log=raw_output)