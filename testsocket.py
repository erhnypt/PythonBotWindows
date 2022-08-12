import json
import websocket

SOCKET="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"



def on_open(ws):
    print("baglantı saglandi")

def on_close(ws):
    print("baglantı koptu")

def on_message(ws,message):
    json_message=json.loads(message)

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
