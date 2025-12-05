#!/usr/bin/env python3
"""
LF Compiler - Optimized Version with Packaging

Properly handles multi-line Python code and creates compressed packages
Security-enhanced and performance optimized version
"""

import sys
import os
import json
import hashlib
import zipfile
import tempfile
import re
from typing import Dict, List, Any, Tuple, Optional
import secrets
import importlib.util

def sanitize_input(text: str) -> str:
    """Sanitize input to prevent code injection"""
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'\bimport\b.*os\b', 
        r'\bexec\b', 
        r'\beval\b', 
        r'\bopen\b\s*\(\s*[^)]*\.\./',
        r'\b__.*__\b', 
        r'\bimportlib\b',
        r'\bsubprocess\b',
        r'\bos\b\.',
        r'\bsys\b\.',
        r'\bshutil\b',
        r'\brequests\b'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError(f"Potentially dangerous code pattern detected: {pattern}")
    
    return text

def parse_lf_source(source_code: str) -> Dict[str, Any]:
    """Parse LF source file - correctly handles multi-line code with security validation
    
    Args:
        source_code: The LF source code to parse
        
    Returns:
        A dictionary containing directives, code_blocks, and source_hash
    """
    # Sanitize input
    sanitized_code = sanitize_input(source_code)
    lines = sanitized_code.split('\n')
    directives: Dict[str, List[Dict[str, Any]]] = {}
    code_blocks: List[Dict[str, Any]] = []
    
    # Load security module if available
    security_module = None
    try:
        spec = importlib.util.spec_from_file_location("lf_security", "lf-security.py")
        if spec and spec.loader:
            security_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(security_module)
            security_checker = security_module.LFSecurity()
        else:
            print("⚠️  Security module not found, proceeding without enhanced security checks")
    except FileNotFoundError:
        print("⚠️  Security module not found, proceeding without enhanced security checks")
    except Exception as e:
        print(f"⚠️  Error loading security module: {e}")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('//'):
            i += 1
            continue
            
        # Parse directives
        if line.startswith('#'):
            parts = line[1:].split(' ', 1)
            
            if len(parts) == 2:
                directive, value = parts[0], parts[1]
                
                # Extract content within quotes if present
                if value.startswith('"') or value.startswith("'"):
                    quote_char = value[0]
                    end_quote = value.find(quote_char, 1)
                    
                    if end_quote != -1:
                        value = value[1:end_quote]
                    else:
                        raise ValueError(f"Unmatched quote at line {i+1}")
                else:
                    # If no quotes, remove comments and trailing whitespace
                    comment_pos = value.find('//')
                    if comment_pos != -1:
                        value = value[:comment_pos].strip()
                    else:
                        value = value.strip()
                
                # Security check for directive values
                if directive.lower() in ['python_import', 'name', 'author', 'description']:
                    # Validate import/module names
                    if directive.lower() == 'python_import':
                        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', value):
                            raise ValueError(f"Invalid module name '{value}' at line {i+1}")
                    
                    directives.setdefault(directive, []).append({
                        'value': value,
                        'line': i + 1
                    })
            i += 1
            continue
        
        # Check if it's a code line
        raw_line = lines[i]  # Keep original line (with indentation)
        
        # Check if starts with cpp. py. js. etc.
        if raw_line.lstrip().startswith('cpp.'):
            content = raw_line.lstrip()[4:]  # Remove 'cpp.'
            # Perform security check if module is loaded
            if security_module:
                validation_result = security_checker.validate_code(content, 'cpp')
                if not validation_result['is_valid']:
                    print(f"⚠️  Security warning for C++ code at line {i+1}:")
                    for issue in validation_result['issues']:
                        print(f"   - {issue['type']} (severity: {issue['severity']})")
            code_blocks.append({
                'line': i + 1,
                'type': 'cpp',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('py.'):
            content = raw_line.lstrip()[3:]  # Remove 'py.'
            
            # Check if it's a function definition or other multi-line structure
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
                full_content = content
                base_indent = len(raw_line) - len(raw_line.lstrip())
                
                # Find structure body end
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    if not next_line.strip() or next_line.strip().startswith('//'):
                        j += 1
                        continue
                        
                    next_indent = len(next_line) - len(next_line.lstrip())
                    
                    # If indentation <= base indentation, structure ends
                    if next_indent <= base_indent and next_line.strip():
                        break
                    
                    # If next line also starts with py., add to content
                    if next_line.lstrip().startswith('py.'):
                        full_content += '\n' + next_line.lstrip()[3:]
                    else:
                        # Regular Python code line
                        full_content += '\n' + next_line[base_indent:]
                    
                    j += 1
                
                # Perform security check if module is loaded
                if security_module:
                    validation_result = security_checker.validate_code(full_content, 'py')
                    if not validation_result['is_valid']:
                        print(f"⚠️  Security warning for Python code at line {i+1}:")
                        for issue in validation_result['issues']:
                            print(f"   - {issue['type']} (severity: {issue['severity']})")
                
                code_blocks.append({
                    'line': i + 1,
                    'type': 'py',
                    'content': full_content
                })
                i = j  # Skip processed lines
            else:
                # Perform security check if module is loaded
                if security_module:
                    validation_result = security_checker.validate_code(content, 'py')
                    if not validation_result['is_valid']:
                        print(f"⚠️  Security warning for Python code at line {i+1}:")
                        for issue in validation_result['issues']:
                            print(f"   - {issue['type']} (severity: {issue['severity']})")
                
                # Single line Python code
                code_blocks.append({
                    'line': i + 1,
                    'type': 'py',
                    'content': content
                })
                i += 1
                
        elif raw_line.lstrip().startswith('js.'):
            content = raw_line.lstrip()[3:]  # Remove 'js.'
            # Perform security check if module is loaded
            if security_module:
                validation_result = security_checker.validate_code(content, 'js')
                if not validation_result['is_valid']:
                    print(f"⚠️  Security warning for JavaScript code at line {i+1}:")
                    for issue in validation_result['issues']:
                        print(f"   - {issue['type']} (severity: {issue['severity']})")
            code_blocks.append({
                'line': i + 1,
                'type': 'js',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('java.'):
            content = raw_line.lstrip()[5:]  # Remove 'java.'
            code_blocks.append({
                'line': i + 1,
                'type': 'java',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('php.'):
            content = raw_line.lstrip()[4:]  # Remove 'php.'
            code_blocks.append({
                'line': i + 1,
                'type': 'php',
                'content': content
            })
            i += 1
            
        elif raw_line.lstrip().startswith('rust.'):
            content = raw_line.lstrip()[5:]  # Remove 'rust.'
            code_blocks.append({
                'line': i + 1,
                'type': 'rust',
                'content': content
            })
            i += 1
            
        else:
            # Unrecognized code
            if line and not line.startswith('/*'):
                print(f"⚠️  Unparseable line {i+1}: {line}")
            i += 1
    
    return {
        'directives': directives,
        'code_blocks': code_blocks,
        'source_hash': hashlib.sha256(source_code.encode()).hexdigest()[:16]  # More secure hash
    }

def generate_lsf(parsed_data: Dict[str, Any], source_file: str) -> Dict[str, Any]:
    """Generate LSF file
    
    Args:
        parsed_data: The parsed LF source data
        source_file: Path to the source file
        
    Returns:
        LSF format dictionary
    """
    return {
        'format_version': 'LSF-2.0',  # Updated version
        'metadata': {
            'compiler': 'lf-compile-optimized-v2',
            'source_file': os.path.basename(source_file),
            'source_path': os.path.abspath(source_file),
            'compile_time': os.path.getmtime(source_file),
            'security_level': 'enhanced'
        },
        'program': parsed_data
    }

def create_package(parsed_data: Dict[str, Any], source_file: str, lsf_content: Dict[str, Any]) -> str:
    """Create a package with source files for each language
    
    Args:
        parsed_data: The parsed LF source data
        source_file: Path to the source file
        lsf_content: The LSF file content
        
    Returns:
        Path to the created package file
    """
    # Check if multi-file management is disabled
    if parsed_data.get('directives', {}).get('disable_multifile'):
        print("⚠️  Multi-file management is disabled by directive")
        # Create a minimal package with only the LSF file
        package_file = source_file.replace('.lf', '.lfp')  # LF Package format
        with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add only manifest and LSF file
            manifest = {
                'format_version': 'LF-Package-2.0',
                'metadata': {
                    'compiler': 'lf-compile-optimized',
                    'source_file': os.path.basename(source_file),
                    'source_hash': parsed_data['source_hash'],
                    'multifile_disabled': True,
                    'security_level': 'enhanced'
                },
                'files': [],
                'execution_order': [{'type': block['type'], 'content': block['content'], 'line': block['line']} 
                                   for block in parsed_data['code_blocks']],
                'security': {
                    'compiled_with': 'v2',
                    'features': ['enhanced_security', 'input_validation']
                }
            }
            
            # Add manifest
            zipf.writestr('manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
            
            # Add original LSF file
            zipf.writestr('program.lsf', json.dumps(lsf_content, indent=2, ensure_ascii=False))
        
        return package_file
    
    # Create a temporary directory for source files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create source files for each language
        source_files = []
        
        # Create C files
        c_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'cpp']
        if c_files:
            # Sanitize content
            c_content = sanitize_input('\n'.join([block['content'] for block in c_files]))
            c_file_path = os.path.join(temp_dir, 'code.c')
            with open(c_file_path, 'w', encoding='utf-8') as f:
                f.write(c_content)
            source_files.append(('code.c', c_content))
        
        # Create Python files
        py_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'py']
        if py_files:
            # Sanitize content
            py_content = sanitize_input('\n'.join([block['content'] for block in py_files]))
            py_file_path = os.path.join(temp_dir, 'code.py')
            with open(py_file_path, 'w', encoding='utf-8') as f:
                f.write(py_content)
            source_files.append(('code.py', py_content))
        
        # Create JavaScript files
        js_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'js']
        if js_files:
            js_content = sanitize_input('\n'.join([block['content'] for block in js_files]))
            js_file_path = os.path.join(temp_dir, 'code.js')
            with open(js_file_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            source_files.append(('code.js', js_content))
        
        # Create Java files
        java_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'java']
        if java_files:
            java_content = sanitize_input('\n'.join([block['content'] for block in java_files]))
            java_file_path = os.path.join(temp_dir, 'code.java')
            with open(java_file_path, 'w', encoding='utf-8') as f:
                f.write(java_content)
            source_files.append(('code.java', java_content))
        
        # Create PHP files
        php_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'php']
        if php_files:
            php_content = sanitize_input('\n'.join([block['content'] for block in php_files]))
            php_file_path = os.path.join(temp_dir, 'code.php')
            with open(php_file_path, 'w', encoding='utf-8') as f:
                f.write(php_content)
            source_files.append(('code.php', php_content))
        
        # Create Rust files
        rust_files = [block for block in parsed_data['code_blocks'] if block['type'] == 'rust']
        if rust_files:
            rust_content = sanitize_input('\n'.join([block['content'] for block in rust_files]))
            rust_file_path = os.path.join(temp_dir, 'code.rs')
            with open(rust_file_path, 'w', encoding='utf-8') as f:
                f.write(rust_content)
            source_files.append(('code.rs', rust_content))
        
        # Create manifest file
        manifest = {
            'format_version': 'LF-Package-2.0',
            'metadata': {
                'compiler': 'lf-compile-optimized-v2',
                'source_file': os.path.basename(source_file),
                'source_hash': parsed_data['source_hash'],
                'security_level': 'enhanced'
            },
            'files': [{'name': name, 'type': name.split('.')[-1], 'size': len(content)} for name, content in source_files],
            'execution_order': [{'type': block['type'], 'file': f"code.{block['type'] if block['type'] not in ['cpp', 'rust'] else ('c' if block['type'] == 'cpp' else 'rs')}", 'line': block['line']} 
                               for block in parsed_data['code_blocks']],
            'security': {
                'compiled_with': 'v2',
                'features': ['enhanced_security', 'input_validation', 'output_verification']
            }
        }
        
        manifest_path = os.path.join(temp_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        # Create zip package
        package_file = source_file.replace('.lf', '.lfp')  # LF Package format
        with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:  # Higher compression
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
    try:
        parsed_data = parse_lf_source(source_code)
        lsf_content = generate_lsf(parsed_data, input_file)
    except ValueError as e:
        print(f"Parse error: {e}")
        sys.exit(1)
    
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
        
        print(f"Security hash: {parsed_data['source_hash']}")
    except Exception as e:
        print(f"Package creation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()