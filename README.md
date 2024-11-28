# 🎥 Better YouTube Downloader

## 📖 Overview

Better YouTube Downloader is a user-friendly, cross-platform desktop application that allows you to download and convert media from YouTube with ease. Whether you want to download audio tracks, video files, or entire playlists, this tool provides a simple and intuitive interface to meet your media downloading needs.

## ✨ Features

- **Multiple Download Types**
  - Download individual videos or entire playlists
  - Choose between audio and video downloads
  - Support for various formats (MP3, M4A, FLAC, MP4, AVI, MKV)

- **Flexible Quality Options**
  - Select audio quality (128kbps, 192kbps, 256kbps)
  - Select video quality (720p, 1080p, best available)

- **Conversion Capabilities**
  - Convert downloaded media between different formats
  - Supports conversion for both audio and video files

- **User-Friendly Interface**
  - Clean and intuitive GUI built with CustomTkinter
  - Real-time download and conversion logs
  - Easy directory selection for downloads

## 🛠 Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Internet connection

## 🚀 Installation

### Method 1: Using Executable (Windows)
1. Download `Portable_YT_Downloader.exe` from the repository
2. Run the executable directly - no installation required!

### Method 2: From Source

1. Clone the repository
```bash
git clone https://github.com/Chungus1310/Better-Youtube-Downloader.git
cd Better-Youtube-Downloader
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed and accessible in your system PATH

## 🖥 Launching the Application

### Using Python
To launch the application directly using the Python files:

1. Open a terminal or command prompt
2. Navigate to the project directory
3. Run the following command:
```bash
python app.py
```

### Troubleshooting Launch Issues
- Ensure all dependencies are installed correctly
- Verify Python path is set in system environment variables
- Check that all required libraries are compatible with your Python version

## 📚 Libraries Used

### Core Libraries
- `customtkinter`: A modern, customizable UI library extending Tkinter
  - Provides a sleek, contemporary interface
  - Offers advanced widget styling and theming
  - Ensures cross-platform compatibility

- `yt_dlp`: Advanced YouTube video downloading library
  - Fork of youtube-dl with additional features
  - Handles complex video and playlist downloads
  - Supports various extraction and download options

### Supporting Libraries
- `os`: Provides operating system dependent functionality
  - Used for file and directory operations
  - Handles path management and file system interactions

- `sys`: System-specific parameters and functions
  - Manages standard input/output streams
  - Provides access to Python interpreter variables

- `threading`: Enables concurrent download operations
  - Allows multiple downloads to run simultaneously
  - Prevents UI freezing during download processes

- `concurrent.futures`: High-level interface for asynchronous execution
  - Manages thread pools for playlist downloads
  - Simplifies parallel processing of multiple video downloads

### Logging and Utilities
- `logging`: Comprehensive logging framework
  - Tracks application events and errors
  - Provides detailed debug information
  - Configurable logging levels and formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🧑‍💻 Author

Built with ❤️ by Chun

## 🚨 Disclaimer

Respect YouTube's Terms of Service and copyright laws. This tool is for personal, non-commercial use only. i'm not responsible for your downfall.
