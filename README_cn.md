# LF语言系统 v3.0 / LF Language System v3.0

## 🚀 概述 / Overview
LF (Language Fusion) 是一个高级的多语言融合编程语言，允许在单个源文件中无缝集成多种编程语言。它使用智能标记系统来区分不同语言的代码块，并提供统一的编译和执行环境，具有增强的安全性和性能。

LF使开发人员能够在同一个`.lf`文件中使用Python、C++、JavaScript、Java、PHP和Rust编写代码，变量和函数可在语言间共享。

### 主要特性 / Key Features
- **多语言融合**: 在单个文件中使用多种语言 (`.lf`)
- **增强安全性**: 具有多重安全级别的高级安全验证
- **高性能**: 优化的编译和执行引擎
- **跨语言变量共享**: 一种语言中定义的变量可被其他语言访问
- **全面工具集**: 编译器、运行时、安全扫描器和打包工具
- **高级功能**: 基准测试、分析和交互式shell

## 📁 文件扩展名 / File Extensions
- 源文件: `.lf` / Source files: `.lf`
- 编译文件: `.lsf` (LF序列化格式) / Compiled files: `.lsf` (LF Serialized Format)
- 压缩包: `.lfp` (LF包) / Compressed packages: `.lfp` (LF Package)

## 🏗️ 语法结构 / Syntax Structure

### 1. 注释 / Comments
```
// 单行注释 / Single-line comment
/* 多行注释 / Multi-line comment */
```

### 2. 指令 / Directives
以 `#` 开头，用于配置和元数据：/ Start with `#`, used for configuration and metadata:

```
#name "程序名称" / #name "Program Name"
#version "1.0" / #version "1.0"
#author "作者名称" / #author "Author Name"
#python_import "模块名称" / #python_import "module_name"
```

### 3. 代码块 / Code Blocks

#### Python 代码块 / Python Code Blocks
```
py.单行Python代码 / py.Single line Python code
py.多行Python代码开始: / py.Multi-line Python code start:
py.    缩进的代码 / py.    Indented code
py.    继续执行 / py.    Continue execution
```

#### C++ 代码块 / C++ Code Blocks
```
cpp.单行C++代码 / cpp.Single line C++ code
cpp.printf("格式化输出: %s", variable) / cpp.printf("Formatted output: %s", variable)
cpp.cout << "标准输出: " << variable << endl; / cpp.cout << "Standard output: " << variable << endl;
```

#### JavaScript 代码块 / JavaScript Code Blocks
```
js.单行JavaScript代码 / js.Single line JavaScript code
```

#### Java 代码块 / Java Code Blocks
```
java.单行Java代码 / java.Single line Java code
```

#### PHP 代码块 / PHP Code Blocks
```
php.单行PHP代码 / php.Single line PHP code
```

#### Rust 代码块 / Rust Code Blocks
```
rust.单行Rust代码 / rust.Single line Rust code
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
#name "我的LF程序" / #name "My LF Program"
#version "1.0.0" / #version "1.0.0"
#author "开发者" / #author "Developer"
#python_import "math" / #python_import "math"
#python_import "datetime" / #python_import "datetime"
```

### Python 代码块 / Python Code Blocks
语法: `py.Python代码` / Syntax: `py.Python code`

功能 / Features:
- 自动多行函数定义和代码块处理 / Automatic multi-line function definition and code block processing
- 支持所有Python语法 / Support all Python syntax
- 变量和函数在全局环境中共享 / Variables and functions shared in global environment

