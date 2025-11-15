#!/usr/bin/env python3
"""
LF Runtime - Ultimate Fixed Version LF运行时 - 终极修复版本
"""

import sys
import os
import json
import math
import random
import datetime
import re
import time
import tempfile
import subprocess
import shutil

class UltimateLFRuntime:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.global_start_time = time.time()
        self.test_start_times = {}
        self.gcc_compiler = GCCCompiler()

    def execute(self, program_data):
        """Execute program 执行程序"""
        print("🚀 LF Runtime Stress Test Started LF运行时压力测试启动")
        print("-" * 60)
        
        # Initialize global variables 初始化全局变量
        self._initialize_globals()
        
        # Load modules 加载模块
        self._load_modules(program_data.get('directives', {}))
        
        # Preprocessing: merge multi-line Python code 预处理：合并多行Python代码
        merged_blocks = self._merge_python_blocks(program_data.get('code_blocks', []))
        
        # Execute code blocks 执行代码块
        for block in merged_blocks:
            self.execute_block(block)
        
        total_time = time.time() - self.global_start_time
        print("-" * 60)
        print("✅ Stress Test Completed 压力测试完成")
        print(f"📊 Total execution time: {total_time:.3f}s 总执行时间: {total_time:.3f}秒")
        print(f"📊 Final variables: {len(self.variables)} 最终变量数: {len(self.variables)}个")
        print(f"📊 Final functions: {len(self.functions)} 最终函数数: {len(self.functions)}个")
    
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
                    content_stripped.startswith('@') or
                    (content_stripped.endswith(':') and not content_stripped.startswith('#'))
                )
                
                if is_block_start:
                    # Start collecting multi-line code block 开始收集多行代码块
                    full_content = cleaned_content
                    base_indent = len(block['content']) - len(block['content'].lstrip())
                    
                    # Find code block end 查找代码块结束
                    j = i + 1
                    in_multiline_structure = False
                    
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
        
        print(f"📊 Code blocks merged: {len(code_blocks)} -> {len(merged_blocks)} 代码块合并: {len(code_blocks)} -> {len(merged_blocks)}")
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
        """Load Python modules 加载Python模块"""
        for directive_type, items in directives.items():
            if directive_type == 'python_import':
                for item in items:
                    try:
                        module = __import__(item['value'])
                        self.variables[item['value']] = module
                        print(f"📦 Imported module: {item['value']} 导入模块: {item['value']}")
                    except ImportError as e:
                        print(f"⚠️  Failed to import module {item['value']}: {e} 无法导入模块 {item['value']}: {e}")
    
    def execute_block(self, block):
        """Execute single code block 执行单个代码块"""
        # Record test start time 记录测试开始时间
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
        except Exception as e:
            print(f"❌ Execution error at line {block['line']}: {e} 第{block['line']}行执行错误: {e}")
    
    def execute_cpp(self, code, line_number):
        """执行C++代码 - 使用GCC编译器"""
        cpp_code = code[4:]  # 去掉'cpp.'前缀
    
        # 如果是简单的单行printf，用现有逻辑（更快）
        if (cpp_code.strip().startswith('printf(') and 
            cpp_code.count(',') <= 1 and
            '<<' not in cpp_code and
            'cout' not in cpp_code):
            content = cpp_code[7:-1].replace('\\n', '\n')
            result = self._parse_printf_ultimate(content)
            print(result, end='')
            return
    
        # 其他C++代码，用GCC编译器
        self.gcc_compiler.compile_and_execute(cpp_code, line_number)

    def _wrap_cpp_code(self, code):
        """包装C++代码，添加必要的头文件和main函数"""
        return f"""
    #include <iostream>
    #include <vector>
    #include <string>
    #include <map>
    using namespace std;

    // 用户代码开始
    {code}
    // 用户代码结束

    int main() {{
        // 如果是表达式，输出结果
        // 如果是语句，直接执行
        return 0;
    }}
    """
    
    def _parse_printf_ultimate(self, content):
        """修复版printf解析 - 方案二"""
        # 基本清理
        content = content.strip()
    
        # 提取格式字符串
        if content.startswith('"'):
            end_quote = content.find('"', 1)
            if end_quote != -1:
                format_str = content[1:end_quote]
                params_str = content[end_quote+1:].lstrip()

                # 如果有逗号，处理参数
                if params_str.startswith(','):
                    params_str = params_str[1:].strip()
                    # 简单分割参数（假设没有嵌套逗号）
                    params = [p.strip() for p in params_str.split(',')]
                
                    # 替换格式符
                    result = format_str
                    for param in params:
                        value = self._evaluate_expression_simple(param)
                        if '%s' in result:
                            result = result.replace('%s', str(value), 1)
                
                return result
            
            return format_str
    
        return content

    def _evaluate_expression_simple(self, expr):
        """简化版表达式评估"""
        expr = expr.strip()
    
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
                return eval(expr)
            elif expr.startswith('{') and expr.endswith('}'):
                return eval(expr)
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
        """Execute Python code - Enhanced version 执行Python代码 - 增强版"""
        # Create execution environment 创建执行环境
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
        
        # Add variables and functions 添加变量和函数
        env.update(self.variables)
        env.update(self.functions)
        
        try:
            # Execute code 执行代码
            exec(code, env)
            
            # Update variables and functions 更新变量和函数
            for key, value in env.items():
                if key not in ['math', 'random', 'datetime', 'time', 'print', '__builtins__', 'vars', 'globals', 'locals']:
                    if callable(value):
                        self.functions[key] = value
                    else:
                        self.variables[key] = value
                        
        except Exception as e:
            raise Exception(f"Python error: {e} Python错误: {e}")
    
    def execute_javascript(self, code, line_number):
        """Execute JavaScript code 执行JavaScript代码"""
        print(f"[JS] {code}")

