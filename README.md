# LF Language System v3.0

## 🚀 Overview
LF (Language Fusion) is an advanced multi-language fusion programming language that allows seamless integration of multiple programming languages within a single source file. It uses an intelligent tagging system to distinguish code blocks from different languages and provides a unified compilation and execution environment with enhanced security and performance.

LF enables developers to write code in Python, C++, JavaScript, Java, PHP, and Rust within the same `.lf` file, with variables and functions shared across languages.

### Key Features
- **Multi-language Fusion**: Write code in multiple languages in a single file (`.lf`)
- **Enhanced Security**: Advanced security validation with multiple security levels
- **High Performance**: Optimized compilation and execution engine
- **Cross-language Variable Sharing**: Variables defined in one language accessible by others
- **Comprehensive Toolset**: Compiler, runtime, security scanner, and packaging tools
- **Advanced Features**: Benchmarking, analysis, and interactive shell

## 📁 File Extensions
- Source files: `.lf`
- Compiled files: `.lsf` (LF Serialized Format)
- Compressed packages: `.lfp` (LF Package)

## 🏗️ Syntax Structure

### 1. Comments
```text
// Single-line comment
/* Multi-line comment */
```

### 2. Directives
Start with `#`, used for configuration and metadata:

```text
#name "Program Name"
#version "1.0"
#author "Author Name"
#python_import "module_name"
```

### 3. Code Blocks

#### Python Code Blocks
```text
py.Single line Python code
py.Multi-line Python code start:
py.    Indented code
py.    Continue execution
```

#### C++ Code Blocks
```text
cpp.Single line C++ code
cpp.printf("Formatted output: %s", variable)
cpp.cout << "Standard output: " << variable << endl;
```

#### JavaScript Code Blocks
```text
js.Single line JavaScript code
```

#### Java Code Blocks
```text
java.Single line Java code
```

#### PHP Code Blocks
```text
php.Single line PHP code
```

#### Rust Code Blocks
```text
rust.Single line Rust code
```

## 📝 Detailed Syntax Specification

### Directive System
Syntax: `#directive_name "value"`

Available Directives:
- `#name` - Program name
- `#version` - Version number
- `#author` - Author information
- `#description` - Program description
- `#python_import` - Python module import (can be used multiple times)

Example:
```text
#name "My LF Program"
#version "1.0.0"
#author "Developer"
#python_import "math"
#python_import "datetime"
```

### Python Code Blocks
Syntax: `py.Python code`

Features:
- Automatic multi-line function definition and code block processing
- Support all Python syntax
- Variables and functions shared in global environment

Example:
```lf
// Single line Python
py.x = 10
py.name = "LF Language"

// Function definition (automatic multi-line processing)
py.def calculate(a, b):
py.    result = a * b + math.sqrt(a)
py.    return result

// Complex structure
py.if x > 5:
py.    print("x greater than 5")
py.    for i in range(3):
py.        print(f"Loop: {i}")
```

### C++ Code Blocks
Syntax: `cpp.C++ code`

Features:
- Basic support - printf formatted output with variable access
- Full support (requires g++ compiler) - Complete C++ syntax including variables, functions, control structures
- Variable references and expression evaluation

Example:
```lf
cpp.printf("Welcome to LF Language!")
cpp.printf("Current time: %s", datetime.datetime.now().strftime("%Y-%m-%d"))
cpp.printf("Variable count: %s, Function count: %s", len(variables), len(functions))
cpp.cout << "Full C++ support: " << message << endl;
```

### JavaScript Code Blocks
Syntax: `js.JavaScript code`

Current Status:
- Basic support (requires Node.js) - Variable access and JavaScript execution

Example:
```lf
js.console.log("Hello from JavaScript")
js.console.log("Accessing Python variable:", message);
```

### Java Code Blocks
Syntax: `java.Java code`

Current Status:
- Basic support (requires JDK) - Variable access and Java execution

Example:
```lf
java.System.out.println("Hello from Java");
java.System.out.println("Accessing shared variable: " + message);
```

### PHP Code Blocks
Syntax: `php.PHP code`

Current Status:
- Basic support (requires PHP) - Variable access and PHP execution

Example:
```lf
php.echo "Hello from PHP!\n";
php.echo "Accessing shared variable: " . $message . "\n";
```

### Rust Code Blocks
Syntax: `rust.Rust code`

Current Status:
- Basic support (requires Rust toolchain) - Variable access and Rust execution

Example:
```lf
rust.println!("Hello from Rust!");
rust.println!("Accessing shared variable: {}", message);
```

## 🔄 Execution Model

### Variable Scope
- All variables shared in global scope
- Variables defined in Python can be referenced in other languages
- Function definitions in global function table

### Execution Order
1. Parse all directives and import modules
2. Execute all code blocks in order
3. Support cross-language variable access

## 💾 Compilation Output Format
Compiled `.lsf` files use JSON format:

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

## 🎯 Complete Examples

