import ctypes
from ctypes import wintypes as ct
#from ctypes.wintypes import BOOL, HANDLE
import msvcrt
import os

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

# ctypes wrapper for some WinAPI functions
windll = ctypes.WinDLL('kernel32', use_last_error=True)
WaitNamedPipe = windll.WaitNamedPipeW
WaitNamedPipe.restype = ct.BOOL
CreateNamedPipe = windll.CreateNamedPipeW
CreateNamedPipe.restype = ct.HANDLE
ConnectNamedPipe = windll.ConnectNamedPipe
ConnectNamedPipe.restype = ct.BOOL
DisconnectNamedPipe = windll.DisconnectNamedPipe
DisconnectNamedPipe.restype = ct.BOOL
FlushFileBuffers = windll.FlushFileBuffers
FlushFileBuffers.restype = ct.BOOL

class NamedPipe:

    def __init__(self, pipe_name):
        self.pipe_name = r'\\.\pipe\{}'.format(pipe_name)
        self.pipe_handle = INVALID_HANDLE_VALUE

    def create_pipe_server(self):
        self.pipe_handle = CreateNamedPipe(
            self.pipe_name,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES,
            BUFSIZE,
            BUFSIZE,
            NMPWAIT_USE_DEFAULT_WAIT,
            None)

        if self.pipe_handle == INVALID_HANDLE_VALUE:
            raise ctypes.WinError()

    def connect_pipe(self):
        if not ConnectNamedPipe(self.pipe_handle, None):
            raise ctypes.WinError()

    def disconnect_pipe(self):
        if not DisconnectNamedPipe(self.pipe_handle):
            raise ctypes.WinError()

    def write_pipe(self, message):
        fd = msvcrt.open_osfhandle(self.pipe_handle, os.O_WRONLY)
        with os.fdopen(fd, 'w') as pipe:
            pipe.write(message)

    def read_pipe(self):
        fd = msvcrt.open_osfhandle(self.pipe_handle, os.O_RDONLY)
        with os.fdopen(fd, 'r') as pipe:
            return pipe.read(BUFSIZE)

    def flush_pipe(self):
        if not FlushFileBuffers(self.pipe_handle):
            raise ctypes.WinError()

    def close_pipe(self):
        if self.pipe_handle != INVALID_HANDLE_VALUE:
            ctypes.windll.kernel32.CloseHandle(self.pipe_handle)
