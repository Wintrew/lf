# LF语言规范 v1.0 / LF Language Specification v1.0

## 📋 概述 / Overview
LF (Language Fusion) 是一种多语言融合的编程语言，允许在同一个源文件中混合使用多种编程语言。它通过简单的标记系统来区分不同语言的代码块，并提供了统一的编译和执行环境。优化版本移除了外部编译器依赖以提高可移植性和性能。

LF (Language Fusion) is a multi-language fusion programming language that allows mixing multiple programming languages in the same source file. It uses a simple tagging system to distinguish code blocks from different languages and provides a unified compilation and execution environment. This optimized version removes external compiler dependencies for better portability and performance.

## 📁 文件扩展名 / File Extensions
- 源文件: `.lf` / Source files: `.lf`
- 编译后文件: `.lsf` (LF Serialized Format) / Compiled files: `.lsf`
- 压缩包文件: `.lfp` (LF Package) / Compressed packages: `.lfp`

## 🏗️ 语法结构 / Syntax Structure

### 1. 注释 / Comments
```
// 单行注释 / Single-line comment
/* 多行注释 / Multi-line comment */
```

### 2. 指令 / Directives
以 # 开头，用于配置和元数据：Start with #, used for configuration and metadata:

```
#name "Program Name" / 程序名称
#version "1.0" / 版本号
#author "Author Name" / 作者名
#python_import "module_name" / Python模块导入
```

### 3. 代码块 / Code Blocks

#### Python 代码块 / Python Code Blocks
```
py.Single line Python code / 单行Python代码
py.Multi-line Python code start: / 多行Python代码开始:
py.    Indented code / 缩进的代码
py.    Continue execution / 继续执行
```

#### C++ 代码块 / C++ Code Blocks
```
cpp.Single line C++ code / 单行C++代码
cpp.printf("Formatted output: %s", variable) / 格式化输出
cpp.cout << "Standard output: " << variable << endl; / 标准输出
```

#### JavaScript 代码块 / JavaScript Code Blocks
```
js.Single line JavaScript code / 单行JavaScript代码
```

#### Java 代码块 / Java Code Blocks
```
java.Single line Java code / 单行Java代码
java.System.out.println("Output message"); / 输出消息
```

#### PHP 代码块 / PHP Code Blocks
```
php.Single line PHP code / 单行PHP代码
php.echo "Output message"; / 输出消息
```

#### Rust 代码块 / Rust Code Blocks
```
rust.Single line Rust code / 单行Rust代码
```

## 📝 详细语法规范 / Detailed Syntax Specification

### 指令系统 / Directive System
语法: `#指令名称 "值"` / Syntax: `#directive_name "value"`

可用指令 / Available Directives:

- `#name` - 程序名称 / Program name
- `#version` - 版本号 / Version number
- `#author` - 作者信息 / Author information
- `#description` - 程序描述 / Program description
- `#python_import` - Python模块导入（可多次使用）/ Python module import (can be used multiple times)

示例 / Example:

```
#name "My LF Program" / 我的LF程序
#version "1.0.0" / 版本1.0.0
#author "Developer" / 开发者
#python_import "math" / 导入数学模块
#python_import "datetime" / 导入日期时间模块
```

### Python 代码块 / Python Code Blocks
语法: `py.Python代码` / Syntax: `py.Python code`

功能 / Features:
- 自动多行函数定义和代码块处理 / Automatic multi-line function definition and code block processing
- 支持所有Python语法 / Support all Python syntax
- 变量和函数在全局环境中共享 / Variables and functions shared in global environment

示例 / Example:

```lf
// Single line Python / 单行Python
py.x = 10
py.name = "LF Language"

// Function definition (automatic multi-line processing) / 函数定义（自动多行处理）
py.def calculate(a, b):
py.    result = a * b + math.sqrt(a)
py.    return result

// Complex structure / 复杂结构
py.if x > 5:
py.    print("x greater than 5")
py.    for i in range(3):
py.        print(f"Loop: {i}")
```

### C++ 代码块 / C++ Code Blocks
语法: `cpp.C++代码` / Syntax: `cpp.C++ code`

功能 / Features:
- 基础支持 - 带变量访问的printf格式化输出 / Basic support - printf formatted output with variable access
- 完整支持（需要g++编译器）- 完整C++语法包括变量、函数、控制结构 / Full support (requires g++ compiler) - Complete C++ syntax including variables, functions, control structures
- 变量引用和表达式评估 / Variable references and expression evaluation

示例 / Example:

```lf
cpp.printf("Welcome to LF Language!")
cpp.printf("Current time: %s", datetime.datetime.now().strftime("%Y-%m-%d"))
cpp.printf("Variable count: %s, Function count: %s", len(variables), len(functions))
cpp.cout << "Full C++ support: " << message << endl;
```