示例 / Example:
```lf
// 单行Python / Single line Python
py.x = 10
py.name = "LF Language"

// 函数定义（自动多行处理）/ Function definition (automatic multi-line processing)
py.def calculate(a, b):
py.    result = a * b + math.sqrt(a)
py.    return result

// 复杂结构 / Complex structure
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
- 变量引用和表达式计算 / Variable references and expression evaluation

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

示例 / Example:
```lf
js.console.log("Hello from JavaScript")
js.console.log("Accessing Python variable:", message);
```

### Java 代码块 / Java Code Blocks
语法: `java.Java代码` / Syntax: `java.Java code`

当前状态 / Current Status:
- 基础支持（需要JDK）- 变量访问和Java执行 / Basic support (requires JDK) - Variable access and Java execution

示例 / Example:
```lf
java.System.out.println("Hello from Java");
java.System.out.println("Accessing shared variable: " + message);
```

### PHP 代码块 / PHP Code Blocks
语法: `php.PHP代码` / Syntax: `php.PHP code`

当前状态 / Current Status:
- 基础支持（需要PHP）- 变量访问和PHP执行 / Basic support (requires PHP) - Variable access and PHP execution

示例 / Example:
```lf
php.echo "Hello from PHP!\n";
php.echo "Accessing shared variable: " . $message . "\n";
```

### Rust 代码块 / Rust Code Blocks
语法: `rust.Rust代码` / Syntax: `rust.Rust code`

当前状态 / Current Status:
- 基础支持（需要Rust工具链）- 变量访问和Rust执行 / Basic support (requires Rust toolchain) - Variable access and Rust execution

示例 / Example:
```lf
rust.println!("Hello from Rust!");
rust.println!("Accessing shared variable: {}", message);
```

## 🔄 执行模型 / Execution Model

### 变量作用域 / Variable Scope
- 所有变量在全局作用域中共享 / All variables shared in global scope
- Python中定义的变量可在其他语言中引用 / Variables defined in Python can be referenced in other languages
- 函数定义在全局函数表中 / Function definitions in global function table

### 执行顺序 / Execution Order
1. 解析所有指令并导入模块 / Parse all directives and import modules
2. 按顺序执行所有代码块 / Execute all code blocks in order
3. 支持跨语言变量访问 / Support cross-language variable access

## 💾 编译输出格式 / Compilation Output Format
编译后的`.lsf`文件使用JSON格式 / Compiled `.lsf` files use JSON format:

```json
{
  "format_version": "LSF-3.0",
  "metadata": {
    "compiler": "lf-compiler-optimized-v3",
    "source_file": "source_file_name",
    "source_path": "/path/to/source",
    "compile_time": 1234567890.123,
    "security_level": "enhanced",
    "optimization_level": 2
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
    "source_hash": "source_file_hash",
    "parse_time": 0.012,
    "stats": {
      "total_lines": 100,
      "directive_count": 5,
      "code_block_count": 10
    }
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

### 命令 / Commands
LF系统通过主工具支持多个命令 / The LF system supports multiple commands via the main tool:

```bash
# 编译LF源码 / Compile LF source
python lf_main.py compile program.lf

# 运行编译后的LSF或打包的LFP文件 / Run compiled LSF or packaged LFP file
python lf_main.py run program.lsf
python lf_main.py run program.lfp

# 创建独立可执行文件 / Create standalone executable
python lf_main.py package-exe program.lf

# 创建DLL包装器 / Create DLL wrapper
python lf_main.py package-dll program.lf

# 运行性能基准测试 / Run performance benchmark
python lf_main.py benchmark program.lf

# 分析源代码结构 / Analyze source structure
python lf_main.py analyze program.lf

# 启动交互式shell / Start interactive shell
python lf_main.py shell

# 显示版本 / Show version
python lf_main.py version
```

### 直接执行 / Direct Execution
```bash
# 直接编译 / Compile directly
python lf-compile.py program.lf

# 直接运行 / Run directly
python lf-run.py program.lsf
python lf-run.py program.lfp

# 交互式shell / Interactive shell
python lf-run.py --shell
```

## 🔧 安装要求 / Installation Requirements

### 基础功能所需 / Required for basic functionality:
- Python 3.7+

### 完整语言支持可选 / Optional for full language support:
- C++: g++编译器 / g++ compiler
- JavaScript: Node.js
- Java: JDK
- PHP: PHP解释器 / PHP interpreter
- Rust: Rust工具链 / Rust toolchain

## 🔍 功能摘要 / Feature Summary

### 核心功能 / Core Features
- **多语言融合**: 在单个文件中使用多种语言 / Multi-language Fusion: Use multiple languages in single file
- **智能多行处理**: 自动Python代码块识别 / Smart Multi-line Processing: Automatic Python code block recognition
- **变量共享**: 跨语言变量访问 / Variable Sharing: Cross-language variable access
- **模块导入**: 支持Python模块导入 / Module Import: Support Python module import
- **增强安全性**: 多重安全级别与模式验证 / Enhanced Security: Multiple security levels with pattern validation
- **性能优化**: 高性能编译和执行引擎 / Performance Optimized: High-performance compilation and execution engine

### 高级功能 / Advanced Features
- **基准测试**: 性能测量工具 / Benchmarking: Performance measurement tools
- **代码分析**: 源代码结构分析 / Code Analysis: Source structure analysis
- **安全扫描**: 全面安全验证 / Security Scanning: Comprehensive security validation
- **打包**: 可执行文件和DLL创建 / Packaging: Executable and DLL creation
- **交互式Shell**: 实时代码执行 / Interactive Shell: Real-time code execution
- **增强错误处理**: 详细的错误报告 / Enhanced Error Handling: Detailed error reporting

### 安全功能 / Security Features
- **多级安全**: 可配置的安全级别 / Multi-level Security: Configurable security levels
- **模式识别**: 危险代码模式检测 / Pattern Recognition: Detection of dangerous code patterns
- **语言特定扫描**: 为每种语言定制的验证 / Language-specific Scanning: Tailored validation for each language
- **AST分析**: Python代码的抽象语法树解析 / AST Analysis: Abstract Syntax Tree parsing for Python code
- **全面报告**: 详细的安全报告 / Comprehensive Reporting: Detailed security reports

## 🚀 适用场景 / Applicable Scenarios
- 快速原型开发 / Rapid prototyping development
- 多语言学习工具 / Multi-language learning tool
- 脚本自动化任务 / Script automation tasks
- 教育和演示用途 / Education and demonstration purposes
- 跨语言概念验证 / Cross-language proof of concept
- 性能关键应用 / Performance-critical applications
- 安全敏感环境 / Security-sensitive environments

## 📊 系统架构 / System Architecture
```
LF源文件 (.lf) / LF Source File (.lf)
         ↓
    LF编译器 (v3.0) / LF Compiler (v3.0)
         ↓
LSF文件 (.lsf) + LFP包 (.lfp) / LSF File (.lsf) + LFP Package (.lfp)
         ↓
   LF运行时 (v3.0) / LF Runtime (v3.0)
         ↓
  执行结果 / Execution Result
```

## 🔧 中央管理工具 (lf_main.py) / Central Management Tool (lf_main.py)
LF Main工具为所有LF操作提供统一接口：/ The LF Main tool provides a unified interface for all LF operations:
- 编译LF源文件 / Compile LF source files
- 运行LSF或LFP文件 / Run LSF or LFP files
- 将程序打包为独立可执行文件（EXE）/ Package programs as standalone executables (EXE)
- 创建DLL包装器用于集成 / Create DLL wrappers for integration
- 分析源代码结构 / Analyze source code structure
- 基准测试性能 / Benchmark performance
- 扫描安全 / Scan security

用法 / Usage:
```bash
python lf_main.py compile program.lf      # 编译LF源码 / Compile LF source
python lf_main.py run program.lsf         # 运行编译后的LSF文件 / Run compiled LSF file
python lf_main.py run program.lfp         # 运行打包的LFP文件 / Run packaged LFP file
python lf_main.py package-exe program.lf  # 打包为可执行文件 / Package as executable
python lf_main.py package-dll program.lf  # 创建DLL包装器 / Create DLL wrapper
python lf_main.py benchmark program.lf    # 基准测试性能 / Benchmark performance
python lf_main.py analyze program.lf      # 分析源码 / Analyze source
python lf_main.py version                 # 显示版本 / Show version
```

## 🛡️ 安全功能 / Security Features
LF v3.0包含高级安全功能：/ LF v3.0 includes advanced security features:
- **多级验证**: 可配置的安全级别 / Multi-level validation: Configurable security levels
- **模式检测**: 危险代码模式识别 / Pattern detection: Identification of dangerous code patterns
- **语言特定扫描**: 每种语言的定制安全 / Language-specific scanning: Tailored security for each language
- **AST分析**: 深度Python代码分析 / AST analysis: Deep Python code analysis
- **全面报告**: 详细的安全问题报告 / Comprehensive reporting: Detailed security issue reports

安全模块可以独立使用：/ The security module can be used independently:
```bash
python lf-security.py  # 运行安全测试 / Run security tests
```

## 🌟 高级用法 / Advanced Usage
### 复杂多语言集成 / Complex Multi-language Integration
```lf
#name "高级多语言演示" / #name "Advanced Multi-language Demo"
#python_import "json" / #python_import "json"

// Python中的数据处理 / Data processing in Python
py.data = {"name": "LF", "version": 3.0}
py.processed_data = json.dumps(data, indent=2)

// 使用C++输出 / Output using C++
cpp.printf("Processed data: %s", processed_data);

// 在JavaScript中进一步处理 / Further processing in JavaScript
js.processed = JSON.parse(processed_data);
js.processed.timestamp = new Date().toISOString();
js.console.log("Final data:", js.processed);
```

## 📈 v3.0中的性能改进 / Performance Improvements in v3.0
- **更快的编译**: 优化的解析算法 / Faster compilation: Optimized parsing algorithms
- **增强的执行**: 更好的运行时性能 / Enhanced execution: Better runtime performance
- **内存效率**: 减少内存占用 / Memory efficiency: Reduced memory footprint
- **并行处理**: 未来并行执行的潜力 / Parallel processing: Potential for future parallel execution
- **缓存机制**: 改进的编译缓存 / Caching mechanisms: Improved compilation caching