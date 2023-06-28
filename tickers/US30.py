from QLearning.pipe import Pipe
from time import gmtime, strftime

# Create named pipes for all terminals
terminal_sender = Pipe("gerchikSenderUS30")
terminal_sender2 = Pipe("tickmillSenderUS30")
terminal_receiver = Pipe("gerchikRecieverUS30")
terminal_receiver2 = Pipe("tickmillRecieverUS30")

# set difference between broker's prices
DELTA_TICKS = 3
# set maximal spread
MAX_SPREAD = 3
# set minimal delay
MIN_DELAY = 100
# set commands to clients
OP_BUY = '0'
OP_SELL = '1'
OP_CLOSE_BUY = '2'
OP_CLOSE_SELL = '3'
print(DELTA_TICKS)
print(DELTA_TICKS)
if terminal_sender.is_connect():
    if terminal_sender2.is_connect():
        while True:
            data1 = terminal_sender.read_as_string(1024).split(',')
            data2 = terminal_sender2.read_as_string(1024).split(',')

            bid1, ask1, time1_sec = float(data1[2]), float(data1[3]), int(data1[4])
            bid2, ask2, time2_sec = float(data2[2]), float(data2[3]), int(data2[4])

            print('First Broker - Second Broker lag in ms:', time1_sec - time2_sec)
            if data1[1] == data2[1]:
                # Second = Feed, First = Trade
                if MIN_DELAY > time2_sec - time1_sec > 0:
                    if ask1 - bid2 <= -DELTA_TICKS:  # Buy on First
                        terminal_receiver.write(OP_BUY)
                        print(data1[0], 'BUY', data1[1], 'time diff: ', time2_sec - time1_sec)
                    elif ask1 - bid2 >= DELTA_TICKS / 3.0:
                        terminal_receiver.write(OP_CLOSE_BUY)  # Close Buy on First
                        print(data1[0], 'CLOSE BUY', data1[1])
                    elif ask2 - bid1 <= -DELTA_TICKS:  # Sell on First
                        terminal_receiver.write(OP_SELL)
                        print(data1[0], 'SELL', data1[1], 'time diff: ', time2_sec - time1_sec)
                    elif ask2 - bid1 >= DELTA_TICKS / 3.0:
                        terminal_receiver.write(OP_CLOSE_SELL)  # Close Sell on First
                        print(data1[0], 'CLOSE SELL', data1[1])
                    else:
                        terminal_receiver.write('WAIT')
                        terminal_receiver2.write('WAIT')

                # First = Feed, Second = Trade
                if MIN_DELAY > time1_sec - time2_sec > 0:
                    if ask2 - bid2 <= MAX_SPREAD:
                        if ask2 - bid1 <= -DELTA_TICKS:  # Buy on Second
                            terminal_receiver2.write(OP_BUY)
                            print(data2[0], 'BUY', data2[1], 'time diff: ', time1_sec - time2_sec)
                        elif ask2 - bid1 >= DELTA_TICKS / 3.0:
                            terminal_receiver2.write(OP_CLOSE_BUY)  # Close Buy on Second
                            print(data2[0], 'CLOSE BUY', data2[1])
                        elif ask1 - bid2 <= -DELTA_TICKS:  # Sell on Second
                            terminal_receiver2.write(OP_SELL)
                            print(data2[0], 'SELL', data2[1], 'time diff: ', time1_sec - time2_sec)
                        elif ask1 - bid2 >= DELTA_TICKS / 3.0:
                            terminal_receiver2.write(OP_CLOSE_SELL)  # Close Sell on Second
                            print(data2[0], 'CLOSE SELL', data2[1])
                        else:
                            terminal_receiver.write('WAIT')
                            terminal_receiver2.write('WAIT')
