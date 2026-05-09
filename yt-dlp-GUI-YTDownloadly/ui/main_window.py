import re
import os
import sys

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QApplication,
    QFrame,
    QFileDialog,
    QProgressBar
)

from PySide6.QtCore import (
    Qt,
    QProcess,
    QSize,
    QTimer,
    QProcessEnvironment
)

from PySide6.QtGui import (
    QPixmap,
    QIcon
)


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YTDownloadly")
        self.resize(760, 640)

        self.process = None
        self.loading_frame = 0

        self.setup_ui()
        self.load_styles()

    def setup_ui(self):

        root_layout = QVBoxLayout()

        root_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        self.card = QFrame()

        self.card.setObjectName(
            "mainCard"
        )

        card_layout = QVBoxLayout()

        card_layout.setSpacing(22)

        card_layout.setContentsMargins(
            32,
            32,
            32,
            32
        )

        # HEADER
        title_layout = QHBoxLayout()

        title_layout.setAlignment(
            Qt.AlignCenter
        )

        title_layout.setSpacing(10)

        logo = QLabel()

        pixmap = QPixmap(
            resource_path(
                "assets/images/logo.png"
            )
        )

        if not pixmap.isNull():

            logo.setPixmap(
                pixmap.scaled(
                    34,
                    34,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        title = QLabel(
            "YTDownloadly"
        )

        title.setObjectName(
            "title"
        )

        title_layout.addWidget(
            logo
        )

        title_layout.addWidget(
            title
        )

        card_layout.addLayout(
            title_layout
        )

        subtitle = QLabel(
            "Download YouTube videos in your preferred quality and format"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        card_layout.addWidget(
            subtitle
        )

        # URL
        url_label = QLabel(
            "YouTube URL"
        )

        url_label.setObjectName(
            "fieldLabel"
        )

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "https://www.youtube.com/watch?v=..."
        )

        card_layout.addWidget(
            url_label
        )

        card_layout.addWidget(
            self.url_input
        )

        # OPTIONS
        dropdown_layout = QHBoxLayout()

        dropdown_layout.setSpacing(18)

        # TYPE
        type_layout = QVBoxLayout()

        type_label = QLabel(
            "Type"
        )

        type_label.setObjectName(
            "fieldLabel"
        )

        self.type_combo = QComboBox()

        self.type_combo.addItems([
            "Audio only",
            "Video only",
            "Both"
        ])

        self.type_combo.currentTextChanged.connect(
            self.update_options
        )

        type_layout.addWidget(
            type_label
        )

        type_layout.addWidget(
            self.type_combo
        )

        # QUALITY
        quality_layout = QVBoxLayout()

        quality_label = QLabel(
            "Quality"
        )

        quality_label.setObjectName(
            "fieldLabel"
        )

        self.quality_combo = QComboBox()

        quality_layout.addWidget(
            quality_label
        )

        quality_layout.addWidget(
            self.quality_combo
        )

        # FORMAT
        format_layout = QVBoxLayout()

        format_label = QLabel(
            "Format"
        )

        format_label.setObjectName(
            "fieldLabel"
        )

        self.format_combo = QComboBox()

        format_layout.addWidget(
            format_label
        )

        format_layout.addWidget(
            self.format_combo
        )

        dropdown_layout.addLayout(
            type_layout
        )

        dropdown_layout.addLayout(
            quality_layout
        )

        dropdown_layout.addLayout(
            format_layout
        )

        card_layout.addLayout(
            dropdown_layout
        )

        # OUTPUT DIRECTORY
        output_label = QLabel(
            "Output Directory"
        )

        output_label.setObjectName(
            "fieldLabel"
        )

        card_layout.addWidget(
            output_label
        )

        output_layout = QHBoxLayout()

        output_layout.setSpacing(14)

        self.output_input = QLineEdit()

        self.output_input.setPlaceholderText(
            "Choose download folder..."
        )

        self.browse_button = QPushButton(
            "Browse"
        )

        self.browse_button.setObjectName(
            "browseButton"
        )

        self.browse_button.setFixedWidth(
            120
        )

        self.browse_button.clicked.connect(
            self.select_output_folder
        )

        output_layout.addWidget(
            self.output_input
        )

        output_layout.addWidget(
            self.browse_button
        )

        card_layout.addLayout(
            output_layout
        )

        # DOWNLOAD BUTTON
        self.download_button = QPushButton(
            " Download"
        )

        self.download_button.setObjectName(
            "downloadButton"
        )

        self.download_button.setCursor(
            Qt.PointingHandCursor
        )

        self.download_button.setIcon(
            QIcon(
                resource_path(
                    "assets/images/logo_white.png"
                )
            )
        )

        self.download_button.setIconSize(
            QSize(20, 20)
        )

        self.download_button.clicked.connect(
            self.start_download
        )

        card_layout.addWidget(
            self.download_button
        )

        # PROGRESS BAR
        self.progress_bar = QProgressBar()

        self.progress_bar.hide()

        self.progress_bar.setValue(0)

        card_layout.addWidget(
            self.progress_bar
        )

        # LOADING LABEL
        self.loading_label = QLabel()

        self.loading_label.setObjectName(
            "loadingLabel"
        )

        self.loading_label.setAlignment(
            Qt.AlignCenter
        )

        self.loading_label.hide()

        card_layout.addWidget(
            self.loading_label
        )

        # PERCENT
        self.progress_percent = QLabel()

        self.progress_percent.setObjectName(
            "progressPercent"
        )

        self.progress_percent.setAlignment(
            Qt.AlignCenter
        )

        self.progress_percent.hide()

        card_layout.addWidget(
            self.progress_percent
        )

        # INFO
        self.progress_info = QLabel()

        self.progress_info.setObjectName(
            "progressInfo"
        )

        self.progress_info.setAlignment(
            Qt.AlignCenter
        )

        self.progress_info.hide()

        card_layout.addWidget(
            self.progress_info
        )

        # ETA
        self.progress_eta = QLabel()

        self.progress_eta.setObjectName(
            "progressETA"
        )

        self.progress_eta.setAlignment(
            Qt.AlignCenter
        )

        self.progress_eta.hide()

        card_layout.addWidget(
            self.progress_eta
        )

        # TIMER
        self.loading_timer = QTimer()

        self.loading_timer.timeout.connect(
            self.animate_loading
        )

        self.card.setLayout(
            card_layout
        )

        root_layout.addWidget(
            self.card
        )

        self.setLayout(
            root_layout
        )

        self.update_options()

    def update_options(self):

        current_type = (
            self.type_combo.currentText()
        )

        self.quality_combo.clear()
        self.format_combo.clear()

        if current_type == "Audio only":

            self.quality_combo.addItems([
                "Best Quality"
            ])

            self.format_combo.addItems([
                ".flac",
                ".mp3",
                ".wav"
            ])

        else:

            self.quality_combo.addItems([
                "8K",
                "4K",
                "1440p",
                "1080p",
                "720p",
                "480p",
                "360p"
            ])

            self.format_combo.addItems([
                ".mp4",
                ".mkv",
                ".webm"
            ])

    def animate_loading(self):

        frames = [
            "Starting download.",
            "Starting download..",
            "Starting download..."
        ]

        self.loading_label.setText(
            frames[self.loading_frame]
        )

        self.loading_frame += 1

        if self.loading_frame >= len(frames):
            self.loading_frame = 0

    def select_output_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if folder:

            self.output_input.setText(
                folder
            )

    def start_download(self):

        url = self.url_input.text()

        if not url:
            return

        quality_text = (
            self.quality_combo.currentText()
        )

        if quality_text == "8K":
            quality = "4320"

        elif quality_text == "4K":
            quality = "2160"

        elif quality_text == "Best Quality":
            quality = "best"

        else:
            quality = quality_text.replace(
                "p",
                ""
            )

        media_type = (
            self.type_combo.currentText()
        )

        format_type = (
            self.format_combo.currentText()
            .replace(".", "")
        )

        command = []

        # AUDIO ONLY
        if media_type == "Audio only":

            command.extend([
                "-x",
                "--audio-format",
                format_type
            ])

        # VIDEO ONLY
        elif media_type == "Video only":

            command.extend([
                "-f",
                f"bestvideo[height<={quality}]"
            ])

            command.extend([
                "--merge-output-format",
                format_type
            ])

        # BOTH
        else:

            command.extend([
                "-f",
                f"bestvideo[height<={quality}]+bestaudio/best"
            ])

            command.extend([
                "--merge-output-format",
                format_type
            ])

        output_path = (
            self.output_input.text()
        )

        if output_path:

            command.extend([
                "-P",
                output_path
            ])

        command.append(url)

        yt_dlp_path = resource_path(
            "binaries/yt-dlp.exe"
        )

        ffmpeg_path = resource_path(
            "binaries"
        )

        command.insert(
            0,
            "--ffmpeg-location"
        )

        command.insert(
            1,
            ffmpeg_path
        )

        # UI
        self.download_button.hide()

        self.progress_bar.show()

        self.loading_label.show()

        self.progress_percent.hide()
        self.progress_info.hide()
        self.progress_eta.hide()

        self.progress_bar.setValue(0)

        self.loading_timer.start(500)

        # PROCESS
        self.process = QProcess(self)

        env = QProcessEnvironment.systemEnvironment()

        binaries_path = resource_path(
            "binaries"
        )

        current_path = env.value(
            "PATH"
        )

        env.insert(
            "PATH",
            binaries_path
            + os.pathsep
            + current_path
        )

        self.process.setProcessEnvironment(
            env
        )

        self.process.readyReadStandardOutput.connect(
            self.handle_stdout
        )

        self.process.readyReadStandardError.connect(
            self.handle_stderr
        )

        self.process.finished.connect(
            self.download_finished
        )

        self.process.start(
            yt_dlp_path,
            command
        )

    def handle_stdout(self):

        data = self.process.readAllStandardOutput()

        stdout = bytes(data).decode(
            "utf8",
            errors="ignore"
        )

        print(stdout)

        lines = stdout.splitlines()

        for line in lines:

            if "[download]" in line:

                self.loading_timer.stop()

                self.loading_label.hide()

                self.progress_percent.show()
                self.progress_info.show()
                self.progress_eta.show()

                percentage_match = re.search(
                    r"(\d+(?:\.\d+)?)%",
                    line
                )

                if percentage_match:

                    percent = float(
                        percentage_match.group(1)
                    )

                    self.progress_bar.setValue(
                        int(percent)
                    )

                    self.progress_percent.setText(
                        f"{percent:.1f}%"
                    )

                size_match = re.search(
                    r"of\s+(.+?)\s+at",
                    line
                )

                if size_match:

                    downloaded_text = size_match.group(1)

                    self.progress_info.setText(
                        f"Downloaded {downloaded_text}"
                    )

                eta_match = re.search(
                    r"ETA\s+([0-9:]+)",
                    line
                )

                if eta_match:

                    eta = eta_match.group(1)

                    self.progress_eta.setText(
                        f"ETA = {eta}"
                    )

                if "100%" in line:

                    self.progress_bar.setValue(
                        100
                    )

                    self.progress_percent.setText(
                        "100%"
                    )

                    self.progress_eta.setText(
                        "ETA = 00:00"
                    )

    def handle_stderr(self):

        data = (
            self.process.readAllStandardError()
        )

        stderr = bytes(data).decode(
            "utf8",
            errors="ignore"
        )

        print(stderr)

    def download_finished(self):

        self.loading_timer.stop()

        self.progress_bar.setValue(100)

        self.loading_label.hide()

        self.progress_percent.show()

        self.progress_percent.setText(
            "Download complete"
        )

        self.progress_info.setText("")
        self.progress_eta.setText("")

        self.download_button.show()

    def load_styles(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #050816;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel {
                background: transparent;
            }

            #mainCard {
                background-color: #071226;
                border: 1px solid #8b2cff;
                border-radius: 24px;
            }

            #title {
                font-size: 34px;
                font-weight: 700;
                background: transparent;
            }

            #subtitle {
                color: #a0a7b5;
                font-size: 16px;
                background: transparent;
            }

            #fieldLabel {
                color: #d6d9df;
                font-size: 14px;
                font-weight: 500;
                background: transparent;
            }

            QLineEdit {
                background-color: #020409;
                border: 1px solid #8b2cff;
                border-radius: 14px;
                padding: 16px;
                font-size: 15px;
                min-height: 28px;
            }

            QLineEdit:focus {
                border: 1px solid #b14dff;
            }

            QComboBox {
                background-color: #020409;
                border: 1px solid #8b2cff;
                border-radius: 14px;
                padding: 14px;
                min-height: 26px;
                font-size: 15px;
            }

            QComboBox:hover {
                border: 1px solid #b14dff;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
                background: transparent;
            }

            QComboBox::down-arrow {
                image: none;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #111111;
                border: 1px solid #2b2b2b;
                border-radius: 12px;
                padding: 8px;
                selection-background-color: #ffffff;
                selection-color: #000000;
                outline: none;
            }

            #downloadButton {
                background-color: #12c75f;
                border: none;
                border-radius: 16px;
                padding: 18px;
                font-size: 18px;
                font-weight: 700;
                color: white;
            }

            #downloadButton:hover {
                background-color: #19da6b;
            }

            #downloadButton:pressed {
                background-color: #0ea84f;
            }

            #browseButton {
                background-color: #1d2230;
                border: 1px solid #8b2cff;
                border-radius: 14px;
                color: white;
                font-size: 14px;
            }

            #browseButton:hover {
                border: 1px solid #b14dff;
            }

            QProgressBar {
                background-color: #111827;
                border: none;
                border-radius: 10px;
                height: 22px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #12c75f;
                border-radius: 10px;
            }

            #loadingLabel {
                font-size: 18px;
                font-weight: 600;
                color: white;
                background: transparent;
            }

            #progressPercent {
                font-size: 26px;
                font-weight: 700;
                color: white;
                background: transparent;
            }

            #progressInfo {
                font-size: 14px;
                color: #c5ccda;
                background: transparent;
            }

            #progressETA {
                font-size: 14px;
                color: #8fa1c7;
                background: transparent;
            }
        """)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())