import MetaTrader5 as mt5
import pandas as pd
from typing import Dict
from datetime import datetime
from events.events import DataEvent
from queue import Queue

class DataProvider():
    def __init__(self,events_queue:Queue,Symbol_list: list,timeframe: str):
       self.symbols: list = Symbol_list
       self.timeframe: str = timeframe
       self.events_queue = events_queue
       
       #create dic to save latest tick of each symbol
       self.last_bar_datetime: Dict[str,datetime] = {symbol: datetime.min for symbol in self.symbols}
    
    
    def _map_timeFrames(self,timeFrame:str) -> int:
        
        timeFrame_Mapping = {
            '1min': mt5.TIMEFRAME_M1,
            '2min': mt5.TIMEFRAME_M2,                        
            '3min': mt5.TIMEFRAME_M3,                        
            '4min': mt5.TIMEFRAME_M4,                        
            '5min': mt5.TIMEFRAME_M5,                        
            '6min': mt5.TIMEFRAME_M6,                        
            '10min': mt5.TIMEFRAME_M10,                       
            '12min': mt5.TIMEFRAME_M12,
            '15min': mt5.TIMEFRAME_M15,
            '20min': mt5.TIMEFRAME_M20,                       
            '30min': mt5.TIMEFRAME_M30,                       
            '1h': mt5.TIMEFRAME_H1,                          
            '2h': mt5.TIMEFRAME_H2,                          
            '3h': mt5.TIMEFRAME_H3,                          
            '4h': mt5.TIMEFRAME_H4,                          
            '6h': mt5.TIMEFRAME_H6,                          
            '8h': mt5.TIMEFRAME_H8,                          
            '12h': mt5.TIMEFRAME_H12,
            '1d': mt5.TIMEFRAME_D1,                       
            '1w': mt5.TIMEFRAME_W1,                       
            '1M': mt5.TIMEFRAME_MN1,     
        }
        try:
            return timeFrame_Mapping[timeFrame]
        except:
            print(f"TimeFrame {timeFrame} is not valid")
    
    def get_latest_closed_bar(self,symbol: str,timeframe: str) -> pd.Series:
        #get latest bar info
        tf = self._map_timeFrames(timeframe)
        from_position = 1
        num_bars = 1
        try:
            bars_np_array = pd.DataFrame(mt5.copy_rates_from_pos(symbol,tf,from_position,num_bars))
            if bars_np_array is None:
                print(f"Symbol {symbol} doesn´t exist or cannot be achieved")
                return pd.Series()       
            else:
                bars = pd.DataFrame(bars_np_array)   
        
                bars['time'] = pd.to_datetime(bars['time'],unit='s')
                bars.set_index('time',inplace=True)
            
            #change order and reorganize columns
                bars.rename(columns={'tick_volume':'tickvol','real_volume':'vol'},inplace=True)
                bars = bars[['open','high','low','close','tickvol','vol','spread']]
        except Exception as e:
            print(f"unable to retrieve data from the last bar of {symbol} {timeframe}. MT5 error {mt5.last_error()} {e}")     
        else:
            #if dataframe is empty retun an empty series
            if bars.empty:
                return pd.Series()   
            else:
               return bars.iloc[-1] 
                
                
    def get_latest_closed_bars(self,symbol: str,timeframe: str, num_bars: int = 1) -> pd.DataFrame:
        tf = self._map_timeFrames(timeframe)
        from_position = 1
        bars_count = num_bars if num_bars > 0 else 1
        
        try:
            bars_np_array = pd.DataFrame(mt5.copy_rates_from_pos(symbol,tf,from_position,bars_count))
            if bars_np_array is None:
                print(f"Symbol {symbol} doesn´t exist or cannot be achieved")
                return pd.DataFrame()     
            else:
                bars = pd.DataFrame(bars_np_array)   
        
                bars['time'] = pd.to_datetime(bars['time'],unit='s')
                bars.set_index('time',inplace=True)
            
            #change order and reorganize columns
                bars.rename(columns={'tick_volume':'tickvol','real_volume':'vol'},inplace=True)
                bars = bars[['open','high','low','close','tickvol','vol','spread']]
        except Exception as e:
            print(f"unable to retrieve data from the last bar of {symbol} {timeframe}. MT5 error {mt5.last_error()} {e}")     
        else:
            return bars
                
    def get_latest_tick(self, symbol: str) -> dict:
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                print(f"Unable to retrieve data for symbol {symbol}.")
                return {}  
            return tick._asdict()  
        except Exception as e:
            print(f"Something went wrong while retrieving the latest tick for {symbol}: {e}")
            return {}   
    
    def check_for_new_date(self) -> None:
        for symbol in self.symbols:
            latest_bar = self.get_latest_closed_bar(symbol,self.timeframe)
            if latest_bar is None:
                continue
            if not latest_bar.empty and latest_bar.name > self.last_bar_datetime[symbol]:
                self.last_bar_datetime[symbol] = latest_bar.name 
                data_event = DataEvent(symbol=symbol,data=latest_bar)
                
                self.events_queue.put(data_event)
                    
                    
                    