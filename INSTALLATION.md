# 🔧 PROJECT ROBOT - INSTALLATION & SETUP GUIDE

## ⚡ TL;DR (Cara Tercepat)

```bash
# 1. Pastikan Python 3.7+ terinstall
python --version

# 2. Navigate ke folder Project Robot
cd "d:\Project Robot"

# 3. Jalankan GUI
python robot_gui.py

# 4. Done! 🎉
```

---

## 📋 Prerequisites (Syarat)

### 1. Python Installation

#### ✅ Check Python Version
```bash
python --version
# atau
python3 --version
```

Harus: **Python 3.7 atau lebih tinggi**

#### ✅ Install Python (Jika belum)

**Windows:**
1. Download dari [python.org](https://python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10
```

**macOS:**
```bash
brew install python3
```

#### ✅ Verify Installation
```bash
python3 --version
pip3 --version
```

---

## 📥 Project Setup

### Step 1: File Structure
```
Project Robot/  (folder sudah ada)
├── robot_core.py
├── robot_gui.py
├── launch.bat
├── README.md
└── data/
    └── patterns.json
```

Jika ada file yang kurang, pastikan:
- `robot_core.py` - Core engine ✅
- `robot_gui.py` - GUI interface ✅
- `data/patterns.json` - Pattern library ✅

### Step 2: Check Tkinter (GUI)

Tkinter biasanya sudah included dengan Python.

**Verify:**
```bash
python3 -m tkinter
# Akan muncul test window jika installed
```

**Jika tidak ada (Linux):**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Jika tidak ada (macOS):**
```bash
brew install python-tk@3.10
```

---

## 🚀 Running Project Robot

### Method 1: GUI Mode (Recommended)

#### Windows
```bash
# Option A: Direct Python
python robot_gui.py

# Option B: Using launcher
launch.bat

# Option C: GUI launcher
python run_gui.py
```

#### Linux/macOS
```bash
python3 robot_gui.py
```

#### Expected Output
```
🤖 PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN
[GUI window opens with chat interface]
```

### Method 2: CLI Mode

#### Windows
```bash
python robot_core.py
```

#### Linux/macOS
```bash
python3 robot_core.py
```

#### Expected Output
```
============================================================
🤖 PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN
============================================================

Perintah khusus:
  'ajar' - Ajari saya percakapan baru
  'lihat pattern' - Lihat semua yang sudah saya pelajari
  ...

🧑 Anda: [waiting for input]
```

---

## 🔍 Troubleshooting Installation

### Issue: "Python command not found"
```bash
# Solution 1: Use python3
python3 robot_gui.py

# Solution 2: Add Python to PATH (Windows)
# Run installer again, check "Add Python to PATH"

# Solution 3: Use full path
C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe robot_gui.py
```

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
```bash
# Windows: Already included, reinstall Python with tcl/tk

# Linux (Ubuntu):
sudo apt-get install python3-tk

# Linux (Fedora):
sudo dnf install python3-tkinter

# macOS:
brew install python-tk@3.10
```

### Issue: "No such file or directory: robot_gui.py"
```bash
# Make sure you're in the correct directory
cd "d:\Project Robot"
# or check if file exists
dir robot_gui.py

# If not found, extract/create the file
```

### Issue: GUI window doesn't open
```bash
# Try CLI mode first
python robot_core.py

# Check Python version
python --version  # Should be 3.7+

# Try without GUI
python -c "import tkinter; print('Tkinter OK')"
```

### Issue: "Permission denied" (Linux/macOS)
```bash
# Make script executable
chmod +x robot_gui.py

# Run with python3
python3 robot_gui.py
```

---

## ⚙️ System Requirements

### Minimum Requirements
| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.7 | 3.9+ |
| RAM | 100MB | 512MB+ |
| Disk Space | 10MB | 50MB+ |
| OS | Any | Windows 10+, Linux, macOS |

### Supported OS
- ✅ Windows 7, 8, 10, 11
- ✅ Ubuntu 18.04+
- ✅ Fedora 33+
- ✅ macOS 10.14+
- ✅ Raspberry Pi (with Python 3.7+)

---

## 🎯 First Run Checklist

- [ ] Python 3.7+ installed
- [ ] Tkinter available
- [ ] Project Robot files present
- [ ] `data/` folder exists
- [ ] `patterns.json` present
- [ ] Can run `python robot_gui.py` or `python robot_core.py`
- [ ] Chat interface opens/CLI runs
- [ ] Can type and receive responses
- [ ] Can use 'ajar' command to teach
- [ ] Memory saved to `data/conversation_memory.json`

---

## 🔄 First-Time Setup Process

### Complete Setup (5 minutes)

```bash
# 1. Open Terminal/Command Prompt
# Windows: Win+R, type 'cmd'
# Linux/macOS: Open Terminal

# 2. Navigate to Project Robot
cd "d:\Project Robot"
# or
cd "/path/to/Project Robot"

# 3. Verify Python
python --version

# 4. Run application
python robot_gui.py
# or
python robot_core.py

# 5. Test basic commands
# Type: Halo!
# Should get response

# 6. Try teaching
# Type: ajar
# Follow prompts

# 7. Check statistics
# CLI: Type 'stats'
# GUI: Click '📊 Statistik' panel
```

---

## 📦 Dependencies Management

### All Built-in (No Installation Needed!)

Project Robot menggunakan **hanya** Python standard library:
- `json` - Data serialization
- `pathlib` - File operations
- `datetime` - Timestamps
- `random` - Response selection
- `typing` - Type hints
- `tkinter` - GUI (usually included)
- `re` - Regex (optional)

### No pip packages required! 🎉

```bash
# You DON'T need to run:
pip install requirements.txt  # Not needed!

# Everything works out of the box
python robot_gui.py  # Just works!
```

### Optional Packages (For Future Enhancement)

```bash
# If you want advanced features later:
pip install nltk         # NLP
pip install spacy        # NLP
pip install scikit-learn # ML
pip install flask        # Web interface
pip install pyttsx3      # Text-to-speech
```

---

## 🌍 Setup by OS

### Windows Setup

```powershell
# 1. Check Python
python --version

# 2. Navigate
cd "d:\Project Robot"

# 3. Run
python robot_gui.py

# Done! 🎉
```

### Linux (Ubuntu/Debian)

```bash
# 1. Install Python 3
sudo apt update
sudo apt install python3 python3-tk

# 2. Navigate
cd "/path/to/Project Robot"

# 3. Run
python3 robot_gui.py

# Done! 🎉
```

### macOS

```bash
# 1. Install Python
brew install python3

# 2. Install Tkinter
brew install python-tk@3.10

# 3. Navigate
cd "/path/to/Project Robot"

# 4. Run
python3 robot_gui.py

# Done! 🎉
```

### Raspberry Pi (Linux ARM)

```bash
# 1. Install Python & dependencies
sudo apt update
sudo apt install python3 python3-tk python3-pip

# 2. Navigate
cd "/path/to/Project Robot"

# 3. Run (might be slower)
python3 robot_gui.py

# Note: GUI might be slower on low-end RPi
# Use CLI mode for better performance
python3 robot_core.py
```

---

## 💾 Data Directory Setup

### Auto-Created Files

First run akan otomatis create:
```
data/
├── patterns.json              (sudah ada)
└── conversation_memory.json   (auto-created saat pertama)
```

### Manual Setup (Jika diperlukan)

```bash
# Buat data directory
mkdir data

# Check if patterns.json exists
# If not, buat file dengan content dari documentation
```

---

## 🔐 File Permissions

### Linux/macOS

```bash
# Make scripts executable (optional)
chmod +x robot_gui.py
chmod +x robot_core.py
chmod +x run_gui.py

# Then run directly
./robot_gui.py  # harus punya shebang di top
```

### Windows

```cmd
# No special permissions needed
python robot_gui.py
```

---

## 🚨 Common Setup Issues & Solutions

| Issue | Solution |
|-------|----------|
| Python not found | Install Python, add to PATH |
| No tkinter | Install python3-tk (Linux) |
| File not found | cd to correct directory |
| Permission denied | Run with python3 or chmod |
| Slow performance | Use CLI mode instead |
| GUI crashes | Check Python version (3.7+) |
| Memory error | Clear history with 'clear' command |

---

## ✅ Verify Installation

```bash
# Run verification script
python3 << EOF
import json
import sys
from pathlib import Path

print("✓ Python version:", sys.version)
print("✓ Tkinter available:", end=" ")
try:
    import tkinter
    print("YES")
except:
    print("NO - install python3-tk")

print("✓ Files present:")
for f in ["robot_core.py", "robot_gui.py", "data/patterns.json"]:
    exists = Path(f).exists()
    print(f"  {'✓' if exists else '✗'} {f}")

print("\n✓ Ready to run Project Robot!")
EOF
```

---

## 🎮 Quick Test

```bash
# Jalankan aplikasi
python robot_gui.py

# 1. Test basic greeting
Type: "Halo"
Expected: Response greeting

# 2. Test teaching
Click: "🎓 Ajarkan Baru"
Intent: "test"
Keywords: "test, trial"
Responses: "Test response"
Click: "💾 Simpan & Ajarkan"

# 3. Test what you taught
Type: "Ini test"
Expected: "Test response"

# 4. View stats
Check right panel, should show updates

# Success! ✓
```

---

## 🚀 Next Steps

1. ✅ Complete installation
2. ✅ Run application
3. ✅ Try basic commands
4. ✅ Read [QUICKSTART.md](QUICKSTART.md)
5. ✅ Teach robot new patterns
6. ✅ Explore features
7. ✅ Read [README.md](README.md) for details
8. ✅ Check [ADVANCED_GUIDE.md](ADVANCED_GUIDE.md) for tips

---

## 📞 Need Help?

### Check Documentation
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [FEATURES.md](FEATURES.md) - Complete features

### Test Installation
```bash
python3 -c "from pathlib import Path; import json; print('OK' if Path('data/patterns.json').exists() else 'ERROR')"
```

### Common Commands
```bash
# Run GUI
python robot_gui.py

# Run CLI
python robot_core.py

# Check Python
python --version

# Show help
python robot_core.py  # then type 'help'
```

---

## ✨ Congrats!

Jika Anda bisa menjalankan aplikasi dengan sukses, berarti:
- ✅ Python terinstall dengan benar
- ✅ Semua files present
- ✅ Dependencies met
- ✅ Ready to use Project Robot!

**Sekarang mulai ajari robot Anda!** 🤖

---

Last Updated: February 2026
Happy Installation! 🎉
