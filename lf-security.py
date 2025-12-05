#!/usr/bin/env python3
"""
LF Security Module - Enhanced Security Features for LF Language System
Version: 1.0
"""

import re
import ast
import json
import subprocess
from typing import Dict, Any, List

class LFSecurity:
    """Security module for LF Language System"""
    
    def __init__(self):
        self.security_level = "enhanced"
        self.max_execution_time = 30  # seconds
        self.max_memory_usage = 100 * 1024 * 1024  # 100MB
        self.dangerous_patterns = [
            r'\bimport\b.*os\b', 
            r'\bexec\b', 
            r'\beval\b', 
            r'\bopen\b\s*\(\s*[^)]*\../',
            r'\b__.*__\b', 
            r'\bimportlib\b',
            r'\bsubprocess\b',
            r'\bos\b\.',
            r'\bsys\b\.',
            r'\bshutil\b',
            r'\brequests\b',
            r'\bsocket\b',
            r'\bhttplib\b',
            r'\bftplib\b',
            r'\bxmlrpc\b',
            r'\bpickle\b',
            r'\bshelve\b',
            r'\bcPickle\b',
            r'\bmarshal\b',
            r'\bwebbrowser\b',
            r'\bssl\b',
            r'\bzlib\b',
            r'\bbz2\b',
            r'\blzma\b',
            r'\bzipfile\b',
            r'\btarfile\b',
            r'\bcodecs\b'
        ]
        
    def validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code for security issues"""
        issues = []
        
        # Check dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "type": "dangerous_pattern",
                    "pattern": pattern,
                    "severity": "high"
                })
        
        # Language-specific validation
        if language == "py":
            issues.extend(self._validate_python_code(code))
        elif language == "js":
            issues.extend(self._validate_javascript_code(code))
        elif language == "cpp":
            issues.extend(self._validate_cpp_code(code))
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "security_level": self.security_level
        }
    
    def _validate_python_code(self, code: str) -> List[Dict[str, Any]]:
        """Validate Python code for security issues"""
        issues = []
        
        try:
            # Parse AST to check for dangerous constructs
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['os', 'subprocess', 'sys', 'shutil', 'socket', 'urllib', 'requests']:
                            issues.append({
                                "type": "dangerous_import",
                                "module": alias.name,
                                "severity": "high"
                            })
                elif isinstance(node, ast.ImportFrom):
                    if node.module in ['os', 'subprocess', 'sys', 'shutil', 'socket', 'urllib', 'requests']:
                        issues.append({
                            "type": "dangerous_import",
                            "module": node.module,
                            "severity": "high"
                        })
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['exec', 'eval', 'compile', 'open', '__import__']:
                            issues.append({
                                "type": "dangerous_function_call",
                                "function": node.func.id,
                                "severity": "high"
                            })
        except SyntaxError:
            issues.append({
                "type": "syntax_error",
                "severity": "medium"
            })
        
        return issues
    
    def _validate_javascript_code(self, code: str) -> List[Dict[str, Any]]:
        """Validate JavaScript code for security issues"""
        issues = []
        
        # Check for dangerous patterns in JavaScript
        dangerous_js_patterns = [
            r'require\(["\']child_process["\']\)',  # child_process import
            r'require\(["\']fs["\']\)',  # fs import
            r'require\(["\']http["\']\)',  # http import
            r'require\(["\']https["\']\)',  # https import
            r'require\(["\']net["\']\)',  # net import
            r'require\(["\']dgram["\']\)',  # dgram import
            r'require\(["\']tls["\']\)',  # tls import
            r'require\(["\']cluster["\']\)',  # cluster import
            r'require\(["\']worker_threads["\']\)',  # worker_threads import
            r'eval\s*\(',  # eval function
            r'Function\s*\(',  # Function constructor
            r'import\(',  # dynamic import
        ]
        
        for pattern in dangerous_js_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "type": "dangerous_js_pattern",
                    "pattern": pattern,
                    "severity": "high"
                })
        
        return issues
    
    def _validate_cpp_code(self, code: str) -> List[Dict[str, Any]]:
        """Validate C++ code for security issues"""
        issues = []
        
        # Check for dangerous C++ patterns
        dangerous_cpp_patterns = [
            r'#include\s*<system>',  # system include
            r'system\s*\(',  # system function
            r'exec\s*\(',  # exec function
            r'popen\s*\(',  # popen function
            r'WinExec\s*\(',  # Windows exec function
            r'CreateProcess',  # Windows process creation
            r'ShellExecute',  # Windows shell execution
        ]
        
        for pattern in dangerous_cpp_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "type": "dangerous_cpp_pattern",
                    "pattern": pattern,
                    "severity": "high"
                })
        
        return issues

class LFPerformanceMonitor:
    """Performance monitoring for LF execution"""
    
    def __init__(self):
        self.metrics = {}
    
    def get_system_usage(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        return {
            "cpu_percent": process.cpu_percent(),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "num_threads": process.num_threads(),
            "connections": len(process.connections())
        }
    
    def monitor_execution(self, func, *args, **kwargs) -> Any:
        """Monitor execution of a function"""
        import time
        
        start_time = time.time()
        start_memory = self.get_system_usage()["memory_mb"]
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            end_time = time.time()
            end_memory = self.get_system_usage()["memory_mb"]
            
            execution_time = end_time - start_time
            memory_used = end_memory - start_memory
            
            self.metrics = {
                "execution_time": execution_time,
                "memory_used_mb": memory_used,
                "peak_memory_mb": end_memory,
                "start_time": start_time
            }
        
        return result

def main():
    """Main function to test security features"""
    print("🧪 LF Security Module v1.0")
    print("-" * 40)
    
    security = LFSecurity()
    
    # Test cases
    test_codes = [
        ("py", "x = 10\nprint(x)"),
        ("py", "import os\nos.system('ls')"),  # Should be flagged
        ("js", "console.log('Hello')"),
        ("js", "eval('console.log(\"test\")')"),  # Should be flagged
        ("cpp", 'printf("Hello World");'),
        ("cpp", '#include <process.h>\nsystem("ls");')  # Should be flagged
    ]
    
    for lang, code in test_codes:
        print(f"\nTesting {lang.upper()} code:")
        print(f"Code: {code}")
        
        result = security.validate_code(code, lang)
        print(f"Valid: {result['is_valid']}")
        if result['issues']:
            print("Issues found:")
            for issue in result['issues']:
                print(f"  - {issue['type']} (severity: {issue['severity']})")
        print("-" * 40)

if __name__ == "__main__":
    main()
