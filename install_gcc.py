#!/usr/bin/env python3
"""
GCC安装帮助脚本
"""

import platform
import webbrowser

def help_install_gcc():
    system = platform.system()
    
    print("🚀 GCC编译器安装指导")
    print("=" * 40)
    
    if system == "Windows":
        print("推荐安装: MinGW-w64 或 MSYS2")
        print()
        print("1. MinGW-w64 (推荐):")
        print("   下载: https://github.com/niXman/mingw-builds-binaries/releases")
        print("   选择: x86_64-posix-seh")
        print()
        print("2. MSYS2:")
        print("   下载: https://www.msys2.org/")
        print("   安装后运行: pacman -S mingw-w64-x86_64-gcc")
        print()
        webbrowser.open("https://github.com/niXman/mingw-builds-binaries/releases")
    
    elif system == "Linux":
        print("运行以下命令安装:")
        print("sudo apt-get update")
        print("sudo apt-get install gcc g++")
        print()
        print("或者:")
        print("sudo yum install gcc-c++")
    
    elif system == "Darwin":  # macOS
        print("安装Xcode命令行工具:")
        print("xcode-select --install")
        print()
        print("或者用Homebrew:")
        print("brew install gcc")
    
    print("=" * 40)
    print("安装完成后重新运行LF程序")

if __name__ == "__main__":
    help_install_gcc()