import websocket
import json
import time

socket = "wss://stream.binance.com:9443/ws/dodusdt@kline_1m"

def on_candle_close(close_price):
    print(f"Candle closed at price: {close_price}")

def on_message(ws, message):
    data = json.loads(message)
    kline = data['k']
    
    if kline['x']:
        close_price = kline['c']
        on_candle_close(close_price)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed. Reconnecting...")
    time.sleep(5)  # Wait for 5 seconds before reconnecting
    ws.run_forever()  # Reconnect the WebSocket

def on_open(ws):
    print("WebSocket connection opened")

ws = websocket.WebSocketApp(socket,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            on_open=on_open)

# Start the WebSocket connection and run it forever
ws.run_forever()
