from sortedcontainers import SortedDict
from order import order, OrderSide, OrderType

class OrderBook:
    def __init__(self):
        # bids maps price to a list of orders (highest price first)
        self.bids = SortedDict(lambda x: -x)
        # asks maps price to a list of orders (lowest price first)
        self.asks = SortedDict()

    def add_order(self, ord: order):
        """Adds an order to the order book. Orders at the same price level are stored in a list."""
        if ord.side == OrderSide.BID:
            self.bids.setdefault(ord.price, []).append(ord)
        elif ord.side == OrderSide.ASK:
            self.asks.setdefault(ord.price, []).append(ord)
        
    def print_orderbook(self):
        for price, orders in self.bids.items():
            for ord in orders:
                print(f"{ord.order_id}: {ord.stock} {ord.side} {ord.order_type} {ord.price} {ord.quantity} {ord.timestamp}")
        for price, orders in self.asks.items():
            for ord in orders:
                print(f"{ord.order_id}: {ord.stock} {ord.side} {ord.order_type} {ord.price} {ord.quantity} {ord.timestamp}")

