# import your NamedPipe class
from pipe_conn import NamedPipe
from time import gmtime, strftime
import logging

# setup logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Create named pipes for all terminals
logging.debug('Creating named pipes...')

# Create named pipes for all terminals
terminal_sender = NamedPipe("send")
terminal_sender.create_pipe_server()
terminal_sender2 = NamedPipe("send2")
terminal_sender2.create_pipe_server()

terminal_receiver = NamedPipe("gerchik")
terminal_receiver.create_pipe_server()
terminal_receiver2 = NamedPipe("tickmill")
terminal_receiver2.create_pipe_server()

# Set difference between broker's prices
DELTA_TICKS = 0.0003
print(f'DELTA_TICKS = {DELTA_TICKS}')

# Set commands to clients
OP_BUY = 0
OP_SELL = 1

# Attempt to connect to the pipes
logging.debug("Attempting to connect to pipes...")

terminal_sender.connect_pipe()
terminal_sender2.connect_pipe()
terminal_receiver.connect_pipe()
terminal_receiver2.connect_pipe()

while True:
    data1 = terminal_sender.read_pipe().split(',')
    data2 = terminal_sender2.read_pipe().split(',')
    logging.debug(f'Data received: {data1} and {data2}')

    # convert string data to float
    for i in range(2, 5):
        data1[i] = float(data1[i])
        data2[i] = float(data2[i])

    mid1, buy_orders1, sell_orders1 = data1[2], data1[3], data1[4]
    mid2, buy_orders2, sell_orders2 = data2[2], data2[3], data2[4]

    # write commands back to the terminals
    if data1[1] == data2[1]:
        if mid1 - mid2 > DELTA_TICKS:
            terminal_receiver.write_pipe([OP_BUY])
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'BUY', data2[1])
            terminal_receiver2.write_pipe([OP_SELL])
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'SELL', data1[1])

        elif mid2 - mid1 > DELTA_TICKS:
            terminal_receiver.write_pipe([OP_SELL])
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'SELL', data2[1])
            terminal_receiver2.write_pipe([OP_BUY])
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'BUY', data1[1])

        # handle cases where mid1 and mid2 are close to each other
        elif DELTA_TICKS / 3 > mid1 - mid2 > 0:
            terminal_receiver.write_pipe(2)
            terminal_receiver2.write_pipe(2)

        elif DELTA_TICKS / 3 > mid2 - mid1 > 0:
            terminal_receiver2.write_pipe(2)
            terminal_receiver.write_pipe(2)

        else:
            terminal_receiver.write_pipe('-')
            terminal_receiver2.write_pipe('-')

logging.debug('Operation ended.')
