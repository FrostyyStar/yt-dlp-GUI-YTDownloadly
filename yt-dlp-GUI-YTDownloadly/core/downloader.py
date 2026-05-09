import subprocess
from PySide6.QtCore import QObject, Signal


class Downloader(QObject):
    log_signal = Signal(str)
    finished_signal = Signal()

    def run(self, command):
        self.log_signal.emit("Running command...")
        self.log_signal.emit(" ".join(command))

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in process.stdout:
            self.log_signal.emit(line.strip())

        process.wait()

        self.log_signal.emit("Finished.")
        self.finished_signal.emit()