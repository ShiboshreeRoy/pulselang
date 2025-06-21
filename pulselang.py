import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, colorchooser
import webbrowser
import random
import time
import os
import json
import threading
import socket
import hashlib
import zlib
import winsound
from datetime import datetime
from PIL import Image, ImageTk
import pyperclip

# PulseLang mappings with extended symbols
PULSE_MAP = {
    'A': '^~', 'B': '~^^^', 'C': '~^~^', 'D': '~^^', 'E': '^',
    'F': '^^~^', 'G': '~~^', 'H': '^^^', 'I': '~^', 'J': '^~~~',
    'K': '~^~', 'L': '^~^^', 'M': '~~', 'N': '~^', 'O': '~~~',
    'P': '^~~^', 'Q': '~~^~', 'R': '^~^', 'S': '^^^', 'T': '~',
    'U': '^^~', 'V': '^^^~', 'W': '^~~', 'X': '~^^~', 'Y': '~^~~',
    'Z': '~~^^', '1': '^~***', '2': '^^~**', '3': '^^^~*',
    '4': '^^^^~', '5': '~~~~^', ' ': '_', '!': '~*~', '?': '^*^',
    '.': '~~*', ',': '~*~*', '@': '^~*~', '#': '~#~', '$': '$$$',
    '%': '~%~', '&': '~&~', '(': '~(~', ')': '~)~', '+': '~+~',
    '-': '~-~', '=': '~=~', '/': '~/~', '\\': '~\\~', '|': '~|~',
    '<': '~<~', '>': '~>~', '"': '~"~', "'": "~'~", ':': '~:~',
    ';': '~;~', '[': '~[~', ']': '~]~', '{': '~{~', '}': '~}~',
    '0': '~00~', '6': '~66~', '7': '~77~', '8': '~88~', '9': '~99~',
    'Ω': '~Ω~', 'π': '~π~', '∞': '~∞~', '©': '~©~', '®': '~®~',
    '✓': '~✓~', '✗': '~✗~', '→': '~→~', '←': '~←~', '↑': '~↑~', '↓': '~↓~'
}

REVERSE_MAP = {v: k for k, v in PULSE_MAP.items()}

# Enhanced Encoder function with compression and encryption
def encode_to_pulse(text, compression_level=6, obfuscate=False):
    try:
        # Apply compression if requested
        if compression_level > 0:
            text_bytes = text.encode('utf-8')
            compressed = zlib.compress(text_bytes, compression_level)
            text = compressed.hex()
        
        encoded_chars = []
        for c in text.upper():
            if c in PULSE_MAP:
                encoded_chars.append(PULSE_MAP[c])
            else:
                encoded_chars.append(f'?{ord(c)}?')  # mark unknown chars with their ASCII code
        
        result = '[' + '_'.join(encoded_chars) + ']'
        
        # Add obfuscation layer
        if obfuscate:
            result = ''.join(random.choice(['', ' ', '\t']) + result + ''.join(random.choice(['', ' ', '\t'])))
            result = result.replace('~', random.choice(['~', '≈', '∽', '∿']))
            result = result.replace('^', random.choice(['^', '↑', 'Δ', '∧']))
        
        return result
    except Exception as e:
        return f"ENCODING ERROR: {str(e)}"

# Enhanced Decoder function with decompression and error handling
def decode_pulse(pulse, decompress=False):
    try:
        # Clean the input
        pulse = pulse.strip('[] \t\n')
        
        # Handle obfuscated characters
        pulse = pulse.replace('≈', '~').replace('∽', '~').replace('∿', '~')
        pulse = pulse.replace('↑', '^').replace('Δ', '^').replace('∧', '^')
        
        parts = pulse.split('_')
        decoded_chars = []
        for part in parts:
            if part in REVERSE_MAP:
                decoded_chars.append(REVERSE_MAP[part])
            elif part.startswith('?') and part.endswith('?'):
                try:
                    char_code = int(part[1:-1])
                    decoded_chars.append(chr(char_code))
                except:
                    decoded_chars.append('�')
            else:
                decoded_chars.append('�')  # replacement character for errors
        
        result = ''.join(decoded_chars)
        
        # Apply decompression if needed
        if decompress:
            try:
                # Check if the result looks like hex data
                if all(c in "0123456789abcdefABCDEF" for c in result):
                    compressed_bytes = bytes.fromhex(result)
                    decompressed = zlib.decompress(compressed_bytes)
                    result = decompressed.decode('utf-8')
            except:
                pass
        
        return result
    except Exception as e:
        return f"DECODING ERROR: {str(e)}"

