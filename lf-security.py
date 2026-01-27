#!/usr/bin/env python3
"""
LF Security Module - Enhanced Security Validation for LF Language
Version: 3.0
Advanced security features for LF language code validation and protection.
"""

import re
import ast
import json
from typing import Dict, List, Any, Tuple
from enum import Enum

class SecurityLevel(Enum):
    """Security level enumeration"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    STRICT = 4

class SecurityIssueType(Enum):
    """Types of security issues"""
    DANGEROUS_IMPORT = "dangerous_import"
    CODE_EXECUTION = "code_execution"
    FILE_ACCESS = "file_access"
    NETWORK_ACCESS = "network_access"
    SYSTEM_ACCESS = "system_access"
    EVAL_USAGE = "eval_usage"
    FORMAT_STRING = "format_string"
    COMMAND_INJECTION = "command_injection"

class LFSecurity:
    """Enhanced security validation for LF language"""
    
    def __init__(self, level: SecurityLevel = SecurityLevel.HIGH):
        self.level = level
        self.dangerous_patterns = self._get_dangerous_patterns()
        self.security_issues = []    
    def _get_dangerous_patterns(self) -> Dict[str, List[str]]:
        """Get dangerous patterns based on security level"""
        patterns = {
            'imports': [
                r'\bimport\s+os\b',
                r'\bimport\s+sys\b',
                r'\bimport\s+subprocess\b',
                r'\bimport\s+shutil\b',
                r'\bimport\s+requests\b',
                r'\bimport\s+urllib\b',
                r'\bimport\s+socket\b',
                r'\bimport\s+ftplib\b',
                r'\bimport\s+telnetlib\b',
                r'\bimport\s+imaplib\b',
                r'\bimport\s+poplib\b',
                r'\bimportlib\b',
                r'\b__import__\b'
            ],
            'executions': [
                r'\bexec\b',
                r'\beval\b',
                r'\bcompile\b',
                r'\bexecfile\b'
            ],
            'file_access': [
                r'\bopen\s*\(',
                r'\bos\.path\b',
                r'\bshutil\b',
                r'\btempfile\b'
            ],
            'system_access': [
                r'\bos\.system\b',
                r'\bsubprocess\b',
                r'\bplatform\b',
                r'\benviron\b'
            ],
            'network_access': [
                r'\bsocket\b',
                r'\brequests\b',
                r'\burllib\b',
                r'\bhttplib\b',
                r'\bhttp\.client\b'
            ]
        }
        
        return patterns
    
    def validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code for security issues"""
        self.security_issues = []
        
        # Check for dangerous patterns
        self._check_dangerous_patterns(code, language)
        
        # Language-specific checks
        if language.lower() == 'py':
            self._validate_python_code(code)
        elif language.lower() == 'js':
            self._validate_javascript_code(code)
        elif language.lower() == 'java':
            self._validate_java_code(code)
        elif language.lower() == 'cpp':
            self._validate_cpp_code(code)
        elif language.lower() == 'php':
            self._validate_php_code(code)
        elif language.lower() == 'rust':
            self._validate_rust_code(code)
        
        return {
            'is_valid': len(self.security_issues) == 0,
            'issues': self.security_issues,
            'language': language,
            'security_level': self.level.name,
            'issue_count': len(self.security_issues)
        }
    
    def _check_dangerous_patterns(self, code: str, language: str):
        """Check for dangerous patterns in the code"""
        for category, patterns in self.dangerous_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    severity = self._get_severity_for_pattern(pattern)
                    self.security_issues.append({
                        'type': self._get_issue_type_for_pattern(pattern),
                        'severity': severity,
                        'pattern': pattern,
                        'description': f'Potential security risk detected: {pattern}',
                        'category': category,
                        'line_numbers': self._find_line_numbers(code, pattern)
                    })
    
    def _get_severity_for_pattern(self, pattern: str) -> str:
        """Get severity level for a pattern based on security level"""
        high_risk_patterns = [
            r'\bexec\b', r'\beval\b', r'\b__import__\b', r'\bimportlib\b'
        ]
        
        medium_risk_patterns = [
            r'\bsubprocess\b', r'\bos\.system\b', r'\bsocket\b', r'\brequests\b'
        ]
        
        if any(re.search(p, pattern) for p in high_risk_patterns):
            return 'high'
        elif any(re.search(p, pattern) for p in medium_risk_patterns):
            return 'medium'
        else:
            return 'low'
    
    def _get_issue_type_for_pattern(self, pattern: str) -> SecurityIssueType:
        """Get issue type for a pattern"""
        if 'exec' in pattern or 'eval' in pattern:
            return SecurityIssueType.EVAL_USAGE
        elif 'import' in pattern:
            return SecurityIssueType.DANGEROUS_IMPORT
        elif 'open' in pattern or 'shutil' in pattern:
            return SecurityIssueType.FILE_ACCESS
        elif 'socket' in pattern or 'requests' in pattern:
            return SecurityIssueType.NETWORK_ACCESS
        elif 'system' in pattern or 'subprocess' in pattern:
            return SecurityIssueType.SYSTEM_ACCESS
        else:
            return SecurityIssueType.CODE_EXECUTION
    
    def _find_line_numbers(self, code: str, pattern: str) -> List[int]:
        """Find line numbers where pattern occurs"""
        lines = code.split('\n')
        line_numbers = []
        
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                line_numbers.append(i)
        
        return line_numbers[:10]  # Return first 10 matches to avoid too much output
    
    def _validate_python_code(self, code: str):
        """Validate Python code for additional security issues"""
        try:
            # Parse AST to find more complex issues
            tree = ast.parse(code)
            
            # Walk through AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if self._is_dangerous_import(alias.name):
                            self.security_issues.append({
                                'type': SecurityIssueType.DANGEROUS_IMPORT,
                                'severity': 'high',
                                'pattern': alias.name,
                                'description': f'Dangerous import detected: {alias.name}',
                                'category': 'imports',
                                'line_numbers': [node.lineno]
                            })
                elif isinstance(node, ast.ImportFrom):
                    if self._is_dangerous_import(node.module):
                        self.security_issues.append({
                            'type': SecurityIssueType.DANGEROUS_IMPORT,
                            'severity': 'high',
                            'pattern': node.module,
                            'description': f'Dangerous import detected: {node.module}',
                            'category': 'imports',
                            'line_numbers': [node.lineno]
                        })
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['exec', 'eval', 'compile']:
                            self.security_issues.append({
                                'type': SecurityIssueType.EVAL_USAGE,
                                'severity': 'high',
                                'pattern': node.func.id,
                                'description': f'Dangerous function call: {node.func.id}',
                                'category': 'executions',
                                'line_numbers': [node.lineno]
                            })
        except SyntaxError:
            # If code has syntax errors, it can't be properly validated
            self.security_issues.append({
                'type': SecurityIssueType.CODE_EXECUTION,
                'severity': 'medium',
                'pattern': 'syntax_error',
                'description': 'Code contains syntax errors and cannot be properly validated',
                'category': 'parsing',
                'line_numbers': []
            })
    
    def _is_dangerous_import(self, module_name: str) -> bool:
        """Check if import is dangerous"""
        dangerous_modules = [
            'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests', 
            'urllib', 'urllib2', 'httplib', 'http.client', 'ftplib', 
            'telnetlib', 'imaplib', 'poplib', 'pickle', 'dill', 'marshal'
        ]
        
        # Check exact matches or modules that start with dangerous names
        for dangerous in dangerous_modules:
            if module_name.startswith(dangerous):
                return True
        return False
    
    def _validate_javascript_code(self, code: str):
        """Validate JavaScript code for security issues"""
        # Check for dangerous JavaScript patterns
        js_dangerous_patterns = [
            r'eval\s*\(',
            r'Function\s*\(',
            r'import\(',  # Dynamic imports
            r'XMLHttpRequest',
            r'fetch\s*\(',
            r'WebSocket',
            r'ActiveXObject',  # IE-specific
        ]
        
        for pattern in js_dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                self.security_issues.append({
                    'type': SecurityIssueType.CODE_EXECUTION,
                    'severity': 'high' if 'eval' in pattern or 'Function' in pattern else 'medium',
                    'pattern': pattern,
                    'description': f'Dangerous JavaScript pattern detected: {pattern}',
                    'category': 'javascript',
                    'line_numbers': self._find_line_numbers(code, pattern)
                })
    
    def _validate_java_code(self, code: str):
        """Validate Java code for security issues"""
        # Check for dangerous Java patterns
        java_dangerous_patterns = [
            r'Runtime\.getRuntime\(\)',
            r'ProcessBuilder',
            r'FileInputStream',
            r'FileOutputStream',
            r'URL\(',
            r'URLConnection',
            r'Socket\(',
            r'ServerSocket\(',
        ]
        
        for pattern in java_dangerous_patterns:
            if re.search(pattern, code):
                self.security_issues.append({
                    'type': SecurityIssueType.CODE_EXECUTION,
                    'severity': 'high' if 'Runtime' in pattern or 'ProcessBuilder' in pattern else 'medium',
                    'pattern': pattern,
                    'description': f'Dangerous Java pattern detected: {pattern}',
                    'category': 'java',
                    'line_numbers': self._find_line_numbers(code, pattern)
                })
    
    def _validate_cpp_code(self, code: str):
        """Validate C++ code for security issues"""
        # Check for dangerous C++ patterns
        cpp_dangerous_patterns = [
            r'system\s*\(',
            r'exec',
            r'popen\s*\(',
            r'fopen\s*\(',
            r'freopen\s*\(',
            r'ifstream',
            r'ofstream',
            r'WSAStartup',  # Windows socket initialization
            r'socket\s*\(',
        ]
        
        for pattern in cpp_dangerous_patterns:
            if re.search(pattern, code):
                self.security_issues.append({
                    'type': SecurityIssueType.CODE_EXECUTION,
                    'severity': 'high' if 'system' in pattern or 'exec' in pattern else 'medium',
                    'pattern': pattern,
                    'description': f'Dangerous C++ pattern detected: {pattern}',
                    'category': 'cpp',
                    'line_numbers': self._find_line_numbers(code, pattern)
                })
    
    def _validate_php_code(self, code: str):
        """Validate PHP code for security issues"""
        # Check for dangerous PHP patterns
        php_dangerous_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\(',
            r'passthru\s*\(',
            r'popen\s*\(',
            r'fopen\s*\(',
            r'file_get_contents\s*\(',
            r'file_put_contents\s*\(',
            r'curl_exec\s*\(',
        ]
        
        for pattern in php_dangerous_patterns:
            if re.search(pattern, code):
                self.security_issues.append({
                    'type': SecurityIssueType.CODE_EXECUTION,
                    'severity': 'high' if 'eval' in pattern else 'medium',
                    'pattern': pattern,
                    'description': f'Dangerous PHP pattern detected: {pattern}',
                    'category': 'php',
                    'line_numbers': self._find_line_numbers(code, pattern)
                })
    
    def _validate_rust_code(self, code: str):
        """Validate Rust code for security issues"""
        # Check for dangerous Rust patterns
        rust_dangerous_patterns = [
            r'unsafe\s+{',
            r'std::process::Command',
            r'std::fs::',
            r'std::net::TcpStream',
            r'std::net::TcpListener',
            r'libc::system',
        ]
        
        for pattern in rust_dangerous_patterns:
            if re.search(pattern, code):
                self.security_issues.append({
                    'type': SecurityIssueType.CODE_EXECUTION,
                    'severity': 'high' if 'unsafe' in pattern else 'medium',
                    'pattern': pattern,
                    'description': f'Dangerous Rust pattern detected: {pattern}',
                    'category': 'rust',
                    'line_numbers': self._find_line_numbers(code, pattern)
                })
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan an entire LF file for security issues"""
        if not file_path.endswith('.lf'):
            raise ValueError("File must be an .lf file")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the LF file to separate different code blocks
        lines = content.split('\n')
        security_report = {
            'file': file_path,
            'total_lines': len(lines),
            'blocks_analyzed': 0,
            'total_issues': 0,
            'issues_by_type': {},
            'issues_by_language': {},
            'scan_results': []
        }
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('py.'):
                # Collect Python code block
                code_block = []
                j = i
                while j < len(lines) and lines[j].strip().startswith('py.'):
                    code_block.append(lines[j].strip()[3:])  # Remove 'py.'
                    j += 1
                
                code_content = '\n'.join(code_block)
                result = self.validate_code(code_content, 'py')
                
                security_report['scan_results'].append({
                    'type': 'py',
                    'line_start': i + 1,
                    'line_end': j,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i = j
            elif line.startswith('cpp.'):
                code_content = line[4:]  # Remove 'cpp.'
                result = self.validate_code(code_content, 'cpp')
                
                security_report['scan_results'].append({
                    'type': 'cpp',
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i += 1
            elif line.startswith('js.'):
                code_content = line[3:]  # Remove 'js.'
                result = self.validate_code(code_content, 'js')
                
                security_report['scan_results'].append({
                    'type': 'js',
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i += 1
            elif line.startswith('java.'):
                code_content = line[5:]  # Remove 'java.'
                result = self.validate_code(code_content, 'java')
                
                security_report['scan_results'].append({
                    'type': 'java',
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i += 1
            elif line.startswith('php.'):
                code_content = line[4:]  # Remove 'php.'
                result = self.validate_code(code_content, 'php')
                
                security_report['scan_results'].append({
                    'type': 'php',
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i += 1
            elif line.startswith('rust.'):
                code_content = line[5:]  # Remove 'rust.'
                result = self.validate_code(code_content, 'rust')
                
                security_report['scan_results'].append({
                    'type': 'rust',
                    'line_start': i + 1,
                    'line_end': i + 1,
                    'issues': result['issues'],
                    'is_valid': result['is_valid']
                })
                
                i += 1
            else:
                i += 1        
        # Generate summary statistics
        security_report['blocks_analyzed'] = len(security_report['scan_results'])
        
        total_issues = 0
        issues_by_type = {}
        issues_by_language = {}
        
        for result in security_report['scan_results']:
            issue_count = len(result['issues'])
            total_issues += issue_count
            
            for issue in result['issues']:
                issue_type = issue['type'].value
                issues_by_type[issue_type] = issues_by_type.get(issue_type, 0) + 1
                
                lang = result['type']
                issues_by_language[lang] = issues_by_language.get(lang, 0) + 1        
        security_report['total_issues'] = total_issues
        security_report['issues_by_type'] = issues_by_type
        security_report['issues_by_language'] = issues_by_language
        
        return security_report
    
    def generate_security_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate a human-readable security report"""
        report = []
        report.append("🔒 LF Security Scan Report")
        report.append("=" * 50)
        report.append(f"File: {scan_results['file']}")
        report.append(f"Total Lines: {scan_results['total_lines']}")
        report.append(f"Blocks Analyzed: {scan_results['blocks_analyzed']}")
        report.append(f"Total Issues Found: {scan_results['total_issues']}")
        report.append("")
        
        if scan_results['total_issues'] == 0:
            report.append("✅ No security issues detected!")
        else:
            report.append("⚠️  Security Issues Found:")
            report.append("-" * 30)
            
            # Issues by language
            if scan_results['issues_by_language']:
                report.append("Issues by Language:")
                for lang, count in scan_results['issues_by_language'].items():
                    report.append(f"  {lang}: {count} issues")
                report.append("")
            
            # Issues by type
            if scan_results['issues_by_type']:
                report.append("Issues by Type:")
                for issue_type, count in scan_results['issues_by_type'].items():
                    report.append(f"  {issue_type}: {count} issues")
                report.append("")
            
            # Detailed issues
            for result in scan_results['scan_results']:
                if result['issues']:
                    report.append(f"Block Type: {result['type']} (Lines {result['line_start']}-{result['line_end']})")
                    for issue in result['issues']:
                        report.append(f"  - {issue['severity'].upper()}: {issue['description']}")
                        if issue['line_numbers']:
                            report.append(f"    Line(s): {', '.join(map(str, issue['line_numbers']))}")
                    report.append("")        
        return "\n".join(report)

# Example usage and testing function
def test_security_module():
    """Test the security module with sample code"""
    security = LFSecurity()
    
    # Test Python code
    py_code = """
import os
exec("malicious code")
print("safe code")
"""
    
    result = security.validate_code(py_code, 'py')
    print("Python validation result:")
    print(json.dumps(result, indent=2))
    
    # Test C++ code
    cpp_code = """
#include <iostream>
system("rm -rf /");  // Dangerous!
std::cout << "Hello" << std::endl;
"""
    
    result = security.validate_code(cpp_code, 'cpp')
    print("\nC++ validation result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_security_module()