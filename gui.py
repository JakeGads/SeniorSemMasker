from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from clipboard import paste

from main import main

if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("icon.svg")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    def play_video():
        main(paste())

    # Create the menu
    menu = QMenu()

    action = QAction("Start Masked Video") 
    action.triggered.connect(play_video)
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()