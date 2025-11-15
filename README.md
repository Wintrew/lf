LF Language Specification v1.0 / LF语言规范 v1.0
📋 Overview / 概述
LF (Language Fusion) is a multi-language fusion programming language that allows mixing multiple programming languages in the same source file. It uses a simple tagging system to distinguish code blocks from different languages and provides a unified compilation and execution environment.

LF (Language Fusion) 是一种多语言融合的编程语言，允许在同一个源文件中混合使用多种编程语言。它通过简单的标记系统来区分不同语言的代码块，并提供了统一的编译和执行环境。

📁 File Extensions / 文件扩展名
Source files: .lf / 源文件: .lf

Compiled files: .lsf (LF Serialized Format) / 编译后文件: .lsf

🏗️ Syntax Structure / 语法结构
1. Comments / 注释
text
// Single-line comment / 单行注释
/* Multi-line comment / 多行注释 */
2. Directives / 指令
Start with #, used for configuration and metadata / 以 # 开头，用于配置和元数据：

text
#name "Program Name" / 程序名称
#version "1.0" / 版本号
#author "Author Name" / 作者名
#python_import "module_name" / Python模块导入
3. Code Blocks / 代码块
Python Code Blocks / Python 代码块
text
py.Single line Python code / 单行Python代码
py.Multi-line Python code start: / 多行Python代码开始:
py.    Indented code / 缩进的代码
py.    Continue execution / 继续执行
C++ Code Blocks / C++ 代码块
text
cpp.Single line C++ code / 单行C++代码
cpp.printf("Formatted output: %s", variable) / 格式化输出
JavaScript Code Blocks / JavaScript 代码块
text
js.Single line JavaScript code / 单行JavaScript代码
📝 Detailed Syntax Specification / 详细语法规范
Directive System / 指令系统
Syntax / 语法： #directive_name "value"

Available Directives / 可用指令：

#name - Program name / 程序名称

#version - Version number / 版本号

#author - Author information / 作者信息

#description - Program description / 程序描述

#python_import - Python module import (can be used multiple times) / Python模块导入（可多次使用）

Example / 示例：

text
#name "My LF Program" / 我的LF程序
#version "1.0.0" / 版本号
#author "Developer" / 开发者
#python_import "math" / 导入数学模块
#python_import "datetime" / 导入日期时间模块
Python Code Blocks / Python 代码块
Syntax / 语法： py.Python code

Features / 特性：

Automatic multi-line function definition and code block processing / 自动处理多行函数定义和代码块

Support all Python syntax / 支持所有Python语法

Variables and functions shared in global environment / 变量和函数在全局环境中共享

Example / 示例：

lf
// Single line Python / 单行Python
py.x = 10
py.name = "LF Language" / LF语言

// Function definition (automatic multi-line processing) / 函数定义（自动多行处理）
py.def calculate(a, b):
py.    result = a * b + math.sqrt(a)
py.    return result

// Complex structure / 复杂结构
py.if x > 5:
py.    print("x greater than 5") / x大于5
py.    for i in range(3):
py.        print(f"Loop: {i}") / 循环
C++ Code Blocks / C++ 代码块
Syntax / 语法： cpp.C++ code

Currently Supported Features / 当前支持功能：

printf formatted output / 格式化输出

Variable references and expression evaluation / 变量引用和表达式计算

Example / 示例：

lf
cpp.printf("Welcome to LF Language!") / 欢迎使用LF语言!
cpp.printf("Current time: %s", datetime.datetime.now().strftime("%Y-%m-%d")) / 当前时间
cpp.printf("Variable count: %s, Function count: %s", len(variables), len(functions)) / 变量数量，函数数量
JavaScript Code Blocks / JavaScript 代码块
Syntax / 语法： js.JavaScript code

Current Status / 当前状态：

Basic support (placeholder functionality) / 基础支持（占位功能）

Output code content / 输出代码内容

Example / 示例：

lf
js.console.log("Hello from JavaScript") / 来自JavaScript的问候
🔄 Execution Model / 执行模型
Variable Scope / 变量作用域
All variables shared in global scope / 所有变量在全局作用域中共享

Variables defined in Python can be referenced in C++ printf / Python中定义的变量可在C++的printf中引用

Function definitions in global function table / 函数定义在全局函数表中

Execution Order / 执行顺序
Parse all directives and import modules / 解析所有指令并导入模块

Execute all code blocks in order / 按顺序执行所有代码块

Support cross-language variable access / 支持跨语言变量访问

💾 Compilation Output Format / 编译输出格式
Compiled .lsf files use JSON format / 编译后的 .lsf 文件使用JSON格式：

