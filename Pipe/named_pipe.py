import time
import logging
from win32file import *
from win32pipe import *
from win32api import *

class NamedPipe:

    def __init__(self, pipe_name):
        self.pipe_name = pipe_name
        self.pipe_handle = None

    def connect(self):
        self.pipe_handle = CreateNamedPipe(
            self.pipe_name,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            1, 65536, 65536,
            0,
            None
        )

        # if pipe handle is valid, connect to the pipe
        if (self.pipe_handle != INVALID_HANDLE_VALUE):
            ConnectNamedPipe(self.pipe_handle, None)
            return True
        else:
            logging.error("Failed to create pipe on %s" % self.pipe_name)
            return False

    def read(self, max_length=1024):
        result, data = ReadFile(self.pipe_handle, max_length)
        return data.decode('utf-8')

    def write(self, data):
        WriteFile(self.pipe_handle, data.encode('utf-8'))

    def disconnect(self):
        DisconnectNamedPipe(self.pipe_handle)
