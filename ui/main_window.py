"""
Main GUI Window Module
Professional user interface using CustomTkinter
"""

import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from typing import Optional

import customtkinter as ctk

from core.keylogger_engine import KeyloggerEngine
from ui.log_viewer import LogViewerWindow


# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow:
    """
    Main application window with modern professional interface.
    """
    
    # Professional color scheme
    COLORS = {
        'primary': '#1a237e',      # Deep indigo
        'secondary': '#00897b',    # Teal
        'accent': '#ffa000',       # Amber
        'background': '#2c3e50',   # Dark slate
        'surface': '#34495e',      # Lighter slate
        'text': '#ecf0f1',         # Light gray
        'success': '#27ae60',      # Green
        'danger': '#e74c3c',       # Red
        'warning': '#f39c12',      # Orange
        'info': '#3498db'          # Blue
    }
    
    def __init__(self):
        """Initialize the main application window."""
        self.root = ctk.CTk()
        self.root.title("Keylogger Simulator - Security Education Tool")
        self.root.geometry("1100x800")
        
        # Set color theme
        self.root.configure(fg_color=self.COLORS['background'])
        
        # Initialize core engine
        self.keylogger = KeyloggerEngine(encryption_enabled=False)
        self.keylogger.on_key_pressed_callback = self._update_live_display
        
        # Application state
        self.is_logging = False
        self.keystroke_count = 0
        
        # Build UI
        self._setup_ui()
        
        # Show safety warning on startup
        self._show_safety_warning()
    
    def _setup_ui(self):
        """Build the complete user interface."""
        
        # Main container with padding
        main_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self._create_header(main_container)
        
        # Control panel section
        self._create_control_panel(main_container)
        
        # Status panel section
        self._create_status_panel(main_container)
        
        # Live display section
        self._create_live_display(main_container)
        
        # Log management section
        self._create_log_management(main_container)
        
        # Security info section (collapsible)
        self._create_security_section(main_container)
    
    def _create_header(self, parent):
        """Create application header with title and description."""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['primary'],
            corner_radius=10
        )
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="KEYLOGGER SIMULATOR",
            font=("Arial", 28, "bold"),
            text_color=self.COLORS['text']
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Educational Tool for Understanding Keystroke Logging Security",
            font=("Arial", 12),
            text_color=self.COLORS['text']
        )
        subtitle_label.pack(pady=(0, 20))
        
        warning_label = ctk.CTkLabel(
            header_frame,
            text="FOR EDUCATIONAL PURPOSES ONLY - Use only on systems you own",
            font=("Arial", 10),
            text_color=self.COLORS['warning']
        )
        warning_label.pack(pady=(0, 20))
    
    def _create_control_panel(self, parent):
        """Create control buttons panel."""
        control_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        control_frame.pack(fill="x", pady=(0, 20))
        
        # Button container
        button_container = ctk.CTkFrame(
            control_frame,
            fg_color="transparent"
        )
        button_container.pack(pady=15, padx=15)
        
        # Start button
        self.start_button = ctk.CTkButton(
            button_container,
            text="START LOGGING",
            command=self._start_logging,
            height=45,
            width=150,
            font=("Arial", 14, "bold"),
            fg_color=self.COLORS['success'],
            hover_color="#219a52"
        )
        self.start_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            button_container,
            text="STOP LOGGING",
            command=self._stop_logging,
            height=45,
            width=150,
            font=("Arial", 14, "bold"),
            fg_color=self.COLORS['danger'],
            hover_color="#c0392b",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # View logs button
        view_logs_button = ctk.CTkButton(
            button_container,
            text="VIEW LOGS",
            command=self._open_log_viewer,
            height=45,
            width=150,
            font=("Arial", 14),
            fg_color=self.COLORS['info'],
            hover_color="#2980b9"
        )
        view_logs_button.pack(side="left", padx=10)
        
        # Export button
        export_button = ctk.CTkButton(
            button_container,
            text="EXPORT ALL",
            command=self._export_all_logs,
            height=45,
            width=150,
            font=("Arial", 14),
            fg_color=self.COLORS['secondary'],
            hover_color="#00695c"
        )
        export_button.pack(side="left", padx=10)
        
        # Clear display button
        clear_button = ctk.CTkButton(
            button_container,
            text="CLEAR DISPLAY",
            command=self._clear_display,
            height=45,
            width=150,
            font=("Arial", 14),
            fg_color=self.COLORS['primary'],
            hover_color="#0d174e"
        )
        clear_button.pack(side="left", padx=10)
        
        # Encryption toggle
        self.encryption_var = tk.BooleanVar(value=False)
        encryption_check = ctk.CTkCheckBox(
            button_container,
            text="ENABLE ENCRYPTION (Educational)",
            variable=self.encryption_var,
            command=self._toggle_encryption,
            font=("Arial", 12)
        )
        encryption_check.pack(side="right", padx=10)
    
    def _create_status_panel(self, parent):
        """Create status indicator panel."""
        status_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        status_frame.pack(fill="x", pady=(0, 20))
        
        status_container = ctk.CTkFrame(
            status_frame,
            fg_color="transparent"
        )
        status_container.pack(pady=15, padx=15, fill="x")
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            status_container,
            text="● STOPPED",
            font=("Arial", 14, "bold"),
            text_color=self.COLORS['danger']
        )
        self.status_indicator.pack(side="left", padx=20)
        
        # Session info
        self.session_label = ctk.CTkLabel(
            status_container,
            text="No active session",
            font=("Arial", 12),
            text_color=self.COLORS['text']
        )
        self.session_label.pack(side="left", padx=20)
        
        # Keystroke counter
        self.counter_label = ctk.CTkLabel(
            status_container,
            text="Keystrokes: 0",
            font=("Arial", 12, "bold"),
            text_color=self.COLORS['accent']
        )
        self.counter_label.pack(side="right", padx=20)
    
    def _create_live_display(self, parent):
        """Create live keystroke display area."""
        display_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        display_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header
        header_label = ctk.CTkLabel(
            display_frame,
            text="LIVE KEYSTROKE DISPLAY",
            font=("Arial", 14, "bold"),
            text_color=self.COLORS['accent']
        )
        header_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Text area with scrollbar
        text_container = ctk.CTkFrame(
            display_frame,
            fg_color="transparent"
        )
        text_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.display_text = ctk.CTkTextbox(
            text_container,
            font=("Courier New", 11),
            wrap="word",
            fg_color=self.COLORS['background']
        )
        self.display_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ctk.CTkScrollbar(
            text_container,
            command=self.display_text.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.display_text.configure(yscrollcommand=scrollbar.set)
    
    def _create_log_management(self, parent):
        """Create log management section with search and filter."""
        management_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        management_frame.pack(fill="x", pady=(0, 20))
        
        management_container = ctk.CTkFrame(
            management_frame,
            fg_color="transparent"
        )
        management_container.pack(pady=15, padx=15, fill="x")
        
        # Search section
        search_label = ctk.CTkLabel(
            management_container,
            text="SEARCH LOGS:",
            font=("Arial", 12, "bold"),
            text_color=self.COLORS['text']
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            management_container,
            width=250,
            placeholder_text="Enter search term..."
        )
        self.search_entry.pack(side="left", padx=5)
        
        search_button = ctk.CTkButton(
            management_container,
            text="SEARCH",
            command=self._perform_search,
            width=100,
            fg_color=self.COLORS['info']
        )
        search_button.pack(side="left", padx=5)
        
        # Case sensitive toggle
        self.case_sensitive_var = tk.BooleanVar(value=False)
        case_check = ctk.CTkCheckBox(
            management_container,
            text="Case Sensitive",
            variable=self.case_sensitive_var,
            font=("Arial", 11)
        )
        case_check.pack(side="left", padx=10)
        
        # Search results label
        self.search_results_label = ctk.CTkLabel(
            management_container,
            text="",
            font=("Arial", 11),
            text_color=self.COLORS['accent']
        )
        self.search_results_label.pack(side="right", padx=10)
    
    def _create_security_section(self, parent):
        """Create collapsible security awareness section."""
        security_frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        security_frame.pack(fill="x")
        
        # Toggle button
        self.security_toggle = ctk.CTkButton(
            security_frame,
            text="▼ SECURITY AWARENESS INFORMATION",
            command=self._toggle_security_info,
            fg_color="transparent",
            text_color=self.COLORS['info'],
            height=40,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        self.security_toggle.pack(fill="x", padx=15, pady=10)
        
        # Information content (initially hidden)
        self.security_content = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS['surface'],
            corner_radius=10
        )
        self.security_shown = False
        
        # Text widget for security content
        from core.security import SecurityAwarenessContent
        self.security_text = ctk.CTkTextbox(
            self.security_content,
            font=("Arial", 11),
            wrap="word",
            height=400
        )
        self.security_text.pack(fill="both", expand=True, padx=15, pady=15)
        self.security_text.insert("1.0", SecurityAwarenessContent.get_comprehensive_guide())
        self.security_text.configure(state="disabled")
    
    def _toggle_security_info(self):
        """Toggle security information panel visibility."""
        if self.security_shown:
            self.security_content.pack_forget()
            self.security_toggle.configure(text="▼ SECURITY AWARENESS INFORMATION")
            self.security_shown = False
        else:
            self.security_content.pack(fill="x", pady=(0, 20))
            self.security_toggle.configure(text="▲ SECURITY AWARENESS INFORMATION")
            self.security_shown = True
    
    def _show_safety_warning(self):
        """Display safety warning dialog on startup."""
        warning_text = (
            "SAFETY WARNING\n\n"
            "This tool is designed for EDUCATIONAL PURPOSES ONLY.\n\n"
            "IMPORTANT:\n"
            "• Only use this software on systems you own\n"
            "• Never use to monitor others without explicit written consent\n"
            "• Keyloggers are illegal when installed without permission\n"
            "• This tool demonstrates security concepts for defensive purposes\n\n"
            "Do you understand and agree to use this tool responsibly?"
        )
        
        response = messagebox.askyesno(
            "Responsible Use Agreement",
            warning_text,
            icon="warning"
        )
        
        if not response:
            self.root.destroy()
            import sys
            sys.exit(0)
    
    def _start_logging(self):
        """Start the keylogging session."""
        try:
            self.keylogger.start_logging()
            self.is_logging = True
            
            # Update UI
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_indicator.configure(
                text="● RUNNING",
                text_color=self.COLORS['success']
            )
            self.session_label.configure(
                text=f"Session: {self.keylogger.current_session_id}"
            )
            
            self.display_text.insert("end", f"=== Session Started: {self.keylogger.current_session_id} ===\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start logging: {e}")
    
    def _stop_logging(self):
        """Stop the keylogging session."""
        try:
            self.keylogger.stop_logging()
            self.is_logging = False
            
            # Update UI
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_indicator.configure(
                text="● STOPPED",
                text_color=self.COLORS['danger']
            )
            
            self.display_text.insert("end", f"\n=== Session Stopped: {self.keylogger.current_session_id} ===\n")
            
            messagebox.showinfo(
                "Session Saved",
                f"Session {self.keylogger.current_session_id} saved successfully."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop logging: {e}")
    
    def _update_live_display(self, keystroke: str):
        """Update live display with new keystroke."""
        if not self.is_logging:
            return
        
        self.display_text.insert("end", keystroke)
        self.display_text.see("end")
        
        # Update counter
        self.keystroke_count += 1
        self.counter_label.configure(text=f"Keystrokes: {self.keystroke_count}")
    
    def _clear_display(self):
        """Clear the live display area."""
        self.display_text.delete("1.0", "end")
        self.keystroke_count = 0
        self.counter_label.configure(text="Keystrokes: 0")
    
    def _open_log_viewer(self):
        """Open the log viewer window."""
        try:
            LogViewerWindow(self.root, self.keylogger)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log viewer: {e}")
    
    def _export_all_logs(self):
        """Export all logs to a selected directory."""
        log_files = self.keylogger.get_log_files()
        
        if not log_files:
            messagebox.showinfo("No Logs", "No logs available to export.")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        export_path = Path(export_dir)
        exported_count = 0
        
        for log_file in log_files:
            try:
                output_path = export_path / f"{log_file}_export.txt"
                self.keylogger.export_log_to_text(log_file, str(output_path))
                exported_count += 1
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export {log_file}: {e}")
        
        messagebox.showinfo(
            "Export Complete",
            f"Successfully exported {exported_count} log files to:\n{export_dir}"
        )
    
    def _perform_search(self):
        """Perform search across logs."""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.search_results_label.configure(text="Please enter a search term")
            return
        
        case_sensitive = self.case_sensitive_var.get()
        
        try:
            results = self.keylogger.search_logs(search_term, case_sensitive)
            
            if results:
                self.search_results_label.configure(
                    text=f"Found {len(results)} matches across {len(set(r['session_id'] for r in results))} sessions"
                )
                
                # Option to view results
                if messagebox.askyesno("Search Results", f"Found {len(results)} matches. Open Log Viewer to see details?"):
                    self._open_log_viewer()
            else:
                self.search_results_label.configure(text="No matches found")
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Search failed: {e}")
    
    def _toggle_encryption(self):
        """Toggle encryption feature with restart notification."""
        enabled = self.encryption_var.get()
        
        if enabled and not self.keylogger.encryption_enabled:
            response = messagebox.askyesno(
                "Enable Encryption",
                "Enabling encryption will encrypt all future log files.\n\n"
                "This demonstrates how encryption protects sensitive data.\n"
                "Existing logs will remain unencrypted.\n\n"
                "Continue?"
            )
            if response:
                self.keylogger.encryption_enabled = True
                messagebox.showinfo(
                    "Encryption Enabled",
                    "Encryption is now enabled for new log sessions.\n\n"
                    "Note: This is an educational demonstration. In production,\n"
                    "proper key management and secure storage would be required."
                )
        elif not enabled and self.keylogger.encryption_enabled:
            response = messagebox.askyesno(
                "Disable Encryption",
                "Disabling encryption will store future logs in plain text.\n\n"
                "Continue?"
            )
            if response:
                self.keylogger.encryption_enabled = False
    
    def run(self):
        """Run the application main loop."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()
    
    def _on_closing(self):
        """Handle application closing event."""
        if self.is_logging:
            response = messagebox.askyesno(
                "Logging Active",
                "Keylogging session is still active. Stop and save before closing?"
            )
            if response:
                self._stop_logging()
                self.root.destroy()
            else:
                return
        else:
            self.root.destroy()