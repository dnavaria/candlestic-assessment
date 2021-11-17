import os
import sys
from sqlalchemy import create_engine, exc
from sqlalchemy import Table, Column, String, MetaData, BigInteger
class PsqlOps:
    def __init__(self, PSQL_URI):
        
        # changing postgres:// uri to postgresql:// inorder to make it work with sqlalchemy
        if PSQL_URI and PSQL_URI.startswith("postgres://"):
            PSQL_URI = PSQL_URI.replace("postgres://","postgresql://",1)
        else:
            print("Invalid psql uri found")
            sys.exit(0)        
            
        self.PSQL_URI = PSQL_URI
        
        try:
            # creating engine to execute queries    
            self.db = create_engine(self.PSQL_URI)
        except Exception as e:
            sys.exit(f"Error occured while creating connection :: {e}")
        
        # making sure that a database exists before making any queries
        try:
            # self.db.execute("CREATE TABLE IF NOT EXISTS CANDLESTICK (time bigint, open text, close text, highest text, lowest text, volume text, future_contract_name text);")
            meta = MetaData(self.db)
            self.candlestick = Table('candlestick', meta, Column('time', BigInteger), Column('open', String), Column('close', String), Column('highest', String), Column('lowest', String), Column('volume', String), Column('futures_contract_name', String))
            if not self.candlestick.exists():
                self.candlestick.create()
        except Exception as e:
            sys.exit(f"Error occured while checking if database exists or not :: {e}")
    
    def save_candle(self, time=None, open=None, close=None, highest=None, lowest=None, volume=None, futures_contract_name=None) -> bool:
        if time and open and close and highest and lowest and futures_contract_name:
            try:
                with self.db.connect() as connection:
                    insert_query = self.candlestick.insert().values(time=time, open=open, close=close, highest=highest, lowest=lowest, volume=volume, futures_contract_name=futures_contract_name)
                    connection.execute(insert_query)
                return True
            except Exception as e:
                print(f"Exception occured while saving data to postgres db :: {e}")
                return False
        else:
            print("Invalid values received")
            return False    
        
    def get_all_rows(self):
        try:
            with self.db.connect() as connection:
                select_query = self.candlestick.select()
                data = connection.execute(select_query)
                return data
        except Exception as e:
            print(f"Exception occured while fetching data :: {e}")
            return None
                
                
                
            
