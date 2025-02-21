import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv

class PlattformConnector():
    def __init__(self,Symbols:list):
        # load env files and load values
        load_dotenv(find_dotenv())
        # initialize the mt5 platform
        self._initialize_platform()
        # warns about kind of account
        self._live_account_warning()
        #recovery info account 
        self._print_account_info()
        #make sure if algo trade is enabled
        self._check_algoTrading_enabled()
        #add symbols to the marketWatch
        self._add_symbols_to_marketWatch(Symbols)


    def _initialize_platform(self) -> None:
        """
        Initializes MT5 Platform.

        Raises:
        Exception if there is any error initializing MT5 Platform
        """
        if mt5.initialize(
            path=os.getenv("MT5_PATH"),
            login=int(os.getenv("MT5_LOGIN")),
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            timeout=int(os.getenv("MT5_TIMEOUT")),
            portable=eval(os.getenv("MT5_PORTABLE"))):

            print("mt5 opened successfully!")

        else:
            raise Exception(f"Error Occurred Initializing MT5: {mt5.last_error()}")

    def _live_account_warning(self) -> None:
        account_info = mt5.account_info()
        if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("Demo account detected")
        elif account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            print("Real account detected")
            if not input("Capital on risk do yoy want to countinue? y/n ").lower()== "y":
                mt5.shutDown()
                raise Exception("User has decided to stop the bot")
        else:print("Contest account Detected")  
    
    def _check_algoTrading_enabled(self) -> None:
        if not mt5.terminal_info().trade_allowed:
            raise Exception("Algoritmic trading is not enabled, please enable it MANNUALY")      

    def _add_symbols_to_marketWatch(self, Symbols:list) -> None:
        for symbol in Symbols:
            if mt5.symbol_info(symbol) is None:
                print(f"unable to add {symbol} to the marketWatch, {mt5.last_error()}")
                continue
            
            if not mt5.symbol_info(symbol).visible:
                
                if not mt5.symbol_select(symbol,True):
                    print(f"unable to add {symbol} to the marketWatch, {mt5.last_error()}")
                else: print(f"symbol {symbol} has been added successfully to the marketWatch")    
                
            else: print(f"symbol {symbol} is already on the marketWatch") 

    def _print_account_info(self) -> None:
        #recovery account info
        account_info = mt5.account_info()._asdict()
        print(f"+---------------- ACCOUNT INFO ----------------")
        print(f"+ - Account ID: {account_info['login']}")
        print(f"+ - Trader Name: {account_info['name']}")
        print(f"+ - Broker: {account_info['company']}")
        print(f"+ - Server: {account_info['server']}")
        print(f"+ - leverage: {account_info['leverage']}")
        print(f"+ - Currency: {account_info['currency']}")
        print(f"+ - Account Balance: {account_info['balance']}")
        print(f"+----------------------------------------------")