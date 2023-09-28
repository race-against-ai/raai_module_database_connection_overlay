import json
import threading
import asyncio
import pynng

from typing import List, Optional, Dict
from PySide6.QtCore import QObject, Signal, Property

class DataModel(QObject):
    dictDataChanged = Signal(name="dictDataChanged")
    valuesChanged = Signal(name="valuesChanged")
    keysChanged = Signal(name="keysChanged")

    def __init__(self, data: dict) -> None:
        QObject.__init__(self)
        self.__data = data
        self.__values = []
        self.__populate_values()
        # print(self.__data)
    
    def __populate_values(self):
        for value in self.__data.values():
            self.__values.append(value)

    @Property("QVariantMap", notify=dictDataChanged)
    def data(self) -> dict:
        return self.__data
    
    @Property("QVariantList", notify=valuesChanged)
    def values(self) -> List[str]:
        return self.__values

    @Property("QVariantList", notify=keysChanged)
    def keys(self) -> List[str]:
        return self.__data.keys()

class KeyModel(QObject):

    keyChanged = Signal(name="keyChanged")

    def __init__(self, key: str) -> None:
        QObject.__init__(self)
        self.__key = key
    
    @Property(str, notify=keyChanged)
    def key(self) -> str:
        return self.__key

class DatabaseModel(QObject):
    dataChanged = Signal(name="dataChanged")
    availableKeysChanged = Signal(name="availableKeysChanged")
    showUnsentData = Signal(name="showUnsentData")
    availableData = Signal(name="availableData")
    
    connectionEstablished = Signal()
    retryConnection = Signal(name="retryConnection")
    requestFromDatabase = Signal(str, name="requestFromDatabase")
    changeShownData = Signal(str, name="changeShownData")

    def __init__(self, settings: dict, parent=None) -> None:
        super().__init__(parent)
        self.__database_connection_info = {
            "internet_connection": False,
            "unsent_data": {},
            "current_driver": "None",
            "current_convention": "None",
            "current_lap": {},
            "data": {}
        }
        self.__settings = settings

        self._data: List[DataModel] = []
        self.__database_keys: List[KeyModel] = []
        
        self.__lap_times = []
        self.__unsent_data = []
        self.__drivers = []
        self.__conventions = []

        self.__request_socket = None
        self.__connection_state = False
        self.__connect_to_server()
        self.__valid_requests = ["get_data", "get_data_by_id", "refresh", "reconnect"]

        self.__available_data_entries = ["Lap Times", "Drivers", "Conventions", "Unsent Data"]
        self.__current_shown_Data = "Lap Times"

        self.__determine_shown_data()

        self.retryConnection.connect(self.__connect_to_server)
        self.requestFromDatabase.connect(self.__send_request)
        self.changeShownData.connect(self.__change_shown_data)
    

    def __connect_to_server(self) -> None:
        if self.__connection_state == False:
            request_address = self.__settings["pynng"]["requesters"]["connection_overlay"]["address"]
            print(f"Connecting to {request_address}")
            self.__request_socket = pynng.Req0()
            try: 
                print("Trying to connect")
                self.__request_socket.dial(request_address, block=True)
                self.__connection_state = True
                self.__update_connection_status()
                print("Connected")
            except pynng.exceptions.ConnectionRefused:
                print("Connection failed")
                self.__connection_state = False
                self.__update_connection_status()

    def __update_connection_status(self) -> None:
        self.connectionEstablished.emit()
    
    def __update_database_entries(self) -> None:
        self.__database_connection_info = self.__database_connection_info
        self.__lap_times = self.__database_connection_info["lap_times"]
        # print(self.__lap_times)
        self.__unsent_data = self.__database_connection_info["unsent_data"]
        # print(self.__unsent_data)
        self.__drivers = self.__database_connection_info["drivers"]
        # print(self.__drivers)
        self.__conventions = self.__database_connection_info["conventions"]
        # print(self.__conventions)
        self.__determine_shown_data()

    def __determine_shown_data(self) -> None:
        data = self.__current_shown_Data
        if data == "Lap Times":
            self.__convert_database_to_data(self.__lap_times)
        elif data == "Drivers":
            self.__convert_database_to_data(self.__drivers)
        elif data == "Conventions":
            self.__convert_database_to_data(self.__conventions)
        elif data == "Unsent Data":
            self.__convert_database_to_data(self.__unsent_data)
        else:
            print("Invalid data type")
        self.dataChanged.emit()

    def __convert_data_to_model(self, data: dict) -> DataModel:
        return DataModel(data)

    def __convert_database_to_data(self, database: dict) -> None:
        print_check = False
        self.__database_keys = []
        self.__cleanup_data()
        if len(database) > 0:
            for key in database["1"].keys():
                self.__database_keys.append(KeyModel(key))
                print(key)
            self.__database_keys.append(KeyModel(""))
            for entry in database:
                if not print_check:
                    print(database[entry])
                    print_check = True

                self.__add_data(self.__convert_data_to_model(database[entry]))
        
        self.availableKeysChanged.emit()
        self.dataChanged.emit()

    def __cleanup_data(self) -> None:
        self._data = []
        self.dataChanged.emit()

    def __add_data(self, data: DataModel) -> None:
        self._data.append(data)
    
    def __send_request(self, request: str) -> None:
        if self.__connection_state and request in self.__valid_requests:
            try:
                self.__request_socket.send(request.encode(), block=False)
                print(f"Sent request: {request}")
                response = self.__request_socket.recv()

                if request == "refresh":
                    response = response.decode('utf-8')
                    try:
                        response = json.loads(response)
                        if isinstance(response, dict):
                            self.__database_connection_info = response
                            self.__update_database_entries()
                            
                    except json.decoder.JSONDecodeError:
                        print("can't be used as dict")

                elif request == "reconnect":
                    print(f"Received response: {response.decode()}")
                
                elif request == "get_data":
                    response = response.decode('utf-8')
                    try:
                        response = json.loads(response)
                        if isinstance(response, dict):
                            self.__database_connection_info = response
                            self.__update_database_entries()
                    except json.decoder.JSONDecodeError:
                        print("can't be used as dict")
                
                elif request == "get_data_by_id":
                    response = response.decode('utf-8')
                    try:
                        response = json.loads(response)
                        if isinstance(response, dict):
                            self.__database_connection_info = response
                            self.__update_database_entries()

                    except json.decoder.JSONDecodeError:
                        print("can't be used as dict")
            
            except pynng.TryAgain:
                print("no response")
                self.__connection_state = False
                self.__update_connection_status()


        elif request not in self.__valid_requests:
            print(f"Invalid request: {request}")

        else:
            print("No connection established")
    
    def __transform_database_data_to_list(self, data: dict) -> List[dict]:
        return sorted([(int(key), value) for key, value in data.items()])

    def __change_shown_data(self, data: str) -> None:
        self.__current_shown_Data = data
        self.__determine_shown_data()
        self.dataChanged.emit()

    @Property(int, notify=dataChanged)
    def keyAmount(self) -> int:
        return len(self.__database_keys)

    @Property("QVariantList", notify=dataChanged)
    def data(self) -> List[DataModel]:
        return self._data

    @Property(bool, notify=connectionEstablished)
    def connection_status(self) -> bool:
        return self.__connection_state
    
    @Property("QVariantList", notify=availableKeysChanged)
    def database_keys(self) -> List[str]:
        return self.__database_keys

    @Property("QVariantList", notify=availableData)
    def available_data_entries(self) -> List[str]:
        return self.__available_data_entries
