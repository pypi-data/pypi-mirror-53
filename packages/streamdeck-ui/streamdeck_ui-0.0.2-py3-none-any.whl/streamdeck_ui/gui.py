import os
import sys
from functools import partial

from PySide2 import QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QSizePolicy, QSystemTrayIcon, QMenu, QAction, QMainWindow

from streamdeck_ui import api
from streamdeck_ui.config import PROJECT_PATH, LOGO
from streamdeck_ui.ui_main import Ui_MainWindow

BUTTON_SYTLE = """
    QToolButton{background-color:black;}
    QToolButton:checked{background-color:darkGray;}
    QToolButton:focus{border:none; }
"""

selected_button = None


def _deck_id(ui):
    return ui.device_list.itemData(0)


def update_button_text(ui, text):
    deck_id = _deck_id(ui)
    api.set_button_text(deck_id, selected_button.index, text)
    redraw_buttons(ui)


def update_button_command(ui, command):
    deck_id = _deck_id(ui)
    api.set_button_command(deck_id, selected_button.index, command)


def update_button_keys(ui, keys):
    deck_id = _deck_id(ui)
    api.set_button_keys(deck_id, selected_button.index, keys)


def update_button_write(ui, write):
    deck_id = _deck_id(ui)
    api.set_button_write(deck_id, selected_button.index, write)


def update_change_brightness(ui, amount):
    deck_id = _deck_id(ui)
    api.set_button_change_brightness(deck_id, selected_button.index, amount)


def select_image(ui):
    file_name = QFileDialog.getOpenFileName(
        ui, "Open Image", os.path.expanduser("~"), "Image Files (*.png *.jpg *.bmp)"
    )[0]
    deck_id = _deck_id(ui)
    api.set_button_icon(deck_id, selected_button.index, file_name)
    redraw_buttons(ui)


def redraw_buttons(ui):
    deck_id = _deck_id(ui)
    current_tab = ui.cards.currentWidget()
    buttons = current_tab.findChildren(QtWidgets.QToolButton)
    for button in buttons:
        button.setText(api.get_button_text(deck_id, button.index))
        button.setIcon(QIcon(api.get_button_icon(deck_id, button.index)))


def set_brightness(ui, value):
    deck_id = _deck_id(ui)
    api.set_brightness(deck_id, value)


def button_clicked(ui, clicked_button, buttons):
    global selected_button
    selected_button = clicked_button
    for button in buttons:
        if button == clicked_button:
            continue

        button.setChecked(False)

    deck_id = _deck_id(ui)
    button_id = selected_button.index
    ui.text.setText(api.get_button_text(deck_id, button_id))
    ui.command.setText(api.get_button_command(deck_id, button_id))
    ui.keys.setText(api.get_button_keys(deck_id, button_id))
    ui.write.setText(api.get_button_write(deck_id, button_id))
    ui.change_brightness.setValue(api.get_button_change_brightness(deck_id, button_id))


def build_buttons(ui, tab):
    deck_id = _deck_id(ui)
    deck = api.get_deck(deck_id)

    for child in tab.children()[0].children():
        child.deleteLater()

    row_layout = QtWidgets.QVBoxLayout()
    tab.children()[0].addLayout(row_layout, 0, 0)
    index = 0
    buttons = []
    for _row in range(deck["layout"][0]):
        column_layout = QtWidgets.QHBoxLayout()
        row_layout.addLayout(column_layout)

        for _column in range(deck["layout"][1]):
            button = QtWidgets.QToolButton()
            button.setCheckable(True)
            button.index = index
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setIconSize(QSize(100, 100))
            button.setStyleSheet(BUTTON_SYTLE)
            buttons.append(button)
            column_layout.addWidget(button)
            index += 1

    for button in buttons:
        button.clicked.connect(
            lambda button=button, buttons=buttons: button_clicked(ui, button, buttons)
        )

    redraw_buttons(ui)
    buttons[0].click()





class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window_shown: bool = True

    def closeEvent(self, event):
        self.window_shown = False
        self.hide()
        event.ignore()

    def systray_clicked(self, _status=None):
        self.hide()
        if self.window_shown:
            self.window_shown = False
            return

        self.show()
        self.activateWindow()
        getattr(self, "raise")()
        self.window_shown = True


def start():
    app = QApplication(sys.argv)

    logo = QIcon(LOGO)
    main_window = MainWindow()
    ui = main_window.ui
    main_window.setWindowIcon(logo)
    tray = QSystemTrayIcon(logo, app)
    tray.activated.connect(main_window.systray_clicked)

    menu = QMenu()
    action_exit = QAction("Exit")
    action_exit.triggered.connect(app.exit)
    menu.addAction(action_exit)

    tray.setContextMenu(menu)

    ui.text.textChanged.connect(partial(update_button_text, ui))
    ui.command.textChanged.connect(partial(update_button_command, ui))
    ui.keys.textChanged.connect(partial(update_button_keys, ui))
    ui.write.textChanged.connect(partial(update_button_write, ui))
    ui.change_brightness.valueChanged.connect(partial(update_change_brightness, ui))
    ui.imageButton.clicked.connect(partial(select_image, ui))
    ui.brightness.valueChanged.connect(partial(set_brightness, ui))
    for deck_id, deck in api.open_decks().items():
        ui.device_list.addItem(f"{deck['type']} - {deck_id}", userData=deck_id)

    build_buttons(ui, ui.cards.currentWidget())

    ui.brightness.setValue(api.get_brightness(_deck_id(ui)))

    tray.show()
    main_window.show()
    return sys.exit(app.exec_())


if __name__ == "__main__":
    start()
