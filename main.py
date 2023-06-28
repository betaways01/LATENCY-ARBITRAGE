from QLearning.pipe import Pipe
from time import gmtime, strftime

import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Create named pipes for all terminals
logging.debug('Creating named pipes...')

# Create named pipes for all terminals
terminal_sender = Pipe("send")
if terminal_sender.handle is None:
    logging.error("Failed to create pipe 'send'")
    import sys
    sys.exit(1)

terminal_sender2 = Pipe("send")
if terminal_sender2.handle is None:
    logging.error("Failed to create pipe 'send'")
    import sys
    sys.exit(1)

terminal_receiver = Pipe("gerchik")
if terminal_receiver.handle is None:
    logging.error("Failed to create pipe 'gerchik'")
    import sys
    sys.exit(1)

terminal_receiver2 = Pipe("tickmill")
if terminal_receiver2.handle is None:
    logging.error("Failed to create pipe 'tickmill'")
    import sys
    sys.exit(1)

# set difference between broker's prices
DELTA_TICKS = 0.0003
# set commands to clients
OP_BUY = 0
OP_SELL = 1


# print statements to indicate success or failure:
if terminal_sender.is_connect():
    logging.debug("Pipe 'send' connected")
else:
    logging.error("Failed to connect pipe 'send'")
    import sys
    sys.exit(1)

if terminal_sender2.is_connect():
    logging.debug("Pipe 'send' connected")
else:
    logging.error("Failed to connect pipe 'send'")
    import sys
    sys.exit(1)

if terminal_receiver.is_connect():
    logging.debug("Pipe 'gerchik' connected")
else:
    logging.error("Failed to connect pipe 'gerchik'")
    import sys
    sys.exit(1)

if terminal_receiver2.is_connect():
    logging.debug("Pipe 'tickmill' connected")
else:
    logging.error("Failed to connect pipe 'tickmill'")
    import sys
    sys.exit(1)



if terminal_sender.is_connect():
    if terminal_sender2.is_connect():
        while True:
            data1 = terminal_sender.read_as_string(1024).split(',')
            data2 = terminal_sender2.read_as_string(1024).split(',')
            logging.debug(f'Data received: {data1} and {data2}')

            for i in range(2, 5):
                data1[i] = float(data1[i])
            for i in range(2, 5):
                data2[i] = float(data2[i])

            mid1, buy_orders1, sell_orders1 = data1[2], data1[3], data1[4]
            mid2, buy_orders2, sell_orders2 = data2[2], data2[3], data2[4]

            if data1[1] == data2[1]:
                if mid1 - mid2 > DELTA_TICKS:
                    terminal_receiver2.write([OP_BUY])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'BUY', data2[1])
                    terminal_receiver.write([OP_SELL])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'SELL', data1[1])

                elif mid2 - mid1 > DELTA_TICKS:
                    terminal_receiver2.write([OP_SELL])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'SELL', data2[1])
                    terminal_receiver.write([OP_BUY])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'BUY', data1[1])

                elif DELTA_TICKS / 3 > mid1 - mid2 > 0:
                    terminal_receiver.write(2)
                    terminal_receiver2.write(2)

                elif DELTA_TICKS / 3 > mid2 - mid1 > 0:
                    terminal_receiver2.write(2)
                    terminal_receiver.write(2)

                else:
                    terminal_receiver.write('-')
                    terminal_receiver2.write('-')

logging.debug('Operation ended.')
