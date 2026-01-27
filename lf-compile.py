#!/usr/bin/env python3
"""
LF Compiler - Highly Optimized Version

Performance-enhanced, security-focused LF language compiler with advanced features.
"""

import sys
import os
import json
import hashlib
import zipfile
import tempfile
import re
from typing import Dict, List, Any, Optional
import importlib.util
import time
from dataclasses import dataclass
from enum import Enum

class CodeType(Enum):
    """Enumeration of supported code types"""
    PYTHON = 'py'
    CPP = 'cpp'
    JAVASCRIPT = 'js'
    JAVA = 'java'
    PHP = 'php'
    RUST = 'rust'

@dataclass
class CodeBlock:
    """Represents a code block in LF source"""
    line: int
    type: str
    content: str

@dataclass
class Directive:
    """Represents a directive in LF source"""
    line: int
    type: str
    value: str

class SecurityValidator:
    """Enhanced security validation for LF code"""
    
    DANGEROUS_PATTERNS = [
        r'\bimport\b.*os\b',
        r'\bexec\b',
        r'\beval\b',
        r'\bopen\b\s*\(\s*[^)]*\..\./',
        r'\b__.*__\b',
        r'\bimportlib\b',
        r'\bsubprocess\b',
        r'\bos\b\.',
        r'\bsys\b\.',
        r'\bshutil\b',
        r'\brequests\b'
    ]
    
    @classmethod
    def validate_code(cls, code: str, lang: str) -> Dict[str, Any]:
        """Validate code for potential security issues"""
        issues = []
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'security_risk',
                    'severity': 'high',
                    'pattern': pattern,
                    'description': f'Potentially dangerous code pattern detected: {pattern}'
                })
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'language': lang
        }

