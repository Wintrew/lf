#!/usr/bin/env python3
"""
LF Main - Central Management Tool for LF Language System
Version: 2.0
"""

import sys
import os
import argparse
import subprocess
import shutil
from pathlib import Path

VERSION = "2.0"
DESCRIPTION = "LF Language System - Multi-language Fusion Programming Environment"

class LFMain:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.compiler_path = self.project_root / "lf-compile.py"
        self.runtime_path = self.project_root / "lf-run.py"
        
    def show_version(self):
        """Show version information"""
        print(f"LF Language System v{VERSION}")
        print("Multi-language Fusion Programming Environment")
        print("Supports Python, C++, JavaScript, Java, PHP, and Rust")
        
    def compile_source(self, source_file, output_dir=None):
        """Compile LF source file"""
        if not source_file.endswith('.lf'):
            print(f"Error: {source_file} is not a valid .lf file")
            return False
            
        if not os.path.exists(source_file):
            print(f"Error: File {source_file} not found")
            return False
            
        try:
            # Run compiler
            cmd = [sys.executable, str(self.compiler_path), source_file]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(result.stdout)
                return True
            else:
                print(f"Compilation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"Compilation error: {e}")
            return False
    
    def run_program(self, file_path):
        """Run compiled LSF or packaged LFP file"""
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found")
            return False
            
        if not (file_path.endswith('.lsf') or file_path.endswith('.lfp')):
            print(f"Error: {file_path} is not a valid LSF or LFP file")
            return False
            
        try:
            # Run program
            cmd = [sys.executable, str(self.runtime_path), file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            print(result.stdout)
            if result.stderr:
                print(f"Runtime warning: {result.stderr}")
                
            return True
        except Exception as e:
            print(f"Runtime error: {e}")
            return False
    
    def package_to_exe(self, source_file):
        """Package LF program as standalone executable"""
        # First compile the source
        if not self.compile_source(source_file):
            return False
            
        # Get base name
        base_name = os.path.splitext(source_file)[0]
        lfp_file = base_name + ".lfp"
        
        if not os.path.exists(lfp_file):
            print(f"Error: Package file {lfp_file} not found")
            return False
            
        try:
            # Use PyInstaller to create executable
            # Create temporary script for execution
            temp_script = f"_temp_{base_name}.py"
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(f'''import sys
import os
sys.path.append(os.path.dirname(__file__))

# Embed the package file
package_data = """''')
                
                # Read and embed package file
                with open(lfp_file, 'rb') as pkg:
                    import base64
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
        print("Error: lf-run.py not found")
    
    # Clean up
    try:
        os.unlink(tmp_path)
    except:
        pass

if __name__ == "__main__":
    run_embedded_package()
''')
            
            # Run PyInstaller
            pyinstaller_cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name", base_name,
                "--add-data", f"{self.runtime_path};.",
                "--distpath", ".",
                temp_script
            ]
            
            result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True, encoding='utf-8')
            
            # Clean up temporary files
            try:
                os.remove(temp_script)
                if os.path.exists(f"{temp_script}.spec"):
                    os.remove(f"{temp_script}.spec")
                if os.path.exists("build"):
                    shutil.rmtree("build")
            except:
                pass
                
            if result.returncode == 0:
                exe_file = f"{base_name}.exe"
                if os.path.exists(exe_file):
                    print(f"✅ Successfully created {exe_file}")
                    return True
                else:
                    print("Error: Executable file not found")
                    return False
            else:
                print(f"PyInstaller error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Packaging error: {e}")
            return False
    
    def create_dll_wrapper(self, source_file):
        """Create a DLL wrapper for LF program"""
        # First compile the source
        if not self.compile_source(source_file):
            return False
            
        # Get base name
        base_name = os.path.splitext(source_file)[0]
        lfp_file = base_name + ".lfp"
        
        if not os.path.exists(lfp_file):
            print(f"Error: Package file {lfp_file} not found")
            return False
            
        try:
            # Create DLL wrapper script
            dll_wrapper = f"{base_name}_wrapper.py"
            with open(dll_wrapper, 'w', encoding='utf-8') as f:
                f.write(f'''# LF DLL Wrapper
import base64
import tempfile
import subprocess
import sys
import os

# Embedded package data
PACKAGE_DATA = """''')
                
                # Read and embed package file
                with open(lfp_file, 'rb') as pkg:
                    import base64
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
            output = "Error: lf-run.py not found"
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
            
            print(f"✅ Successfully created DLL wrapper: {dll_wrapper}")
            print("To convert to actual DLL, use a tool like py2exe or cx_Freeze")
            return True
            
        except Exception as e:
            print(f"DLL wrapper creation error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("action", choices=["compile", "run", "package-exe", "package-dll", "shell", "version"], 
                       help="Action to perform")
    parser.add_argument("file", nargs='?', help="Source or executable file (not required for shell)")
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
        lf_main.compile_source(args.file, args.output)
    elif args.action == "run":
        lf_main.run_program(args.file)
    elif args.action == "package-exe":
        lf_main.package_to_exe(args.file)
    elif args.action == "package-dll":
        lf_main.create_dll_wrapper(args.file)
    elif args.action == "shell":
        # Execute the runtime script with shell argument to maintain interactivity
        import subprocess
        cmd = [sys.executable, str(lf_main.runtime_path), "--shell"]
        result = subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()