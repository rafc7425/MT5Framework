from enum import Enum
from pydantic import BaseModel
import pandas as pd

#Definition of diferent kinds of events 

class EventTytpe(str,Enum):
    DATA = "DATA"
    SIGNAL = "SIGNAL"


class BaseEvent(BaseModel):
    event_type:EventTytpe
    class Config:
        arbitrary_types_allowed = True
    
class DataEvent(BaseEvent):
    event_type:EventTytpe = EventTytpe.DATA    
    symbol: str
    data: pd.Series
        
    