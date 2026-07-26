#!/usr/bin/env python3
"""
Installation and Setup Script
Run this to install all dependencies and setup the tool
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] {description} - SUCCESS")
            return True
        else:
            print(f"[-] {description} - FAILED")
            print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[-] {description} - ERROR: {str(e)}")
        return False


def main():
    print("\n" + "="*60)
    print("  Android Repair CLI - Installation Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print(f"[-] Python 3.7+ required. You have {sys.version}")
        sys.exit(1)
    
    print(f"[+] Python version: {sys.version}")
    
    # Install dependencies
    print("\n[*] Installing Python dependencies...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements")
    
    # Create necessary directories
    print("\n[*] Creating directories...")
    Path("logs").mkdir(exist_ok=True)
    Path("backups").mkdir(exist_ok=True)
    Path("firmware").mkdir(exist_ok=True)
    print("[+] Directories created")
    
    # Build executable (Windows only)
    if platform.system() == "Windows":
        print("\n[*] Building Windows executable...")
        if run_command(f"{sys.executable} -m pip install pyinstaller", "Installing PyInstaller"):
            run_command(f"{sys.executable} -m PyInstaller android_repair.spec", "Building executable")
            print("\n[+] Executable built: dist/android-repair.exe")
    
    print("\n" + "="*60)
    print("  Installation Complete!")
    print("="*60)
    print("\n[*] Next steps:")
    print("    1. Connect your Android device via USB")
    print("    2. Enable USB debugging on your device")
    print("    3. Run: python main.py --help")
    print("    4. Or run: android-repair --help")
    print("\n")


if __name__ == "__main__":
    main()
