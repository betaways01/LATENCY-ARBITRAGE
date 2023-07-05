// ReceiveCommandsEA.mq4

#property strict

extern string PipeName = "mt4_pipe1";  // Change this for each terminal

int handle;

int OnInit()
{
   // Open the pipe in OnInit so that it stays open
   handle = FileOpen("\\\\.\\pipe\\" + PipeName, FILE_BIN | FILE_READ);
   if (handle == INVALID_HANDLE)
   {
      Print("Failed to open pipe: " + (string)GetLastError());
      return(INIT_FAILED);
   }

   return(INIT_SUCCEEDED);
}

void OnTick()
{
   if (FileIsEnding(handle))  // If there is data to read
   {
      // Read the command from the pipe
      string command = FileReadString(handle);

      // Execute the trade
      if (command == "BUY")
      {
         int ticket = OrderSend(_Symbol, OP_BUY, 1, Ask, 3, 0, 0);
         if(ticket < 0) Print("Buy order failed. Error code: ", GetLastError());
      }
      else if (command == "SELL")
      {
         int ticket = OrderSend(_Symbol, OP_SELL, 1, Bid, 3, 0, 0);
         if(ticket < 0) Print("Sell order failed. Error code: ", GetLastError());
      }
   }
}

void OnDeinit(const int reason)
{
   // Close the pipe when the EA is removed
   FileClose(handle);
}
