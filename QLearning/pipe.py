# check if necessary packages are installed and import
try:
    from win32file import *
    from win32pipe import *
    from win32api import *
except ImportError:
    print("Please install the 'pywin32' module by running 'pip install pywin32==300'")
    import sys
    sys.exit(1)

import logging

# Constants
INVALID_HANDLE_VALUE = -1
ERROR_PIPE_BUSY = 231
ERROR_MORE_DATA = 234
BUFSIZE = 4096
NMPWAIT_USE_DEFAULT_WAIT = 0x00000000
PIPE_ACCESS_DUPLEX = 0x3
PIPE_TYPE_MESSAGE = 0x4
PIPE_READMODE_MESSAGE = 0x2
PIPE_WAIT = 0
PIPE_UNLIMITED_INSTANCES = 255

class Pipe:
    def __init__(self, name):
        try:
            self.handle = CreateNamedPipe("\\\\.\\pipe\\" + name,
                                          PIPE_ACCESS_DUPLEX,
                                          PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                                          PIPE_UNLIMITED_INSTANCES,
                                          1024,
                                          1024,
                                          0,
                                          None)
        except PermissionError:
            logging.error(f"Lack of permissions to create pipe '{name}'.")
            self.handle = None
        except WindowsError as e:
            if e.winerror == ERROR_PIPE_BUSY:
                logging.error(f"Pipe '{name}' is already in use.")
            elif e.winerror == ERROR_MORE_DATA:
                logging.error(f"System limit for number of pipes has been reached.")
            self.handle = None
        else:
            if self.handle == INVALID_HANDLE_VALUE:
                logging.error(f"Failed to create pipe '{name}': {GetLastError()}")
                self.handle = None

    def is_connect(self):
        if ConnectNamedPipe(self.handle) == 0:
            return True
        else:
            return False

    def get_handle(self):
        return self.handle

    def read(self, size):
        return ReadFile(self.handle, size)

    def read_as_string(self, size):
        data = ReadFile(self.handle, size)
        string = bytearray(data[1]).decode().strip()
        return str(string)

    def write(self, data):
        WriteFile(self.handle, bytearray(data, 'cp1251'))
        FlushFileBuffers(self.handle)
        #SetFilePointer(self.handle, 0, FILE_END)
        '''if wr[0] != 0:
            print(GetLastError())'''
