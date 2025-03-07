import queue
from data_provider.data_provider import DataProvider
from typing import Dict, Callable
from events.events import DataEvent
import time

class TradingDirector():
    def __init__(self,events_queue: queue.Queue,data_provider:DataProvider):
        self.events_queue = events_queue
        self.DATAPROVIDER = data_provider
        
        #Trading controller
        self.continue_trading: bool = True
        
    
        self.event_handler: Dict[str,Callable]  = {
            "DATA": self._handle_data_event,
        }
        
    def _handle_data_event(self,event:DataEvent):
        print(f"New Data Retrieved from {event.symbol} - Latest price from close {event.data.close}")    
        
    def execute(self)->None:
        #Main loop definition
        while self.continue_trading:
            try:
                event = self.events_queue.get(block=False)
            except queue.Empty:
                self.DATAPROVIDER.check_for_new_date()
            else:
                if event is not None:
                    handler = self.event_handler.get(event.event_type)
                    handler(event)
                else:
                    self.continue_trading = False
                    print("ERROR: Received Null Event. Finishing Framework Execution ")    
                        
            time.sleep(1)      
        print("END")      