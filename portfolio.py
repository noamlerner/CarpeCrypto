class portfolio:
    def __init__(self,starting_amount=1000):
        self.amount = starting_amount
        self.holding = 0

    def buy(self, price):
        if self.amount != 0:
            self.holding = self.amount / price
            self.amount = 0

    def sell(self, price):
        if self.holding != 0:
            self.amount = self.holding * price
            self.holding = 0

    def value(self, price):
        return self.holding * price + self.amount

    def is_holding(self):
        if self.holding == 0:
            return "0"
        return "1"