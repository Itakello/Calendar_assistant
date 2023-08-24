import re
from typing import Any, Dict, List, Optional

import yaml
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits.openapi.spec import ReducedOpenAPISpec
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.agents.tools import Tool
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.memory import ReadOnlySharedMemory
from langchain.prompts import PromptTemplate
from langchain.requests import RequestsWrapper
from langchain.tools.base import BaseTool

from parsing_requests_prompt import CUSTOM_PARSING_REQUEST_PROMPT

# Idea: add examples if the planner is no working correctly

API_PLANNER_PROMPT = """You are an API planner for a calendar assistant. Your task is to create a plan of API calls based on the user's query using the endpoints provided below. 

Remember:
1) Determine if the user's query can be addressed with the available API endpoints. If not, explain why.
2) If possible, create a step-by-step plan of API calls.
3) If the plan involves a DELETE call, always include a step to ask the user for confirmation before proceeding.

Note: The DELETE endpoint should only be used when the user explicitly requests to delete something. 

Here are the endpoints you can use for calendar management:

{endpoints}

User query: {query}
Plan:"""

API_PLANNER_TOOL_NAME = "api_planner"
API_PLANNER_TOOL_DESCRIPTION = f"Can be used to generate the right API calls to assist with a user query, like {API_PLANNER_TOOL_NAME}(query). Should always be called before trying to call the API controller."

API_CONTROLLER_PROMPT = """You are an API controller for a calendar assistant. Your task is to execute the plan of API calls provided by the planner and handle any non-obvious requests or conflicts.

For example, if a user wants to add an event at a time slot that is already occupied, you should:
1) Alert the user about the conflict and provide details about the existing event.
2) Ask the user if they would like to modify the existing event or the new event.
3) Ask the user how they would like to modify chosen event delete or change the time slor.
4) Depending on the user's decision, you may need to recall the planner to generate a new plan.

Remember, you can only use the DELETE tool when the user explicitly asks to delete something or gives confirmation to do so.

Here is documentation on the API:
Base url: {api_url}
Endpoints:
{api_docs}

Here are tools to execute requests against the API: {tool_descriptions}

Starting below, you should follow this format:

Plan: the plan of API calls to execute
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the output of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing the plan (or, I cannot finish executing the plan without knowing some other information.)
Final Answer: the final output from executing the plan or missing information I'd need to re-plan correctly.

Begin!

Plan: {input}
Thought:
{agent_scratchpad}"""

API_CONTROLLER_TOOL_NAME = "api_controller"
API_CONTROLLER_TOOL_DESCRIPTION = f"Can be used to execute a plan of API calls, like {API_CONTROLLER_TOOL_NAME}(plan)."

API_ORCHESTRATOR_PROMPT = """You are an agent that assists with user queries against API, things like querying information or creating resources.
Some user queries can be resolved in a single API call, particularly if you can find appropriate params from the OpenAPI spec; though some require several API call.
You should always plan your API calls first, and then execute the plan second.
If the plan includes a DELETE call, be sure to ask the User for authorization first unless the User has specifically asked to delete something.
You should never return information without executing the api_controller tool.


Here are the tools to plan and execute API requests: {tool_descriptions}


Starting below, you should follow this format:

User query: the query a User wants help with related to the API
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing a plan and have the information the user asked for or the data the used asked to create
Final Answer: the final output from executing the plan


Example:
User query: can you add some trendy stuff to my shopping cart.
Thought: I should plan API calls first.
Action: api_planner
Action Input: I need to find the right API calls to add trendy items to the users shopping cart
Observation: 1) GET /items with params 'trending' is 'True' to get trending item ids
2) GET /user to get user
3) POST /cart to post the trending items to the user's cart
Thought: I'm ready to execute the API calls.
Action: api_controller
Action Input: 1) GET /items params 'trending' is 'True' to get trending item ids
2) GET /user to get user
3) POST /cart to post the trending items to the user's cart
...

Begin!

User query: {input}
Thought: I should generate a plan to help with this query and then copy that plan exactly to the controller.
{agent_scratchpad}"""



class RequestsGetToolWithParsing(BaseRequestsTool, BaseTool):
    name = "requests_get"
    description = REQUESTS_GET_TOOL_DESCRIPTION
    response_length: Optional[int] = MAX_RESPONSE_LENGTH
    llm_chain: LLMChain = Field(
        default_factory=_get_default_llm_chain_factory(PARSING_GET_PROMPT)
    )

    def _run(self, text: str) -> str:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise e
        data_params = data.get("params")
        response = self.requests_wrapper.get(data["url"], params=data_params)
        response = response[: self.response_length]
        return self.llm_chain.predict(
            response=response, instructions=data["output_instructions"]
        ).strip()

    async def _arun(self, text: str) -> str:
        raise NotImplementedError()


