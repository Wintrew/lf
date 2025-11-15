#!/usr/bin/env python3
"""
LF Compiler - Final Version 多语言融合编译器 - 最终版
Properly handles multi-line Python code 正确处理多行Python代码
"""

import sys
import os
import json
import hashlib

def parse_lf_source(source_code):
    """Parse LF source file - correctly handles multi-line code 解析LF源文件 - 正确处理多行代码"""
    lines = source_code.split('\n')
    directives = {}
    code_blocks = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments 跳过空行和注释
        if not line or line.startswith('//'):
            i += 1
            continue
            
        # Parse directives 解析指令
        if line.startswith('#'):
            parts = line[1:].split(' ', 1)
            if len(parts) == 2:
                directive, value = parts[0], parts[1].strip('"\'')
                directives.setdefault(directive, []).append({
                    'value': value,
                    'line': i + 1
                })
            i += 1
            continue
        
        # Check if it's a code line 检查是否是代码行
        raw_line = lines[i]  # Keep original line (with indentation) 保留原始行（包含缩进）
        
        # Check if starts with cpp. py. js. 检查是否以 cpp. py. js. 开头
        if raw_line.lstrip().startswith('cpp.'):
            content = raw_line.lstrip()[4:]  # Remove 'cpp.' 去掉 'cpp.'
            code_blocks.append({
                'line': i + 1,
                'type': 'cpp',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('py.'):
            content = raw_line.lstrip()[3:]  # Remove 'py.' 去掉 'py.'
            
            # Check if it's a function definition 检查是否是函数定义
            if content.strip().startswith('def ') and content.strip().endswith(':'):
                # This is a function definition, need to capture multiple lines 这是一个函数定义，需要捕获多行
                full_content = content
                base_indent = len(raw_line) - len(raw_line.lstrip())
                
                # Find function body end 查找函数体结束
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if not next_line.strip() or next_line.strip().startswith('//'):
                        j += 1
                        continue
                        
                    next_indent = len(next_line) - len(next_line.lstrip())
                    
                    # If indentation <= base indentation, function ends 如果缩进小于等于基础缩进，说明函数结束
                    if next_indent <= base_indent and next_line.strip():
                        break
                    
                    # If next line also starts with py., add to content 如果下一行也是py.开头，添加到内容中
                    if next_line.lstrip().startswith('py.'):
                        full_content += '\n' + next_line.lstrip()[3:]
                    else:
                        # Regular Python code line 普通Python代码行
                        full_content += '\n' + next_line[base_indent:]
                    
                    j += 1
                
                code_blocks.append({
                    'line': i + 1,
                    'type': 'py',
                    'content': full_content
                })
                i = j  # Skip processed lines 跳过已处理的行
            else:
                # Single line Python code 单行Python代码
                code_blocks.append({
                    'line': i + 1,
                    'type': 'py',
                    'content': content
                })
                i += 1
                
        elif raw_line.lstrip().startswith('js.'):
            content = raw_line.lstrip()[3:]  # Remove 'js.' 去掉 'js.'
            code_blocks.append({
                'line': i + 1,
                'type': 'js',
                'content': content
            })
            i += 1
            
        else:
            # Unrecognized code 无法识别的代码
            if line and not line.startswith('/*'):
                print(f"⚠️  Unparseable line {i+1}: {line} 无法解析第{i+1}行: {line}")
            i += 1
    
    return {
        'directives': directives,
        'code_blocks': code_blocks,
        'source_hash': hashlib.md5(source_code.encode()).hexdigest()[:8]
    }

def generate_lsf(parsed_data, source_file):
    """Generate LSF file 生成LSF文件"""
    return {
        'format_version': 'LSF-1.0',
        'metadata': {
            'compiler': 'lf-compile-final',
            'source_file': os.path.basename(source_file)
        },
        'program': parsed_data
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: lf-compile-final.py <input.lf> 用法: lf-compile-final.py <input.lf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith('.lf'):
        print("Error: Requires .lf file 错误：需要 .lf 文件")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: File not found {input_file} 错误：文件不存在 {input_file}")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Read failed: {e} 读取失败: {e}")
        sys.exit(1)
    
    print(f"Compiling {input_file}... 编译 {input_file}...")
    parsed_data = parse_lf_source(source_code)
    lsf_content = generate_lsf(parsed_data, input_file)
    
    output_file = input_file.replace('.lf', '.lsf')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(lsf_content, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {output_file} 生成 {output_file}")
        print(f"Directives: {len(parsed_data['directives'])} 指令: {len(parsed_data['directives'])}")
        print(f"Code blocks: {len(parsed_data['code_blocks'])} 代码块: {len(parsed_data['code_blocks'])}")
        
        # Show code block details 显示代码块详情
        for block in parsed_data['code_blocks']:
            print(f"  {block['type']}: {block['content'][:50]}...")
        
    except Exception as e:
        print(f"Write failed: {e} 写入失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()