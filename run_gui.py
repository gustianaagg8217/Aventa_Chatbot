#!/usr/bin/env python3
"""
Project Robot - GUI Launcher Script
Starter script untuk menjalankan GUI dengan ease
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    gui_file = script_dir / "robot_gui.py"
    
    if not gui_file.exists():
        print("❌ Error: robot_gui.py tidak ditemukan!")
        print(f"Lokasi yang dicari: {gui_file}")
        sys.exit(1)
    
    print("🤖 Project Robot - GUI Launcher")
    print("=" * 50)
    print(f"📁 Menjalankan dari: {script_dir}")
    print("⏳ Loading interface...")
    print("=" * 50)
    
    try:
        # Change to script directory
        os.chdir(script_dir)
        
        # Run GUI
        subprocess.run([sys.executable, str(gui_file)], check=False)
    
    except FileNotFoundError:
        print("❌ Python tidak ditemukan!")
        print("Pastikan Python 3.7+ sudah terinstall dan ditambahkan ke PATH")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
