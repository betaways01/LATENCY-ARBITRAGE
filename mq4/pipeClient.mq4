//+------------------------------------------------------------------+
//|                                                   pipeClient.mq4 |
//|                                                           Trendy |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Trendy"
#property link      ""
#property version   "1.00"
#property strict
#import "kernel32.dll"
void GetSystemTime(int &t[4]);
#import

#include <Files\FilePipe.mqh>
//#include <MyLib.mqh>
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
input string recieveChannelName="tickmill";
input int    postfixLenght     = 0;
input string symbolName = "EURUSD";
input int markUpSpread = 4;
input double offset_value = 2.0;

int systemTimeBuffer[8];
char fromServer[];
string serverMessages[];
string fromServerString="hello";
uint msgLenght;
CFilePipe  send;
CFilePipe  recieve;
int sendHandle,recieveHandle;
string toServer;
MqlTick last_tick;
long last_time=0;
long time_system=0;
long file_size = 0;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   EventSetMillisecondTimer(1);
   while(!IsStopped())
     {
      sendHandle=send.Open("\\\\.\\pipe\\"+recieveChannelName+"Sender"+symbolName,FILE_READ|FILE_WRITE);
      if(sendHandle!=INVALID_HANDLE)
        {
         Print("Pipe send open");
         break;
        }
      Print("Wait send, Sleep...");
      Sleep(1000);
     }
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   Comment("");
   send.Close();
   recieve.Close();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
   if(SymbolInfoTick(Symbol(),last_tick))
     {
      if(last_tick.time_msc>last_time) // new tick
        {
         last_time = last_tick.time_msc;
         getSystemTime(systemTimeBuffer);
         time_system=systemTimeBuffer[6]+systemTimeBuffer[7]*1000+systemTimeBuffer[4]*60*1000+systemTimeBuffer[5]*60*60*1000;
        }
      toServer=StringConcatenate(AccountCompany(),",",
                                 last_tick.bid+markUpSpread*Point+offset_value,",",
                                 last_tick.ask-markUpSpread*Point+offset_value,",",
                                 time_system);
      if(!FileWriteString(sendHandle,toServer,StringLen(toServer)))
        {
         Print("Client: sending string failed, Deinit EA");
         ExpertRemove();
        }
      FileFlush(sendHandle);
      //FileSeek(sendHandle,0,SEEK_END);
     }
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void getSystemTime(int &b[8])
  {
   /*
        значения элементов  переданного массива будут иметь следующие индексы
        wYear As Integer           1  год
        wMonth As Integer          0  месяц
        wDayOfWeek As Integer      3  день недели
        wDay As Integer            2  день
        wHour As Integer           5  час
        wMinute As Integer         4  минута
        wSecond As Integer         7  секунда
        wMilliseconds As Integer   6  миллисекунда
      */
   int a[4];
   GetSystemTime(a);
   for(int i=0; i<4; i++)
     {
      b[2*i]=a[i];
      b[2*i+1]=a[i];
      b[2*i]>>=16;
      b[2*i+1]<<=16;
      b[2*i+1]>>=16;
     }
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
