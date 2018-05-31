from PyQt5.QtCore import pyqtSignal

from .base import AbstractGetRequest


class GetBoxDirRequest(AbstractGetRequest):
    finished = pyqtSignal(str)

    def __init__(self):
        super().__init__('/info/boxes_dir/')

    def process_response_data(self, data: dict):
        if data.get('status') == 'success':
            self.finished.emit(
                data.get('data').get('boxes_dir')
            )