### JavaScript 代码块 / JavaScript Code Blocks
语法: `js.JavaScript代码` / Syntax: `js.JavaScript code`

当前状态 / Current Status:
- 基础支持（需要Node.js）- 变量访问和JavaScript执行 / Basic support (requires Node.js) - Variable access and JavaScript execution
- 输出代码内容 / Output code content

示例 / Example:

```lf
js.console.log("Hello from JavaScript")
js.console.log("Accessing Python variable:", message);
```

### Java 代码块 / Java Code Blocks
语法: `java.Java代码` / Syntax: `java.Java code`

当前状态 / Current Status:
- 基础支持（需要JDK）- 变量访问和Java执行 / Basic support (requires JDK) - Variable access and Java execution
- 输出代码内容 / Output code content

示例 / Example:

```lf
java.System.out.println("Hello from Java");
java.System.out.println("Accessing shared variable: " + message);
```

### PHP 代码块 / PHP Code Blocks
语法: `php.PHP代码` / Syntax: `php.PHP代码`

当前状态 / Current Status:
- 基础支持（需要PHP）- 变量访问和PHP执行 / Basic support (requires PHP) - Variable access and PHP execution
- 输出代码内容 / Output code content

示例 / Example:

```lf
php.echo "Hello from PHP!\n";
php.echo "Accessing shared variable: " . $message . "\n";
```

### Rust 代码块 / Rust Code Blocks
语法: `rust.Rust代码` / Syntax: `rust.Rust代码`

当前状态 / Current Status:
- 基础支持（需要Rust工具链）- 变量访问和Rust执行 / Basic support (requires Rust toolchain) - Variable access and Rust execution
- 输出代码内容 / Output code content

示例 / Example:

```lf
rust.println!("Hello from Rust!");
rust.println!("Accessing shared variable: {}", message);
```

## 🔄 执行模型 / Execution Model

### 变量作用域 / Variable Scope
- 所有变量在全局作用域中共享 / All variables shared in global scope
- 在Python中定义的变量可在其他语言中引用 / Variables defined in Python can be referenced in other languages
- 函数定义在全局函数表中 / Function definitions in global function table

### 执行顺序 / Execution Order
1. 解析所有指令并导入模块 / Parse all directives and import modules
2. 按顺序执行所有代码块 / Execute all code blocks in order
3. 支持跨语言变量访问 / Support cross-language variable access

## 💾 编译输出格式 / Compilation Output Format
编译后的.lsf文件使用JSON格式 / Compiled .lsf files use JSON format:

```json
{
  "format_version": "LSF-1.0",
  "metadata": {
    "compiler": "lf-compile-optimized",
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
```

## 🎯 完整示例 / Complete Examples

### 示例1: 基础程序 / Example 1: Basic Program
```lf
// Basic LF program example / 基础LF程序示例
#name "Hello LF"
#version "1.0"
#author "LF Developer"

// Python variable definition / Python变量定义
py.message = "Hello, World!"
py.count = 42

// C++ output / C++输出
cpp.printf("Message: %s", message)
cpp.printf("Count: %s", count)

// Python function / Python函数
py.def greet(name):
py.    return f"Hello, {name}!"

// Using function / 使用函数
py.result = greet("LF User")
cpp.printf("Function result: %s", result)
```

### 示例2: 数学计算 / Example 2: Mathematical Calculation
```lf
#name "Math Calculation Example"
#python_import "math"

py.radius = 5.0
py.area = math.pi * radius ** 2
py.circumference = 2 * math.pi * radius

cpp.printf("Radius: %.2f", radius)
cpp.printf("Area: %.2f", area)
cpp.printf("Circumference: %.2f", circumference)

py.def factorial(n):
py.    if n <= 1:
py.        return 1
py.    else:
py.        return n * factorial(n-1)

py.fact_10 = factorial(10)
cpp.printf("10 factorial: %s", fact_10)
```

## ⚡ 运行说明 / Running Instructions

### 编译 / Compilation
```bash
python lf-compile.py program.lf
```

This generates both program.lsf and program.lfp (package file)

### 执行 / Execution
```bash
python lf-run.py program.lsf        # Execute LSF file / 执行LSF文件
python lf-run.py program.lfp        # Execute package file / 执行包文件
python lf-run.py --shell            # Start interactive shell / 启动交互式shell
```

## ⚡ 使用lf_main进行中央管理 / Central Management with lf_main
LF Main是一个用于管理LF程序的中央工具 / LF Main is a central tool for managing LF programs:

### 编译 / Compilation
```bash
python lf_main.py compile program.lf    # Compile LF source / 编译LF源文件
```

### 执行 / Execution
```bash
python lf_main.py run program.lsf       # Run LSF file / 运行LSF文件
python lf_main.py run program.lfp       # Run package file / 运行包文件
```

### 打包 / Packaging
```bash
python lf_main.py package-exe program.lf    # Create standalone executable / 创建独立可执行文件
python lf_main.py package-dll program.lf    # Create DLL wrapper / 创建DLL包装器
```

