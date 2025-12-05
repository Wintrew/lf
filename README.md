# LF Language Specification v1.0

## 📋 Overview
LF (Language Fusion) is a multi-language fusion programming language that allows mixing multiple programming languages in the same source file. It uses a simple tagging system to distinguish code blocks from different languages and provides a unified compilation and execution environment. This optimized version removes external compiler dependencies for basic functionality and adds support for complete language execution when compilers are available. 

LF is a programming language that allows in the same source file: `.lf`

## 📁 File Extensions
- Source files: `.lf`
- Compiled files: `.lsf` (LF Serialized Format)
- Compressed packages: `.lfp` (LF Package)

## 🏗️ Syntax Structure

### 1. Comments
```
// Single-line comment
/* Multi-line comment */
```

### 2. Directives
Start with `#`, used for configuration and metadata:

```
#name "Program Name"
#version "1.0"
#author "Author Name"
#python_import "module_name"
```

### 3. Code Blocks

#### Python Code Blocks
```
py.Single line Python code
py.Multi-line Python code start:
py.    Indented code
py.    Continue execution
```

#### C++ Code Blocks
```
cpp.Single line C++ code
cpp.printf("Formatted output: %s", variable)
cpp.cout << "Standard output: " << variable << endl;
```

#### JavaScript Code Blocks
```
js.Single line JavaScript code
```

#### Java Code Blocks
```
java.Single line Java code
```

#### PHP Code Blocks
```
php.Single line PHP code
```

#### Rust Code Blocks
```
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

```
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
- Output code content

Example:

```lf
js.console.log("Hello from JavaScript")
js.console.log("Accessing Python variable:", message);
```

### Java Code Blocks
Syntax: `java.Java code`

Current Status:
- Basic support (requires JDK) - Variable access and Java execution
- Output code content

Example:

```lf
java.System.out.println("Hello from Java");
java.System.out.println("Accessing shared variable: " + message);
```

### PHP Code Blocks
Syntax: `php.PHP code`

Current Status:
- Basic support (requires PHP) - Variable access and PHP execution
- Output code content

Example:

```lf
php.echo "Hello from PHP!
";
php.echo "Accessing shared variable: " . $message . "
";
```

### Rust Code Blocks
Syntax: `rust.Rust code`

Current Status:
- Basic support (requires Rust toolchain) - Variable access and Rust execution
- Output code content

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

### Compilation
```bash
python lf-compile.py program.lf
```

This generates both program.lsf and program.lfp (package file)

### Execution
```bash
python lf-run.py program.lsf        # Execute LSF file
python lf-run.py program.lfp        # Execute package file
python lf-run.py --shell            # Start interactive shell
```

## ⚡ Central Management with lf_main
LF Main is a central tool for managing LF programs:

### Compilation
```bash
python lf_main.py compile program.lf    # Compile LF source
```

### Execution
```bash
python lf_main.py run program.lsf       # Run LSF file
python lf_main.py run program.lfp       # Run package file
```

### Packaging
```bash
python lf_main.py package-exe program.lf    # Create standalone executable
python lf_main.py package-dll program.lf    # Create DLL wrapper
```

## 🔧 Installation Requirements
Required for basic functionality (Python, C++ printf):
- Python 3.6+

Optional for full language support:
- C++: g++ compiler
- JavaScript: Node.js
- Java: JDK
- PHP: PHP interpreter
- Rust: Rust toolchain

To install all required environments, run:
```
install_lf_environment.bat
```

## 🔍 Feature Summary
- Multi-language Fusion - Use multiple languages in single file
- Smart Multi-line Processing - Automatic Python code block recognition
- Variable Sharing - Cross-language variable access
- Module Import - Support Python module import
- Formatted Output - Enhanced printf functionality
- Error Handling - Comprehensive error reporting mechanism
- Optimized Runtime - No external compiler dependencies for basic functions
- Enhanced C++ Support - Full C++ syntax execution with cross-language variable access (requires g++ compiler)
- Package Support - Create compressed packages with separate source files
- Real-time Execution - Execute code in their native environments (requires language interpreters/compilers)
- Cross-language Variable Sharing - Variables defined in one language can be accessed by others

## 🚀 Applicable Scenarios
- Rapid prototyping development
- Multi-language learning tool
- Script automation tasks
- Education and demonstration purposes
- Cross-language proof of concept

## 📊 System Architecture
```
LF Source File (.lf)
         ↓
    LF Compiler
         ↓
LSF File (.lsf) + LFP Package (.lfp)
         ↓
   LF Runtime
         ↓
  Execution Result
```

## 🔧 Central Management Tool (lf_main.py)
LF Main is a central management tool that provides a unified interface for all LF operations:
- Compile LF source files
- Run LSF or LFP files
- Package programs as standalone executables (EXE)
- Create DLL wrappers for integration with other applications

Usage:
```bash
python lf_main.py compile program.lf      # Compile LF source
python lf_main.py run program.lsf         # Run compiled LSF file
python lf_main.py run program.lfp         # Run packaged LFP file
python lf_main.py package-exe program.lf  # Package as executable
python lf_main.py package-dll program.lf  # Create DLL wrapper
```

## 🌟 Advanced Usage
### Complex Multi-language Integration
```lf
#name "Advanced Multi-language Demo"
#python_import "json"

// Data processing in Python
```