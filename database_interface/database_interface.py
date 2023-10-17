"""
Copyright (C) 2023, NG:ITL
"""

import os
import sys
import json

from pathlib import Path
from typing import List, Optional, Dict

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QSocketNotifier
from database_interface.database_interface_model import DatabaseModel

def find_qml_main_file(relative_path: str) -> Path:
    search_directory_list = [
        Path(os.getcwd()),
        Path(os.getcwd()).parent,
        Path(__file__).parent
    ]
    for directory in search_directory_list:
        filepath = directory / relative_path
        if filepath.is_file():
            print(f'chose: {filepath}')
            return filepath
    raise FileNotFoundError(f'Unable to find QML File: {relative_path}')

def resource_path() -> Path:
    base_path = getattr(sys, "_MEIPASS", os.getcwd())
    return Path(base_path)


class DatabaseInterface:

    def __init__(self) -> None:
        self.__app = QGuiApplication(sys.argv)
        self.__engine = QQmlApplicationEngine()
        self.__engine.load(resource_path() / "frontend/qml/main.qml")
        self.__engine.rootContext().setContextProperty("databaseInterface", self)
        self.__config = json.load(open(find_qml_main_file("database_interface_config.json")))
        self.database = DatabaseModel(settings=self.__config, parent=self.__app)
        self.__engine.rootContext().setContextProperty("database", self.database)

    
    def run(self) -> None:
        if not self.__engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.__app.exec())
