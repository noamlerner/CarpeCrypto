class portfolio:
    def __init__(self,starting_amount=1000):
        self.amount = starting_amount
        self.holding = 0

    def buy(self, prices):
        if self.amount != 0:
            self.holding = self.amount / prices.iloc[-1]
            self.amount = 0

    def sell(self, prices):
        if self.holding != 0:
            self.amount = self.holding * prices.iloc[-1]
            self.holding = 0

    def value(self, prices):
        return self.holding * prices.iloc[-1] + self.amount

    def is_holding(self):
        return self.holding != 0