import json


contract_quantity = 0
tp = 0.001
sl = 0.00025


trades = []


def enter_long(price):
    global trades
    trades.append({
        "entry": price,
        "type": "long",
        "resolved": False,
        "exit": None,
        "profit": None
    })
    

def enter_short(price):
    global trades
    trades.append({
        "entry": price,
        "type": "short",
        "resolved": False,
        "exit": None,
        "profit": None
    })


def update(price):
    global trades

    for i in range(len(trades)):

        if trades[i]["resolved"] == False:

            if trades[i]["type"] == "long":
                if price >= trades[i]["entry"] + tp:
                    trades[i]["resolved"] = True
                    trades[i]["exit"] = price
                    trades[i]["profit"] = trades[i]["exit"] - trades[i]["entry"]

                if price <= trades[i]["entry"] - sl:
                    trades[i]["resolved"] = True
                    trades[i]["exit"] = price
                    trades[i]["profit"] = trades[i]["exit"] - trades[i]["entry"]



            if trades[i]["type"] == "short":
                if price <= trades[i]["entry"] - tp:
                    trades[i]["resolved"] = True
                    trades[i]["exit"] = price
                    trades[i]["profit"] = trades[i]["entry"] - trades[i]["exit"]

                if price >= trades[i]["entry"] + sl:
                    trades[i]["resolved"] = True
                    trades[i]["exit"] = price
                    trades[i]["profit"] = trades[i]["entry"] - trades[i]["exit"]
            update_json()



def update_json():
    global trades

    with open("trade_data.json", 'w') as f:
        json.dump(trades, f, indent=4)