json
{
  "format_version": "LSF-1.0",
  "metadata": {
    "compiler": "lf-compile-final",
    "source_file": "source_file_name"
  },
  "program": {
    "directives": {
      "directive_type": [
        {"value": "value", "line": "line_number"}
      ]
    },
    "code_blocks": [
      {"line": "line_number", "type": "code_type", "content": "code_content"}
    ],
    "source_hash": "source_file_hash"
  }
}
🎯 Complete Examples / 完整示例
Example 1: Basic Program / 示例1: 基础程序
lf
// Basic LF program example / 基础LF程序示例
#name "Hello LF" / 程序名称
#version "1.0" / 版本号
#author "LF Developer" / LF开发者

// Python variable definition / Python变量定义
py.message = "Hello, World!"
py.count = 42

// C++ output / C++输出
cpp.printf("Message: %s", message) / 消息
cpp.printf("Count: %s", count) / 计数

// Python function / Python函数
py.def greet(name):
py.    return f"Hello, {name}!" / 你好

// Using function / 使用函数
py.result = greet("LF User") / LF用户
cpp.printf("Function result: %s", result) / 函数结果
Example 2: Mathematical Calculation / 示例2: 数学计算
lf
#name "Math Calculation Example" / 数学计算示例
#python_import "math" / 导入数学模块

py.radius = 5.0 / 半径
py.area = math.pi * radius ** 2 / 面积
py.circumference = 2 * math.pi * radius / 周长

cpp.printf("Radius: %.2f", radius) / 半径
cpp.printf("Area: %.2f", area) / 面积
cpp.printf("Circumference: %.2f", circumference) / 周长

py.def factorial(n): / 阶乘函数
py.    if n <= 1:
py.        return 1
py.    else:
py.        return n * factorial(n-1)

py.fact_10 = factorial(10) / 10的阶乘
cpp.printf("10 factorial: %s", fact_10) / 10的阶乘
Example 3: Performance Test / 示例3: 性能测试
lf
#name "Performance Test" / 性能测试
#python_import "time" / 导入时间模块

py.start_time = time.time() / 开始时间
py.data = [] / 数据列表

// Create large amount of data / 创建大量数据
py.for i in range(10000):
py.    data.append(i * i)

py.end_time = time.time() / 结束时间
py.duration = end_time - start_time / 持续时间

cpp.printf("Data generation completed!") / 数据生成完成
cpp.printf("Data volume: %s elements", len(data)) / 数据量
cpp.printf("Execution time: %.3f seconds", duration) / 执行时间
cpp.printf("First 5 elements: %s", data[:5]) / 前5个元素
⚡ Running Instructions / 运行方式
Compilation / 编译
bash
python lf-compile-final.py program.lf
Execution / 执行
bash
python lf-run-ultimate-fixed.py program.lsf
🔍 Feature Summary / 特性总结
Multi-language Fusion - Use multiple languages in single file / 多语言融合 - 在单一文件中使用多种语言

Smart Multi-line Processing - Automatic Python code block recognition / 智能多行处理 - 自动识别Python代码块

Variable Sharing - Cross-language variable access / 变量共享 - 跨语言变量访问

Module Import - Support Python module import / 模块导入 - 支持Python模块导入

Formatted Output - Enhanced printf functionality / 格式化输出 - 增强的printf功能

Error Handling - Comprehensive error reporting mechanism / 错误处理 - 完善的错误报告机制

🚀 Applicable Scenarios / 适用场景
Rapid prototyping development / 快速原型开发

Multi-language learning tool / 多语言学习工具

Script automation tasks / 脚本自动化任务

Education and demonstration purposes / 教育和演示用途

Cross-language proof of concept / 跨语言概念验证

📊 System Architecture / 系统架构
text
LF Source File (.lf) / LF源文件
         ↓
    LF Compiler / LF编译器
         ↓
LSF File (.lsf) / LSF文件
         ↓
   LF Runtime / LF运行时
         ↓
  Execution Result / 执行结果
🔧 Technical Features / 技术特性
Compiler Features / 编译器特性
Multi-language code block parsing / 多语言代码块解析

Smart indentation detection / 智能缩进检测

Directive processing / 指令处理

Source file validation / 源文件验证

Runtime Features / 运行时特性
Cross-language variable management / 跨语言变量管理

Multi-line code execution / 多行代码执行

Enhanced printf with expression evaluation / 支持表达式评估的增强printf

Comprehensive error handling / 全面错误处理

🌟 Advanced Usage / 高级用法
Complex Multi-language Integration / 复杂多语言集成
lf
#name "Advanced Multi-language Demo" / 高级多语言演示
#python_import "json" / 导入JSON模块

// Data processing in Python / Python中的数据处