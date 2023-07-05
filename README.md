# LATENCY-ARBITRAGE

Python and MT4 system for latency arbitrage

1. Create a named pipe on Windows, provide methods to connect to pipes, read from them, write to them, and close them. This code will make use of the ctypes module to access the necessary Windows API functions for creating and manipulating the named pipe.

**Now, one can use this `NamedPipe` class in an application to facilitate the communication between Python scripts and MT4 terminals.**

Continue with the next steps:

1. Create Scripts to Connect to Each Terminal: one will want to create separate scripts for each terminal. These scripts will use the NamedPipe class we've defined to connect to the named pipe associated with each terminal.

1. Create MT4 Scripts: one will need to create scripts in MQL4 (the programming language used by MT4) that send market data to the named pipe and receive trading commands from it. These scripts will need to be loaded onto the MT4 terminals.

1. Create Arbitrage Script: this script will be the main part of your system. It will read market data from the named pipes, calculate the differences in bid/ask prices between the two terminals, and send trading commands back to the terminals when it detects an arbitrage opportunity.

1. Test the System: once we've created all the scripts, we can start testing the system. You'll want to begin with paper trading to ensure the system is working correctly before risking real money.

`DONE . . .`
