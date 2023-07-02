from pipe_conn import NamedPipe

gerchik_pipe = NamedPipe('gerchik')

gerchik_pipe.create_pipe_server()
gerchik_pipe.connect_pipe()

while True:
    data = gerchik_pipe.read_pipe()
    print(f"Received from Gerchik: {data}")
