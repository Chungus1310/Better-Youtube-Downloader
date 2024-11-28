import customtkinter as ctk
from tkinter import filedialog, StringVar, IntVar, messagebox
import os
import sys
import threading
from downloader import download_media, download_playlist, convert_media

# Constants
DOWNLOAD_DIR = "downloaded_media"
AUDIO_FORMATS = ["mp3", "m4a", "flac"]
VIDEO_FORMATS = ["mp4", "avi", "mkv"]
AUDIO_QUALITIES = ["128kbps", "192kbps", "256kbps"]
VIDEO_QUALITIES = ["720p", "1080p", "best"]

# Custom class to redirect output to CTkTextbox
class LogStream:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        """Write method to insert message into CTkTextbox."""
        self.widget.insert("end", message)
        self.widget.see("end")  # Scroll to the end

    def flush(self):
        """Flush method for compatibility with sys.stdout/stderr."""
        pass

# Function to log messages into the CTkTextbox
def log_message(log_widget, message):
    """Logs a message to the provided CTkTextbox."""
    log_widget.insert("end", f"{message}\n")
    log_widget.see("end")  # Scroll to the end

# Functions for the application
def update_dropdowns(*args):
    """Update format and quality dropdowns based on download type."""
    if download_type_var.get() == "Audio":
        format_option_menu.configure(values=AUDIO_FORMATS)
        format_option_var.set(AUDIO_FORMATS[0])
        quality_menu.configure(values=AUDIO_QUALITIES)
        quality_var.set(AUDIO_QUALITIES[0])
    else:
        format_option_menu.configure(values=VIDEO_FORMATS)
        format_option_var.set(VIDEO_FORMATS[0])
        quality_menu.configure(values=VIDEO_QUALITIES)
        quality_var.set(VIDEO_QUALITIES[0])

def start_download_thread():
    """Start the download process in a new thread."""
    threading.Thread(target=start_download, daemon=True).start()

def start_download():
    """Perform the download operation."""
    url = url_var.get()
    if not url:
        messagebox.showerror("Error", "Please provide a YouTube URL.")
        return

    output_dir = output_dir_var.get()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        if is_playlist.get():
            message = download_playlist(
                url, download_type_var.get(), format_option_var.get(), quality_var.get(),
                output_dir, log_text, max_downloads.get()
            )
        else:
            message = download_media(
                url, download_type_var.get(), format_option_var.get(), quality_var.get(),
                output_dir, log_text
            )

        if convert_to_var.get() != "None":
            conversion_message = convert_media(output_dir, format_option_var.get(), convert_to_var.get())
            message += f"\n{conversion_message}"

        log_message(log_text, message)
    except Exception as e:
        log_message(log_text, f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_output_dir():
    """Open a dialog to select the output directory."""
    folder = filedialog.askdirectory()
    if folder:
        output_dir_var.set(folder)

# Initialize the main window
app = ctk.CTk()
app.title("Shadow wizard kitten gang")
app.geometry("800x600")

# Variables
url_var = StringVar()
output_dir_var = StringVar(value=DOWNLOAD_DIR)
download_type_var = StringVar(value="Audio")
format_option_var = StringVar(value=AUDIO_FORMATS[0])
quality_var = StringVar(value=AUDIO_QUALITIES[0])
convert_to_var = StringVar(value="None")
max_downloads = IntVar(value=5)
is_playlist = IntVar(value=0)

# Attach event handler to update dropdowns
download_type_var.trace_add("write", update_dropdowns)

# Header
header = ctk.CTkLabel(app, text="🎥 YouTube Media Downloader", font=("Arial", 20))
header.pack(pady=10)

# Input Frame
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(input_frame, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
url_entry = ctk.CTkEntry(input_frame, textvariable=url_var, width=400)
url_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(input_frame, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
output_dir_entry = ctk.CTkEntry(input_frame, textvariable=output_dir_var, width=400)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
browse_button = ctk.CTkButton(input_frame, text="Browse", command=browse_output_dir)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# Options Frame
options_frame = ctk.CTkFrame(app)
options_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(options_frame, text="Download Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
download_type_menu = ctk.CTkOptionMenu(options_frame, variable=download_type_var, values=["Audio", "Video"])
download_type_menu.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(options_frame, text="Format:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
format_option_menu = ctk.CTkOptionMenu(options_frame, variable=format_option_var, values=AUDIO_FORMATS)
format_option_menu.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(options_frame, text="Quality:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
quality_menu = ctk.CTkOptionMenu(options_frame, variable=quality_var, values=AUDIO_QUALITIES)
quality_menu.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(options_frame, text="Convert To:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
convert_to_menu = ctk.CTkOptionMenu(options_frame, variable=convert_to_var, values=["None"] + AUDIO_FORMATS + VIDEO_FORMATS)
convert_to_menu.grid(row=3, column=1, padx=5, pady=5)

ctk.CTkLabel(options_frame, text="Max Playlist Downloads:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
max_download_spinbox = ctk.CTkEntry(options_frame, textvariable=max_downloads, width=50)
max_download_spinbox.grid(row=4, column=1, padx=5, pady=5)

playlist_check = ctk.CTkCheckBox(options_frame, text="Is Playlist", variable=is_playlist)
playlist_check.grid(row=5, column=0, padx=5, pady=5, sticky="w")

# Start Button
start_button = ctk.CTkButton(app, text="Start Download", command=start_download_thread)
start_button.pack(pady=10)

# Logs Section
log_frame = ctk.CTkFrame(app)
log_frame.pack(fill="both", expand=True, padx=20, pady=10)

log_label = ctk.CTkLabel(log_frame, text="Logs:")
log_label.pack(anchor="w", padx=5, pady=5)

log_text = ctk.CTkTextbox(log_frame, wrap="word", height=200)
log_text.pack(fill="both", expand=True, padx=5, pady=5)

# Redirect stdout and stderr to the log window
sys.stdout = LogStream(log_text)
sys.stderr = LogStream(log_text)

# Add "Built by Chun" watermark to the bottom-right corner
footer_label = ctk.CTkLabel(app, text="Built by Chun", font=("Arial", 10), anchor="e")
footer_label.pack(side="bottom", anchor="se", padx=10, pady=5)

# Run the app
app.mainloop()
