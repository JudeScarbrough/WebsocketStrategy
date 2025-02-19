import websocket
import json
import threading
import time

# MEXC WebSocket URL
WS_URL = "wss://contract.mexc.com/edge"

# Symbol and interval
SYMBOL = "PNUT_USDT"
INTERVAL = "Min1"

last_candle_timestamp = None

def on_message(ws, message):
    """Handles incoming WebSocket messages."""
    global last_candle_timestamp
    data = json.loads(message)
    if data.get("channel") == "push.kline":
        kline = data.get("data", {})
        if kline.get("interval") == INTERVAL and kline.get("symbol") == SYMBOL:
            candle_timestamp = kline.get("t")
            if last_candle_timestamp is None or candle_timestamp > last_candle_timestamp:
                last_candle_timestamp = candle_timestamp
                print(f"Candle closed: Close Price = {kline['c']}")

def on_error(ws, error):
    """Handles WebSocket errors."""
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket closure."""
    print("WebSocket Closed")

def on_open(ws):
    """Handles WebSocket opening and subscribes to K-line data."""
    print("WebSocket Connected")
    
    # Subscribe to K-line data
    subscribe_msg = {
        "method": "sub.kline",
        "param": {
            "symbol": SYMBOL,
            "interval": INTERVAL
        }
    }
    ws.send(json.dumps(subscribe_msg))
    
    # Start sending ping messages periodically
    def send_pings():
        while ws.keep_running:
            time.sleep(10)  # Send a ping every 10 seconds
            try:
                ws.send(json.dumps({"method": "ping"}))
            except Exception as e:
                print(f"Ping error: {e}")
                break
    
    threading.Thread(target=send_pings, daemon=True).start()

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    
    # Run WebSocket without SSL verification
    ws.run_forever(sslopt={"cert_reqs": 0})
