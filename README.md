# 基于 LLM Agent 的智能测试用例生成器

## 📖 项目简介

本项目是一个基于大语言模型（LLM）和 Agent 技术的智能测试用例生成系统。它能够自动完成从需求分析到测试用例生成，再到 Excel 文件导出的全流程自动化，极大地提升测试工程师的工作效率。

### 🎯 核心功能

随着 AI 和大模型（LLM）技术的成熟和普及，测试工程师可以利用 AI 生成和优化测试用例，提高测试覆盖率，减少测试设计的重复性工作。本项目实现了以下三个核心流程：

1. **需求分析 → 测试点提取**  
   Agent 通过调用大语言模型（如 GPT-3.5）解析需求语义，自动提取出可测试的功能点、边界条件、异常路径等。

2. **测试点 → 结构化测试用例**  
   结合原始需求与提取的测试点，生成完整的结构化测试用例，包含标题、前置条件、测试步骤、预期结果等字段。

3. **测试用例 → Excel 文件导出**  
   使用 Python Agent 自动调用 pandas 工具，将 JSON 格式的测试用例导出为 Excel 文件，便于后续导入测试管理平台。

## 🏗️ 项目结构

```
requirement-to-testcase/
│
├── main.py                         # 项目主入口，串联整个流程
├── agents/
│   └── export_excel_agent.py       # Excel 导出 Agent
├── prompts/
│   ├── generate_test_points.md     # 测试点提取 Prompt 模板
│   ├── generate_test_cases.md      # 测试用例生成 Prompt 模板
│   └── export_to_excel.md          # Excel 导出 Prompt 模板
├── utils.py                        # 工具函数（Prompt 加载）
├── requirements.txt                # 项目依赖
├── .env                            # 环境变量配置（需自行创建）
└── README.md                       # 项目说明文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.10 或更高版本
- OpenAI API Key（或其他兼容的 LLM API）

### 2. 安装步骤

#### 2.1 克隆项目

```bash
git clone https://github.com/bridgeshi85/requirement-to-testcase.git
cd requirement-to-testcase
```

#### 2.2 创建虚拟环境

```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

#### 2.3 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- `langchain==0.3.25` - LLM 应用框架
- `openai==1.10.0` - OpenAI API 客户端
- `pandas==2.2.2` - 数据处理和表格操作
- `openpyxl==3.1.2` - Excel 文件支持
- `python-dotenv==1.0.1` - 环境变量管理
- `langchain-experimental==0.3.4` - LangChain 实验性功能

#### 2.4 配置 API Key

在项目根目录创建 `.env` 文件，添加以下内容：

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **注意**：本示例使用 GPT-3.5-turbo 模型，你也可以修改代码切换到其他 LLM 模型。

### 3. 运行项目

```bash
python main.py
```

运行后，程序将：
1. 分析示例需求，提取测试点
2. 基于测试点生成结构化测试用例
3. 自动将测试用例导出为 `test_cases.xlsx` 文件

## 💡 使用说明

### 自定义需求

修改 `main.py` 中的 `requirement` 变量，替换为你自己的需求描述：

```python
requirement = "你的需求描述..."
```

例如：

```python
requirement = """
用户可以在商城中浏览商品列表，选择商品加入购物车。
购物车支持修改商品数量、删除商品。
用户点击结算后跳转到订单确认页面。
"""
```

### 工作流程详解

#### Step 1: 提取测试点

程序会调用 `generate_test_points.md` Prompt，从需求中提取测试点。

**示例输入：**
```
用户可以使用邮箱和密码登录系统，成功后跳转到首页。若邮箱或密码错误，应显示错误信息。
```

**示例输出：**
```
- 使用正确的邮箱和密码登录系统，验证是否成功跳转到首页
- 使用错误的邮箱登录系统，验证是否显示错误信息
- 使用错误的密码登录系统，验证是否显示错误信息
- 使用错误的邮箱和密码登录系统，验证是否显示错误信息
- 使用空邮箱登录系统，验证是否显示错误信息
- 使用空密码登录系统，验证是否显示错误信息
```

#### Step 2: 生成测试用例

基于测试点和原始需求，调用 `generate_test_cases.md` Prompt 生成结构化的 JSON 测试用例。

**测试用例格式：**
```json
[
  {
    "title": "邮箱密码正确时登录成功",
    "description": "验证邮箱和密码输入正确后可登录系统",
    "precondition": "已打开登录页面",
    "steps": [
      "输入正确邮箱地址",
      "输入正确密码",
      "点击登录按钮"
    ],
    "expected_result": "成功跳转到系统首页",
    "actual_result": "待测试",
    "pass_fail": "待测试"
  }
]
```

#### Step 3: 导出 Excel

使用 ReAct Agent 自动调用 Python REPL 工具，执行 pandas 代码将 JSON 转换为 Excel 文件。

Agent 会自动：
1. 识别任务需求
2. 选择合适的工具（Python REPL）
3. 编写并执行 pandas 代码
4. 生成 `test_cases.xlsx` 文件

## 🔧 自定义 Prompt

项目中的三个 Prompt 模板可以根据需要自定义：

1. **`prompts/generate_test_points.md`**  
   控制如何从需求中提取测试点

2. **`prompts/generate_test_cases.md`**  
   控制测试用例的生成格式和质量

3. **`prompts/export_to_excel.md`**  
   控制 Excel 导出的逻辑

修改这些文件可以调整生成结果的风格和结构。

## 📊 输出示例

运行成功后，控制台会显示类似以下内容：

```
- 使用正确的邮箱和密码登录系统，验证是否成功跳转到首页
- 使用错误的邮箱登录系统，验证是否显示错误信息
...

📄 生成的测试用例 JSON：
[
  {
    "title": "邮箱密码正确时登录成功",
    ...
  }
]

> Entering new AgentExecutor chain...
Action: Python_REPL
...
Final Answer: The test cases have been successfully written to an Excel file named test_cases.xlsx.
> Finished chain.
```

生成的 `test_cases.xlsx` 文件可直接用于：
- 测试管理工具（如 Jira、TestRail）导入
- 团队协作和评审
- 测试执行跟踪

## ⚠️ 注意事项

1. **API 调用费用**  
   本项目会调用 OpenAI API，产生一定费用。建议在测试时使用较小的需求文本。

2. **模型选择**  
   默认使用 `gpt-3.5-turbo` 模型。如需更好的效果，可以修改为 `gpt-4` 或其他模型：
   ```python
   llm = ChatOpenAI(temperature=0, model="gpt-4")
   ```

3. **中文支持**  
   所有 Prompt 和示例均使用简体中文，确保生成的测试用例符合中文场景需求。

4. **安全性**  
   不要将 `.env` 文件提交到版本控制系统。已在 `.gitignore` 中排除。

## 🔍 技术栈

- **LangChain**: 用于构建 LLM 应用和 Agent
- **OpenAI GPT-3.5**: 核心语言模型
- **Pandas + OpenPyXL**: Excel 文件生成
- **Python REPL Tool**: Agent 自动执行 Python 代码
- **ReAct Agent**: 推理 + 行动的 Agent 架构

## 🎓 适用场景

- 快速需求分析和测试点提取
- 批量测试用例生成
- 测试用例标准化和规范化
- 提升测试团队效率
- 减少重复性测试设计工作

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

本项目遵循 MIT License。

## 📞 联系方式

项目地址：[https://github.com/bridgeshi85/requirement-to-testcase](https://github.com/bridgeshi85/requirement-to-testcase)

---

**让 AI 赋能测试，让测试更智能！** 🚀
