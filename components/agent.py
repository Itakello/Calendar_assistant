import json
from pathlib import Path

from langchain import LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent, Tool
#from langchain.chains import OpenAPIEndpointChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import CombinedMemory, ConversationSummaryMemory
from langchain.requests import TextRequestsWrapper
from langchain.schema import BaseMemory
from langchain.tools import APIOperation, OpenAPISpec

from .memory import CalendarMemory
from .openapi_chain import OpenAPIEndpointChainRaw
from .output_parser import CustomOutputParser
from .prompt_template import TEMPLATE, CustomPromptTemplate


def save_operations() -> None:
    """Save the operations from the OpenAPI spec to files."""
    specs = OpenAPISpec.from_file("calendar_openapi.yaml")
    paths  = list(specs.paths.keys())
    
    for path in paths:
        methods = specs.get_methods_for_path(path)
        for method in methods:
            operation = APIOperation.from_openapi_spec(specs, path, method)
            with open(f"api_operations/{operation.operation_id}.json", "w") as f:
                f.write(operation.json())

def get_operations(path: str) -> list[str]:
    """Get the operations from the OpenAPI spec from files."""	
    folder_path = Path(path)

    operations = list()
    for file_path in folder_path.glob('*.json'):
        with open(file_path, 'r') as f:
            operation_json = json.load(f)
            operation = APIOperation.parse_obj(operation_json)
            operations.append(operation)
    return operations

def get_requests_wrapper(access_token: str) -> TextRequestsWrapper:
    """Get the requests wrapper with the access token."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    requests_wrapper = TextRequestsWrapper(headers=headers)
    return requests_wrapper

def transform_ops_to_tools(operations: list[APIOperation], llm: OpenAI, request_wrapper: TextRequestsWrapper) -> list[Tool]:
    tools = list()
    for op in operations:
        chain = OpenAPIEndpointChainRaw.from_api_operation(
            operation=op,
            llm=llm,
            requests=request_wrapper,
            verbose=True,
            raw_response=True
        )
        tool = Tool.from_function(
            func=chain.run,
            name=chain.api_operation.operation_id,
            description=chain.api_operation.description,
            verbose=True,
            #return_direct=True
        )
        tools.append(tool)
    return tools

def get_tools(operations_filepath: str, llm: OpenAI, access_token: str) -> list[Tool]:    
    operations = get_operations(operations_filepath)
    req_wrapper = get_requests_wrapper(access_token)
    return transform_ops_to_tools(operations, llm, req_wrapper)

def get_memory(llm: ChatOpenAI) -> BaseMemory:
    conv_memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="history",
        input_key="input"
    )
    cal_memory = CalendarMemory(memory_key="calendars")
    return CombinedMemory(
        memories=[conv_memory, cal_memory]
    )

def get_agent(access_token: str) -> AgentExecutor:
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
    tools = get_tools("api_operations", llm, access_token)
    memory = get_memory(llm)
    prompt = CustomPromptTemplate(
        template=TEMPLATE,
        tools=tools,
        input_variables=["input", "intermediate_steps", "history", "calendars"]
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        allowed_tools=[tool.name for tool in tools],
        verbose=True,
        stop=["\nObservation:"],
        output_parser=CustomOutputParser(),
        return_intermediate_step=True
    )
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=memory,
        return_intermediate_step=True
    )
        
    return agent_chain