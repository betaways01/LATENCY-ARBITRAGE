import logging
from Pipe.named_pipe import NamedPipe

DELTA_TICKS = 0.00001  # Change this according to your needs

# Create named pipes for communication with MT4
terminal_sender1 = NamedPipe('\\\\.\\pipe\\mt4_pipe1')
terminal_sender2 = NamedPipe('\\\\.\\pipe\\mt4_pipe2')

# Connect to the named pipes
if not terminal_sender1.connect() or not terminal_sender2.connect():
    logging.error('Failed to connect to one or more terminal senders. Exiting...')
    exit()

while True:
    data1 = terminal_sender1.read().split(',')
    data2 = terminal_sender2.read().split(',')

    mid1, buy_orders1, sell_orders1 = map(float, data1[2:5])
    mid2, buy_orders2, sell_orders2 = map(float, data2[2:5])

    if data1[1] == data2[1]:  # Check if symbols match
        if mid1 - mid2 > DELTA_TICKS:
            terminal_sender2.write('BUY')
            logging.info(f'{data2[0]}: BUY {data2[1]}')
            terminal_sender1.write('SELL')
            logging.info(f'{data1[0]}: SELL {data1[1]}')
        elif mid2 - mid1 > DELTA_TICKS:
            terminal_sender2.write('SELL')
            logging.info(f'{data2[0]}: SELL {data2[1]}')
            terminal_sender1.write('BUY')
            logging.info(f'{data1[0]}: BUY {data1[1]}')
        elif abs(mid1 - mid2) < DELTA_TICKS / 3:
            terminal_sender1.write('2')
            terminal_sender2.write('2')
        else:
            terminal_sender1.write('-')
            terminal_sender2.write('-')
