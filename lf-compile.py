#!/usr/bin/env python3
"""
LF Compiler - Optimized Version with Packaging
Properly handles multi-line Python code and creates compressed packages
"""

import sys
import os
import json
import hashlib
import zipfile
import tempfile

def parse_lf_source(source_code):
    """Parse LF source file - correctly handles multi-line code 解果lf源文件 - 正确处理多行代码"""
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
                directive, value = parts[0], parts[1]
                # Extract content within quotes if present 提取引号内的内容（如果存在）
                if value.startswith('"') or value.startswith("'"):
                    quote_char = value[0]
                    end_quote = value.find(quote_char, 1)
                    if end_quote != -1:
                        value = value[1:end_quote]
                else:
                    # If no quotes, remove comments and trailing whitespace
                    # 如果没有引号，移除注释和尾随空格
                    comment_pos = value.find('/')
                    if comment_pos != -1:
                        value = value[:comment_pos].strip()
                    else:
                        value = value.strip()
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
            
            # Check if it's a function definition or other multi-line structure
            # 检查是否是函数定义或其他多行结构
            content_stripped = content.strip()
            is_multiline_structure = (
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
            
            if is_multiline_structure:
                # This is a multi-line structure, need to capture multiple lines
                # 这是一个多行结构，需要捕获多行
                full_content = content
                base_indent = len(raw_line) - len(raw_line.lstrip())
                
                # Find structure body end 查找结构体结束
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if not next_line.strip() or next_line.strip().startswith('//'):
                        j += 1
                        continue
                        
                    next_indent = len(next_line) - len(next_line.lstrip())
                    
                    # If indentation <= base indentation, structure ends
                    # 如果缩进小于等于基础缩进，说明结构结束
                    if next_indent <= base_indent and next_line.strip():
                        break
                    
                    # If next line also starts with py., add to content
                    # 如果下一行也是py.开头，添加到内容中
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
            
        elif raw_line.lstrip().startswith('java.'):
            content = raw_line.lstrip()[5:]  # Remove 'java.' 去掉 'java.'
            code_blocks.append({
                'line': i + 1,
                'type': 'java',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('php.'):
            content = raw_line.lstrip()[4:]  # Remove 'php.' 去掉 'php.'
            code_blocks.append({
                'line': i + 1,
                'type': 'php',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('rust.'):
            content = raw_line.lstrip()[5:]  # Remove 'rust.' 去掉 'rust.'
            code_blocks.append({
                'line': i + 1,
                'type': 'rust',
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
    """Generate LSF file"""
    return {
        'format_version': 'LSF-1.0',
        'metadata': {
            'compiler': 'lf-compile-optimized',
            'source_file': os.path.basename(source_file)
        },
        'program': parsed_data
    }


def create_package(parsed_data, source_file, lsf_content):
    """Create a package with source files for each language"""
    # Create a temporary directory for source files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create source files for each language
        source_files = []
        
        # Create C files
        c_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'cpp']
        if c_files:
            c_content = '\n'.join([block['content'] for block in c_files])
            c_file_path = os.path.join(temp_dir, 'code.c')
            with open(c_file_path, 'w', encoding='utf-8') as f:
                f.write(c_content)
            source_files.append(('code.c', c_content))
        
        # Create Python files
        py_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'py']
        if py_files:
            py_content = '\n'.join([block['content'] for block in py_files])
            py_file_path = os.path.join(temp_dir, 'code.py')
            with open(py_file_path, 'w', encoding='utf-8') as f:
                f.write(py_content)
            source_files.append(('code.py', py_content))
        
        # Create JavaScript files
        js_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'js']
        if js_files:
            js_content = '\n'.join([block['content'] for block in js_files])
            js_file_path = os.path.join(temp_dir, 'code.js')
            with open(js_file_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            source_files.append(('code.js', js_content))
        
        # Create Java files
        java_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'java']
        if java_files:
            java_content = '\n'.join([block['content'] for block in java_files])
            java_file_path = os.path.join(temp_dir, 'code.java')
            with open(java_file_path, 'w', encoding='utf-8') as f:
                f.write(java_content)
            source_files.append(('code.java', java_content))
        
        # Create PHP files
        php_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'php']
        if php_files:
            php_content = '\n'.join([block['content'] for block in php_files])
            php_file_path = os.path.join(temp_dir, 'code.php')
            with open(php_file_path, 'w', encoding='utf-8') as f:
                f.write(php_content)
            source_files.append(('code.php', php_content))
        
        # Create Rust files
        rust_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'rust']
        if rust_files:
            rust_content = '\n'.join([block['content'] for block in rust_files])
            rust_file_path = os.path.join(temp_dir, 'code.rs')
            with open(rust_file_path, 'w', encoding='utf-8') as f:
                f.write(rust_content)
            source_files.append(('code.rs', rust_content))
        
        # Create manifest file
        manifest = {
            'format_version': 'LF-Package-1.0',
            'metadata': {
                'compiler': 'lf-compile-optimized',
                'source_file': os.path.basename(source_file),
                'source_hash': parsed_data['source_hash']
            },
            'files': [{'name': name, 'type': name.split('.')[-1]} for name, _ in source_files],
            'execution_order': [{'type': block['type'], 'file': f"code.{block['type'] if block['type'] not in ['cpp', 'rust'] else ('c' if block['type'] == 'cpp' else 'rs')}"} 
                               for block in parsed_data['code_blocks']]
        }
        
        manifest_path = os.path.join(temp_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        # Create zip package
        package_file = source_file.replace('.lf', '.lfp')  # LF Package format
        with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add source files
            for name, content in source_files:
                zipf.writestr(name, content)
            
            # Add manifest
            zipf.write(manifest_path, 'manifest.json')
            
            # Add original LSF file
            lsf_path = os.path.join(temp_dir, 'program.lsf')
            with open(lsf_path, 'w', encoding='utf-8') as f:
                json.dump(lsf_content, f, indent=2, ensure_ascii=False)
            zipf.write(lsf_path, 'program.lsf')
        
        return package_file

def main():
    if len(sys.argv) != 2:
        print("Usage: lf-compile.py <input.lf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith('.lf'):
        print("Error: Requires .lf file")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: File not found {input_file}")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Read failed: {e}")
        sys.exit(1)
    
    print(f"Compiling {input_file}...")
    parsed_data = parse_lf_source(source_code)
    lsf_content = generate_lsf(parsed_data, input_file)
    
    # Generate LSF file
    output_file = input_file.replace('.lf', '.lsf')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(lsf_content, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {output_file}")
    except Exception as e:
        print(f"Write failed: {e}")
        sys.exit(1)
    
    # Create package
    try:
        package_file = create_package(parsed_data, input_file, lsf_content)
        print(f"✅ Generated package {package_file}")
        print(f"Directives: {len(parsed_data['directives'])}")
        print(f"Code blocks: {len(parsed_data['code_blocks'])}")
        
        # Show code block details
        for block in parsed_data['code_blocks']:
            print(f"  {block['type']}: {block['content'][:50]}...")
    except Exception as e:
        print(f"Package creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()