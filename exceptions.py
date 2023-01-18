class NoSuficientSupplyError(Exception):
    def __init__(self, supply: int, quantity: int, msg: str = None):
        self.supply = supply
        self.quantity = quantity
        if msg is None: msg = f"Buy called for {quantity} items, but there are only {supply}."
        super().__init__(msg)

class EmptyTableError(Exception):
    pass
