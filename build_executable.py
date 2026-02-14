"""
Build Script for Git Push Tool
Creates standalone executables for Windows (.exe) and Mac (.app)
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable for the current platform"""
    print(f"\nBuilding executable for {sys.platform}...")
    
    # Common PyInstaller options
    options = [
        "git_push_tool.py",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (GUI only)
        "--name=GitPushTool",
        "--clean",
    ]
    
    # Platform-specific options
    if sys.platform == "darwin":  # macOS
        options.extend([
            "--icon=NONE",  # You can add a .icns file here if you have one
        ])
        print("Building macOS application...")
    elif sys.platform == "win32":  # Windows
        options.extend([
            "--icon=NONE",  # You can add a .ico file here if you have one
        ])
        print("Building Windows executable...")
    else:  # Linux
        print("Building Linux executable...")
    
    # Run PyInstaller
    subprocess.check_call(["pyinstaller"] + options)
    
    print("\n✓ Build complete!")
    print(f"Your executable is in the 'dist' folder")
    
    if sys.platform == "darwin":
        print("  → dist/GitPushTool.app")
    elif sys.platform == "win32":
        print("  → dist/GitPushTool.exe")
    else:
        print("  → dist/GitPushTool")

def main():
    print("="*60)
    print("Git Push Tool - Build Script")
    print("="*60)
    
    try:
        # Check if PyInstaller is installed
        try:
            import PyInstaller
        except ImportError:
            install_pyinstaller()
        
        # Build the executable
        build_executable()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()