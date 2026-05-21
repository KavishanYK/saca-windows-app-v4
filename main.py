from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


PROJECT_ROOT = Path(__file__).resolve().parent


def load_font(app: QApplication) -> None:
    font_path = PROJECT_ROOT / "assets" / "fonts" / "Batolah.ttf"
    if font_path.exists():
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                app.setFont(QFont(families[0]))
                print(f"[SACA] Font loaded: {families[0]}")
        else:
            print(f"[SACA] Failed to load font: {font_path}")
    else:
        print(f"[SACA] Font not found: {font_path}")


def load_stylesheet(app: QApplication) -> None:
    qss_path = PROJECT_ROOT / "assets" / "styles" / "main.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        print(f"[SACA] Stylesheet not found: {qss_path}")


def main() -> int:
    app = QApplication(sys.argv)
    load_font(app)
    load_stylesheet(app)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
