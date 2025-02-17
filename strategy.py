import collections
import execute
import position_logging


prices = []
MA5 = 0
MA10 = 0
MA30 = 0
MA60 = 0


def lists_ready():
    if len(prices) >= 60:
        return True
    return False


def update_MAs(price):
    global prices
    global MA5
    global MA10
    global MA30
    global MA60

    if len(prices) > 60:
        prices.pop()

    def calc_MA(length):
        values = []
        for i in range(length):
            if i < len(prices) - 1:
                values.append(prices[i])


        if len(values) > 0:
            return sum(values)/len(values)
        else:
            return 0 
            

    MA5 = calc_MA(5)
    MA10 = calc_MA(10)
    MA30 = calc_MA(30)
    MA60 = calc_MA(60)


strategy_state = "trash"

def push_price_update(price):

    print(f"price to strategy: {price}")

    global prices
    global strategy_state
    global MA5
    global MA10
    global MA30
    global MA60

    prices.insert(0, price)
    position_logging.update(price)
    update_MAs(price)

    if lists_ready():
        
        
        



        
        if strategy_state == "trash":
            
            if MA5 < MA10 < MA30 < MA60:
                strategy_state = "buy_primed"

            if MA5 > MA10 > MA30 > MA60:
                strategy_state = "sell_primed"
                


        if strategy_state == "buy_primed":
            
            if MA10 < MA5 < MA30 < MA60:
                strategy_state = "buy_phase2"
                pass

        if strategy_state == "sell_primed":
            
            if MA10 > MA5 > MA30 > MA60:
                strategy_state = "sell_phase2"
                pass






        if strategy_state == "buy_phase2":
            if MA10 < MA30 < MA5 < MA60:
                strategy_state = "buy"
                pass

        if strategy_state == "sell_phase2":
            if MA10 > MA30 > MA5 > MA60:
                strategy_state = "sell"
                pass



        if strategy_state == "buy":
            #execute buy
            execute.enter_long()
            position_logging.enter_long(price)
            strategy_state = "trash"
            pass

        if strategy_state == "sell":
            #execute buy
            execute.enter_short()
            position_logging.enter_short(price)
            strategy_state = "trash"
            pass
