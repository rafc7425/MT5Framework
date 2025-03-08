from enum import Enum
from pydantic import BaseModel
import pandas as pd

#Definition of diferent kinds of events 

class EventTytpe(str,Enum):
    DATA = "DATA"
    SIGNAL = "SIGNAL"
    
class OrderType(str,Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"    
class SignalType(str,Enum):
    BUY = "BUY"
    SELL = "SELL"    

class BaseEvent(BaseModel):
    event_type:EventTytpe
    class Config:
        arbitrary_types_allowed = True
    
class DataEvent(BaseEvent):
    event_type:EventTytpe = EventTytpe.DATA    
    symbol: str
    data: pd.Series
        
class SignalEvent(BaseEvent):
    event_type: EventTytpe = EventTytpe.SIGNAL
    symbol:str
    signal: SignalType
    target: OrderType
    target_Price:float 
    magic_number:int 
    sl:float
    tp:float  