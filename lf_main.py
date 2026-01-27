#!/usr/bin/env python3
"""
LF Main - Highly Optimized Central Management Tool for LF Language System
Version: 3.0
Enhanced with advanced features, better error handling, and performance improvements.
"""

import sys
import os
import argparse
import subprocess
import shutil
from pathlib import Path
import time
import json
from typing import Optional, Dict, Any
import tempfile
import base64
import zipfile

VERSION = "3.0"
DESCRIPTION = "LF Language System - Multi-language Fusion Programming Environment v3.0"

class LFMain:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.compiler_path = self.project_root / "lf-compile.py"
        self.runtime_path = self.project_root / "lf-run.py"
        self.security_path = self.project_root / "lf-security.py"
        
    def show_version(self):
        """Show version information with enhanced details"""
        print(f"LF Language System v{VERSION}")
        print("Multi-language Fusion Programming Environment")
        print("Supports Python, C++, JavaScript, Java, PHP, and Rust")
        print("Enhanced security, performance, and features")
        
    def compile_source(self, source_file: str, output_dir: Optional[str] = None) -> bool:
        """Compile LF source file with enhanced error handling"""
        start_time = time.time()
        
        if not source_file.endswith('.lf'):
            print(f"❌ Error: {source_file} is not a valid .lf file")
            return False
            
        if not os.path.exists(source_file):
            print(f"❌ Error: File {source_file} not found")
            return False
            
        try:
            # Run compiler
            cmd = [sys.executable, str(self.compiler_path), source_file]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                end_time = time.time()
                print(result.stdout)
                print(f"⏱️  Compilation completed in {end_time - start_time:.3f}s")
                return True
            else:
                print(f"❌ Compilation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False
    
    def run_program(self, file_path: str) -> bool:
        """Run compiled LSF or packaged LFP file with enhanced features"""
        start_time = time.time()
        
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_path} not found")
            return False
            
        if not (file_path.endswith('.lsf') or file_path.endswith('.lfp')):
            print(f"❌ Error: {file_path} is not a valid LSF or LFP file")
            return False
            
        try:
            # Run program
            cmd = [sys.executable, str(self.runtime_path), file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  Runtime warning: {result.stderr}")
            
            end_time = time.time()
            print(f"⏱️  Execution completed in {end_time - start_time:.3f}s")
                
            return True
        except Exception as e:
            print(f"❌ Runtime error: {e}")
            return False
    
    def package_to_exe(self, source_file: str) -> bool:
        """Package LF program as standalone executable with enhanced features"""
        start_time = time.time()
        
        # First compile the source
        if not self.compile_source(source_file):
            return False
            
        # Get base name
        base_name = os.path.splitext(source_file)[0]
        lfp_file = base_name + ".lfp"
        
        if not os.path.exists(lfp_file):
            print(f"❌ Error: Package file {lfp_file} not found")
            return False
            
        try:
            # Use PyInstaller to create executable
            # Create temporary script for execution
            temp_script = f"_temp_{os.path.basename(base_name)}.py"
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(f'''import sys
import os
sys.path.append(os.path.dirname(__file__))

# Embed the package file
package_data = """''')
                
                # Read and embed package file
                with open(lfp_file, 'rb') as pkg:
                    encoded = base64.b64encode(pkg.read()).decode('utf-8')
                    f.write(encoded)
                    
                f.write(f'''"""

import base64
import tempfile
import zipfile
import subprocess
import sys
import os

def run_embedded_package():
    # Write package data to temporary file
    with tempfile.NamedTemporaryFile(suffix='.lfp', delete=False) as tmp:
        tmp.write(base64.b64decode(package_data))
        tmp_path = tmp.name
    
    # Run with lf-run.py
    runtime_path = os.path.join(os.path.dirname(__file__), 'lf-run.py')
    if not os.path.exists(runtime_path):
        # If runtime not found, try to find it in the same directory as this script
        runtime_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lf-run.py')
    
    if os.path.exists(runtime_path):
        subprocess.run([sys.executable, runtime_path, tmp_path])
    else:
        print("❌ Error: lf-run.py not found")
    
    # Clean up
    try:
        os.unlink(tmp_path)
    except:
        pass

if __name__ == "__main__":
    run_embedded_package()
''')
            
            # Run PyInstaller with enhanced options
            pyinstaller_cmd = [
                sys.executable, "-m", "PyInstaller",  # Use module to ensure it works
                "--onefile",
                "--name", os.path.basename(base_name),
                "--add-data", f"{self.runtime_path};.",
                "--distpath", ".",
                "--clean",
                temp_script
            ]
            
            result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True, encoding='utf-8')
            
            # Clean up temporary files
            cleanup_success = True
            try:
                os.remove(temp_script)
                if os.path.exists(f"{temp_script}.spec"):
                    os.remove(f"{temp_script}.spec")
                if os.path.exists("build"):
                    shutil.rmtree("build")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean up temporary files: {e}")
                cleanup_success = False
                
            if result.returncode == 0:
                exe_file = f"{os.path.basename(base_name)}.exe"
                if os.path.exists(exe_file):
                    end_time = time.time()
                    print(f"✅ Successfully created {exe_file}")
                    print(f"⏱️  Packaging completed in {end_time - start_time:.3f}s")
                    print(f"📊 Executable size: {os.path.getsize(exe_file)} bytes")
                    return True
                else:
                    print("❌ Error: Executable file not found")
                    return False
            else:
                print(f"❌ PyInstaller error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Packaging error: {e}")
            return False
    
    def create_dll_wrapper(self, source_file: str) -> bool:
        """Create a DLL wrapper for LF program with enhanced features"""
        start_time = time.time()
        
        # First compile the source
        if not self.compile_source(source_file):
            return False
            
        # Get base name
        base_name = os.path.splitext(source_file)[0]
        lfp_file = base_name + ".lfp"
        
        if not os.path.exists(lfp_file):
            print(f"❌ Error: Package file {lfp_file} not found")
            return False
            
        try:
            # Create DLL wrapper script
            dll_wrapper = f"{os.path.basename(base_name)}_wrapper.py"
            with open(dll_wrapper, 'w', encoding='utf-8') as f:
                f.write(f'''# LF DLL Wrapper v3.0
import base64
import tempfile
import subprocess
import sys
import os

# Embedded package data
PACKAGE_DATA = """''')
                
                # Read and embed package file
                with open(lfp_file, 'rb') as pkg:
                    encoded = base64.b64encode(pkg.read()).decode('utf-8')
                    f.write(encoded)
                    
                f.write(f'''"""

def run_lf_program():
    """Run the embedded LF program"""
    # Write package data to temporary file
    with tempfile.NamedTemporaryFile(suffix='.lfp', delete=False) as tmp:
        tmp.write(base64.b64decode(PACKAGE_DATA))
        tmp_path = tmp.name
    
    # Run with lf-run.py
    try:
        # Find runtime in the same directory
        runtime_dir = os.path.dirname(os.path.abspath(__file__))
        runtime_path = os.path.join(runtime_dir, 'lf-run.py')
        
        if not os.path.exists(runtime_path):
            # Try current directory
            runtime_path = 'lf-run.py'
            
        if os.path.exists(runtime_path):
            result = subprocess.run([sys.executable, runtime_path, tmp_path], 
                                  capture_output=True, text=True)
            output = result.stdout
            if result.stderr:
                output += "\nError: " + result.stderr
        else:
            output = "❌ Error: lf-run.py not found"
    except Exception as e:
        output = f"Runtime error: {{e}}"
    
    # Clean up
    try:
        os.unlink(tmp_path)
    except:
        pass
        
    return output

# Export functions for DLL usage
run = run_lf_program

if __name__ == "__main__":
    # Test execution
    print(run_lf_program())
''')
            
            end_time = time.time()
            print(f"✅ Successfully created DLL wrapper: {dll_wrapper}")
            print(f"⏱️  Wrapper creation completed in {end_time - start_time:.3f}s")
            print("ℹ️  To convert to actual DLL, use tools like py2exe or cx_Freeze")
            return True
            
        except Exception as e:
            print(f"❌ DLL wrapper creation error: {e}")
            return False
    
    def benchmark(self, source_file: str) -> bool:
        """Run benchmark on LF program to measure performance"""
        if not source_file.endswith('.lf'):
            print(f"❌ Error: {source_file} is not a valid .lf file")
            return False
            
        if not os.path.exists(source_file):
            print(f"❌ Error: File {source_file} not found")
            return False
        
        print(f"🚀 Benchmarking {source_file}...")
        
        # Compile and measure time
        compile_start = time.time()
        compile_success = self.compile_source(source_file)
        compile_time = time.time() - compile_start
        
        if not compile_success:
            print("❌ Benchmark failed during compilation")
            return False
        
        # Run and measure time
        output_file = source_file.replace('.lf', '.lsf')
        run_start = time.time()
        run_success = self.run_program(output_file)
        run_time = time.time() - run_start
        
        if not run_success:
            print("❌ Benchmark failed during execution")
            return False
        
        # Print benchmark results
        print("\n📊 BENCHMARK RESULTS:")
        print(f"   Compilation time: {compile_time:.3f}s")
        print(f"   Execution time: {run_time:.3f}s")
        print(f"   Total time: {compile_time + run_time:.3f}s")
        
        return True
    
    def analyze(self, source_file: str) -> bool:
        """Analyze LF source file for structure and statistics"""
        if not source_file.endswith('.lf'):
            print(f"❌ Error: {source_file} is not a valid .lf file")
            return False
            
        if not os.path.exists(source_file):
            print(f"❌ Error: File {source_file} not found")
            return False
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            total_lines = len(lines)
            
            # Count different elements
            directives = 0
            python_blocks = 0
            cpp_blocks = 0
            js_blocks = 0
            java_blocks = 0
            php_blocks = 0
            rust_blocks = 0
            comments = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    directives += 1
                elif stripped.startswith('py.'):
                    python_blocks += 1
                elif stripped.startswith('cpp.'):
                    cpp_blocks += 1
                elif stripped.startswith('js.'):
                    js_blocks += 1
                elif stripped.startswith('java.'):
                    java_blocks += 1
                elif stripped.startswith('php.'):
                    php_blocks += 1
                elif stripped.startswith('rust.'):
                    rust_blocks += 1
                elif stripped.startswith('//'):
                    comments += 1
            
            print(f"\n🔍 ANALYSIS OF {source_file}:")
            print(f"   Total lines: {total_lines}")
            print(f"   Directives: {directives}")
            print(f"   Comments: {comments}")
            print(f"   Python blocks: {python_blocks}")
            print(f"   C++ blocks: {cpp_blocks}")
            print(f"   JavaScript blocks: {js_blocks}")
            print(f"   Java blocks: {java_blocks}")
            print(f"   PHP blocks: {php_blocks}")
            print(f"   Rust blocks: {rust_blocks}")
            
            total_code_blocks = python_blocks + cpp_blocks + js_blocks + java_blocks + php_blocks + rust_blocks
            print(f"   Total code blocks: {total_code_blocks}")
            
            return True
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s compile program.lf              # Compile LF source
  %(prog)s run program.lsf                 # Run compiled program
  %(prog)s package-exe program.lf          # Create executable
  %(prog)s benchmark program.lf            # Run performance benchmark
  %(prog)s analyze program.lf              # Analyze source structure
  %(prog)s shell                           # Start interactive shell
        """
    )
    parser.add_argument("action", 
                       choices=["compile", "run", "package-exe", "package-dll", "shell", "version", "benchmark", "analyze"], 
                       help="Action to perform")
    parser.add_argument("file", nargs='?', help="Source or executable file (not required for shell, version)")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--version", "-v", action="store_true", help="Show version information")
    
    args = parser.parse_args()
    
    lf_main = LFMain()
    
    # Handle version flag
    if args.version:
        lf_main.show_version()
        return
    
    if args.action == "version":
        lf_main.show_version()
        return
    elif args.action == "compile":
        if not args.file:
            print("❌ Error: Please specify a .lf file to compile")
            return
        lf_main.compile_source(args.file, args.output)
    elif args.action == "run":
        if not args.file:
            print("❌ Error: Please specify a .lsf or .lfp file to run")
            return
        lf_main.run_program(args.file)
    elif args.action == "package-exe":
        if not args.file:
            print("❌ Error: Please specify a .lf file to package")
            return
        lf_main.package_to_exe(args.file)
    elif args.action == "package-dll":
        if not args.file:
            print("❌ Error: Please specify a .lf file to create DLL wrapper")
            return
        lf_main.create_dll_wrapper(args.file)
    elif args.action == "benchmark":
        if not args.file:
            print("❌ Error: Please specify a .lf file to benchmark")
            return
        lf_main.benchmark(args.file)
    elif args.action == "analyze":
        if not args.file:
            print("❌ Error: Please specify a .lf file to analyze")
            return
        lf_main.analyze(args.file)
    elif args.action == "shell":
        # Execute the runtime script with shell argument to maintain interactivity
        cmd = [sys.executable, str(lf_main.runtime_path), "--shell"]
        result = subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
