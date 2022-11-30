class Market:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.maker_commission = 0
        self.taker_commission = 0
        self.api = ""
