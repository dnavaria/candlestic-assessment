import os, json
from websocket import create_connection
from dotenv import load_dotenv
from postgres_ops import PsqlOps
import datetime
load_dotenv(".env")
PSQL_URI = os.environ.get("PSQL_URI")

psql_obj = PsqlOps(PSQL_URI=PSQL_URI)

ws = create_connection("wss://fx-ws.gateio.ws/v4/ws/btc")
ws.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1m", "BTC_USD"]}')

def format_date(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


while True:
    data = json.loads(ws.recv())
    print(data)
    result = list(data["result"])
    if result[0] == "status":
        continue
    for i in range(len(result)):
        candle = result[i]
        print(candle["t"], candle["o"], candle["c"], candle["h"], candle["l"], candle["v"], candle["n"])
        psql_obj.save_candle(time=format_date(candle["t"]), open=candle["o"], close=candle["c"], highest=candle["h"], lowest=candle["l"], volume=candle["v"], futures_contract_name=candle["n"])
    
    
    