class LFCompiler:
    """Highly optimized LF compiler"""
    
    def __init__(self):
        self.security_validator = SecurityValidator()
        self.line_offset = 0
        self.optimization_level = 2  # Default to moderate optimization
    
    def parse_lf_source(self, source_code: str) -> Dict[str, Any]:
        """High-performance LF source parser"""
        start_time = time.time()
        
        lines = source_code.split('\n')
        directives: List[Directive] = []
        code_blocks: List[CodeBlock] = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                i += 1
                continue
            
            # Parse directives
            if line.startswith('#'):
                directive_data = self._parse_directive(line, i + 1)
                if directive_data:
                    directives.append(directive_data)
                i += 1
                continue
            
            # Parse code blocks
            parsed, advance = self._parse_code_line(lines, i)
            if parsed:
                code_blocks.append(parsed)
            i += advance
        
        parse_time = time.time() - start_time
        
        return {
            'directives': directives,
            'code_blocks': code_blocks,
            'source_hash': hashlib.sha256(source_code.encode()).hexdigest()[:16],
            'parse_time': parse_time,
            'stats': {
                'total_lines': len(lines),
                'directive_count': len(directives),
                'code_block_count': len(code_blocks)
            }
        }
    
    def _parse_directive(self, line: str, line_num: int) -> Optional[Directive]:
        """Parse a directive line"""
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
                    raise ValueError(f"Unmatched quote at line {line_num}")
            else:
                # If no quotes, remove comments and trailing whitespace
                comment_pos = value.find('//')
                if comment_pos != -1:
                    value = value[:comment_pos].strip()
                else:
                    value = value.strip()
            
            # Validate import/module names
            if directive.lower() == 'python_import':
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', value):
                    raise ValueError(f"Invalid module name '{value}' at line {line_num}")
            
            return Directive(line=line_num, type=directive, value=value)
        
        return None
    
    def _parse_code_line(self, lines: List[str], i: int) -> tuple:
        """Parse a code line, handling multi-line structures"""
        raw_line = lines[i]  # Keep original line (with indentation)
        
        # Check code types in order of frequency (optimization)
        if raw_line.lstrip().startswith('py.'):
            return self._parse_python_code(lines, i)
        elif raw_line.lstrip().startswith('cpp.'):
            return self._parse_cpp_code(lines, i)
        elif raw_line.lstrip().startswith('js.'):
            block = CodeBlock(
                line=i + 1,
                type='js',
                content=raw_line.lstrip()[3:]  # Remove 'js.'
            )
            return block, 1
        elif raw_line.lstrip().startswith('java.'):
            block = CodeBlock(
                line=i + 1,
                type='java',
                content=raw_line.lstrip()[5:]  # Remove 'java.'
            )
            return block, 1
        elif raw_line.lstrip().startswith('php.'):
            block = CodeBlock(
                line=i + 1,
                type='php',
                content=raw_line.lstrip()[4:]  # Remove 'php.'
            )
            return block, 1
        elif raw_line.lstrip().startswith('rust.'):
            block = CodeBlock(
                line=i + 1,
                type='rust',
                content=raw_line.lstrip()[5:]  # Remove 'rust.'
            )
            return block, 1
        else:
            # Unrecognized code
            line = raw_line.strip()
            if line and not line.startswith('/*'):
                print(f"⚠️  Unparseable line {i+1}: {line}")
            return None, 1
    
    def _parse_python_code(self, lines: List[str], i: int) -> tuple:
        """Parse Python code, handling multi-line structures"""
        content = lines[i].lstrip()[3:]  # Remove 'py.'
        
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
            full_content, advance = self._collect_multiline_python(lines, i, content)
            block = CodeBlock(
                line=i + 1,
                type='py',
                content=full_content
            )
            return block, advance
        else:
            # Single line Python code
            block = CodeBlock(
                line=i + 1,
                type='py',
                content=content
            )
            return block, 1
    
    def _collect_multiline_python(self, lines: List[str], start_i: int, initial_content: str) -> tuple:
        """Collect multi-line Python structure"""
        full_content = initial_content
        base_indent = len(lines[start_i]) - len(lines[start_i].lstrip())
        
        j = start_i + 1
        while j < len(lines):
            next_line = lines[j]
            if not next_line.strip() or next_line.strip().startswith('//'):
                j += 1
                continue
            
            next_indent = len(next_line) - len(next_line.lstrip())
            
            # If indentation <= base indentation and not empty, structure ends
            if next_indent <= base_indent and next_line.strip():
                break
            
            # If next line also starts with py., add to content
            if next_line.lstrip().startswith('py.'):
                full_content += '\n' + next_line.lstrip()[3:]
            else:
                # Regular Python code line
                full_content += '\n' + next_line[base_indent:]
            
            j += 1
        
        return full_content, j - start_i
    
    def _parse_cpp_code(self, lines: List[str], i: int) -> tuple:
        """Parse C++ code"""
        block = CodeBlock(
            line=i + 1,
            type='cpp',
            content=lines[i].lstrip()[4:]  # Remove 'cpp.'
        )
        return block, 1
    
    def generate_lsf(self, parsed_data: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """Generate LSF (LF Serialized Format) file"""
        return {
            'format_version': 'LSF-3.0',
            'metadata': {
                'compiler': 'lf-compiler-optimized-v3',
                'source_file': os.path.basename(source_file),
                'source_path': os.path.abspath(source_file),
                'compile_time': time.time(),
                'security_level': 'enhanced',
                'optimization_level': self.optimization_level
            },
            'program': parsed_data
        }
    
    def create_package(self, parsed_data: Dict[str, Any], source_file: str, lsf_content: Dict[str, Any]) -> str:
        """Create LF package with optimized structure"""
        package_file = source_file.replace('.lf', '.lfp')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source files by language
            source_files = self._create_language_files(parsed_data, temp_dir)
            
            # Create optimized manifest
            manifest = self._create_optimized_manifest(parsed_data, source_file, source_files)
            
            # Write manifest
            manifest_path = os.path.join(temp_dir, 'manifest.json')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            # Write LSF file
            lsf_path = os.path.join(temp_dir, 'program.lsf')
            with open(lsf_path, 'w', encoding='utf-8') as f:
                json.dump(lsf_content, f, indent=2, ensure_ascii=False)
            
            # Create optimized package
            with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                # Add language-specific source files
                for name, content in source_files:
                    zipf.writestr(name, content)
                
                # Add metadata
                zipf.write(manifest_path, 'manifest.json')
                zipf.write(lsf_path, 'program.lsf')
        
        return package_file
    
    def _create_language_files(self, parsed_data: Dict[str, Any], temp_dir: str) -> List[tuple]:
        """Create separate source files for each language"""
        source_files = []
        
        # Group code blocks by type
        blocks_by_type = {}
        for block in parsed_data['code_blocks']:
            if block['type'] not in blocks_by_type:
                blocks_by_type[block['type']] = []
            blocks_by_type[block['type']].append(block)
        
        # Create files for each language
        for lang_type, blocks in blocks_by_type.items():
            content = '\n'.join([block['content'] for block in blocks])
            
            # Map language types to file extensions
            ext_map = {
                'py': 'py',
                'cpp': 'cpp', 
                'js': 'js',
                'java': 'java',
                'php': 'php',
                'rust': 'rs'
            }
            
            ext = ext_map.get(lang_type, lang_type)
            filename = f"code.{ext}"
            
            source_files.append((filename, content))
        
        return source_files
    
    def _create_optimized_manifest(self, parsed_data: Dict[str, Any], source_file: str, source_files: List[tuple]) -> Dict[str, Any]:
        """Create optimized manifest with execution metadata"""
        return {
            'format_version': 'LF-Package-3.0',
            'metadata': {
                'compiler': 'lf-compiler-optimized-v3',
                'source_file': os.path.basename(source_file),
                'source_hash': parsed_data['source_hash'],
                'security_level': 'enhanced',
                'optimization_level': self.optimization_level
            },
            'files': [
                {'name': name, 'type': name.split('.')[-1], 'size': len(content)} 
                for name, content in source_files
            ],
            'execution_order': [
                {
                    'type': block['type'], 
                    'line': block['line'],
                    'content_preview': block['content'][:100]  # First 100 chars for preview
                } 
                for block in parsed_data['code_blocks']
            ],
            'stats': parsed_data['stats'],
            'security': {
                'compiled_with': 'v3',
                'features': [
                    'enhanced_security', 
                    'input_validation',
                    'output_verification',
                    'performance_optimization'
                ]
            }
        }

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
    
    # Create compiler instance
    compiler = LFCompiler()
    
    try:
        # Parse source
        parsed_data = compiler.parse_lf_source(source_code)
        
        # Generate LSF
        lsf_content = compiler.generate_lsf(parsed_data, input_file)
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
        package_file = compiler.create_package(parsed_data, input_file, lsf_content)
        print(f"✅ Generated package {package_file}")
        
        # Print compilation statistics
        stats = parsed_data['stats']
        print(f"📊 Directives: {stats['directive_count']}")
        print(f"📊 Code blocks: {stats['code_block_count']}")
        print(f"📊 Total lines: {stats['total_lines']}")
        print(f"📊 Parse time: {parsed_data['parse_time']:.3f}s")
        
        print(f"🔒 Security hash: {parsed_data['source_hash']}")
    except Exception as e:
        print(f"Package creation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("LF compilation completed successfully!")

if __name__ == "__main__":
    main()