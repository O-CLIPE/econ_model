class Good:
    def __init__(self, name, **kwargs):
        self.good_id: int = None     #
        self.name: str = name        #  IN DATABASE
        self.price: float = None     #
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(name, str):
            raise ValueError("name must be a string")

class Product:
    def __init__(self, name, good_id, producer_id, **kwargs):
        self.product_id: int = None         #
        self.good_id: int = good_id         #
        self.producer_id: int = producer_id #
        self.name: str = name               #  IN DATBASE
        self.value: float = None            #
        self.price: float = None            #
        self.supply: int = None             #

        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(self.name, str):
            raise ValueError("name must be str")
        if not isinstance(self.product_id, int):
            raise ValueError("product_id must be int")
        if not isinstance(self.good_id, int):
            raise ValueError("good_id must be int")

    def __repr__(self) -> str:
        return f"<Product n.{self.product_id} '{self.name}' type: {self.good_id} from: {self.producer_id}>"

class Entity: # a market is just a relation between entities
    def __init__(self, name, **kwargs):
        self.entity_id: int = None   # 
        self.name: str = name        # 
        self.income: float = None    #  IN DATABASE
        self.expenses: float = None  #
        self.value: float = None     #

        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(self.name, str):
            raise ValueError("The name must be a name.")

    def __repr__(self) -> str:
        return f"<Entity n.{self.entity_id} '{self.name}'>"

    def set_ebit(self):
        self.ebit = self.income - self.expenses

