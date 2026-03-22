# Keylogger Simulator

A professional Python application demonstrating keystroke logging mechanics with real-time capture, structured logging, encryption, and comprehensive log management.

## Overview

Keylogger Simulator is a feature-rich application that captures keyboard input with millisecond-precision timestamps, stores data in structured JSON format, and provides a modern graphical interface for log management and analysis.

### Features

- **Real-time Keystroke Capture**: Captures all keyboard input with timestamps
- **Structured JSON Logging**: Stores keystrokes in organized JSON format with session management
- **AES-256 Encryption**: Optional encryption for stored logs
- **Modern Professional GUI**: Built with CustomTkinter featuring a professional color scheme
- **Log Management**: View, search, filter, and export logs through an intuitive interface
- **Cross-platform Support**: Works on Windows, macOS, and Linux

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [User Guide](#user-guide)
- [Architecture](#architecture)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone or Download the Repository**

```bash
git clone https://github.com/yourusername/keylogger-simulator.git
cd keylogger-simulator
```

2. **Create Virtual Environment (Recommended)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install pynput customtkinter cryptography
```

4. **Verify Installation**

```bash
python app.py
```

### Project Structure

```
keylogger_simulator/
├── app.py                      # Main application entry point
├── core/
│   ├── __init__.py
│   ├── keylogger_engine.py     # Core logging functionality
│   └── security.py             # Encryption and security utilities
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Main GUI interface
│   └── log_viewer.py           # Log viewing and management
├── logs/                       # Directory for stored logs
├── config.json                 # Configuration file (auto-generated)
└── README.md                   # This documentation
```

## Quick Start

### Basic Usage

1. **Launch the Application**

```bash
python app.py
```

2. **Start Logging**

   Click the "START LOGGING" button. The status indicator will turn green.

3. **Type Normally**

   Type in any application (text editor, browser, etc.). Keystrokes appear in the live display.

4. **Stop Logging**

   Click "STOP LOGGING" or press the ESC key to end the session.

5. **View Logs**

   Click "VIEW LOGS" to browse, search, and analyze captured sessions.

### Example Session

```
=== Session Started: 20250322_143022 ===
Hello world! This is a test.
[SHIFT]this is capitalized[ENTER]
Password: ********
=== Session Stopped: 20250322_143022 ===
```

## User Guide

### Main Interface Components

#### Control Panel

| Button | Function |
|--------|----------|
| **START LOGGING** | Begins capturing keystrokes, creates new session |
| **STOP LOGGING** | Ends current session and saves data to disk |
| **VIEW LOGS** | Opens log viewer for browsing and analysis |
| **EXPORT ALL** | Exports all logs to text format in selected directory |
| **CLEAR DISPLAY** | Clears the live keystroke display area |

#### Status Indicators

- **Status**: Shows RUNNING (green) or STOPPED (red)
- **Session**: Displays current session ID
- **Keystrokes**: Real-time counter of captured keystrokes

#### Security Features

- **Enable Encryption**: Toggle AES-256 encryption for new sessions (existing logs remain unencrypted)

### Log Viewer

The log viewer provides comprehensive log analysis capabilities:

1. **Log Selection**: Browse all sessions in the left panel
2. **Log Display**: View complete keystroke sequence with timestamps
3. **Search Function**: Find specific text within the current log
4. **Export Feature**: Export individual logs to readable text format

### Search Functionality

The main interface includes a global search feature:

1. Enter search term in the search field
2. Choose case sensitivity option
3. Click "SEARCH" to find matches across all logs
4. View results count and open relevant logs

### Export Options

- **Export All**: Exports all logs to text format in a single operation
- **Individual Export**: Export specific logs from the log viewer

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   GUI Layer  │  │  Core Engine │  │   Security   │    │
│  │              │  │              │  │              │    │
│  │ Main Window  │◄─┤ Keylogger    │◄─┤ Encryption   │    │
│  │ Log Viewer   │  │ Engine       │  │ Utilities    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                 │                  │             │
│         ▼                 ▼                  ▼             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                    Data Storage                       │ │
│  │            logs/session_*.json or .enc               │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Keylogger Engine (core/keylogger_engine.py)

The core engine handles all keystroke capture and logging:

- **Thread-safe Operation**: Runs listener in separate thread
- **Special Key Mapping**: Converts special keys to readable format
- **Buffer Management**: Auto-saves every 50 keystrokes
- **Session Management**: Unique session IDs with timestamps
- **Error Handling**: Comprehensive exception management

#### 2. Security Module (core/security.py)

Provides encryption functionality:

- **AES-256 Encryption**: Using Fernet symmetric encryption
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Encrypted File Format**: `.enc` extension for encrypted logs

#### 3. GUI Components (ui/)

Modern interface built with CustomTkinter:

- **Main Window**: Control panel and live display
- **Log Viewer**: Dedicated log analysis interface
- **Professional Styling**: Custom color scheme and responsive layout

## Technical Details

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pynput | 1.7.6+ | Cross-platform keyboard input capture |
| customtkinter | 5.2.0+ | Modern GUI toolkit |
| cryptography | 41.0.0+ | Encryption functions |

### Supported Platforms

- **Windows**: Windows 10/11
- **macOS**: Catalina (10.15) and newer
- **Linux**: Ubuntu 20.04+, Debian 11+, Fedora 35+

### Performance

- **CPU Usage**: < 1% when idle, < 5% during active typing
- **Memory Usage**: ~50-100 MB RAM
- **Storage**: ~10 KB per 1000 keystrokes (unencrypted)

### Log File Format

```json
{
  "session_id": "20250322_143022",
  "start_time": "2025-03-22T14:30:22.123456",
  "end_time": "2025-03-22T14:35:45.789012",
  "total_keystrokes": 245,
  "keystrokes": [
    {
      "timestamp": "2025-03-22T14:30:22.234567",
      "key": "H",
      "key_type": "character",
      "raw_value": "'H'"
    },
    {
      "timestamp": "2025-03-22T14:30:22.345678",
      "key": "e",
      "key_type": "character",
      "raw_value": "'e'"
    },
    {
      "timestamp": "2025-03-22T14:30:22.456789",
      "key": "l",
      "key_type": "character",
      "raw_value": "'l'"
    }
  ]
}
```

### Encryption Implementation

- **Algorithm**: AES-256 via Fernet (symmetric encryption)
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Key Storage**: Derived from environment variable or default key
- **File Format**: Encrypted logs use `.enc` extension

## Troubleshooting

### Common Issues

#### Application won't start

**Solution**: Verify Python version (3.8+) and installed dependencies

```bash
python --version
pip list | grep -E "pynput|customtkinter|cryptography"
```

#### Keyboard not capturing

**Solution**: Run with administrator/sudo privileges if required by OS

```bash
# Linux/macOS
sudo python app.py

# Windows (run as administrator)
```

#### Encryption errors

**Solution**: Ensure cryptography package is installed correctly

```bash
pip install --upgrade cryptography
```

#### GUI display issues

**Solution**: Update CustomTkinter

```bash
pip install --upgrade customtkinter
```

### Log Files

Logs are stored in the `logs/` directory. To troubleshoot:

1. Check log files for error messages
2. Verify write permissions to logs directory
3. Clear old logs if storage is limited

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 Keylogger Simulator Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Version History

| Version | Date | Features |
|---------|------|----------|
| 1.0.0 | 2025-03 | Core functionality, GUI, encryption |
| 1.1.0 | 2025-03 | Log viewer, search, export features |
| 1.2.0 | 2025-03 | Enhanced interface and performance improvements |
```
