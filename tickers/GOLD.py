from QLearning.pipe import Pipe
import time

# Create named pipes for all terminals
currency = "DAX"
terminal1 = "gerchik"
terminal2 = "quantix"

terminal_sender = Pipe(terminal1 + "Sender" + currency)
terminal_sender2 = Pipe(terminal2 + "Sender" + currency)
terminal_receiver = Pipe(terminal1 + "Receiver" + currency)
terminal_receiver2 = Pipe(terminal2 + "Receiver" + currency)

# set difference between broker's prices
DELTA_TICKS = 4.0
# set maximal delay
MAX_DELAY = 1000
# set commands to clients
OP_BUY = '0'
OP_SELL = '1'
OP_CLOSE_BUY = '2'
OP_CLOSE_SELL = '3'
print(DELTA_TICKS)
if terminal_receiver.is_connect() and terminal_receiver2.is_connect():
    while True:
        data1 = terminal_sender.read_as_string(1024).split(',')
        data2 = terminal_sender2.read_as_string(1024).split(',')

        bid1, ask1, time1 = float(data1[1]), float(data1[2]), int(data1[3])
        bid2, ask2, time2 = float(data2[1]), float(data2[2]), int(data2[3])

        if 0 < time1 - time2 < MAX_DELAY:
            if bid1 - ask2 >= DELTA_TICKS:
                terminal_receiver2.write(OP_BUY)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), data2[0], 'BUY', time2 - time1, bid1 - ask2)
            elif bid2 - ask1 >= DELTA_TICKS:
                terminal_receiver2.write(OP_SELL)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), data2[0], 'SELL', time2 - time1, bid2 - ask1)

        if 0 < time2 - time1 < MAX_DELAY:
            if bid2 - ask1 >= DELTA_TICKS:
                terminal_receiver.write(OP_BUY)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), data1[0], 'BUY', time1 - time2, bid2 - ask1)
            elif bid1 - ask2 >= DELTA_TICKS:
                terminal_receiver.write(OP_SELL)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), data1[0], 'SELL', time1 - time2, bid1 - ask2)

        if bid2 - ask1 >= DELTA_TICKS / 3.0:
            terminal_receiver2.write(OP_CLOSE_BUY)
        elif bid1 - ask2 >= DELTA_TICKS / 3.0:
            terminal_receiver2.write(OP_CLOSE_SELL)
        else:
            terminal_receiver2.write('WAIT')

        if bid1 - ask2 >= DELTA_TICKS / 3.0:
            terminal_receiver.write(OP_CLOSE_BUY)
        elif bid2 - ask1 >= DELTA_TICKS / 3.0:
            terminal_receiver.write(OP_CLOSE_SELL)
        else:
            terminal_receiver.write('WAIT')