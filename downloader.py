import os
import yt_dlp
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def log_message(log_widget, message):
    """Logs a message to the provided CTkTextbox."""
    log_widget.insert("end", f"{message}\n")
    log_widget.see("end")  # Scroll to the end


def download_media(url, download_type, format_option, quality, output_dir, log_widget):
    """
    Download a single video or audio file from a given URL.
    """
    try:
        logging.info(f"Starting download for {url}.")
        log_message(log_widget, f"Starting download for {url}.")

        # Validate format options
        valid_audio_formats = ["mp3", "m4a", "flac"]
        valid_video_formats = ["mp4", "avi", "mkv"]

        if download_type == "Audio" and format_option not in valid_audio_formats:
            raise ValueError(f"Invalid audio format: {format_option}")
        if download_type == "Video" and format_option not in valid_video_formats:
            raise ValueError(f"Invalid video format: {format_option}")

        # Output file template
        output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

        # yt_dlp options
        ydl_opts = {
            "format": f"bestvideo[ext={format_option}]+bestaudio/best[ext={format_option}]" if download_type == "Video" else "bestaudio",
            "merge_output_format": format_option if download_type == "Video" else None,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format_option,
                    "preferredquality": quality.replace("kbps", "") if "kbps" in quality else None,
                }
            ] if download_type == "Audio" else [],
            "outtmpl": output_template,
            "quiet": False,
            "progress_hooks": [lambda d: download_progress_hook(d, log_widget)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            log_message(log_widget, f"Download completed: {url}")
        return f"Downloaded {url}"
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        log_message(log_widget, f"Error downloading {url}: {e}")
        return f"Error downloading {url}: {e}"


def download_progress_hook(d, log_widget):
    """
    Hook for yt_dlp to track download progress and log to the UI.
    """
    if d["status"] == "downloading":
        download_speed = d.get("speed", 0)
        speed_kbps = f"{download_speed / 1024:.2f} KB/s" if download_speed else "Unknown speed"
        log_message(log_widget, f"Downloading: {d.get('filename', 'Unknown file')} at {speed_kbps}")


def download_playlist(playlist_url, download_type, format_option, quality, output_dir, log_widget, max_downloads):
    """
    Download a playlist by extracting individual video URLs and processing each one.
    """
    try:
        logging.info(f"Starting playlist download for {playlist_url}.")
        log_message(log_widget, f"Starting playlist download for {playlist_url}.")

        # Extract playlist entries
        ydl_opts = {"extract_flat": True, "quiet": False}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            video_urls = [entry["url"] for entry in playlist_info["entries"][:max_downloads]]

        # Download each video in the playlist
        messages = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    download_media,
                    url, download_type, format_option, quality, output_dir, log_widget
                ) for url in video_urls
            ]
            for future in concurrent.futures.as_completed(futures):
                messages.append(future.result())

        log_message(log_widget, "\n".join(messages))
        return "\n".join(messages)
    except Exception as e:
        logging.error(f"Error downloading playlist: {e}")
        log_message(log_widget, f"Error downloading playlist: {e}")
        return f"Error downloading playlist: {e}"


def convert_media(output_dir, input_format, output_format):
    """
    Convert media files in a directory from one format to another using FFmpeg.
    """
    try:
        logging.info(f"Starting conversion from {input_format} to {output_format}.")
        files_to_convert = [f for f in os.listdir(output_dir) if f.endswith(input_format)]

        for file in files_to_convert:
            input_path = os.path.join(output_dir, file)
            output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.{output_format}")
            logging.info(f"Converting file {file} to {output_format}.")
            os.system(f"ffmpeg -i \"{input_path}\" \"{output_path}\"")

        logging.info(f"Conversion completed for {len(files_to_convert)} files.")
        return f"Converted {len(files_to_convert)} files to {output_format}"
    except Exception as e:
        logging.error(f"Error converting files: {e}")
        return f"Error converting files: {e}"
