import requests
import time
import json

# Define the API endpoint
url = "https://api.binance.com/api/v3/klines"

# Get the current time (in milliseconds)
end_time = int(time.time() * 1000)

# Calculate the start time for the past 10 hours (10 * 60 * 60 * 1000 ms)
start_time = end_time - (10 * 60 * 60 * 1000)

# Set the parameters for the request
params = {
    'symbol': 'PNUTUSDT',
    'interval': '1m',  # 1-minute candles
    'startTime': start_time,
    'endTime': end_time,
    'limit': 1000,  # Maximum limit is 1000
}

# Make the request to the Binance API
response = requests.get(url, params=params)

# Check if the response is successful
if response.status_code == 200:
    kline_data = response.json()

    # Transform the data into a dictionary with keys: open, high, low, close, t (timestamp)
    labeled_data = []
    for kline in kline_data:
        labeled_data.append({
            't': kline[0],          # Timestamp (open time)
            'open': kline[1],       # Open price
            'high': kline[2],       # High price
            'low': kline[3],        # Low price
            'close': kline[4],      # Close price
        })

    # Save the labeled data to a JSON file
    with open('data.json', 'w') as file:
        json.dump(labeled_data, file, indent=4)
    
    print("Labeled data saved to labeled_data.json")
else:
    print(f"Error: {response.status_code}, {response.text}")
