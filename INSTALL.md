# Android Repair CLI - Installation Guide

## Quick Installation

### **Option 1: Automated Installation (Recommended)**

#### Windows:
```bash
python install.py
```

#### macOS/Linux:
```bash
python3 install.py
```

This will:
- ✅ Install all Python dependencies
- ✅ Create necessary directories
- ✅ Build a standalone Windows .exe file (Windows only)

---

### **Option 2: Manual Installation**

#### Step 1: Install Python
- Download Python 3.8+ from https://www.python.org/
- Check "Add Python to PATH" during installation

#### Step 2: Install Dependencies

**Windows (Command Prompt):**
```bash
pip install -r requirements.txt
```

**macOS/Linux (Terminal):**
```bash
pip3 install -r requirements.txt
```

#### Step 3: Install Android SDK Tools (ADB)

**Option A - Automatic:**
```bash
pip install adb-shell
```

**Option B - Manual:**
1. Download from: https://developer.android.com/tools/adb
2. Extract to a folder
3. Add to system PATH

---

## Running the Tool

### **Method 1: CLI Commands**

```bash
# Show version
python main.py version

# Check ADB connection
python main.py check-adb

# List connected devices
python main.py devices

# Get device info
python main.py info

# Fix FRP
python main.py fix-frp

# Factory reset
python main.py factory-reset --confirm

# Wipe cache
python main.py wipe-cache

# Backup device
python main.py backup

# Help
python main.py help-guide
```

### **Method 2: Windows Executable (After Build)**

```bash
android-repair version
android-repair devices
android-repair info
android-repair fix-frp
```

---

## Device Setup

### **Enable USB Debugging on Android**

1. **Go to Settings**
2. **About Phone**
3. **Tap "Build Number" 7 times** (to enable Developer Options)
4. **Go back and enter Developer Options**
5. **Enable "USB Debugging"**
6. **Connect to PC via USB**
7. **Authorize the PC connection**

---

## Troubleshooting

### **"No ADB connection found"**
- Install Android SDK Platform Tools
- Enable USB Debugging on device
- Try different USB cable
- Check device in Settings → Connected devices

### **"No devices connected"**
- Ensure device is connected via USB
- Enable USB Debugging
- Authorize this computer on device
- Restart ADB server: `adb kill-server && adb start-server`

### **"Permission denied" errors**
- Grant USB debugging permissions on device
- Try with Administrator/sudo
- Reconnect device

---

## Building Standalone Executable

### **For Windows:**

```bash
pip install pyinstaller
pyinstaller android_repair.spec
```

Executable will be created at: `dist/android-repair.exe`

### **For macOS:**

```bash
pip3 install pyinstaller
pyinstaller --onefile main.py
```

### **For Linux:**

```bash
pip3 install pyinstaller
pyinstaller --onefile main.py
```

---

## Supported Devices

✅ Tecno Spark Go (KL4)
✅ Samsung Galaxy A Series
✅ Samsung Galaxy S Series  
✅ Xiaomi Redmi Series
✅ Most Android devices with ADB support

---

## Features

✅ Device Detection & Info
✅ ADB Connection Management
✅ FRP (Factory Reset Protection) Fix
✅ Factory Reset
✅ Cache Wipe
✅ Device Backup
✅ Battery Status Check
✅ Root Detection
✅ Detailed Logging

---

## Support

📧 GitHub: https://github.com/Cherish594/www.cherishedcclxv.com

⚠️ **Disclaimer**: Use at your own risk. Always backup data before operations.

---
