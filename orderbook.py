from sortedcontainers import SortedDict

class OrderBook:
    def __init__(self):
        self.bids = SortedDict(lambda x: -x)
        self.asks = SortedDict()
