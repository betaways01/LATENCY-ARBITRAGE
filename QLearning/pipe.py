# check if necessary packages are installed and import
try:
    from win32file import *
    from win32pipe import *
    from win32api import *
except ImportError:
    print("Please install the 'pywin32' module by running 'pip install pywin32==300'")
    import sys
    sys.exit(1)


class Pipe:
    def __init__(self, name):
        self.handle = CreateNamedPipe("\\\\.\\pipe\\" + name,
                                      PIPE_ACCESS_DUPLEX,
                                      PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                                      PIPE_UNLIMITED_INSTANCES,
                                      1024,
                                      1024,
                                      0,
                                      None)
        if self.handle == INVALID_HANDLE_VALUE:
            print("CreateNamedPipe Error : ", GetLastError())
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
