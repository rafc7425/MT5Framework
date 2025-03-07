from platform_connector.platform_connector import PlattformConnector
from data_provider.data_provider import DataProvider
from queue import Queue
from trading_director.trading_director import TradingDirector

if __name__ == "__main__":
    symbols = ['EURUSD', 'EURJPY']
    timeframe = '1min'
    
    events_queue = Queue()
    
    CONNECT = PlattformConnector(symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_queue,Symbol_list=symbols,timeframe=timeframe)
    
    TRADINGDIRECTOR = TradingDirector(events_queue=events_queue,data_provider=DATA_PROVIDER)
    TRADINGDIRECTOR.execute()