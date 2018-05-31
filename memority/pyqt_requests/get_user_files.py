from PyQt5.QtCore import pyqtSignal

from .base import AbstractGetRequest


class GetUserFilesRequest(AbstractGetRequest):
    finished = pyqtSignal(list)

    def __init__(self):
        super().__init__('/files/')

    def process_response_data(self, data: dict):
        if data.get('status') == 'success':
            self.finished.emit(
                data.get('data').get('files')
            )
