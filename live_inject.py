import websocket
import json
import time
import strategy


socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"




def on_message(ws, message):
    data = json.loads(message)
    kline = data['k']
    

    if kline['x']:
        close_price = float(kline['c'])
        strategy.push_price_update(close_price)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed. Reconnecting...")
    time.sleep(5)
    ws.run_forever()


def on_open(ws):
    print("WebSocket connection opened")


ws = websocket.WebSocketApp(socket,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            on_open=on_open)


ws.run_forever()
