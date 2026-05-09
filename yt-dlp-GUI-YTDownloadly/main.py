import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # TASKBAR + WINDOW ICON
    app.setWindowIcon(
        QIcon(
            resource_path(
                "assets/images/logo.ico"
            )
        )
    )

    window = MainWindow()

    window.setWindowIcon(
        QIcon(
            resource_path(
                "assets/images/logo.ico"
            )
        )
    )

    window.show()

    sys.exit(app.exec())