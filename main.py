from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from agents.export_excel_agent import export_test_cases_with_agent
from utils import load_prompt_template

load_dotenv()


def generate_test_cases_from_points(test_points: str, requirement: str) -> str:
    prompt_path = "prompts/generate_test_cases.md"
    prompt_text = load_prompt_template(prompt_path)

    prompt_template = PromptTemplate(
        input_variables=["requirement", "test_points"],
        template=prompt_text,
    )

    llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    testcase_chain = LLMChain(llm=llm, prompt=prompt_template)

    response = testcase_chain.run({
        "requirement": requirement,
        "test_points": test_points
    })

    return response  # 返回的是 JSON 字符串


def main():
    # 加载外部 Prompt 文件
    prompt_path = "prompts/generate_test_points.md"
    prompt_text = load_prompt_template(prompt_path)

    # 解析 Prompt 文件
    test_point_prompt_template = PromptTemplate(
        input_variables=["requirement"],
        template=prompt_text,
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    parser_chain = LLMChain(llm=llm, prompt=test_point_prompt_template)

    # 示例调用
    requirement = "用户可以使用邮箱和密码登录系统，成功后跳转到首页。若邮箱或密码错误，应显示错误信息。"
    test_points = parser_chain.run(requirement)
    print(test_points)

    # Step 2: 根据测试点生成测试用例
    test_case_json = generate_test_cases_from_points(test_points, requirement)
    print("📄 生成的测试用例 JSON：\n", test_case_json)

    # Step 3: 导出为 Excel 文件
    export_test_cases_with_agent(test_case_json, filename="test_cases.xlsx")


if __name__ == "__main__":
    main()
