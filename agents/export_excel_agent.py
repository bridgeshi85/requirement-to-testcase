from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from utils import load_prompt_template


def export_test_cases_with_agent(test_case_json: str, filename: str = "test_cases.xlsx"):

    # 加载 Prompt 模板
    prompt_path = "prompts/export_to_excel.md"
    export_instructions = load_prompt_template(prompt_path)

    # 加载 ReAct Agent 的基础 Prompt
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=export_instructions)
    tools = [PythonREPLTool()]

    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        tools=tools,
    )

    python_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = python_agent.invoke({"input": "请将测试用例写入Excel 文件"})
    return result
