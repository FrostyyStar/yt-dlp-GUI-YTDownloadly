from dataclasses import dataclass


@dataclass
class DownloadOptions:
    url: str
    output_path: str

    mode: str = "video"
    format: str = "mp4"
    resolution: str = "best"

    subtitles: bool = False
    playlist: bool = False