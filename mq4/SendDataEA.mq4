// SendDataEA.mq4

#property strict

extern string PipeName = "mt4_pipe1";  // Change this for each terminal

int handle;

int OnInit()
{
   // Open the pipe in OnInit so that it stays open
   handle = FileOpen("\\\\.\\pipe\\" + PipeName, FILE_BIN | FILE_WRITE);
   if (handle == INVALID_HANDLE)
   {
      Print("Failed to open pipe: " + (string)GetLastError());
      return(INIT_FAILED);
   }

   return(INIT_SUCCEEDED);
}

void OnTick()
{
   // Prepare the data
   string timestamp = TimeToStr(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   double mid = (Bid + Ask) / 2;
   string data = timestamp + "," + _Symbol + "," + DoubleToString(mid, _Digits) + ","; 

   // Add additional data as needed...

   // Write the data to the pipe
   FileWriteString(handle, data);
}

void OnDeinit(const int reason)
{
   // Close the pipe when the EA is removed
   FileClose(handle);
}