## 🔧 安装要求 / Installation Requirements
基础功能所需（Python, C++ printf）/ Required for basic functionality (Python, C++ printf):
- Python 3.6+

完整语言支持可选 / Optional for full language support:
- C++: g++编译器 / g++ compiler
- JavaScript: Node.js
- Java: JDK
- PHP: PHP解释器 / PHP interpreter
- Rust: Rust工具链 / Rust toolchain

要安装所有必需环境，请运行 / To install all required environments, run:
```
install_lf_environment.bat
```

## 🔍 功能摘要 / Feature Summary
- 多语言融合 - 在单个文件中使用多种语言 / Multi-language Fusion - Use multiple languages in single file
- 智能多行处理 - 自动Python代码块识别 / Smart Multi-line Processing - Automatic Python code block recognition
- 变量共享 - 跨语言变量访问 / Variable Sharing - Cross-language variable access
- 模块导入 - 支持Python模块导入 / Module Import - Support Python module import
- 格式化输出 - 增强的printf功能 / Formatted Output - Enhanced printf functionality
- 错误处理 - 全面的错误报告机制 / Error Handling - Comprehensive error reporting mechanism
- 优化运行时 - 基础功能无外部编译器依赖 / Optimized Runtime - No external compiler dependencies for basic functions
- 增强C++支持 - 完整C++语法执行（需要g++编译器）/ Enhanced C++ Support - Full C++ syntax execution with cross-language variable access (requires g++ compiler)
- 包支持 - 创建带有独立源文件的压缩包 / Package Support - Create compressed packages with separate source files
- 实时执行 - 在原生环境中执行代码 / Real-time Execution - Execute code in their native environments (requires language interpreters/compilers)
- 跨语言变量共享 - 一种语言中定义的变量可被其他语言访问 / Cross-language Variable Sharing - Variables defined in one language can be accessed by others

### 压缩包格式 / Package Format
.lfp (LF压缩包) 格式包含 / The .lfp (LF Package) format contains:
- 每种语言的原生格式源文件 / Source files for each language in their native format
- 包含执行指令的 manifest.json 文件 / A manifest.json file with execution instructions
- 原始 .lsf 文件 / The original .lsf file

## 🚀 适用场景 / Applicable Scenarios
- 快速原型开发 / Rapid prototyping development
- 多语言学习工具 / Multi-language learning tool
- 脚本自动化任务 / Script automation tasks
- 教育和演示用途 / Education and demonstration purposes
- 跨语言概念验证 / Cross-language proof of concept

## 📊 系统架构 / System Architecture
```
LF源文件 / LF Source File (.lf)
         ↓
    LF编译器 / LF Compiler
         ↓
LSF文件 + LFP包 / LSF File (.lsf) + LFP Package (.lfp)
         ↓
   LF运行时 / LF Runtime
         ↓
  执行结果 / Execution Result
```

## 🔧 中央管理工具 (lf_main.py) / Central Management Tool (lf_main.py)
LF Main是一个中央管理工具，为所有LF操作提供统一接口：
LF Main is a central management tool that provides a unified interface for all LF operations:
- 编译LF源文件 / Compile LF source files
- 运行LSF或LFP文件 / Run LSF or LFP files
- 将程序打包为独立可执行文件（EXE）/ Package programs as standalone executables (EXE)
- 创建DLL包装器以便与其他应用程序集成 / Create DLL wrappers for integration with other applications

用法 / Usage:
```bash
python lf_main.py compile program.lf      # 编译LF源文件 / Compile LF source
python lf_main.py run program.lsf         # 运行编译后的LSF文件 / Run compiled LSF file
python lf_main.py run program.lfp         # 运行打包的LFP文件 / Run packaged LFP file
python lf_main.py package-exe program.lf  # 打包为可执行文件 / Package as executable
python lf_main.py package-dll program.lf  # 创建DLL包装器 / Create DLL wrapper
```

## 🔧 技术特性 / Technical Features

### 编译器特性 / Compiler Features
- 多语言代码块解析 / Multi-language code block parsing
- 智能缩进检测 / Smart indentation detection
- 指令处理 / Directive processing
- 源文件验证 / Source file validation

### 运行时特性 / Runtime Features
- 跨语言变量管理 / Cross-language variable management
- 多行代码执行 / Multi-line code execution
- 支持表达式评估的增强printf / Enhanced printf with expression evaluation
- 全面错误处理 / Comprehensive error handling
- 无外部编译器依赖 / No external compiler dependencies

## 🌟 高级用法 / Advanced Usage

### 复杂多语言集成 / Complex Multi-language Integration
```lf
#name "Advanced Multi-language Demo" / 高级多语言演示
#python_import "json" / 导入JSON模块

// Data processing in Python / Python中的数据处理
```