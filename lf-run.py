#!/usr/bin/env python3
"""
LF Runtime - Highly Optimized Version with Enhanced Features

Performance-enhanced, feature-rich LF runtime with advanced execution capabilities.
"""

import sys
import os
import json
import math
import random
import datetime
import re
import time
import zipfile
import tempfile
import subprocess
import ast
import shutil
import importlib.util
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ExecutionStats:
    """Execution statistics"""
    start_time: float
    language_stats: Dict[str, int]
    memory_usage: int
    total_executions: int

class OptimizedLFRuntime:
    """Highly optimized LF runtime with enhanced features"""
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.global_start_time = time.time()
        self.test_start_times = {}
        self.security_level = "enhanced"
        self.max_execution_time = 60  # Increased for complex programs
        self.max_memory_usage = 200 * 1024 * 1024  # 200MB
        self.execution_stats = ExecutionStats(
            start_time=time.time(),
            language_stats={},
            memory_usage=0,
            total_executions=0
        )
        self.temp_files = []  # Track temporary files for cleanup
    
    def execute_package(self, package_path: str):
        """Execute program from a package"""
        print("📦 Loading package from:", package_path)
        print("-" * 50)
        
        try:
            # Extract and read manifest from package
            with zipfile.ZipFile(package_path, 'r') as zipf:
                # Read manifest
                manifest_content = zipf.read('manifest.json').decode('utf-8')
                manifest = json.loads(manifest_content)
                
                print(f"📦 Package: {manifest['metadata']['source_file']}")
                print(f"📦 Files: {[f['name'] for f in manifest['files']]}")
                
                # Read program data from the original LSF file
                lsf_content = zipf.read('program.lsf').decode('utf-8')
                lsf_data = json.loads(lsf_content)
                program_data = lsf_data['program']
                
        except Exception as e:
            print(f"❌ Package loading failed: {e}")
            return
        
        # Execute based on manifest instructions
        self.execute(program_data)
    
    def execute(self, program_data: Dict[str, Any]):
        """Execute LF program with enhanced features"""
        print("🚀 LF Runtime Started")
        print("-" * 50)
        
        # Initialize global variables
        self._initialize_globals()
        
        # Load modules from directives
        self._load_modules(program_data.get('directives', {}))
        
        # Preprocessing: merge multi-line Python code
        merged_blocks = self._merge_python_blocks(program_data.get('code_blocks', []))
        
        # Execute code blocks
        for block in merged_blocks:
            self.execute_block(block)
        
        total_time = time.time() - self.global_start_time
        print("-" * 50)
        print("✅ Execution Completed")
        print(f"📊 Total execution time: {total_time:.3f}s")
        print(f"📊 Final variables: {len(self.variables)}")
        print(f"📊 Final functions: {len(self.functions)}")
        
        # Print execution statistics
        self._print_execution_stats(total_time)
        
        # Cleanup temporary files
        self._cleanup_temp_files()
    
    def _initialize_globals(self):
        """Initialize global variables with enhanced functionality"""
        self.variables.update({
            'global_start_time': self.global_start_time,
            'datetime': datetime,
            'time': time,
            'math': math,
            'random': random,
            'cpp': self,  # Let Python code access cpp methods
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'range': range,
            'print': self._enhanced_print,
            'input': input,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter
        })
    
    def _enhanced_print(self, *args, **kwargs):
        """Enhanced print function with additional features"""
        print(*args, **kwargs)
        # Could add logging, formatting, or other features here
    
    def _merge_python_blocks(self, code_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced multi-line Python code block merger with better performance"""
        merged_blocks = []
        i = 0
        
        while i < len(code_blocks):
            block = code_blocks[i]
            
            if block['type'] == 'py':
                # Clean py. prefix
                cleaned_content = self._clean_python_code(block['content'])
                
                # Check if it's a code block start
                content_stripped = cleaned_content.strip()
                
                # Conditions for detecting block start
                is_block_start = (
                    content_stripped.startswith('def ') or 
                    content_stripped.startswith('class ') or
                    content_stripped.startswith('if ') or
                    content_stripped.startswith('for ') or
                    content_stripped.startswith('while ') or
                    content_stripped.startswith('with ') or
                    content_stripped.startswith('try:') or
                    content_stripped.startswith('try ') or
                    content_stripped.startswith('except ') or
                    content_stripped.startswith('elif ') or
                    content_stripped.startswith('else:') or
                    content_stripped.startswith('@') or
                    (content_stripped.endswith(':') and not content_stripped.startswith('#'))
                )
                
                # Check if this is part of a multi-line structure (list, dict, etc.)
                is_multiline_data_structure = self._is_start_of_multiline_structure(content_stripped)
                
                if is_block_start or is_multiline_data_structure:
                    # Start collecting multi-line code block
                    full_content = cleaned_content
                    base_indent = len(block['content']) - len(block['content'].lstrip())
                    
                    # Find code block end
                    j = i + 1
                    in_multiline_structure = is_multiline_data_structure
                    
                    while j < len(code_blocks) and code_blocks[j]['type'] == 'py':
                        next_block = code_blocks[j]
                        next_content_cleaned = self._clean_python_code(next_block['content'])
                        next_indent = len(next_block['content']) - len(next_block['content'].lstrip())
                        
                        # Check if in multi-line structure (dict, list, etc.)
                        if not in_multiline_structure:
                            in_multiline_structure = self._is_in_multiline_structure(full_content)
                        
                        # If indentation <= base indentation and content not empty, and not in multi-line structure, block ends
                        if (next_indent <= base_indent and 
                            next_content_cleaned.strip() and 
                            not next_content_cleaned.strip().startswith('#') and
                            not next_content_cleaned.strip().startswith('//') and
                            not in_multiline_structure):
                            break
                        
                        full_content += '\n' + next_content_cleaned
                        j += 1
                    
                    merged_blocks.append({
                        'line': block['line'],
                        'type': 'py',
                        'content': full_content
                    })
                    i = j
                else:
                    merged_blocks.append({
                        'line': block['line'],
                        'type': 'py',
                        'content': cleaned_content
                    })
                    i += 1
            else:
                merged_blocks.append(block)
                i += 1
        
        print(f"📊 Python blocks merged: {len(code_blocks)} -> {len(merged_blocks)}")
        return merged_blocks
    
    def _is_in_multiline_structure(self, content: str) -> bool:
        """Check if in multi-line structure (dict, list, etc.)"""
        lines = content.split('\n')
        if not lines:
            return False
        
        last_line = lines[-1].strip()
        # If last line ends with these characters, might still be in multi-line structure
        multiline_indicators = [',', '{', '[', '(', '\\']
        return any(last_line.endswith(indicator) for indicator in multiline_indicators)
    
    def _is_start_of_multiline_structure(self, content: str) -> bool:
        """Check if this line starts a multi-line data structure"""
        # Check for assignment with multi-line structures
        if '=' in content:
            right_side = content.split('=', 1)[1].strip()
            return (right_side.startswith('[') and not right_side.endswith(']')) or \
                   (right_side.startswith('{') and not right_side.endswith('}')) or \
                   (right_side.startswith('(') and not right_side.endswith(')'))
        return False
    
    def _clean_python_code(self, content: str) -> str:
        """Clean py. prefix in Python code with enhanced performance"""
        # Use regex to remove all py. prefixes, but keep in strings
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Only replace py. prefix in non-string parts
            parts = re.split(r'(".*?"|\'.*?\')', line)
            for idx, part in enumerate(parts):
                if idx % 2 == 0:  # Non-string part
                    part = re.sub(r'\\bpy\\.(\\w+)', r'\\1', part)
                parts[idx] = part
            cleaned_line = ''.join(parts)
            cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def _load_modules(self, directives: Dict[str, Any]):
        """Load Python modules with enhanced error handling"""
        for directive_type, items in directives.items():
            if directive_type == 'python_import':
                for item in items:
                    # Remove potential quotes around module names
                    module_name = item['value'].strip('"\\'')
                    try:
                        spec = importlib.util.find_spec(module_name)
                        if spec is not None:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            self.variables[module_name] = module
                            print(f"📦 Imported module: {module_name}")
                        else:
                            # Try standard import
                            module = __import__(module_name)
                            self.variables[module_name] = module
                            print(f"📦 Imported module: {module_name}")
                    except ImportError as e:
                        print(f"⚠️  Failed to import module {module_name}: {e}")
                    except Exception as e:
                        print(f"⚠️  Error importing module {module_name}: {e}")
    
    def execute_block(self, block: Dict[str, Any]):
        """Execute single code block with enhanced error handling"""
        # Record execution statistics
        lang_type = block['type']
        self.execution_stats.language_stats[lang_type] = self.execution_stats.language_stats.get(lang_type, 0) + 1
        self.execution_stats.total_executions += 1
        
        # Record test start time if needed
        if "Test" in block.get('content', '') and lang_type == 'py':
            test_name = block['content'].split(':')[0] if ':' in block['content'] else block['content']
            self.test_start_times[test_name] = time.time()
        
        try:
            if lang_type == 'cpp':
                self.execute_cpp(block['content'], block['line'])
            elif lang_type == 'py':
                self.execute_python(block['content'], block['line'])
            elif lang_type == 'js':
                self.execute_javascript(block['content'], block['line'])
            elif lang_type == 'java':
                self.execute_java(block['content'], block['line'])
            elif lang_type == 'php':
                self.execute_php(block['content'], block['line'])
            elif lang_type == 'rust':
                self.execute_rust(block['content'], block['line'])
            else:
                print(f"⚠️  Unknown code type: {lang_type}")
        except Exception as e:
            print(f"❌ Execution error at line {block['line']}: {e}")
            import traceback
            traceback.print_exc()
    
    def execute_cpp(self, code: str, line_number: int):
        """Execute C++ code with enhanced features and better error handling"""
        # Ensure correct removal of 'cpp.' prefix, if present
        if code.startswith('cpp.'):
            cpp_code = code[4:]  # Remove 'cpp.' prefix
        else:
            cpp_code = code  # If prefix has been removed, use directly
        
        # For simple printf commands, use fast path
        if (cpp_code.strip().startswith('printf(') and 
            '<<' not in cpp_code and
            'cout' not in cpp_code and
            cpp_code.count(';') <= 1):
            # Extract printf parameters
            start = cpp_code.find('(')
            end = cpp_code.rfind(')')
            if start != -1 and end != -1:
                content = cpp_code[start+1:end]
                result = self._parse_printf_ultimate(content)
                print(result, end='')
            else:
                self._execute_cpp_full(cpp_code, line_number)
            return
        else:
            # For complex C++ code, use full execution mode
            self._execute_cpp_full(cpp_code, line_number)
    
    def _execute_cpp_full(self, cpp_code: str, line_number: int):
        """Full execution of C++ code with error handling"""
        temp_cpp_file = None
        temp_exe = None
        
        try:
            # Create temporary C++ file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                # Generate complete C++ program
                full_cpp_program = self._generate_cpp_program(cpp_code)
                f.write(full_cpp_program)
                temp_cpp_file = f.name
            
            # Create executable file path
            if os.name == 'nt':  # Windows
                temp_exe = temp_cpp_file.replace('.cpp', '.exe')
            else:  # Linux/macOS
                temp_exe = temp_cpp_file.replace('.cpp', '.out')
            
            # Compile C++ code
            compile_cmd = [
                'g++',
                temp_cpp_file, 
                '-o', temp_exe,
                '-std=c++11',
                '-O2'  # Optimization level
            ]
            
            compile_result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True,
                timeout=30  # Increased timeout for complex programs
            )
            
            if compile_result.returncode == 0:
                # Run compiled program
                run_result = subprocess.run(
                    [temp_exe], 
                    capture_output=True, 
                    text=True,
                    timeout=20  # Increased timeout
                )
                print(run_result.stdout, end='')
                if run_result.stderr:
                    print(f"⚠️  C++ Runtime Warning: {run_result.stderr}")
            else:
                # Compilation error, provide friendly error message
                error_msg = self._format_cpp_compile_error(compile_result.stderr, line_number, cpp_code)
                print(error_msg)
            
            # Track temporary files for cleanup
            if temp_cpp_file:
                self.temp_files.append(temp_cpp_file)
            if temp_exe:
                self.temp_files.append(temp_exe)
                
        except FileNotFoundError:
            print(f"⚠️  [C++] Compiler not found. Please install g++. Skipping execution.")
        except subprocess.TimeoutExpired:
            print(f"⚠️  [C++] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"⚠️  [C++] Execution error at line {line_number}: {e}.")
    
    def _generate_cpp_program(self, user_code: str) -> str:
        """Generate complete C++ program with variable declarations"""
        # Generate necessary headers
        headers = [
            "#include <iostream>",
            "#include <string>",
            "#include <vector>",
            "#include <map>",
            "#include <cmath>",
            "#include <cstdlib>"  # For stdlib functions
        ]
        
        # Generate variable declarations
        variable_declarations = []
        for var_name, var_value in self.variables.items():
            # Only pass simple variables (avoid passing functions and modules)
            if not callable(var_value) and not hasattr(var_value, '__name__'):
                cpp_var = self._python_to_cpp_variable(var_name, var_value)
                if cpp_var:
                    variable_declarations.append(cpp_var)
        
        # Generate complete C++ program
        program = "\n".join(headers) + "\n\n"
        program += "using namespace std;\n\n"
        
        # Add variable declarations
        if variable_declarations:
            program += "// Python variables\n"
            program += "\n".join(variable_declarations) + "\n\n"
        
        # Add main function and user code
        program += "int main() {\n"
        program += "    // User code\n"
        program += "    " + user_code.replace('\n', '\n    ') + "\n"
        program += "    return 0;\n"
        program += "}"
        
        return program
    
    def _python_to_cpp_variable(self, var_name: str, var_value: Any) -> Optional[str]:
        """Convert Python variable to C++ variable declaration"""
        try:
            # Handle different types of Python variables
            if isinstance(var_value, bool):
                return f"bool {var_name} = {'true' if var_value else 'false'};"
            elif isinstance(var_value, int):
                return f"int {var_name} = {var_value};"
            elif isinstance(var_value, float):
                return f"double {var_name} = {var_value};"
            elif isinstance(var_value, str):
                # Escape string quotes
                escaped_str = var_value.replace('"', '\\"")
                return f'string {var_name} = "{escaped_str}";'
            elif isinstance(var_value, list):
                # Handle simple lists
                if var_value and all(isinstance(x, (int, float)) for x in var_value):
                    elements = ', '.join(str(x) for x in var_value)
                    return f"vector<decltype({var_value[0]})> {var_name} = {{{elements}}};"
            elif isinstance(var_value, dict):
                # Handle simple dict
                if var_value and all(isinstance(k, str) and isinstance(v, str) for k, v in var_value.items()):
                    return f"// map<string, string> {var_name}; // Dictionary not fully supported"
        except:
            pass  # Conversion failed, skip variable
        
        return None  # Cannot convert variable type
    
    def _format_cpp_compile_error(self, error_output: str, line_number: int, original_code: str) -> str:
        """Format C++ compile error message"""
        lines = error_output.split('\n')
        simplified_errors = []
        
        for line in lines:
            if 'error:' in line and 'temp_' not in line:
                # Remove temporary file path information
                clean_line = re.sub(r'/tmp/tmp\\w+\\.cpp', f'line {line_number}', line)
                simplified_errors.append(clean_line)
        
        if simplified_errors:
            error_msg = '\n'.join(simplified_errors[:5])  # Show first 5 errors
            return f"[C++] Compile Error:\n{error_msg}\nCode: {original_code}"
        else:
            return f"[C++] Compile Error at line {line_number}: {original_code}"
    
    def _parse_printf_ultimate(self, content: str) -> str:
        """Enhanced printf parsing with better expression evaluation"""
        content = content.strip()
        
        # Extract format string
        if content.startswith('"'):
            end_quote = content.find('"', 1)
            if end_quote != -1:
                format_str = content[1:end_quote]
                params_str = content[end_quote+1:].lstrip()
                
                # If there are commas, process parameters
                if params_str.startswith(','):
                    params_str = params_str[1:].strip()
                    params = self._split_printf_params(params_str)
                    
                    # Replace format specifiers with actual values
                    result = format_str
                    import re
                    pattern = r'%[0-9.]*[sdfFgGeExXoOc]'
                    
                    for param in params:
                        value = self._evaluate_expression_simple(param)
                        match = re.search(pattern, result)
                        if match:
                            start, end = match.span()
                            result = result[:start] + str(value) + result[end:]
                        else:
                            break  # No more format specifiers
                    
                    return result
                else:
                    # No parameters, return format string directly
                    return format_str
            else:
                return content
        
        return content
    
    def _split_printf_params(self, params_str: str) -> List[str]:
        """Split printf parameters correctly"""
        params = []
        current_param = ""
        paren_count = 0
        bracket_count = 0
        brace_count = 0
        in_string = False
        string_char = ''
        
        for char in params_str:
            if not in_string:
                if char in '"\\'':
                    in_string = True
                    string_char = char
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == ',' and paren_count == 0 and bracket_count == 0 and brace_count == 0:
                    params.append(current_param.strip())
                    current_param = ""
                    continue
            else:
                if char == string_char:
                    in_string = False
                    string_char = ''
            
            current_param += char
        
        # Add last parameter
        if current_param.strip():
            params.append(current_param.strip())
        
        return params
    
    def _evaluate_expression_simple(self, expr: str) -> Any:
        """Simplified expression evaluation with security"""
        expr = expr.strip()
        
        # Direct variable lookup first
        if expr in self.variables:
            value = self.variables[expr]
            if not callable(value):
                return value
        
        # String literal
        if len(expr) >= 2 and ((expr[0] == '"' and expr[-1] == '"') or 
                               (expr[0] == "'" and expr[-1] == "'")):
            return expr[1:-1]
        
        # len() function
        if expr.startswith('len(') and expr.endswith(')'):
            inner_expr = expr[4:-1].strip()
            if inner_expr in self.variables:
                value = self.variables[inner_expr]
                return len(value)
        
        # Numeric literal
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except:
            pass
        
        # Try safe evaluation
        try:
            # Create safe evaluation environment
            safe_env = dict(self.variables)
            import builtins
            safe_builtins = {
                'len': len,
                'int': int,
                'float': float,
                'str': str,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'range': range,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round
            }
            safe_env.update(safe_builtins)
            
            result = eval(expr, {"__builtins__": {}}, safe_env)
            return result
        except:
            pass
        
        return expr
    
    def execute_python(self, code: str, line_number: int):
        """Execute Python code with enhanced security and features"""
        # Create execution environment
        env = {
            'math': math,
            'random': random,
            'datetime': datetime,
            'time': time,
            'print': print,
            'input': input,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'range': range,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'range': range,
                'abs': abs,
                'min': min,
                'max': max,
                'sum': sum,
                'print': print,
                'input': input,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter
            },
            'vars': lambda: self.variables,
            'globals': lambda: self.variables,
            'locals': lambda: env
        }
        
        # Add variables and functions
        env.update(self.variables)
        env.update(self.functions)
        
        try:
            # Execute code
            exec(code, env)
            
            # Update variables and functions
            for key, value in env.items():
                if key not in [
                    'math', 'random', 'datetime', 'time', 'print', 'input',
                    'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'range',
                    'abs', 'min', 'max', 'sum', 'sorted', 'enumerate', 'zip', 'map', 'filter',
                    '__builtins__', 'vars', 'globals', 'locals'
                ]:
                    if callable(value):
                        self.functions[key] = value
                    else:
                        self.variables[key] = value
                        
        except Exception as e:
            raise Exception(f"Python error at line {line_number}: {e}")
    
    def execute_javascript(self, code: str, line_number: int):
        """Execute JavaScript code with enhanced error handling"""
        if code.startswith('js.'):
            js_code = code[3:]  # Remove 'js.' prefix
        else:
            js_code = code
        
        temp_js_file = None
        
        try:
            # Create JavaScript environment with Python variables
            js_env = "/* Python variables */\n"
            for var_name, var_value in self.variables.items():
                if not callable(var_value) and not hasattr(var_value, '__name__'):
                    if isinstance(var_value, bool):
                        js_env += f"const {var_name} = {json.dumps(var_value).lower()};\n"
                    elif isinstance(var_value, (int, float)):
                        js_env += f"const {var_name} = {json.dumps(var_value)};\n"
                    elif isinstance(var_value, str):
                        escaped_str = var_value.replace('"', '\\"")
                        js_env += f'const {var_name} = "{escaped_str}";\n'
                    elif isinstance(var_value, (list, dict)):
                        try:
                            js_env += f"const {var_name} = {json.dumps(var_value)};\n"
                        except:
                            pass  # Skip unserializable objects
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                f.write(js_env + js_code.strip())
                temp_js_file = f.name
            
            # Execute JavaScript code using Node.js
            result = subprocess.run(
                ['node', temp_js_file], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            print(result.stdout, end='')
            if result.stderr:
                print(f"⚠️  JavaScript Runtime Error: {result.stderr}", file=sys.stderr)
            
            # Track temporary file for cleanup
            if temp_js_file:
                self.temp_files.append(temp_js_file)
                
        except FileNotFoundError:
            print("⚠️  [JS] Node.js not found. Please install Node.js.")
        except subprocess.TimeoutExpired:
            print(f"⚠️  [JS] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"⚠️  [JS] Execution error at line {line_number}: {e}.")
    
    def execute_java(self, code: str, line_number: int):
        """Execute Java code with enhanced error handling"""
        if code.startswith('java.'):
            java_code = code[5:]  # Remove 'java.' prefix
        else:
            java_code = code
        
        temp_java_file = None
        temp_class_file = None
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
                temp_filename = os.path.basename(f.name)
                class_name = temp_filename.replace('.java', '')
                
                # Create Java environment with Python variables
                java_vars = "// Python variables\n"
                for var_name, var_value in self.variables.items():
                    if not callable(var_value) and not hasattr(var_value, '__name__'):
                        if isinstance(var_value, bool):
                            java_vars += f"        boolean {var_name} = {str(var_value).lower()};\n"
                        elif isinstance(var_value, int):
                            java_vars += f"        int {var_name} = {var_value};\n"
                        elif isinstance(var_value, float):
                            java_vars += f"        double {var_name} = {var_value};\n"
                        elif isinstance(var_value, str):
                            escaped_str = var_value.replace('"', '\\\"')
                            java_vars += f'        String {var_name} = "{escaped_str}";\n'
                
                java_class = f"public class {class_name} {{\n    public static void main(String[] args) {{\n{java_vars}        {java_code.strip()}\n    }}\n}}"
                f.write(java_class)
                temp_java_file = f.name
            
            # Compile Java code
            compile_result = subprocess.run(
                ['javac', temp_java_file], 
                capture_output=True, 
                text=True, 
                timeout=20
            )
            
            if compile_result.returncode == 0:
                # Run compiled class
                temp_class_file = temp_java_file.replace('.java', '.class')
                class_name = os.path.basename(temp_java_file).replace('.java', '')
                
                run_result = subprocess.run(
                    ['java', '-cp', os.path.dirname(temp_java_file), class_name], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                
                print(run_result.stdout, end='')
                if run_result.stderr:
                    print(f"⚠️  Java Runtime Error: {run_result.stderr}", file=sys.stderr)
            else:
                print(f"❌ Java Compile Error: {compile_result.stderr}")
            
            # Track temporary files for cleanup
            if temp_java_file:
                self.temp_files.append(temp_java_file)
            if temp_class_file and os.path.exists(temp_class_file):
                self.temp_files.append(temp_class_file)
                
        except FileNotFoundError:
            print("⚠️  [JAVA] Java compiler not found. Please install JDK.")
        except subprocess.TimeoutExpired:
            print(f"⚠️  [JAVA] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"⚠️  [JAVA] Execution error at line {line_number}: {e}.")
    
    def execute_php(self, code: str, line_number: int):
        """Execute PHP code"""
        if code.startswith('php.'):
            php_code = code[4:]  # Remove 'php.' prefix
        else:
            php_code = code
        
        temp_php_file = None
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False, encoding='utf-8') as f:
                php_script = f"<?php\n{php_code.strip()}\n?>"
                f.write(php_script)
                temp_php_file = f.name
            
            result = subprocess.run(
                ['php', temp_php_file], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            print(result.stdout, end='')
            if result.stderr:
                print(f"⚠️  PHP Runtime Error: {result.stderr}", file=sys.stderr)
            
            # Track temporary file for cleanup
            if temp_php_file:
                self.temp_files.append(temp_php_file)
                
        except FileNotFoundError:
            print("⚠️  [PHP] PHP interpreter not found. Please install PHP.")
        except subprocess.TimeoutExpired:
            print(f"⚠️  [PHP] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"⚠️  [PHP] Execution error at line {line_number}: {e}.")
    
    def execute_rust(self, code: str, line_number: int):
        """Execute Rust code with enhanced error handling"""
        if code.startswith('rust.'):
            rust_code = code[5:]  # Remove 'rust.' prefix
        else:
            rust_code = code
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_rs_file = os.path.join(temp_dir, 'main.rs')
                temp_exe = os.path.join(temp_dir, 'main.exe' if os.name == 'nt' else 'main')
                
                rust_program = f"fn main() {{\n    {rust_code.strip()}\n}}"
                with open(temp_rs_file, 'w', encoding='utf-8') as f:
                    f.write(rust_program)
                
                compile_result = subprocess.run(
                    ['rustc', temp_rs_file, '-o', temp_exe], 
                    capture_output=True, 
                    text=True, 
                    timeout=60,  # Rust compilation may be slow
                    cwd=temp_dir
                )
                
                if compile_result.returncode == 0:
                    run_result = subprocess.run(
                        [temp_exe], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    print(run_result.stdout, end='')
                    if run_result.stderr:
                        print(f"⚠️  Rust Runtime Error: {run_result.stderr}", file=sys.stderr)
                else:
                    print(f"❌ Rust Compile Error: {compile_result.stderr}")
        except FileNotFoundError:
            print("⚠️  [RUST] Rust compiler not found. Please install Rust.")
        except subprocess.TimeoutExpired:
            print(f"⚠️  [RUST] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"⚠️  [RUST] Execution error at line {line_number}: {e}.")
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except:
                pass  # Ignore cleanup errors
        self.temp_files = []
    
    def _print_execution_stats(self, total_time: float):
        """Print execution statistics"""
        print(f"📊 Language execution stats:")
        for lang, count in self.execution_stats.language_stats.items():
            print(f"   {lang}: {count} blocks")
        print(f"📊 Total blocks executed: {self.execution_stats.total_executions}")
        print(f"⏱️  Total execution time: {total_time:.3f}s")

def main():
    if len(sys.argv) != 2:
        print("Usage: lf-run.py <file.lsf or file.lfp>")
        print("   or: lf-run.py --shell  (for interactive shell)")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    if input_arg == '--shell' or input_arg == '-s':
        # Start interactive shell
        start_shell()
    elif input_arg.endswith('.lsf') or input_arg.endswith('.lfp'):
        runtime = OptimizedLFRuntime()
        
        if input_arg.endswith('.lfp'):  # Package file
            runtime.execute_package(input_arg)
        else:  # Regular LSF file
            if not os.path.exists(input_arg):
                print(f"Error: File not found {input_arg}")
                sys.exit(1)
            try:
                with open(input_arg, 'r', encoding='utf-8') as f:
                    lsf_data = json.load(f)
            except Exception as e:
                print(f"Read failed: {e}")
                sys.exit(1)
            
            runtime.execute(lsf_data['program'])
    else:
        print("Error: Requires .lsf or .lfp file or --shell flag")
        sys.exit(1)

def start_shell():
    """Start LF language interactive shell with enhanced features"""
    print("🚀 LF Language Interactive Shell")
    print("Type 'exit' or 'quit' to exit")
    print("Use 'py.', 'cpp.', 'js.', etc. prefixes to specify languages")
    print("Commands: 'stats' for execution stats, 'vars' for variables, 'funcs' for functions")
    print("-" * 70)
    
    runtime = OptimizedLFRuntime()
    # Initialize Python environment
    runtime._initialize_globals()
    
    while True:
        try:
            # Get user input
            user_input = input("LF> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'stats':
                print(f"📊 Variables: {len(runtime.variables)}, Functions: {len(runtime.functions)}")
                continue
            elif user_input.lower() == 'vars':
                print("📊 Variables:")
                for name, value in runtime.variables.items():
                    if not callable(value) and not hasattr(value, '__name__'):
                        print(f"  {name}: {value}")
                continue
            elif user_input.lower() == 'funcs':
                print("📊 Functions:")
                for name in runtime.functions:
                    print(f"  {name}")
                continue
            
            if not user_input:
                continue
            
            # Check if it's a language prefix command
            if any(user_input.startswith(prefix) for prefix in ['py.', 'cpp.', 'js.', 'java.', 'php.', 'rust.']):
                # Parse single line command
                lines = [user_input]
                parsed_data = parse_single_line(lines)
                
                # Execute code blocks
                for block in parsed_data['code_blocks']:
                    runtime.execute_block(block)
            else:
                print(f"⚠️  Please use language prefixes (py., cpp., js., java., php., rust.) or commands (stats, vars, funcs)")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def parse_single_line(lines):
    """Parse single line input for shell"""
    directives = {}
    code_blocks = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        raw_line = line
        
        if raw_line.startswith('cpp.'):
            content = raw_line[4:]
            code_blocks.append({
                'line': i + 1,
                'type': 'cpp',
                'content': content
            })
        elif raw_line.startswith('py.'):
            content = raw_line[3:]
            code_blocks.append({
                'line': i + 1,
                'type': 'py',
                'content': content
            })
        elif raw_line.startswith('js.'):
            content = raw_line[3:]
            code_blocks.append({
                'line': i + 1,
                'type': 'js',
                'content': content
            })
        elif raw_line.startswith('java.'):
            content = raw_line[5:]
            code_blocks.append({
                'line': i + 1,
                'type': 'java',
                'content': content
            })
        elif raw_line.startswith('php.'):
            content = raw_line[4:]
            code_blocks.append({
                'line': i + 1,
                'type': 'php',
                'content': content
            })
        elif raw_line.startswith('rust.'):
            content = raw_line[5:]
            code_blocks.append({
                'line': i + 1,
                'type': 'rust',
                'content': content
            })
        else:
            print(f"⚠️  Unrecognized language prefix: {line}")
    
    return {
        'directives': directives,
        'code_blocks': code_blocks,
        'source_hash': 'shell'
    }

if __name__ == "__main__":
    main()
