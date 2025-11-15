#!/usr/bin/env python3
"""
LF Runtime - Optimized Version with Package Support LF运行时 - 支持压缩包的优化版
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

class OptimizedLFRuntime:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.global_start_time = time.time()
        self.test_start_times = {}
    
    def execute_package(self, package_path):
        """Execute program from a package"""
        print("📦 Loading package from:", package_path)
        print("-" * 50)
        
        # Extract and read manifest from package
        with zipfile.ZipFile(package_path, 'r') as zipf:
            # Read manifest
            manifest_content = zipf.read('manifest.json').decode('utf-8')
            manifest = json.loads(manifest_content)
            
            print(f"Manifest loaded: {manifest['metadata']['source_file']}")
            print(f"Files in package: {[f['name'] for f in manifest['files']]}")
            
            # Read program data from the original LSF file
            lsf_content = zipf.read('program.lsf').decode('utf-8')
            lsf_data = json.loads(lsf_content)
            program_data = lsf_data['program']
            
        # Execute based on manifest instructions
        self.execute(program_data)
    

    def execute(self, program_data):
        """Execute program"""
        print("🚀 LF Runtime Started")
        print("-" * 50)
        
        # Initialize global variables
        self._initialize_globals()
        
        # Load modules
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
    
    def _initialize_globals(self):
        """Initialize global variables 初始化全局变量"""
        self.variables.update({
            'global_start_time': self.global_start_time,
            'datetime': datetime,
            'time': time,
            'math': math,
            'random': random,
            'cpp': self,  # Let Python code access cpp methods 让Python代码可以访问cpp方法
            'len': len,
            'str': str,
            'int': int,
            'list': list,
            'dict': dict
        })
    
    def _merge_python_blocks(self, code_blocks):
        """Merge multi-line Python code blocks - Enhanced version 合并多行Python代码块 - 增强版"""
        merged_blocks = []
        i = 0
        
        while i < len(code_blocks):
            block = code_blocks[i]
            
            if block['type'] == 'py':
                # Clean py. prefix 清理py.前缀
                cleaned_content = self._clean_python_code(block['content'])
                
                # Check if it's a code block start 检查是否是代码块开始
                content_stripped = cleaned_content.strip()
                
                # Conditions for detecting block start 检测代码块开始的条件
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
                # 检查这是否是多行结构（列表、字典等）的一部分
                is_multiline_data_structure = self._is_start_of_multiline_structure(content_stripped)
                
                if is_block_start or is_multiline_data_structure:
                    # Start collecting multi-line code block 开始收集多行代码块
                    full_content = cleaned_content
                    base_indent = len(block['content']) - len(block['content'].lstrip())
                    
                    # Find code block end 查找代码块结束
                    j = i + 1
                    in_multiline_structure = is_multiline_data_structure
                    
                    while j < len(code_blocks) and code_blocks[j]['type'] == 'py':
                        next_block = code_blocks[j]
                        next_content_cleaned = self._clean_python_code(next_block['content'])
                        next_indent = len(next_block['content']) - len(next_block['content'].lstrip())
                        
                        # Check if in multi-line structure (dict, list, etc.) 检查是否在多行结构中（字典、列表等）
                        if not in_multiline_structure:
                            in_multiline_structure = self._is_in_multiline_structure(full_content)
                        
                        # If indentation <= base indentation and content not empty, and not in multi-line structure, block ends 如果缩进小于等于基础缩进且内容非空，且不在多行结构中，说明代码块结束
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
        
        print(f"📊 Code blocks merged: {len(code_blocks)} -> {len(merged_blocks)}")
        return merged_blocks
    
    def _is_in_multiline_structure(self, content):
        """Check if in multi-line structure (dict, list, etc.) 检查是否在多行结构中（字典、列表等）"""
        lines = content.split('\n')
        if not lines:
            return False
        
        last_line = lines[-1].strip()
        # If last line ends with these characters, might still be in multi-line structure 如果最后一行以这些字符结尾，可能还在多行结构中
        multiline_indicators = [',', '{', '[', '(', '\\']
        return any(last_line.endswith(indicator) for indicator in multiline_indicators)
    
    def _is_start_of_multiline_structure(self, content):
        """Check if this line starts a multi-line data structure 检查此行是否启动多行数据结构"""
        # Check for assignment with multi-line structures 检查赋值语句中的多行结构
        if '=' in content:
            right_side = content.split('=', 1)[1].strip()
            return (right_side.startswith('[') and not right_side.endswith(']')) or \
                   (right_side.startswith('{') and not right_side.endswith('}')) or \
                   (right_side.startswith('(') and not right_side.endswith(')'))
        return False
    
    def _clean_python_code(self, content):
        """Clean py. prefix in Python code 清理Python代码中的py.前缀"""
        # Use regex to remove all py. prefixes, but keep in strings 使用正则表达式移除所有 py. 前缀，但保留在字符串中的
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Only replace py. prefix in non-string parts 只在非字符串部分替换py.前缀
            parts = re.split(r'(".*?"|\'.*?\')', line)
            for i, part in enumerate(parts):
                if i % 2 == 0:  # Non-string part 非字符串部分
                    part = re.sub(r'\bpy\.(\w+)', r'\1', part)
                parts[i] = part
            cleaned_line = ''.join(parts)
            cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def _load_modules(self, directives):
        """Load Python modules"""
        for directive_type, items in directives.items():
            if directive_type == 'python_import':
                for item in items:
                    # Remove potential quotes around module names
                    module_name = item['value'].strip('"\'')
                    try:
                        module = __import__(module_name)
                        self.variables[module_name] = module
                        print(f"\U0001f4e6 Imported module: {module_name}")
                    except ImportError as e:
                        print(f"\u26a0\ufe0f  Failed to import module {module_name}: {e}")
    
    def execute_block(self, block):
        """Execute single code block"""
        # Record test start time
        if "Test" in block.get('content', '') and block['type'] == 'py':
            test_name = block['content'].split(':')[0] if ':' in block['content'] else block['content']
            self.test_start_times[test_name] = time.time()
        
        try:
            if block['type'] == 'cpp':
                self.execute_cpp(block['content'], block['line'])
            elif block['type'] == 'py':
                self.execute_python(block['content'], block['line'])
            elif block['type'] == 'js':
                self.execute_javascript(block['content'], block['line'])
            elif block['type'] == 'java':
                self.execute_java(block['content'], block['line'])
            elif block['type'] == 'php':
                self.execute_php(block['content'], block['line'])
            elif block['type'] == 'rust':
                self.execute_rust(block['content'], block['line'])
        except Exception as e:
            print(f"❌ Execution error at line {block['line']}: {e}")
    
    def execute_cpp(self, code, line_number):
        """Execute C++ code - Support full C++ syntax"""
        # Ensure correct removal of 'cpp.' prefix, if present
        if code.startswith('cpp.'):
            cpp_code = code[4:]  # Remove 'cpp.' prefix
        else:
            cpp_code = code  # If prefix has been removed, use directly
    
        # If it's a simple single-line printf, still use the fast path
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
                # For simple printf, execute directly
                self._execute_cpp_full(cpp_code, line_number)
            return
        else:
            # For complex C++ code, use full execution mode
            self._execute_cpp_full(cpp_code, line_number)
    
    def _execute_cpp_full(self, cpp_code, line_number):
        """Full execution of C++ code"""
        try:
            # Create temporary C++ file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                # Generate complete C++ program, including variable declarations and user code
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
                'g++',  # Use g++ compiler
                temp_cpp_file, 
                '-o', temp_exe,
                '-std=c++11',  # Use C++11 standard
                '-O2'          # Optimization level
            ]
            
            compile_result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True,
                timeout=15  # Compilation timeout
            )
            
            if compile_result.returncode == 0:
                # Run compiled program
                run_result = subprocess.run(
                    [temp_exe], 
                    capture_output=True, 
                    text=True,
                    timeout=10  # Run timeout
                )
                print(run_result.stdout, end='')
                if run_result.stderr:
                    print(f"C++ Runtime Warning: {run_result.stderr}")
            else:
                # Compilation error, provide friendly error message
                error_msg = self._format_cpp_compile_error(compile_result.stderr, line_number, cpp_code)
                print(error_msg)
            
            # Clean up temporary files
            self._cleanup_temp_files(temp_cpp_file, temp_exe)
            
        except FileNotFoundError:
            print(f"[C++] Compiler not found. Please install g++.")
        except subprocess.TimeoutExpired:
            print(f"[C++] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"[C++] Execution error at line {line_number}: {e}.")
    
    def _generate_cpp_program(self, user_code):
        """生成完整的C++程序，包含变量声明和用户代码"""
        # 生成必要的头文件
        headers = [
            "#include <iostream>",
            "#include <string>",
            "#include <vector>",
            "#include <map>",
            "#include <cmath>"
        ]
        
        # 生成变量声明
        variable_declarations = []
        for var_name, var_value in self.variables.items():
            # 只传递简单的变量（避免传递函数和模块）
            if not callable(var_value) and not hasattr(var_value, '__name__'):
                cpp_var = self._python_to_cpp_variable(var_name, var_value)
                if cpp_var:
                    variable_declarations.append(cpp_var)
        
        # 生成完整的C++程序
        program = "\n".join(headers) + "\n\n"
        program += "using namespace std;\n\n"
        
        # 添加变量声明
        if variable_declarations:
            program += "// Python variables / Python变量\n"
            program += "\n".join(variable_declarations) + "\n\n"
        
        # 添加主函数和用户代码
        program += "int main() {\n"
        # 在主函数中添加变量声明的初始化
        program += "    // User code / 用户代码\n"
        program += "    " + user_code.replace('\n', '\n    ') + "\n"
        program += "    return 0;\n"
        program += "}"
        
        return program
    
    def _python_to_cpp_variable(self, var_name, var_value):
        """将Python变量转换为C++变量声明"""
        try:
            # 处理不同类型的Python变量
            if isinstance(var_value, bool):
                return f"bool {var_name} = {'true' if var_value else 'false'};"
            elif isinstance(var_value, int):
                return f"int {var_name} = {var_value};"
            elif isinstance(var_value, float):
                return f"double {var_name} = {var_value};"
            elif isinstance(var_value, str):
                # 转义字符串中的引号
                escaped_str = var_value.replace('"', '\\"')
                return f'string {var_name} = "{escaped_str}";'
            elif isinstance(var_value, list):
                # 简单处理列表（只支持同类型列表）
                if var_value and all(isinstance(x, int) for x in var_value):
                    elements = ', '.join(str(x) for x in var_value)
                    return f"int {var_name}[] = {{{elements}}};"
                elif var_value and all(isinstance(x, float) for x in var_value):
                    elements = ', '.join(str(x) for x in var_value)
                    return f"double {var_name}[] = {{{elements}}};"
                elif var_value and all(isinstance(x, str) for x in var_value):
                    elements = ', '.join(f'"{x.replace(chr(34), chr(92)+chr(34))}"' for x in var_value)
                    return f"string {var_name}[] = {{{elements}}};"
            elif isinstance(var_value, dict):
                # 简单处理字典（只支持字符串到字符串的映射）
                if all(isinstance(k, str) and isinstance(v, str) for k, v in var_value.items()):
                    return f"// map<string, string> {var_name}; // Dictionary not fully supported"
        except:
            pass  # 转换失败时跳过
        
        return None  # 无法转换的变量类型
    
    def _format_cpp_compile_error(self, error_output, line_number, original_code):
        """格式化C++编译错误信息"""
        # 简化GCC的错误输出
        lines = error_output.split('\n')
        simplified_errors = []
        
        for line in lines:
            if 'error:' in line and 'temp_' not in line:
                # 移除临时文件路径信息
                clean_line = re.sub(r'/tmp/tmp\w+\.cpp', f'第{line_number}行', line)
                simplified_errors.append(clean_line)
        
        if simplified_errors:
            error_msg = '\n'.join(simplified_errors[:5])  # 显示前5个错误
            return f"[C++] Compile Error:\n{error_msg}\nCode: {original_code}"
        else:
            return f"[C++] Compile Error at line {line_number}: {original_code}"
    
    def _parse_printf_ultimate(self, content):
        """Enhanced printf parsing"""
        # Basic cleanup
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
                    # Split parameters, handling nested structures
                    params = self._split_printf_params(params_str)
                
                    # Replace format specifiers
                    result = format_str
                    for param in params:
                        value = self._evaluate_expression_simple(param)
                        # Handle different format specifiers
                        if '%s' in result:
                            result = result.replace('%s', str(value), 1)
                        elif '%.2f' in result:
                            result = result.replace('%.2f', f"{float(value):.2f}", 1)
                        elif '%d' in result:
                            result = result.replace('%d', str(int(value)), 1)
                        # If there are other format specifiers, replace with value
                        elif '%' in result:
                            # Find position of first % symbol
                            percent_pos = result.find('%')
                            if percent_pos != -1:
                                # Find end position of format specifier
                                format_end = percent_pos + 1
                                while format_end < len(result) and result[format_end] in '0123456789.fFgGeEsSdDxXoO':
                                    format_end += 1
                                # Replace the entire format specifier
                                result = result[:percent_pos] + str(value) + result[format_end:]
                
                    return result
                else:
                    # No parameters, return format string directly
                    return format_str
            else:
                # No closing quote found, return original content
                return content
    
        return content

    def _split_printf_params(self, params_str):
        """Split printf parameters correctly 正确分割printf参数"""
        params = []
        current_param = ""
        paren_count = 0
        bracket_count = 0
        brace_count = 0
        in_string = False
        string_char = ''
        
        for char in params_str:
            if not in_string:
                if char in '\"\'':
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
                    # 参数分隔符
                    params.append(current_param.strip())
                    current_param = ""
                    continue
            else:
                if char == string_char:
                    in_string = False
                    string_char = ''
            
            current_param += char
        
        # 添加最后一个参数
        if current_param.strip():
            params.append(current_param.strip())
        
        return params

    def _evaluate_expression_simple(self, expr):
        """简化版表达式评估"""
        expr = expr.strip()
    
        # 处理复杂的变量引用，如 people[0].name, data["metadata"]["average"] 等
        try:
            # 将expr转换为Python可执行的表达式
            # 需要将变量名替换为实际变量值
            result = self._evaluate_python_expr(expr)
            if result is not None:
                return result
        except:
            pass  # 如果转换失败，继续使用原来的逻辑
    
        # 直接变量查找
        if expr in self.variables:
            value = self.variables[expr]
            if not callable(value):
                return value
    
        # 字符串
        if len(expr) >= 2 and ((expr[0] == '"' and expr[-1] == '"') or 
                               (expr[0] == "'" and expr[-1] == "'")):
            return expr[1:-1]
            # 处理 len() 表达式
        if expr.startswith('len(') and expr.endswith(')'):
            inner_expr = expr[4:-1].strip()  # 去掉 len( 和 )
            if inner_expr in self.variables:
                value = self.variables[inner_expr]
                return len(value)
    
        # 数字字面量
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except:
            pass
        return expr

    def _evaluate_python_expr(self, expr):
        """使用Python环境评估表达式"""
        try:
            # 创建安全的执行环境，包含变量
            env = dict(self.variables)
            # 添加一些内置函数
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
            env.update(safe_builtins)
            # 安全评估表达式
            result = eval(expr, {"__builtins__": {}}, env)
            return result
        except Exception as e:
            # 如果评估失败，返回None
            # print(f"Debug: Expression '{expr}' evaluation failed: {e}")  # 调试信息
            return None
    
    def _evaluate_expressions_in_string(self, text):
        """Evaluate expressions in string 评估字符串中的表达式"""
        # Process datetime.datetime.now().strftime(...) 处理 datetime.datetime.now().strftime(...)
        datetime_pattern = r'datetime\.datetime\.now\(\)\.strftime\(([^)]+)\)'
        def replace_datetime(match):
            try:
                format_str = match.group(1).strip('\"\'')
                return datetime.datetime.now().strftime(format_str)
            except:
                return match.group(0)
        
        text = re.sub(datetime_pattern, replace_datetime, text)
        
        # Process variable references 处理变量引用
        text = self._replace_variables_in_string(text)
        
        # Process len() expressions 处理len()表达式
        len_pattern = r'len\(([^)]+)\)'
        def replace_len(match):
            try:
                expr = match.group(1)
                if expr == 'variables':
                    return str(len(self.variables))
                elif expr == 'functions':
                    return str(len(self.functions))
                else:
                    # Try to evaluate other expressions 尝试评估其他表达式
                    value = self._evaluate_expression(expr)
                    return str(len(value)) if value else '0'
            except:
                return match.group(0)
        
        text = re.sub(len_pattern, replace_len, text)
        
        # Process time expressions 处理时间表达式
        time_patterns = {
            r'total_duration:\.3f': f"{(time.time() - self.global_start_time):.3f}",
            r'duration:\.3f': "0.123",  # Default value 默认值
        }
        
        for pattern, replacement in time_patterns.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _evaluate_expression(self, expr):
        """Evaluate expression 评估表达式"""
        expr = expr.strip()
        
        # If it's a variable name 如果是变量名
        if expr in self.variables:
            return self.variables[expr]
        
        # If it's a literal 如果是字面量
        try:
            if expr.startswith('[') and expr.endswith(']'):
                # Safely evaluate list expressions 安全评估列表表达式
                return ast.literal_eval(expr)
            elif expr.startswith('{') and expr.endswith('}'):
                # Safely evaluate dict expressions 安全评估字典表达式
                return ast.literal_eval(expr)
            elif expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
            elif expr.startswith("'") and expr.endswith("'"):
                return expr[1:-1]
        except:
            pass
        
        return None
    
    def _replace_variables_in_string(self, text):
        """Replace variable references in string 替换字符串中的变量引用"""
        # Find all possible variable names 查找所有可能的变量名
        words = re.findall(r'\b[a-zA-Z_]\w*\b', text)
        
        for word in words:
            if word in self.variables and word not in ['printf', 'py', 'datetime', 'time']:
                value = self.variables[word]
                
                # Skip functions and modules 跳过函数和模块
                if callable(value) or hasattr(value, '__name__'):
                    continue
                
                # Format value 格式化值
                if isinstance(value, float):
                    formatted_value = f"{value:.3f}"
                elif isinstance(value, (list, tuple)):
                    if len(value) > 5:
                        formatted_value = f"{value[:3]}...] ({len(value)} elements) (共{len(value)}个元素)"
                    else:
                        formatted_value = str(value)
                elif isinstance(value, dict):
                    formatted_value = f"dict({len(value)} keys) (共{len(value)}个键)"
                else:
                    formatted_value = str(value)
                
                # Exact replacement 精确替换
                text = re.sub(r'\b' + re.escape(word) + r'\b', formatted_value, text)
        
        return text
    
    def execute_python(self, code, line_number):
        """Execute Python code - Enhanced version"""
        # Create execution environment
        env = {
            'math': math,
            'random': random,
            'datetime': datetime,
            'time': time,
            'print': print,
            '__builtins__': __builtins__,
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
                if key not in ['math', 'random', 'datetime', 'time', 'print', '__builtins__', 'vars', 'globals', 'locals']:
                    if callable(value):
                        self.functions[key] = value
                    else:
                        self.variables[key] = value
                        
        except Exception as e:
            raise Exception(f"Python error: {e}")
    
    def execute_javascript(self, code, line_number):
        """Execute JavaScript code"""
        # Ensure correct removal of 'js.' prefix, if present
        if code.startswith('js.'):
            js_code = code[3:]  # Remove 'js.' prefix
        else:
            js_code = code  # If prefix has been removed, use directly
        
        # Create temporary JavaScript file and execute
        try:
            # Create a JavaScript environment with Python variables
            js_env = "/* Python variables */\n"
            for var_name, var_value in self.variables.items():
                # Only pass simple variables (avoid passing functions and modules)
                if not callable(var_value) and not hasattr(var_value, '__name__'):
                    # Convert Python variables to JavaScript variables
                    if isinstance(var_value, bool):
                        js_env += f"const {var_name} = {json.dumps(var_value).lower()};\n"
                    elif isinstance(var_value, (int, float)):
                        js_env += f"const {var_name} = {json.dumps(var_value)};\n"
                    elif isinstance(var_value, str):
                        # Escape quotes in string
                        escaped_str = var_value.replace('"', '\"')
                        js_env += f'const {var_name} = "{escaped_str}";\n'
                    elif isinstance(var_value, (list, dict)):
                        try:
                            js_env += f"const {var_name} = {json.dumps(var_value)};\n"
                        except:
                            pass  # Skip objects that can't be serialized
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                f.write(js_env + js_code.strip())
                temp_js_file = f.name
            
            # Execute JavaScript code using Node.js
            result = subprocess.run(
                ['node', temp_js_file], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            print(result.stdout, end='')
            if result.stderr:
                print(f"JavaScript Runtime Error: {result.stderr}", file=sys.stderr)
            
            # Clean up temporary file
            self._cleanup_temp_files(temp_js_file, None)
        except FileNotFoundError:
            print("[JS] Node.js not found. Please install Node.js.")
        except subprocess.TimeoutExpired:
            print(f"[JS] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"[JS] Execution error at line {line_number}: {e}.")
    
    def execute_java(self, code, line_number):
        """Execute Java code"""
        # Ensure correct removal of 'java.' prefix, if present
        if code.startswith('java.'):
            java_code = code[5:]  # Remove 'java.' prefix
        else:
            java_code = code  # If prefix has been removed, use directly
        
        # Create temporary Java file and execute
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
                # Create a simple Java class to execute code
                java_class = f"public class TempJava {{\n    public static void main(String[] args) {{\n        {java_code.strip()}\n    }}\n}}"
                f.write(java_class)
                temp_java_file = f.name
            
            # Compile Java code
            compile_result = subprocess.run(
                ['javac', temp_java_file], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if compile_result.returncode == 0:
                # Run compiled class
                class_file = temp_java_file.replace('.java', '.class')
                run_result = subprocess.run(
                    ['java', '-cp', os.path.dirname(temp_java_file), 'TempJava'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                print(run_result.stdout, end='')
                if run_result.stderr:
                    print(f"Java Runtime Error: {run_result.stderr}", file=sys.stderr)
            else:
                print(f"Java Compile Error: {compile_result.stderr}")
            
            # Clean up temporary files
            self._cleanup_temp_files(temp_java_file, temp_java_file.replace('.java', '.class'))
        except FileNotFoundError:
            print("[JAVA] Java compiler not found. Please install JDK.")
        except subprocess.TimeoutExpired:
            print(f"[JAVA] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"[JAVA] Execution error at line {line_number}: {e}.")
    
    def execute_php(self, code, line_number):
        """Execute PHP code"""
        # Ensure correct removal of 'php.' prefix, if present
        if code.startswith('php.'):
            php_code = code[4:]  # Remove 'php.' prefix
        else:
            php_code = code  # If prefix has been removed, use directly
        
        # Create temporary PHP file and execute
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False, encoding='utf-8') as f:
                # Create PHP script
                php_script = f"<?php\n{php_code.strip()}\n?>"
                f.write(php_script)
                temp_php_file = f.name
            
            # Execute PHP code
            result = subprocess.run(
                ['php', temp_php_file], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            print(result.stdout, end='')
            if result.stderr:
                print(f"PHP Runtime Error: {result.stderr}", file=sys.stderr)
            
            # Clean up temporary files
            self._cleanup_temp_files(temp_php_file, None)
        except FileNotFoundError:
            print("[PHP] PHP interpreter not found. Please install PHP.")
        except subprocess.TimeoutExpired:
            print(f"[PHP] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"[PHP] Execution error at line {line_number}: {e}.")
    
    def execute_rust(self, code, line_number):
        """Execute Rust code"""
        # Ensure correct removal of 'rust.' prefix, if present
        if code.startswith('rust.'):
            rust_code = code[5:]  # Remove 'rust.' prefix
        else:
            rust_code = code  # If prefix has been removed, use directly
        
        # Create temporary Rust file and execute
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_rs_file = os.path.join(temp_dir, 'main.rs')
                temp_exe = os.path.join(temp_dir, 'main.exe' if os.name == 'nt' else 'main')
                
                # Create Rust program
                rust_program = f"fn main() {{\n    {rust_code.strip()}\n}}"
                with open(temp_rs_file, 'w', encoding='utf-8') as f:
                    f.write(rust_program)
                
                # Compile Rust code
                compile_result = subprocess.run(
                    ['rustc', temp_rs_file, '-o', temp_exe], 
                    capture_output=True, 
                    text=True, 
                    timeout=30,  # Rust compilation may be slow
                    cwd=temp_dir
                )
                
                if compile_result.returncode == 0:
                    # Run compiled program
                    run_result = subprocess.run(
                        [temp_exe], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    print(run_result.stdout, end='')
                    if run_result.stderr:
                        print(f"Rust Runtime Error: {run_result.stderr}", file=sys.stderr)
                else:
                    print(f"Rust Compile Error: {compile_result.stderr}")
        except FileNotFoundError:
            print("[RUST] Rust compiler not found. Please install Rust.")
        except subprocess.TimeoutExpired:
            print(f"[RUST] Execution timeout at line {line_number}.")
        except Exception as e:
            print(f"[RUST] Execution error at line {line_number}: {e}.")
    
    def _cleanup_temp_files(self, file1, file2):
        """清理临时文件"""
        try:
            if file1 and os.path.exists(file1):
                os.unlink(file1)
            if file2 and os.path.exists(file2):
                os.unlink(file2)
        except:
            pass  # 忽略清理错误

def main():
    if len(sys.argv) != 2:
        print("Usage: lf-run-optimized.py <file.lsf or file.lfp>")
        print("   or: lf-run-optimized.py --shell  (for interactive shell)")
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
    """Start LF language interactive shell"""
    print("🚀 LF Language Interactive Shell")
    print("Type 'exit' or 'quit' to exit")
    print("Use 'py.', 'cpp.', 'js.', etc. prefixes to specify languages")
    print("-" * 50)
    
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
                print(f"⚠️  Please use language prefixes (py., cpp., js., java., php., rust.)")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def parse_single_line(lines):
    """解析单行输入的辅助函数"""
    directives = {}
    code_blocks = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        raw_line = line
        
        # 检查语言前缀
        if raw_line.startswith('cpp.'):
            content = raw_line[4:]  # Remove 'cpp.' 去掉 'cpp.'
            code_blocks.append({
                'line': i + 1,
                'type': 'cpp',
                'content': content
            })
        elif raw_line.startswith('py.'):
            content = raw_line[3:]  # Remove 'py.' 去掉 'py.'
            code_blocks.append({
                'line': i + 1,
                'type': 'py',
                'content': content
            })
        elif raw_line.startswith('js.'):
            content = raw_line[3:]  # Remove 'js.' 去掉 'js.'
            code_blocks.append({
                'line': i + 1,
                'type': 'js',
                'content': content
            })
        elif raw_line.startswith('java.'):
            content = raw_line[5:]  # Remove 'java.' 去掉 'java.'
            code_blocks.append({
                'line': i + 1,
                'type': 'java',
                'content': content
            })
        elif raw_line.startswith('php.'):
            content = raw_line[4:]  # Remove 'php.' 去掉 'php.'
            code_blocks.append({
                'line': i + 1,
                'type': 'php',
                'content': content
            })
        elif raw_line.startswith('rust.'):
            content = raw_line[5:]  # Remove 'rust.' 去掉 'rust.'
            code_blocks.append({
                'line': i + 1,
                'type': 'rust',
                'content': content
            })
        else:
            print(f"⚠️  Unrecognized language prefix / 未识别的语言前缀: {line}")
    
    return {
        'directives': directives,
        'code_blocks': code_blocks,
        'source_hash': 'shell'
    }

if __name__ == "__main__":
    main()