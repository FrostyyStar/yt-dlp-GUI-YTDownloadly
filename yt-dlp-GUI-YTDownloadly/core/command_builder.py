from core.models import DownloadOptions


class CommandBuilder:
    @staticmethod
    def build(options: DownloadOptions):
        command = ["yt-dlp"]

        if options.mode == "audio":
            command.extend([
                "-x",
                "--audio-format",
                options.format
            ])
        else:
            command.extend([
                "-f",
                f"bestvideo[height<={options.resolution}]+bestaudio/best"
                if options.resolution != "best"
                else "best"
            ])

            command.extend([
                "--merge-output-format",
                options.format
            ])

        if options.subtitles:
            command.extend([
                "--write-subs",
                "--sub-langs",
                "all"
            ])

        if not options.playlist:
            command.append("--no-playlist")

        command.extend([
            "-P",
            options.output_path
        ])

        command.append(options.url)

        return command