def main():
    if len(sys.argv) != 2:
        print("Usage: lf-run-ultimate-fixed.py <file.lsf> 用法: lf-run-ultimate-fixed.py <file.lsf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith('.lsf'):
        print("Error: Requires .lsf file 错误：需要 .lsf 文件")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: File not found {input_file} 错误：文件不存在 {input_file}")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lsf_data = json.load(f)
    except Exception as e:
        print(f"Read failed: {e} 读取失败: {e}")
        sys.exit(1)
    
    runtime = UltimateLFRuntime()
    runtime.execute(lsf_data['program'])

class GCCCompiler:
    def __init__(self):
        self.gcc_path = self._find_gcc()
        self.supported = self.gcc_path is not None
    
    def _find_gcc(self):
        """查找系统GCC编译器"""
        # 在Windows上可能是gcc.exe, 在Linux/macOS上是gcc
        possible_names = ['gcc', 'gcc.exe', 'g++', 'g++.exe']
        
        for name in possible_names:
            path = shutil.which(name)
            if path:
                print(f"✅ 找到GCC编译器: {path}")
                return path
        
        # 如果没找到，检查常见安装位置
        common_paths = [
            "C:\\MinGW\\bin\\gcc.exe",
            "C:\\msys64\\mingw64\\bin\\gcc.exe", 
            "C:\\Program Files\\mingw-w64\\bin\\gcc.exe"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print(f"✅ 找到GCC编译器: {path}")
                return path
        
        print("❌ 未找到GCC编译器")
        print("💡 请安装: ")
        print("   Windows: MinGW-w64 或 MSYS2")
        print("   Linux: sudo apt-get install gcc g++")
        print("   macOS: brew install gcc")
        return None
    
    def compile_and_execute(self, cpp_code, line_number):
        """编译并执行C++代码"""
        if not self.supported:
            print(f"[C++] {cpp_code}  # GCC编译器未安装")
            return
        
        try:
            # 创建临时C++文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                wrapped_code = self._wrap_cpp_code(cpp_code)
                f.write(wrapped_code)
                temp_cpp_file = f.name
            
            # 创建临时可执行文件
            if os.name == 'nt':  # Windows
                temp_exe = temp_cpp_file.replace('.cpp', '.exe')
            else:  # Linux/macOS
                temp_exe = temp_cpp_file.replace('.cpp', '.out')
            
            # 编译命令
            compile_cmd = [
                self.gcc_path, 
                temp_cpp_file, 
                '-o', temp_exe,
                '-std=c++11',  # C++11标准
                '-O2',         # 优化级别
            ]
            
            # 编译
            result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True,
                timeout=10  # 编译超时
            )
            
            if result.returncode == 0:
                # 执行
                run_result = subprocess.run(
                    [temp_exe], 
                    capture_output=True, 
                    text=True,
                    timeout=5  # 运行超时
                )
                print(run_result.stdout, end='')
                if run_result.stderr:
                    print(f"C++ Runtime Warning: {run_result.stderr}")
            else:
                # 编译错误，提供友好信息
                error_msg = self._format_compile_error(result.stderr, line_number, cpp_code)
                print(error_msg)
            
            # 清理临时文件
            self._cleanup_temp_files(temp_cpp_file, temp_exe)
            
        except subprocess.TimeoutExpired:
            print(f"⏰ C++代码执行超时 (第{line_number}行)")
            self._cleanup_temp_files(temp_cpp_file, temp_exe)
        except Exception as e:
            print(f"❌ C++执行错误: {e}")
            self._cleanup_temp_files(temp_cpp_file, temp_exe)
    
    def _wrap_cpp_code(self, code):
        """包装C++代码，添加必要的头文件"""
        return f"""
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
using namespace std;

// 用户代码开始
{code}
// 用户代码结束

int main() {{
    // 执行用户代码
    return 0;
}}
"""
    
    def _format_compile_error(self, error_output, line_number, original_code):
        """格式化编译错误信息"""
        # 简化GCC的错误输出
        lines = error_output.split('\n')
        simplified_errors = []
        
        for line in lines:
            if 'error:' in line and 'temp_' not in line:
                # 移除临时文件路径信息
                clean_line = re.sub(r'/tmp/tmp\w+\.cpp', f'第{line_number}行', line)
                simplified_errors.append(clean_line)
        
        if simplified_errors:
            error_msg = '\n'.join(simplified_errors[:3])  # 只显示前3个错误
            return f"❌ C++编译错误:\n{error_msg}\n💡 代码: {original_code}"
        else:
            return f"❌ C++编译错误 (第{line_number}行): {original_code}"
    
    def _cleanup_temp_files(self, cpp_file, exe_file):
        """清理临时文件"""
        try:
            if os.path.exists(cpp_file):
                os.unlink(cpp_file)
            if os.path.exists(exe_file):
                os.unlink(exe_file)
        except:
            pass  # 忽略清理错误

if __name__ == "__main__":
    main()