from enum import Enum
from datetime import datetime, UTC

global next_order_id = 0

class OrderSide(Enum):
    BID = "BID"
    ASK = "ASK"

class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class order:
    def __init__(self, stock, side: OrderSide, order_type: OrderType, price, quantity, timestamp):
        global next_order_id
        self.order_id = next_order_id
        next_order_id += 1
        self.stock = stock
        self.side = side
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.timestamp = datetime.now(IST)
    
class trade:
    def __init__(self,trade_id,stock,price,quantity,aggressor,bid_id,ask_id,timestamp):
        self.trade_id = trade_id
        self.stock = stock
        self.price = price
        self.quantity = quantity
        self.aggressor = aggressor
        self.bid_id = bid_id
        self.ask_id = ask_id
        self.timestamp = datetime.now(IST)
        