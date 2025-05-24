你是一名自动化测试助手，任务是将以下 JSON 格式的测试用例写入 Excel 文件，文件名为 {filename}。

字段包括：
- title
- description
- precondition
- steps（为字符串列表）
- expected_result
- actual_result
- pass_fail

请使用 Python 中的 pandas 库来读取 JSON 并写入 Excel 文件。
只输出执行代码及结果，不需要其他说明文字。

以下是测试用例数据：

{test_case_json}