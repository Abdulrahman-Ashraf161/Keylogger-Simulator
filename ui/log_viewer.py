"""
Log Viewer Window Module
Professional log viewing and management interface
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Dict, Any

import customtkinter as ctk

from core.keylogger_engine import KeyloggerEngine


class LogViewerWindow:
    """
    Dedicated window for viewing, searching, and managing logs.
    """
    
    COLORS = {
        'primary': '#1a237e',
        'secondary': '#00897b',
        'accent': '#ffa000',
        'background': '#2c3e50',
        'surface': '#34495e',
        'text': '#ecf0f1',
        'success': '#27ae60',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db'
    }
    
    def __init__(self, parent, keylogger: KeyloggerEngine):
        """
        Initialize the log viewer window.
        
        Args:
            parent: Parent Tkinter window
            keylogger: KeyloggerEngine instance
        """
        self.parent = parent
        self.keylogger = keylogger
        
        # Create window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Log Viewer - Keylogger Simulator")
        self.window.geometry("1000x700")
        self.window.configure(fg_color=self.COLORS['background'])
        
        self.current_log_data: Optional[Dict[str, Any]] = None
        self.current_filename: Optional[str] = None
        
        self._setup_ui()
        self._refresh_log_list()
    
    def _setup_ui(self):
        """Build the log viewer interface."""
        
        # Main container
        main_container = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Log list
        left_panel = ctk.CTkFrame(
            main_container,
            fg_color=self.COLORS['surface'],
            corner_radius=10,
            width=250
        )
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Log list header
        header_label = ctk.CTkLabel(
            left_panel,
            text="AVAILABLE LOGS",
            font=("Arial", 14, "bold"),
            text_color=self.COLORS['accent']
        )
        header_label.pack(pady=(15, 10))
        
        # Refresh button
        refresh_button = ctk.CTkButton(
            left_panel,
            text="REFRESH LIST",
            command=self._refresh_log_list,
            height=30,
            fg_color=self.COLORS['info']
        )
        refresh_button.pack(pady=(0, 10), padx=10)
        
        # Log listbox with scrollbar
        list_container = ctk.CTkFrame(
            left_panel,
            fg_color="transparent"
        )
        list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_listbox = tk.Listbox(
            list_container,
            bg=self.COLORS['background'],
            fg=self.COLORS['text'],
            selectbackground=self.COLORS['accent'],
            selectforeground=self.COLORS['background'],
            font=("Arial", 10),
            height=20
        )
        self.log_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_container, command=self.log_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_listbox.config(yscrollcommand=scrollbar.set)
        
        self.log_listbox.bind('<<ListboxSelect>>', self._on_log_select)
        
        # Right panel - Log content
        right_panel = ctk.CTkFrame(
            main_container,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Log info header
        self.info_frame = ctk.CTkFrame(
            right_panel,
            fg_color="transparent"
        )
        self.info_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        self.log_info_label = ctk.CTkLabel(
            self.info_frame,
            text="No log selected",
            font=("Arial", 12, "bold"),
            text_color=self.COLORS['text']
        )
        self.log_info_label.pack(side="left")
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.info_frame,
            text="EXPORT AS TEXT",
            command=self._export_current_log,
            height=30,
            width=120,
            fg_color=self.COLORS['secondary'],
            state="disabled"
        )
        self.export_button.pack(side="right")
        
        # Search bar
        search_frame = ctk.CTkFrame(
            right_panel,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="SEARCH IN LOG:",
            font=("Arial", 11)
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Enter text to search..."
        )
        self.search_entry.pack(side="left", padx=5)
        
        search_button = ctk.CTkButton(
            search_frame,
            text="FIND",
            command=self._search_in_log,
            width=80,
            fg_color=self.COLORS['info']
        )
        search_button.pack(side="left", padx=5)
        
        # Log content display
        self.content_text = ctk.CTkTextbox(
            right_panel,
            font=("Courier New", 10),
            wrap="word"
        )
        self.content_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def _refresh_log_list(self):
        """Refresh the list of available log files."""
        self.log_listbox.delete(0, tk.END)
        
        log_files = self.keylogger.get_log_files()
        
        if not log_files:
            self.log_listbox.insert(tk.END, "No logs available")
        else:
            for log_file in log_files:
                # Extract session ID from filename
                session_id = log_file.replace('.json', '').replace('.enc', '')
                self.log_listbox.insert(tk.END, session_id)
    
    def _on_log_select(self, event):
        """Handle log selection from listbox."""
        selection = self.log_listbox.curselection()
        
        if not selection:
            return
        
        selected = self.log_listbox.get(selection[0])
        
        if selected == "No logs available":
            return
        
        # Find the actual filename
        log_files = self.keylogger.get_log_files()
        for log_file in log_files:
            if selected in log_file:
                self.current_filename = log_file
                break
        
        if self.current_filename:
            self._load_log(self.current_filename)
    
    def _load_log(self, filename: str):
        """
        Load and display a log file.
        
        Args:
            filename: Name of the log file to load
        """
        try:
            log_data = self.keylogger.read_log_file(filename)
            self.current_log_data = log_data
            
            # Update info display
            info_text = (
                f"Session: {log_data['session_id']} | "
                f"Keystrokes: {log_data['total_keystrokes']} | "
                f"Start: {log_data['start_time'][:19]}"
            )
            self.log_info_label.configure(text=info_text)
            
            # Enable export button
            self.export_button.configure(state="normal")
            
            # Display content
            self._display_log_content(log_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log: {e}")
            self.log_info_label.configure(text="Error loading log")
    
    def _display_log_content(self, log_data: Dict[str, Any]):
        """
        Display log content in the text area.
        
        Args:
            log_data: Parsed log data dictionary
        """
        self.content_text.delete("1.0", "end")
        
        # Header
        self.content_text.insert("end", "=" * 70 + "\n")
        self.content_text.insert("end", "KEYSTROKE LOG DETAILS\n")
        self.content_text.insert("end", "=" * 70 + "\n\n")
        
        self.content_text.insert("end", f"Session ID: {log_data['session_id']}\n")
        self.content_text.insert("end", f"Start Time: {log_data['start_time']}\n")
        self.content_text.insert("end", f"End Time: {log_data['end_time']}\n")
        self.content_text.insert("end", f"Total Keystrokes: {log_data['total_keystrokes']}\n\n")
        
        # Keystroke sequence
        self.content_text.insert("end", "=" * 70 + "\n")
        self.content_text.insert("end", "KEYSTROKE SEQUENCE\n")
        self.content_text.insert("end", "=" * 70 + "\n\n")
        
        sequence = ''.join(stroke['key'] for stroke in log_data['keystrokes'])
        self.content_text.insert("end", sequence + "\n\n")
        
        # Detailed timestamp log
        self.content_text.insert("end", "=" * 70 + "\n")
        self.content_text.insert("end", "DETAILED TIMESTAMP LOG\n")
        self.content_text.insert("end", "=" * 70 + "\n\n")
        
        for stroke in log_data['keystrokes']:
            self.content_text.insert("end", f"[{stroke['timestamp']}] {stroke['key']}\n")
    
    def _search_in_log(self):
        """Search for text within the current log."""
        if not self.current_log_data:
            messagebox.showinfo("No Log", "Please select a log file first")
            return
        
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term")
            return
        
        # Search through keystrokes
        results = []
        for stroke in self.current_log_data['keystrokes']:
            if search_term.lower() in stroke['key'].lower():
                results.append(stroke)
        
        if results:
            # Highlight and show results
            self.content_text.tag_remove("highlight", "1.0", "end")
            
            # Configure highlight tag
            self.content_text.tag_config("highlight", background=self.COLORS['warning'], foreground="black")
            
            # Find and highlight occurrences
            content = self.content_text.get("1.0", "end")
            start_idx = "1.0"
            
            while True:
                start_idx = self.content_text.search(search_term, start_idx, "end", nocase=True)
                if not start_idx:
                    break
                
                end_idx = f"{start_idx}+{len(search_term)}c"
                self.content_text.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
            
            messagebox.showinfo("Search Results", f"Found {len(results)} matching keystrokes")
        else:
            messagebox.showinfo("Search Results", "No matches found")
    
    def _export_current_log(self):
        """Export the current log to text format."""
        if not self.current_filename:
            messagebox.showinfo("No Log", "No log selected for export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            output_path = f"{export_dir}/{self.current_filename}_export.txt"
            self.keylogger.export_log_to_text(self.current_filename, output_path)
            messagebox.showinfo("Export Complete", f"Log exported to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")