### Example 1: Basic Program
```lf
// Basic LF program example
#name "Hello LF"
#version "1.0"
#author "LF Developer"

// Python variable definition
py.message = "Hello, World!"
py.count = 42

// C++ output
cpp.printf("Message: %s", message)
cpp.printf("Count: %s", count)

// Python function
py.def greet(name):
py.    return f"Hello, {name}!"

// Using function
py.result = greet("LF User")
cpp.printf("Function result: %s", result)
```

### Example 2: Mathematical Calculation
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

## ⚡ Running Instructions

### Commands
The LF system supports multiple commands via the main tool:

```bash
# Compile LF source
python lf_main.py compile program.lf

# Run compiled LSF or packaged LFP file
python lf_main.py run program.lsf
python lf_main.py run program.lfp

# Create standalone executable
python lf_main.py package-exe program.lf

# Create DLL wrapper
python lf_main.py package-dll program.lf

# Run performance benchmark
python lf_main.py benchmark program.lf

# Analyze source structure
python lf_main.py analyze program.lf

# Start interactive shell
python lf_main.py shell

# Show version
python lf_main.py version
```

### Direct Execution
```bash
# Compile directly
python lf-compile.py program.lf

# Run directly
python lf-run.py program.lsf
python lf-run.py program.lfp

# Interactive shell
python lf-run.py --shell
```

## 🔧 Installation Requirements

### Required for basic functionality:
- Python 3.7+

### Optional for full language support:
- C++: g++ compiler
- JavaScript: Node.js
- Java: JDK
- PHP: PHP interpreter
- Rust: Rust toolchain

## 🔍 Feature Summary

### Core Features
- **Multi-language Fusion**: Use multiple languages in single file
- **Smart Multi-line Processing**: Automatic Python code block recognition
- **Variable Sharing**: Cross-language variable access
- **Module Import**: Support Python module import
- **Enhanced Security**: Multiple security levels with pattern validation
- **Performance Optimized**: High-performance compilation and execution engine

### Advanced Features
- **Benchmarking**: Performance measurement tools
- **Code Analysis**: Source structure analysis
- **Security Scanning**: Comprehensive security validation
- **Packaging**: Executable and DLL creation
- **Interactive Shell**: Real-time code execution
- **Enhanced Error Handling**: Detailed error reporting

### Security Features
- **Multi-level Security**: Configurable security levels (Low, Medium, High, Strict)
- **Pattern Recognition**: Detection of dangerous code patterns
- **Language-specific Scanning**: Tailored validation for each language
- **AST Analysis**: Abstract Syntax Tree parsing for Python code
- **Comprehensive Reporting**: Detailed security reports

## 🚀 Applicable Scenarios
- Rapid prototyping development
- Multi-language learning tool
- Script automation tasks
- Education and demonstration purposes
- Cross-language proof of concept
- Performance-critical applications
- Security-sensitive environments

## 📊 System Architecture
```
LF Source File (.lf)
         ↓
    LF Compiler (v3.0)
         ↓
LSF File (.lsf) + LFP Package (.lfp)
         ↓
   LF Runtime (v3.0)
         ↓
  Execution Result
```

## 🔧 Central Management Tool (lf_main.py)
The LF Main tool provides a unified interface for all LF operations:
- Compile LF source files
- Run LSF or LFP files
- Package programs as standalone executables (EXE)
- Create DLL wrappers for integration
- Analyze source code structure
- Benchmark performance
- Scan security

Usage:
```bash
python lf_main.py compile program.lf      # Compile LF source
python lf_main.py run program.lsf         # Run compiled LSF file
python lf_main.py run program.lfp         # Run packaged LFP file
python lf_main.py package-exe program.lf  # Package as executable
python lf_main.py package-dll program.lf  # Create DLL wrapper
python lf_main.py benchmark program.lf    # Benchmark performance
python lf_main.py analyze program.lf      # Analyze source
python lf_main.py version                 # Show version
```

## 🛡️ Security Features
LF v3.0 includes advanced security features:
- **Multi-level validation**: Configurable security levels
- **Pattern detection**: Identification of dangerous code patterns
- **Language-specific scanning**: Tailored security for each language
- **AST analysis**: Deep Python code analysis
- **Comprehensive reporting**: Detailed security issue reports

The security module can be used independently:
```bash
python lf-security.py  # Run security tests
```

## 🌟 Advanced Usage
### Complex Multi-language Integration
```lf
#name "Advanced Multi-language Demo"
#python_import "json"

// Data processing in Python
py.data = {"name": "LF", "version": 3.0}
py.processed_data = json.dumps(data, indent=2)

// Output using C++
cpp.printf("Processed data: %s", processed_data);

// Further processing in JavaScript
js.processed = JSON.parse(processed_data);
js.processed.timestamp = new Date().toISOString();
js.console.log("Final data:", js.processed);
```

## 📈 Performance Improvements in v3.0
- **Faster compilation**: Optimized parsing algorithms
- **Enhanced execution**: Better runtime performance
- **Memory efficiency**: Reduced memory footprint
- **Parallel processing**: Potential for future parallel execution
- **Caching mechanisms**: Improved compilation caching