# Tkinter app with hacker theme and advanced features
class PulseLangGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PULSE LANG v3.0 - SECURE ENCODER")
        self.geometry("1200x700")
        self.configure(bg="#0a0a12", padx=10, pady=10)
        self.minsize(1000, 600)
        
        # Set hacker theme colors
        self.bg_color = "#0a0a12"
        self.fg_color = "#00ff41"  # Matrix green
        self.accent_color = "#ff00ff"  # Cyberpunk purple
        self.error_color = "#ff0033"
        self.warning_color = "#ffcc00"
        self.text_bg = "#0f0f1a"
        self.button_bg = "#1a1a2e"
        
        # Load settings
        self.settings = self.load_settings()
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Consolas', 10))
        self.style.configure('TButton', background=self.button_bg, foreground=self.fg_color, 
                            font=('Consolas', 9, 'bold'), borderwidth=1)
        self.style.map('TButton', 
                      background=[('active', self.accent_color), ('pressed', self.accent_color)],
                      foreground=[('active', 'white'), ('pressed', 'white')])
        self.style.configure('TLabelFrame', background=self.bg_color, foreground=self.accent_color,
                           font=('Consolas', 10, 'bold'))
        self.style.configure('TEntry', fieldbackground=self.text_bg, foreground=self.fg_color)
        
        # Create main frames
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill='x', pady=(0, 10))
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill='x', pady=(5, 0))
        
        # Create header with hacker aesthetic
        self.create_header()
        
        # Create main content
        self.create_encoder_section()
        self.create_decoder_section()
        
        # Create advanced options panel
        self.create_advanced_panel()
        
        # Create status bar
        self.create_status_bar()
        
        # Create terminal output
        self.create_terminal()
        
        # Create history panel
        self.create_history_panel()
        
        # Start terminal animation
        self.terminal_text = ""
        self.terminal_animation()
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Set initial values
        self.log_action("System initialized")
        self.log_action("PulseLang v3.0 online")
        self.log_action("Ready for secure encoding")
        self.log_action(f"Developer: Shiboshree Roy")
        self.log_action(f"Session ID: {hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}")
        
        # Initialize history
        self.history = []
        
        # Start network monitoring thread
        self.network_monitor_active = True
        threading.Thread(target=self.network_monitor, daemon=True).start()
        
        # Play startup sound
        self.play_sound("startup")
    
    def load_settings(self):
        """Load application settings from file"""
        settings = {
            "theme": "matrix",
            "compression": 6,
            "obfuscate": False,
            "auto_decode": True,
            "sound_effects": True,
            "history_size": 50
        }
        
        try:
            if os.path.exists("pulselang_settings.json"):
                with open("pulselang_settings.json", "r") as f:
                    loaded = json.load(f)
                    settings.update(loaded)
        except:
            pass
            
        return settings
    
    def save_settings(self):
        """Save application settings to file"""
        try:
            with open("pulselang_settings.json", "w") as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def play_sound(self, sound_type):
        """Play system sound effect"""
        if not self.settings.get("sound_effects", True):
            return
            
        try:
            if sound_type == "encode":
                winsound.Beep(800, 200)
                winsound.Beep(1200, 100)
            elif sound_type == "decode":
                winsound.Beep(1200, 200)
                winsound.Beep(800, 100)
            elif sound_type == "error":
                winsound.Beep(300, 500)
            elif sound_type == "warning":
                winsound.Beep(600, 300)
                winsound.Beep(400, 300)
            elif sound_type == "success":
                winsound.Beep(1000, 100)
                winsound.Beep(1500, 100)
                winsound.Beep(2000, 100)
            elif sound_type == "startup":
                winsound.Beep(400, 100)
                winsound.Beep(800, 100)
                winsound.Beep(1200, 100)
        except:
            pass
    
    def create_header(self):
        # Title with hacker aesthetic
        title_label = ttk.Label(self.header_frame, 
                              text="PULSE LANG v3.0", 
                              font=('Courier New', 24, 'bold'),
                              foreground=self.accent_color)
        title_label.pack(side='left', padx=10)
        
        # Developer credit
        dev_label = ttk.Label(self.header_frame, 
                            text="Developed by Shiboshree Roy", 
                            font=('Courier New', 9),
                            foreground="#00ccff")
        dev_label.pack(side='left', padx=10, pady=(5, 0))
        
        # Create buttons on the right
        button_frame = ttk.Frame(self.header_frame)
        button_frame.pack(side='right', padx=10)
        
        # Create buttons with hacker names
        buttons = [
            ("SEND PULSE", self.send_pulse),
            ("ANALYZE", self.analyze_signal),
            ("SETTINGS", self.show_settings),
            ("CLEAR", self.clear_all),
            ("ABOUT", self.show_about)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=12)
            btn.pack(side='left', padx=5)
        
        # Add a visual separator
        sep = ttk.Separator(self.header_frame, orient='vertical')
        sep.pack(side='right', fill='y', padx=10)
    
    def create_encoder_section(self):
        # Encoder frame
        encoder_frame = ttk.LabelFrame(self.main_frame, text="ENCODER")
        encoder_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Input label
        input_label = ttk.Label(encoder_frame, text="INPUT TEXT:")
        input_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Input text area with scrollbar
        input_frame = ttk.Frame(encoder_frame)
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.encoder_input = scrolledtext.ScrolledText(
            input_frame, 
            height=8, 
            bg=self.text_bg, 
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Consolas', 10),
            relief='flat'
        )
        self.encoder_input.pack(fill='both', expand=True)
        
        # Button panel
        btn_frame = ttk.Frame(encoder_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        encode_btn = ttk.Button(btn_frame, text="ENCODE →", command=self.encode_text, width=10)
        encode_btn.pack(side='left', padx=2)
        
        clear_input_btn = ttk.Button(btn_frame, text="CLEAR", command=self.clear_encoder_input, width=8)
        clear_input_btn.pack(side='left', padx=2)
        
        load_file_btn = ttk.Button(btn_frame, text="LOAD FILE", command=self.load_text_file, width=10)
        load_file_btn.pack(side='right', padx=2)
        
        # Output label
        output_label = ttk.Label(encoder_frame, text="PULSE OUTPUT:")
        output_label.pack(anchor='w', padx=5, pady=(10, 0))
        
        # Output text area
        self.encoder_output = scrolledtext.ScrolledText(
            encoder_frame, 
            height=6, 
            bg=self.text_bg, 
            fg=self.fg_color,
            font=('Consolas', 10),
            relief='flat'
        )
        self.encoder_output.pack(fill='x', padx=5, pady=5)
        self.encoder_output.config(state='disabled')
        
        # Button panel for output
        output_btn_frame = ttk.Frame(encoder_frame)
        output_btn_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        copy_btn = ttk.Button(output_btn_frame, text="COPY", command=self.copy_encoded, width=8)
        copy_btn.pack(side='left', padx=2)
        
        save_btn = ttk.Button(output_btn_frame, text="SAVE", command=self.save_encoded_file, width=8)
        save_btn.pack(side='left', padx=2)
        
        qr_btn = ttk.Button(output_btn_frame, text="GENERATE QR", command=self.generate_qr, width=12)
        qr_btn.pack(side='right', padx=2)
    
    def create_decoder_section(self):
        # Decoder frame
        decoder_frame = ttk.LabelFrame(self.main_frame, text="DECODER")
        decoder_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Input label
        input_label = ttk.Label(decoder_frame, text="PULSE INPUT:")
        input_label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Input text area with scrollbar
        input_frame = ttk.Frame(decoder_frame)
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.decoder_input = scrolledtext.ScrolledText(
            input_frame, 
            height=8, 
            bg=self.text_bg, 
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Consolas', 10),
            relief='flat'
        )
        self.decoder_input.pack(fill='both', expand=True)
        
        # Button panel
        btn_frame = ttk.Frame(decoder_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        decode_btn = ttk.Button(btn_frame, text="DECODE →", command=self.decode_text, width=10)
        decode_btn.pack(side='left', padx=2)
        
        clear_input_btn = ttk.Button(btn_frame, text="CLEAR", command=self.clear_decoder_input, width=8)
        clear_input_btn.pack(side='left', padx=2)
        
        paste_btn = ttk.Button(btn_frame, text="PASTE", command=self.paste_to_decoder, width=8)
        paste_btn.pack(side='right', padx=2)
        
        # Output label
        output_label = ttk.Label(decoder_frame, text="DECODED TEXT:")
        output_label.pack(anchor='w', padx=5, pady=(10, 0))
        
        # Output text area
        self.decoder_output = scrolledtext.ScrolledText(
            decoder_frame, 
            height=6, 
            bg=self.text_bg, 
            fg=self.fg_color,
            font=('Consolas', 10),
            relief='flat'
        )
        self.decoder_output.pack(fill='x', padx=5, pady=5)
        self.decoder_output.config(state='disabled')
        
        # Button panel for output
        output_btn_frame = ttk.Frame(decoder_frame)
        output_btn_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        copy_btn = ttk.Button(output_btn_frame, text="COPY", command=self.copy_decoded, width=8)
        copy_btn.pack(side='left', padx=2)
        
        save_btn = ttk.Button(output_btn_frame, text="SAVE", command=self.save_decoded_file, width=8)
        save_btn.pack(side='left', padx=2)
        
        analyze_btn = ttk.Button(output_btn_frame, text="ANALYZE", command=self.analyze_decoded, width=10)
        analyze_btn.pack(side='right', padx=2)
    
    def create_advanced_panel(self):
        # Advanced options frame
        advanced_frame = ttk.LabelFrame(self.main_frame, text="ADVANCED OPTIONS")
        advanced_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Create a notebook for tabs
        notebook = ttk.Notebook(advanced_frame)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Compression tab
        compression_frame = ttk.Frame(notebook)
        notebook.add(compression_frame, text="Compression")
        
        ttk.Label(compression_frame, text="Compression Level:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.compression_var = tk.IntVar(value=self.settings.get("compression", 6))
        compression_slider = ttk.Scale(compression_frame, from_=0, to=9, variable=self.compression_var, 
                                      orient='horizontal', length=200)
        compression_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(compression_frame, text="0 = No Compression, 1 = Fast, 9 = Best").grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='w')
        
        # Security tab
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        
        self.obfuscate_var = tk.BooleanVar(value=self.settings.get("obfuscate", False))
        ttk.Checkbutton(security_frame, text="Enable Obfuscation", variable=self.obfuscate_var).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.auto_decode_var = tk.BooleanVar(value=self.settings.get("auto_decode", True))
        ttk.Checkbutton(security_frame, text="Auto-Detect Compression", variable=self.auto_decode_var).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        # Theme tab
        theme_frame = ttk.Frame(notebook)
        notebook.add(theme_frame, text="Theme")
        
        themes = [
            ("Matrix Green", "matrix"),
            ("Cyber Red", "cyber_red"),
            ("Neon Blue", "neon_blue"),
            ("Hacker Classic", "hacker_classic")
        ]
        
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "matrix"))
        for i, (name, value) in enumerate(themes):
            rb = ttk.Radiobutton(theme_frame, text=name, variable=self.theme_var, value=value)
            rb.grid(row=i, column=0, padx=5, pady=2, sticky='w')
        
        ttk.Button(theme_frame, text="Custom Colors", command=self.choose_colors).grid(row=0, column=1, padx=5, pady=5)
        
        # Audio tab
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio")
        
        self.sound_var = tk.BooleanVar(value=self.settings.get("sound_effects", True))
        ttk.Checkbutton(audio_frame, text="Enable Sound Effects", variable=self.sound_var).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Apply button
        apply_btn = ttk.Button(advanced_frame, text="APPLY SETTINGS", command=self.apply_settings)
        apply_btn.pack(pady=5)
    
    def create_terminal(self):
        # Terminal output frame
        terminal_frame = ttk.LabelFrame(self.main_frame, text="SYSTEM TERMINAL")
        terminal_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.terminal_output = scrolledtext.ScrolledText(
            terminal_frame, 
            height=8, 
            bg="#001a00",  # Dark green background for terminal
            fg=self.fg_color,
            font=('Consolas', 9),
            relief='flat',
            state='disabled'
        )
        self.terminal_output.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Terminal controls
        terminal_controls = ttk.Frame(terminal_frame)
        terminal_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        ttk.Button(terminal_controls, text="CLEAR TERMINAL", command=self.clear_terminal).pack(side='left')
        ttk.Button(terminal_controls, text="EXPORT LOG", command=self.export_log).pack(side='right')
    
    def create_history_panel(self):
        # History frame
        history_frame = ttk.LabelFrame(self.main_frame, text="OPERATION HISTORY")
        history_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Create treeview for history
        columns = ("timestamp", "operation", "input_length", "output_length")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=5)
        
        # Define headings
        self.history_tree.heading("timestamp", text="Timestamp")
        self.history_tree.heading("operation", text="Operation")
        self.history_tree.heading("input_length", text="Input Length")
        self.history_tree.heading("output_length", text="Output Length")
        
        # Set column widths
        self.history_tree.column("timestamp", width=150)
        self.history_tree.column("operation", width=100)
        self.history_tree.column("input_length", width=100)
        self.history_tree.column("output_length", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add context menu
        self.history_menu = tk.Menu(self, tearoff=0)
        self.history_menu.add_command(label="View Details", command=self.view_history_details)
        self.history_menu.add_command(label="Delete Entry", command=self.delete_history_entry)
        self.history_menu.add_separator()
        self.history_menu.add_command(label="Clear History", command=self.clear_history)
        
        # Bind right-click event
        self.history_tree.bind("<Button-3>", self.show_history_menu)
    
    def create_status_bar(self):
        # Status bar at bottom
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill='x', pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("System Status: Ready")
        
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var, 
                               font=('Consolas', 9), foreground=self.warning_color)
        status_label.pack(side='left', padx=10)
        
        # Add network status
        self.network_var = tk.StringVar()
        self.network_var.set("Network: Checking...")
        network_label = ttk.Label(self.status_frame, textvariable=self.network_var,
                                font=('Consolas', 9), foreground="#00ff00")
        network_label.pack(side='left', padx=20)
        
        # Add a progress bar for visual effect
        self.progress = ttk.Progressbar(self.status_frame, orient='horizontal', 
                                      mode='determinate', length=200)
        self.progress.pack(side='right', padx=10)
        
        # Add connection status
        self.connection_var = tk.StringVar()
        self.connection_var.set("Connection: SECURE")
        connection_label = ttk.Label(self.status_frame, textvariable=self.connection_var,
                                   font=('Consolas', 9), foreground="#00ff00")
        connection_label.pack(side='right', padx=20)
    
    def log_action(self, message):
        """Add a message to the terminal output"""
        self.terminal_output.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.terminal_output.insert(tk.END, f"[{timestamp}] {message}\n")
        self.terminal_output.see(tk.END)
        self.terminal_output.config(state='disabled')
    
    def terminal_animation(self):
        """Animate the terminal with random hacker-like messages"""
        messages = [
            "Scanning network interfaces...",
            "Firewall status: ACTIVE",
            "Monitoring signal integrity...",
            "Encryption protocols engaged",
            "Analyzing frequency patterns...",
            "Signal modulation stable",
            "Decryption algorithms loaded",
            "No security threats detected",
            "Establishing secure channel...",
            "Data packets encrypted",
            "Running diagnostic checks...",
            "Security audit in progress...",
            "Quantum encryption initialized",
            "Neural network analysis started",
            "Validating cryptographic keys..."
        ]
        
        # Add a random message
        if random.random() < 0.3:  # 30% chance to add a message
            self.log_action(random.choice(messages))
        
        # Schedule next animation
        self.after(5000, self.terminal_animation)
    
    def network_monitor(self):
        """Monitor network status in background thread"""
        while self.network_monitor_active:
            try:
                # Try to resolve a known domain to check connectivity
                socket.gethostbyname("google.com")
                self.network_var.set("Network: ONLINE")
                self.status_frame.winfo_children()[1].configure(foreground="#00ff00")
            except:
                self.network_var.set("Network: OFFLINE")
                self.status_frame.winfo_children()[1].configure(foreground="#ff0000")
            
            time.sleep(10)
    
    def encode_text(self):
        text = self.encoder_input.get("1.0", tk.END).strip()
        if not text:
            self.log_action("ENCODE ERROR: No input text provided")
            self.status_var.set("Status: Encoding failed - no input")
            self.progress.configure(value=0)
            self.play_sound("error")
            return
        
        # Show progress animation
        self.progress.configure(value=25)
        self.update()
        self.play_sound("encode")
        
        try:
            compression = self.compression_var.get()
            obfuscate = self.obfuscate_var.get()
            
            encoded = encode_to_pulse(text, compression, obfuscate)
            self.progress.configure(value=75)
            
            # Enable output and insert result
            self.encoder_output.config(state='normal')
            self.encoder_output.delete("1.0", tk.END)
            self.encoder_output.insert(tk.END, encoded)
            self.encoder_output.config(state='disabled')
            
            self.progress.configure(value=100)
            self.log_action(f"Encoded {len(text)} characters (Compression: {compression}, Obfuscation: {'ON' if obfuscate else 'OFF'})")
            self.status_var.set("Status: Encoding successful")
            
            # Add to history
            self.add_to_history("Encode", text, encoded)
            
            # Schedule progress bar reset
            self.after(1500, lambda: self.progress.configure(value=0))
            
            self.play_sound("success")
            
        except Exception as e:
            self.log_action(f"ENCODE ERROR: {str(e)}")
            self.status_var.set("Status: Encoding failed")
            self.progress.configure(value=0)
            self.play_sound("error")
    
    def decode_text(self):
        code = self.decoder_input.get("1.0", tk.END).strip()
        if not code:
            self.log_action("DECODE ERROR: No input code provided")
            self.status_var.set("Status: Decoding failed - no input")
            self.progress.configure(value=0)
            self.play_sound("error")
            return
        
        # Show progress animation
        self.progress.configure(value=25)
        self.update()
        self.play_sound("decode")
        
        try:
            decompress = self.auto_decode_var.get()
            
            decoded = decode_pulse(code, decompress)
            self.progress.configure(value=75)
            
            # Enable output and insert result
            self.decoder_output.config(state='normal')
            self.decoder_output.delete("1.0", tk.END)
            self.decoder_output.insert(tk.END, decoded)
            self.decoder_output.config(state='disabled')
            
            self.progress.configure(value=100)
            self.log_action(f"Decoded {len(code)} characters (Auto-decompress: {'ON' if decompress else 'OFF'})")
            self.status_var.set("Status: Decoding successful")
            
            # Add to history
            self.add_to_history("Decode", code, decoded)
            
            # Schedule progress bar reset
            self.after(1500, lambda: self.progress.configure(value=0))
            
            self.play_sound("success")
            
        except Exception as e:
            self.log_action(f"DECODE ERROR: {str(e)}")
            self.status_var.set("Status: Decoding failed")
            self.progress.configure(value=0)
            self.play_sound("error")
    
    def add_to_history(self, operation, input_data, output_data):
        """Add an operation to the history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "operation": operation,
            "input": input_data,
            "output": output_data,
            "input_length": len(input_data),
            "output_length": len(output_data)
        }
        
        # Add to list
        self.history.append(entry)
        
        # Add to treeview
        self.history_tree.insert("", "end", values=(
            timestamp,
            operation,
            len(input_data),
            len(output_data)
        ))
        
        # Limit history size
        max_size = self.settings.get("history_size", 50)
        if len(self.history) > max_size:
            self.history.pop(0)
            self.history_tree.delete(self.history_tree.get_children()[0])
    
    def view_history_details(self):
        """View details of selected history entry"""
        selected = self.history_tree.focus()
        if not selected:
            return
            
        # Get the selected item
        item = self.history_tree.item(selected)
        values = item['values']
        
        # Find the corresponding history entry
        for entry in self.history:
            if entry['timestamp'] == values[0] and entry['operation'] == values[1]:
                # Create a details window
                detail_win = tk.Toplevel(self)
                detail_win.title("Operation Details")
                detail_win.geometry("600x400")
                detail_win.transient(self)
                detail_win.grab_set()
                
                # Create notebook for input/output
                notebook = ttk.Notebook(detail_win)
                notebook.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Input tab
                input_frame = ttk.Frame(notebook)
                notebook.add(input_frame, text="Input")
                
                input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD)
                input_text.insert(tk.END, entry['input'])
                input_text.config(state='disabled')
                input_text.pack(fill='both', expand=True, padx=5, pady=5)
                
                # Output tab
                output_frame = ttk.Frame(notebook)
                notebook.add(output_frame, text="Output")
                
                output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
                output_text.insert(tk.END, entry['output'])
                output_text.config(state='disabled')
                output_text.pack(fill='both', expand=True, padx=5, pady=5)
                
                # Stats tab
                stats_frame = ttk.Frame(notebook)
                notebook.add(stats_frame, text="Statistics")
                
                stats = [
                    f"Timestamp: {entry['timestamp']}",
                    f"Operation: {entry['operation']}",
                    f"Input Length: {entry['input_length']} characters",
                    f"Output Length: {entry['output_length']} characters",
                    f"Compression Ratio: {entry['input_length']/entry['output_length']:.2f}" 
                    if entry['operation'] == 'Encode' and entry['output_length'] > 0 else ""
                ]
                
                for i, stat in enumerate(stats):
                    if stat:  # Skip empty strings
                        ttk.Label(stats_frame, text=stat).pack(anchor='w', padx=10, pady=5)
                
                break
    
    def delete_history_entry(self):
        """Delete selected history entry"""
        selected = self.history_tree.focus()
        if not selected:
            return
            
        # Get the selected item
        item = self.history_tree.item(selected)
        values = item['values']
        
        # Find the corresponding history entry and remove
        for i, entry in enumerate(self.history):
            if entry['timestamp'] == values[0] and entry['operation'] == values[1]:
                del self.history[i]
                break
                
        # Remove from treeview
        self.history_tree.delete(selected)
    
    def clear_history(self):
        """Clear all history entries"""
        self.history = []
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.log_action("Operation history cleared")
    
    def copy_encoded(self):
        encoded = self.encoder_output.get("1.0", tk.END).strip()
        if encoded:
            self.clipboard_clear()
            self.clipboard_append(encoded)
            self.log_action("Copied encoded pulse to clipboard")
            self.status_var.set("Status: Encoded pulse copied to clipboard")
            self.play_sound("success")
    
    def copy_decoded(self):
        decoded = self.decoder_output.get("1.0", tk.END).strip()
        if decoded:
            self.clipboard_clear()
            self.clipboard_append(decoded)
            self.log_action("Copied decoded text to clipboard")
            self.status_var.set("Status: Decoded text copied to clipboard")
            self.play_sound("success")
    
    def paste_to_decoder(self):
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                self.decoder_input.delete("1.0", tk.END)
                self.decoder_input.insert(tk.END, clipboard_content)
                self.log_action("Pasted content to decoder")
                self.play_sound("success")
        except:
            self.log_action("Failed to paste from clipboard")
            self.play_sound("error")
    
    def clear_encoder_input(self):
        self.encoder_input.delete("1.0", tk.END)
        self.log_action("Encoder input cleared")
    
    def clear_decoder_input(self):
        self.decoder_input.delete("1.0", tk.END)
        self.log_action("Decoder input cleared")
    
    def clear_terminal(self):
        self.terminal_output.config(state='normal')
        self.terminal_output.delete("1.0", tk.END)
        self.terminal_output.config(state='disabled')
        self.log_action("Terminal cleared")
    
    def clear_all(self):
        self.encoder_input.delete("1.0", tk.END)
        self.encoder_output.config(state='normal')
        self.encoder_output.delete("1.0", tk.END)
        self.encoder_output.config(state='disabled')
        
        self.decoder_input.delete("1.0", tk.END)
        self.decoder_output.config(state='normal')
        self.decoder_output.delete("1.0", tk.END)
        self.decoder_output.config(state='disabled')
        
        self.log_action("All fields cleared")
        self.status_var.set("System Status: Ready")
        self.play_sound("success")
    
    def load_text_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.encoder_input.delete("1.0", tk.END)
                    self.encoder_input.insert(tk.END, content)
                    self.log_action(f"Loaded file: {os.path.basename(filepath)}")
                    self.status_var.set(f"Status: Loaded {len(content)} characters from file")
                    self.play_sound("success")
            except Exception as e:
                self.log_action(f"LOAD ERROR: {str(e)}")
                self.status_var.set("Status: File load failed")
                self.play_sound("error")
    
    def save_encoded_file(self):
        encoded = self.encoder_output.get("1.0", tk.END).strip()
        if not encoded:
            self.log_action("SAVE ERROR: No encoded content to save")
            self.play_sound("error")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pls",
            filetypes=[("PulseLang files", "*.pls"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(encoded)
                    self.log_action(f"Saved encoded pulse to: {os.path.basename(filepath)}")
                    self.status_var.set("Status: File saved successfully")
                    self.play_sound("success")
            except Exception as e:
                self.log_action(f"SAVE ERROR: {str(e)}")
                self.status_var.set("Status: File save failed")
                self.play_sound("error")
    
    def save_decoded_file(self):
        decoded = self.decoder_output.get("1.0", tk.END).strip()
        if not decoded:
            self.log_action("SAVE ERROR: No decoded content to save")
            self.play_sound("error")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(decoded)
                    self.log_action(f"Saved decoded text to: {os.path.basename(filepath)}")
                    self.status_var.set("Status: File saved successfully")
                    self.play_sound("success")
            except Exception as e:
                self.log_action(f"SAVE ERROR: {str(e)}")
                self.status_var.set("Status: File save failed")
                self.play_sound("error")
    
    def export_log(self):
        """Export terminal log to file"""
        log_content = self.terminal_output.get("1.0", tk.END)
        if not log_content.strip():
            self.log_action("EXPORT ERROR: No log content to export")
            self.play_sound("error")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                    self.log_action(f"Exported log to: {os.path.basename(filepath)}")
                    self.status_var.set("Status: Log exported successfully")
                    self.play_sound("success")
            except Exception as e:
                self.log_action(f"EXPORT ERROR: {str(e)}")
                self.status_var.set("Status: Log export failed")
                self.play_sound("error")
    
    def send_pulse(self):
        """Simulate sending the pulse signal"""
        encoded = self.encoder_output.get("1.0", tk.END).strip()
        if not encoded:
            self.log_action("TRANSMISSION ERROR: No pulse to send")
            self.status_var.set("Status: Transmission failed - no pulse")
            self.play_sound("error")
            return
        
        # Show transmission animation
        self.log_action("Initializing transmission sequence...")
        self.status_var.set("Status: Transmitting pulse...")
        self.play_sound("encode")
        
        # Create a progress window
        progress_win = tk.Toplevel(self)
        progress_win.title("Pulse Transmission")
        progress_win.geometry("400x200")
        progress_win.transient(self)
        progress_win.grab_set()
        
        # Create progress bar
        progress_label = ttk.Label(progress_win, text="Transmitting pulse signal...", font=('Arial', 10))
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_win, orient='horizontal', length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        status_label = ttk.Label(progress_win, text="0%")
        status_label.pack(pady=5)
        
        # Simulate transmission in a separate thread
        def transmit():
            for i in range(1, 101):
                progress_bar['value'] = i
                status_label.config(text=f"{i}%")
                progress_win.update()
                time.sleep(0.03)
                
            progress_win.destroy()
            self.log_action("Pulse transmission complete")
            self.log_action("Signal integrity: 100%")
            self.status_var.set("Status: Pulse transmitted successfully")
            self.play_sound("success")
        
        threading.Thread(target=transmit, daemon=True).start()
    
    def analyze_signal(self):
        """Perform signal analysis simulation"""
        self.log_action("Starting signal analysis...")
        self.status_var.set("Status: Analyzing signal...")
        self.play_sound("decode")
        
        # Create a progress window
        progress_win = tk.Toplevel(self)
        progress_win.title("Signal Analysis")
        progress_win.geometry("400x200")
        progress_win.transient(self)
        progress_win.grab_set()
        
        # Create progress bar
        progress_label = ttk.Label(progress_win, text="Analyzing signal characteristics...", font=('Arial', 10))
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_win, orient='horizontal', length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        status_label = ttk.Label(progress_win, text="0%")
        status_label.pack(pady=5)
        
        # Simulate analysis in a separate thread
        def analyze():
            for i in range(1, 101):
                progress_bar['value'] = i
                status_label.config(text=f"{i}%")
                progress_win.update()
                time.sleep(0.02)
                
            progress_win.destroy()
            
            # Generate fake analysis results
            encryption_strength = random.randint(85, 99)
            frequency_variance = random.uniform(0.2, 1.8)
            entropy_level = random.uniform(4.5, 7.5)
            compression_ratio = random.uniform(1.5, 3.0)
            
            self.log_action(f"Signal analysis complete")
            self.log_action(f"Encryption strength: {encryption_strength}%")
            self.log_action(f"Frequency variance: {frequency_variance:.2f} Hz")
            self.log_action(f"Entropy level: {entropy_level:.2f} bits")
            self.log_action(f"Compression ratio: {compression_ratio:.2f}:1")
            
            if encryption_strength > 90:
                security_status = "SECURE"
                color = "#00ff00"
            else:
                security_status = "VULNERABLE"
                color = self.error_color
            
            self.log_action(f"Security status: {security_status}")
            self.status_var.set("Status: Analysis complete")
            self.connection_var.set(f"Connection: {security_status}")
            self.connection_var_label = self.status_frame.winfo_children()[2]
            self.connection_var_label.configure(foreground=color)
            
            self.play_sound("success")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_decoded(self):
        """Analyze decoded text"""
        decoded = self.decoder_output.get("1.0", tk.END).strip()
        if not decoded:
            self.log_action("ANALYSIS ERROR: No decoded content")
            self.play_sound("error")
            return
        
        # Perform text analysis
        char_count = len(decoded)
        word_count = len(decoded.split())
        line_count = len(decoded.split('\n'))
        
        # Detect language patterns
        languages = []
        if ' the ' in decoded.lower():
            languages.append('English')
        if ' le ' in decoded.lower() or ' la ' in decoded.lower():
            languages.append('French')
        if ' der ' in decoded.lower() or ' die ' in decoded.lower():
            languages.append('German')
        if ' el ' in decoded.lower() or ' la ' in decoded.lower():
            languages.append('Spanish')
        
        # Create analysis window
        analysis_win = tk.Toplevel(self)
        analysis_win.title("Text Analysis")
        analysis_win.geometry("400x300")
        analysis_win.transient(self)
        analysis_win.grab_set()
        
        # Create analysis content
        frame = ttk.Frame(analysis_win)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Text Analysis Results", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        # Basic stats
        ttk.Label(frame, text="Character Count:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        ttk.Label(frame, text=str(char_count)).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(frame, text="Word Count:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        ttk.Label(frame, text=str(word_count)).grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(frame, text="Line Count:").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        ttk.Label(frame, text=str(line_count)).grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        # Language detection
        lang_text = ", ".join(languages) if languages else "Unknown"
        ttk.Label(frame, text="Detected Languages:").grid(row=4, column=0, sticky='e', padx=5, pady=2)
        ttk.Label(frame, text=lang_text).grid(row=4, column=1, sticky='w', padx=5, pady=2)
        
        # Entropy calculation
        entropy = self.calculate_entropy(decoded)
        ttk.Label(frame, text="Entropy:").grid(row=5, column=0, sticky='e', padx=5, pady=2)
        ttk.Label(frame, text=f"{entropy:.4f} bits/byte").grid(row=5, column=1, sticky='w', padx=5, pady=2)
        
        # Close button
        ttk.Button(frame, text="Close", command=analysis_win.destroy).grid(row=6, column=0, columnspan=2, pady=10)
    
    def calculate_entropy(self, text):
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
            
        entropy = 0.0
        text_length = len(text)
        
        # Count frequency of each character
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        for count in freq.values():
            p = count / text_length
            entropy -= p * (p and math.log(p, 2))
            
        return entropy
    
    def generate_qr(self):
        """Generate QR code for encoded pulse (simulated)"""
        encoded = self.encoder_output.get("1.0", tk.END).strip()
        if not encoded:
            self.log_action("QR ERROR: No encoded content")
            self.play_sound("error")
            return
            
        # Create QR window
        qr_win = tk.Toplevel(self)
        qr_win.title("PulseLang QR Code")
        qr_win.geometry("300x350")
        qr_win.transient(self)
        qr_win.grab_set()
        
        # Create QR content
        frame = ttk.Frame(qr_win)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="PulseLang QR Code", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Placeholder for QR code
        qr_placeholder = tk.Canvas(frame, width=200, height=200, bg='white')
        qr_placeholder.pack(pady=10)
        
        # Draw simulated QR pattern
        self.draw_qr_pattern(qr_placeholder)
        
        # Add info label
        ttk.Label(frame, text="Scan this QR code with PulseLang Reader", font=('Arial', 9)).pack(pady=5)
        
        # Add close button
        ttk.Button(frame, text="Close", command=qr_win.destroy).pack(pady=5)
        
        self.log_action("Generated QR code for pulse signal")
        self.play_sound("success")
    
    def draw_qr_pattern(self, canvas):
        """Draw a simulated QR pattern"""
        # Draw outer border
        canvas.create_rectangle(10, 10, 190, 190, outline='black', width=2)
        
        # Draw position markers
        canvas.create_rectangle(20, 20, 50, 50, fill='black')
        canvas.create_rectangle(20, 150, 50, 180, fill='black')
        canvas.create_rectangle(150, 20, 180, 50, fill='black')
        
        # Draw timing patterns
        for i in range(10):
            x = 55 + i * 12
            canvas.create_rectangle(x, 25, x+6, 30, fill='black')
            canvas.create_rectangle(25, x, 30, x+6, fill='black')
        
        # Draw random data pattern
        for y in range(60, 140, 15):
            for x in range(60, 140, 15):
                if random.random() > 0.5:
                    canvas.create_rectangle(x, y, x+10, y+10, fill='black')
    
    def choose_colors(self):
        """Allow user to choose custom colors"""
        # Choose foreground color
        fg_color = colorchooser.askcolor(title="Choose Text Color", 
                                        initialcolor=self.fg_color)[1]
        if not fg_color:
            return
            
        # Choose background color
        bg_color = colorchooser.askcolor(title="Choose Background Color", 
                                        initialcolor=self.bg_color)[1]
        if not bg_color:
            return
            
        # Choose accent color
        accent_color = colorchooser.askcolor(title="Choose Accent Color", 
                                           initialcolor=self.accent_color)[1]
        if not accent_color:
            return
            
        # Update colors
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.accent_color = accent_color
        
        # Update theme
        self.apply_theme()
        
        self.log_action("Custom theme applied")
        self.play_sound("success")
    
    def apply_settings(self):
        """Apply settings from advanced panel"""
        # Update settings dictionary
        self.settings['theme'] = self.theme_var.get()
        self.settings['compression'] = self.compression_var.get()
        self.settings['obfuscate'] = self.obfuscate_var.get()
        self.settings['auto_decode'] = self.auto_decode_var.get()
        self.settings['sound_effects'] = self.sound_var.get()
        
        # Apply theme
        self.apply_theme()
        
        # Save settings
        self.save_settings()
        
        self.log_action("Settings applied and saved")
        self.status_var.set("Status: Settings updated")
        self.play_sound("success")
    
    def apply_theme(self):
        """Apply the selected theme"""
        theme = self.settings['theme']
        
        if theme == "matrix":
            self.bg_color = "#0a0a12"
            self.fg_color = "#00ff41"
            self.accent_color = "#ff00ff"
        elif theme == "cyber_red":
            self.bg_color = "#120a0a"
            self.fg_color = "#ff3333"
            self.accent_color = "#00ffff"
        elif theme == "neon_blue":
            self.bg_color = "#0a0c12"
            self.fg_color = "#00ccff"
            self.accent_color = "#ff00cc"
        elif theme == "hacker_classic":
            self.bg_color = "#000000"
            self.fg_color = "#00ff00"
            self.accent_color = "#ff7700"
        
        # Update UI colors
        self.configure(bg=self.bg_color)
        self.style.configure('.', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TButton', background=self.button_bg, foreground=self.fg_color)
        self.style.configure('TLabelFrame', background=self.bg_color, foreground=self.accent_color)
        
        # Update text areas
        for widget in [self.encoder_input, self.encoder_output, 
                      self.decoder_input, self.decoder_output]:
            widget.config(bg=self.text_bg, fg=self.fg_color, insertbackground=self.fg_color)
        
        # Update terminal
        self.terminal_output.config(bg="#001a00", fg=self.fg_color)
    
    def show_settings(self):
        """Show the settings panel (already visible, just bring to focus)"""
        self.log_action("Settings panel accessed")
    
    def show_history_menu(self, event):
        """Show context menu for history"""
        item = self.history_tree.identify_row(event.y)
        if item:
            self.history_tree.selection_set(item)
            self.history_tree.focus(item)
            self.history_menu.post(event.x_root, event.y_root)
    
    def show_about(self):
        about_text = """PULSE LANG v3.0 - Advanced Signal Encryption System

Developed by: Shiboshree Roy
Copyright © 2023 - All rights reserved

PulseLang is a proprietary signal encryption protocol
designed for secure communications in hostile environments.
This advanced implementation features enhanced error correction,
signal analysis tools, and multi-channel transmission protocols.

Key Features:
- Advanced compression algorithms
- Signal obfuscation techniques
- Real-time network monitoring
- Operation history tracking
- QR code generation
- Customizable themes

Warning: Unauthorized use of this technology is strictly prohibited.
All transmissions are monitored for security compliance."""

        messagebox.showinfo("About PulseLang", about_text)
        self.log_action("Displayed about information")

if __name__ == "__main__":
    import math  # Needed for entropy calculation
    app = PulseLangGUI()
    app.mainloop()