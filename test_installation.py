#!/usr/bin/env python3
"""
Project Robot - Quick Testing Script
Gunakan untuk verify installation & basic functionality
"""

import sys
import json
from pathlib import Path


def test_python_version():
    """Test Python version"""
    print("🔍 Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (Need 3.7+)")
        return False


def test_tkinter():
    """Test Tkinter availability"""
    print("🔍 Checking Tkinter...", end=" ")
    try:
        import tkinter
        print("✅ Available")
        return True
    except ImportError:
        print("❌ Not available (Install python3-tk)")
        return False


def test_robot_core():
    """Test robot_core.py exists and is readable"""
    print("🔍 Checking robot_core.py...", end=" ")
    if Path("robot_core.py").exists():
        print("✅ Found")
        return True
    else:
        print("❌ Not found")
        return False


def test_robot_gui():
    """Test robot_gui.py exists"""
    print("🔍 Checking robot_gui.py...", end=" ")
    if Path("robot_gui.py").exists():
        print("✅ Found")
        return True
    else:
        print("❌ Not found")
        return False


def test_patterns_json():
    """Test patterns.json exists and is valid"""
    print("🔍 Checking patterns.json...", end=" ")
    patterns_file = Path("data/patterns.json")
    if not patterns_file.exists():
        print("❌ Not found")
        return False
    
    try:
        with open(patterns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Valid ({len(data)} intents)")
        return True
    except Exception as e:
        print(f"❌ Invalid: {str(e)}")
        return False


def test_data_directory():
    """Test data directory exists"""
    print("🔍 Checking data/ directory...", end=" ")
    if Path("data").is_dir():
        print("✅ Found")
        return True
    else:
        print("❌ Not found (will be created on first run)")
        return False


def test_imports():
    """Test all standard library imports"""
    print("🔍 Checking imports...", end=" ")
    try:
        import json
        import pathlib
        import datetime
        import random
        import re
        import typing
        print("✅ All standard library OK")
        return True
    except ImportError as e:
        print(f"❌ Missing: {str(e)}")
        return False


def test_robot_functionality():
    """Test basic robot functionality"""
    print("🔍 Testing robot functionality...", end=" ")
    try:
        from robot_core import RobotBrain
        robot = RobotBrain()
        
        # Test basic response
        response = robot.process_input("Halo")
        if response and len(response) > 0:
            print("✅ Working")
            return True
        else:
            print("❌ No response")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def print_header():
    """Print test header"""
    print("\n" + "="*60)
    print("🤖 PROJECT ROBOT - INSTALLATION TEST")
    print("="*60 + "\n")


def print_summary(results):
    """Print test summary"""
    passed = sum(results.values())
    total = len(results)
    
    print("\n" + "="*60)
    print(f"📊 TEST RESULTS: {passed}/{total} passed")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! You're ready to use Project Robot!")
        print("\n📖 Next steps:")
        print("   1. Run: python robot_gui.py")
        print("   2. Or:  python robot_core.py")
        print("   3. Read: README.md or QUICKSTART.md")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. See errors above.")
        print("\n📖 Help:")
        print("   1. Read: INSTALLATION.md")
        print("   2. Check: Python 3.7+ installed")
        print("   3. Check: Tkinter installed")
        print("   4. Verify: All files present")
        return False


def main():
    """Run all tests"""
    print_header()
    
    tests = {
        "Python Version": test_python_version(),
        "Tkinter": test_tkinter(),
        "Standard Library": test_imports(),
        "Data Directory": test_data_directory(),
        "patterns.json": test_patterns_json(),
        "robot_core.py": test_robot_core(),
        "robot_gui.py": test_robot_gui(),
        "Robot Functionality": test_robot_functionality(),
    }
    
    success = print_summary(tests)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
