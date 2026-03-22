#!/usr/bin/env python3
"""
Keylogger Simulator - Main Application Entry Point
Educational tool for understanding keystroke logging security
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """
    Main application entry point.
    """
    print("=" * 60)
    print("KEYLOGGER SIMULATOR - Educational Security Tool")
    print("=" * 60)
    print("\nIMPORTANT: This tool is for educational purposes only.")
    print("Only use on systems you own or have explicit permission.")
    print("\nStarting application...\n")
    
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()