class RequestsPostToolWithParsing(BaseRequestsTool, BaseTool):
    name = "requests_post"
    description = REQUESTS_POST_TOOL_DESCRIPTION

    response_length: Optional[int] = MAX_RESPONSE_LENGTH
    llm_chain: LLMChain = Field(
        default_factory=_get_default_llm_chain_factory(PARSING_POST_PROMPT)
    )

    def _run(self, text: str) -> str:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise e
        response = self.requests_wrapper.post(data["url"], data["data"])
        response = response[: self.response_length]
        return self.llm_chain.predict(
            response=response, instructions=data["output_instructions"]
        ).strip()

    async def _arun(self, text: str) -> str:
        raise NotImplementedError()

def _create_api_planner_tool(
    api_spec: ReducedOpenAPISpec, llm: BaseLanguageModel
) -> Tool:
    endpoint_descriptions = [
        f"{name} {description}" for name, description, _ in api_spec.endpoints
    ]
    prompt = PromptTemplate(
        template=API_PLANNER_PROMPT,
        input_variables=["query"],
        partial_variables={"endpoints": "- " + "- ".join(endpoint_descriptions)},
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    tool = Tool(
        name=API_PLANNER_TOOL_NAME,
        description=API_PLANNER_TOOL_DESCRIPTION,
        func=chain.run,
    )
    return tool


def _create_api_controller_agent(
    api_url: str,
    api_docs: str,
    requests_wrapper: RequestsWrapper,
    llm: BaseLanguageModel,
) -> AgentExecutor:
    get_llm_chain = LLMChain(llm=llm, prompt=CUSTOM_PARSING_REQUEST_PROMPT)
    post_llm_chain = LLMChain(llm=llm, prompt=CUSTOM_PARSING_REQUEST_PROMPT)
    tools: List[BaseTool] = [
        RequestsGetToolWithParsing(
            requests_wrapper=requests_wrapper, llm_chain=get_llm_chain
        ),
        RequestsPostToolWithParsing(
            requests_wrapper=requests_wrapper, llm_chain=post_llm_chain
        ),
    ]
    prompt = PromptTemplate(
        template=API_CONTROLLER_PROMPT,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "api_url": api_url,
            "api_docs": api_docs,
            "tool_names": ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
        },
    )
    agent = ZeroShotAgent(
        llm_chain=LLMChain(llm=llm, prompt=prompt),
        allowed_tools=[tool.name for tool in tools],
    )
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)


def _create_api_controller_tool(
    api_spec: ReducedOpenAPISpec,
    requests_wrapper: RequestsWrapper,
    llm: BaseLanguageModel,
) -> Tool:
    """Expose controller as a tool.

    The tool is invoked with a plan from the planner, and dynamically
    creates a controller agent with relevant documentation only to
    constrain the context.
    """

    base_url = api_spec.servers[0]["url"]  # TODO: do better.

    def _create_and_run_api_controller_agent(plan_str: str) -> str:
        pattern = r"\b(GET|POST|PATCH|DELETE)\s+(/\S+)+"
        matches = re.findall(pattern, plan_str)
        endpoint_names = [
            "{method} {route}".format(method=method, route=route.split("?")[0])
            for method, route in matches
        ]
        endpoint_docs_by_name = {name: docs for name, _, docs in api_spec.endpoints}
        docs_str = ""
        for endpoint_name in endpoint_names:
            docs = endpoint_docs_by_name.get(endpoint_name)
            if not docs:
                raise ValueError(f"{endpoint_name} endpoint does not exist.")
            docs_str += f"== Docs for {endpoint_name} == \n{yaml.dump(docs)}\n"

        agent = _create_api_controller_agent(base_url, docs_str, requests_wrapper, llm)
        return agent.run(plan_str)

    return Tool(
        name=API_CONTROLLER_TOOL_NAME,
        func=_create_and_run_api_controller_agent,
        description=API_CONTROLLER_TOOL_DESCRIPTION,
    )


def create_openapi_agent(
    api_spec: ReducedOpenAPISpec,
    requests_wrapper: RequestsWrapper,
    llm: BaseLanguageModel,
    shared_memory: Optional[ReadOnlySharedMemory] = None,
    callback_manager: Optional[BaseCallbackManager] = None,
    verbose: bool = True,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Instantiate API planner and controller for a given spec.

    Inject credentials via requests_wrapper.

    We use a top-level "orchestrator" agent to invoke the planner and controller,
    rather than a top-level planner
    that invokes a controller with its plan. This is to keep the planner simple.
    """
    tools = [
        _create_api_planner_tool(api_spec, llm),
        _create_api_controller_tool(api_spec, requests_wrapper, llm),
    ]
    prompt = PromptTemplate(
        template=API_ORCHESTRATOR_PROMPT,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tool_names": ", ".join([tool.name for tool in tools]),
            "tool_descriptions": "\n".join(
                [f"{tool.name}: {tool.description}" for tool in tools]
            ),
        },
    )
    agent = ZeroShotAgent(
        llm_chain=LLMChain(llm=llm, prompt=prompt, memory=shared_memory),
        allowed_tools=[tool.name for tool in tools],
        **kwargs,
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        **(agent_executor_kwargs or {}),
    )