//+------------------------------------------------------------------+
//|                                                 pipeListener.mq4 |
//|                                                                  |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright ""
#property link      ""
#property version   "1.00"
#property strict

#import "kernel32.dll"
void GetSystemTime(int &t[4]);
#import

#include <Files\FilePipe.mqh>
//#include <MyLib.mqh>

extern string recieveChannelName="gerchik";
input int    postfixLenght     = 1;
extern string symbolName="EURUSD";
extern int maxSpread=15;
extern int maxSlippage=10;
extern int trailingSL = 30;
extern double lotSize=0.01;

int systemTimeBuffer[8];
CFilePipe  send;
CFilePipe  recieve;

int sendHandle,recieveHandle;

MqlTick last_tick;

ulong last_time=0;
long time_system=0;
long file_size=0;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetMillisecondTimer(1);
   while(!IsStopped())
     {
      recieveHandle=recieve.Open("\\\\.\\pipe\\"+recieveChannelName+"Receiver"+symbolName,FILE_READ);
      if(recieveHandle!=INVALID_HANDLE)
        {
         Print("Pipe recieve open");
         break;
        }
      Print("Wait receive, Sleep...");
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

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---

  }
  
  
 void closeBuyOnlyProfit(string symbol, int magic)
{
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      if(OrderSymbol() != symbol || OrderMagicNumber() != magic) continue;
      if(OrderType() == OP_BUY && OrderProfit() > 0)
      {
         if(!OrderClose(OrderTicket(), OrderLots(), Bid, 3, clrRed))
            Print("OrderClose error ", GetLastError());
      }
   }
}

void closeSellOnlyProfit(string symbol, int magic)
{
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      if(OrderSymbol() != symbol || OrderMagicNumber() != magic) continue;
      if(OrderType() == OP_SELL && OrderProfit() > 0)
      {
         if(!OrderClose(OrderTicket(), OrderLots(), Ask, 3, clrRed))
            Print("OrderClose error ", GetLastError());
      }
   }
}
 
 
  
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   last_time=GetMicrosecondCount();
   int buyOrders=ordersCount(OP_BUY,Symbol(),111);
   int sellOrders=ordersCount(OP_SELL,Symbol(),111);

   file_size=FileGetInteger(recieveHandle,FILE_SIZE);
   if(file_size>0)
     {
      string fromServerString=FileReadString(recieveHandle,file_size);

      if(fromServerString!="Wait" || fromServerString!="WaitWait")
        {
         if(fromServerString=="1" || fromServerString=="11" || fromServerString=="111")
           {
            if(sellOrders<1 && MarketInfo(Symbol(),MODE_SPREAD)<maxSpread)
              {
               if(!OrderSend(Symbol(),1,lotSize,Bid,maxSlippage,0,0,(string)Bid,111,0,clrNONE))
                 {
                  Print(GetLastError());
                 }
              }
           }
         if(fromServerString=="0" || fromServerString=="00" || fromServerString=="000")
           {
            if(buyOrders<1 && MarketInfo(Symbol(),MODE_SPREAD)<maxSpread)
              {
               if(!OrderSend(Symbol(),0,lotSize,Ask,maxSlippage,0,0,(string)Ask,111,0,clrNONE))
                 {
                  Print(GetLastError());
                 }
              }
           }
         if(buyOrders>0)
           {
            if(fromServerString=="2" || fromServerString=="22" || fromServerString=="222")
               closeBuyOnlyProfit(Symbol(),111);
            else
               Trailing(Symbol(),111,trailingSL);
           }

         if(sellOrders>0)
           {
            if(fromServerString=="3" || fromServerString=="33" || fromServerString=="333")
               closeSellOnlyProfit(Symbol(),111);
            else
               Trailing(Symbol(),111,trailingSL);
           }
        }  
        Comment("ea runtime: ",GetMicrosecondCount()-last_time," server message: ",fromServerString);    
     }
   
  }
//+------------------------------------------------------------------+
void Trailing(string symbol,int magic,int slTicks)
  {
   for(int i=1; i<=OrdersTotal(); i++) //Цикл по всем ордерам,..
     {                                        //отражённым в терминале
      if(OrderSelect(i-1,SELECT_BY_POS)==true)//Если есть следующий
        {
         if(OrderMagicNumber()==magic && OrderSymbol()==symbol)
           {
            if(OrderType()==0)
              {
               if(OrderStopLoss()==0)
                  if(!OrderModify(OrderTicket(),OrderOpenPrice(),NormalizeDouble(OrderOpenPrice()-slTicks*Point+(Ask-Bid),Digits),OrderTakeProfit(),OrderExpiration(),clrNONE))
                     Print("Init Stop Trailing Error: ",GetLastError());

               if(OrderStopLoss()<Bid-slTicks*Point)
                 {
                  if(!OrderModify(OrderTicket(),OrderOpenPrice(),NormalizeDouble(Bid-slTicks*Point,Digits),OrderTakeProfit(),OrderExpiration(),clrNONE))
                     Print("Trailing Error: ",GetLastError());
                 }
              }
            if(OrderType()==1)
              {
               if(OrderStopLoss()==0)
                  if(!OrderModify(OrderTicket(),OrderOpenPrice(),NormalizeDouble(OrderOpenPrice()+slTicks*Point,Digits)+(Ask-Bid),OrderTakeProfit(),OrderExpiration(),clrNONE))
                     Print("Init Stop Trailing Error: ",GetLastError());

               if(OrderStopLoss()>Ask+slTicks*Point)
                 {
                  if(!OrderModify(OrderTicket(),OrderOpenPrice(),NormalizeDouble(Ask+slTicks*Point,Digits),OrderTakeProfit(),OrderExpiration(),clrNONE))
                     Print("Trailing Error: ",GetLastError());
                 }
              }
           }
        }
     }
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int ordersCount(int type,string symbol,int magic)
  {
   int ordersCounter=0;
   for(int i=1; i<=OrdersTotal(); i++) //Цикл по всем ордерам,..
     {
      if(OrderSelect(i-1,SELECT_BY_POS)==true)//Если есть следующий
        {
         if(OrderType()==type && Symbol()==symbol && OrderMagicNumber()==magic)
           {
            ordersCounter++;
           }
        }
     }
   return ordersCounter;
  }
//+------------------------------------------------------------------+
