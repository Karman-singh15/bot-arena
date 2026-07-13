from sortedcontainers import SortedDict
from order import order, OrderSide, OrderType

class OrderBook:
    def __init__(self):
        # bids maps price to a list of orders (highest price first)
        self.bids = SortedDict(lambda x: -x)
        # asks maps price to a list of orders (lowest price first)
        self.asks = SortedDict()
        # Fast lookup mapping order_id -> (side, price)
        self.order_lookup = {}

    def add_limit_order(self, ord: order):
        """Adds a limit order to the order book. Orders at the same price level are stored in a list."""
        if ord.side == OrderSide.BID:
            self.bids.setdefault(ord.price, []).append(ord)
        elif ord.side == OrderSide.ASK:
            self.asks.setdefault(ord.price, []).append(ord)
        self.order_lookup[ord.order_id] = (ord.side, ord.price)

    def add_order(self, ord: order):
        """Alias for add_limit_order."""
        self.add_limit_order(ord)

    def cancel_order(self, order_id):
        """Scans the book and removes the order with the given order_id using self.order_lookup."""
        if order_id not in self.order_lookup:
            return False
        
        side, price = self.order_lookup.pop(order_id)
        if side == OrderSide.BID:
            if price in self.bids:
                orders = self.bids[price]
                for i, ord in enumerate(orders):
                    if ord.order_id == order_id:
                        orders.pop(i)
                        break
                if not orders:
                    del self.bids[price]
                return True
        elif side == OrderSide.ASK:
            if price in self.asks:
                orders = self.asks[price]
                for i, ord in enumerate(orders):
                    if ord.order_id == order_id:
                        orders.pop(i)
                        break
                if not orders:
                    del self.asks[price]
                return True
        return False

    def best_bid(self):
        """Returns the highest price on the bid side, or None if empty."""
        if not self.bids:
            return None
        return self.bids.peekitem(0)[0]

    def best_ask(self):
        """Returns the lowest price on the ask side, or None if empty."""
        if not self.asks:
            return None
        return self.asks.peekitem(0)[0]
k
    def get_depth(self, levels=5):
        """Returns the top N price levels on each side with total quantity."""
        bids_depth = []
        for price, orders in self.bids.items():
            if len(bids_depth) >= levels:
                break
            total_qty = sum(ord.quantity for ord in orders)
            bids_depth.append((price, total_qty))

        asks_depth = []
        for price, orders in self.asks.items():
            if len(asks_depth) >= levels:
                break
            total_qty = sum(ord.quantity for ord in orders)
            asks_depth.append((price, total_qty))

        return {
            "bids": bids_depth,
            "asks": asks_depth
        }

    def print_orderbook(self):
        for price, orders in self.bids.items():
            for ord in orders:
                print(f"{ord.order_id}: {ord.stock} {ord.side} {ord.order_type} {ord.price} {ord.quantity} {ord.timestamp}")
        for price, orders in self.asks.items():
            for ord in orders:
                print(f"{ord.order_id}: {ord.stock} {ord.side} {ord.order_type} {ord.price} {ord.quantity} {ord.timestamp}")

