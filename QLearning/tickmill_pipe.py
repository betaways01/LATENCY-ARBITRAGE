from pipe_conn import NamedPipe

tickmill_pipe = NamedPipe('tickmill')

tickmill_pipe.create_pipe_server()
tickmill_pipe.connect_pipe()

while True:
    data = tickmill_pipe.read_pipe()
    print(f"Received from Tickmill: {data}")
