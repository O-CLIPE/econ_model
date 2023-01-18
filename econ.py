from exceptions import *

class Good:

    instances = []
    def __init__(self, name, **kwargs):
        self.good_id: int = None     #
        self.name: str = name        #  IN DATABASE
        self.price: float = None     #
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        Good.instances.append(self)

    def __repr__(self) -> str:
        return f"<Good n.{self.good_id} '{self.name}' , price: {self.price}>"


class Product:

    instances = []
    def __init__(self, name, good_id, producer_id, **kwargs):
        self.product_id: int = None         #
        self.good_id: int = good_id         #
        self.producer_id: int = producer_id #
        self.name: str = name               #  IN DATBASE
        self.value: float = None            #
        self.price: float = None            #
        self.quantity: int = None           #

        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(self.name, str):
            raise ValueError("name must be str")
        if not isinstance(self.product_id, int):
            raise ValueError("product_id must be int")
        if not isinstance(self.good_id, int):
            raise ValueError("good_id must be int")

        Product.instances.append(self)

    def __repr__(self) -> str:
        return f"<Product n.{self.product_id} '{self.name}' , good_id: {self.good_id} , producer_id: {self.producer_id}>"

class BaseEntity: # Entity with super powers, no limitations

    buys = [] # temporary place for non commited transactions
    __instances = []
    is_subclass = False

    def __init__(self, name: str, **kwargs):
        self.entity_id: int = None   # 
        self.name: str = name        #
        self.cash: float = None      #  IN DATABASE
        self.value: float = None     #

        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(self.name, str):
            raise TypeError(f"Expected str, got {type(self.name)}")

        if not self.is_subclass and self not in BaseEntity.__instances:
            BaseEntity.__instances.append(self)

    def __repr__(self) -> str:
        return f"<Entity n.{self.entity_id} '{self.name}' , cash: {self.cash} , value: {self.value}>"

    def db_atts(self) -> dict:
        return {
            'entity_id': self.entity_id,
            'name': self.name,
            'cash': self.cash,
            'value': self.value
        }
        
    def buy(self, product: Product,  quantity: int):
        if product.quantity < quantity:
            return NoSuficientSupplyError(product.quantity, quantity)
        BaseEntity.to_commit_buy.append((self.entity_id, product.producer_id, quantity))
        self.cash -= product.price * quantity
        product.quantity -= quantity

    @classmethod
    def get_instances(cls):
        return cls.__instances

    
        
                    # ai

class Entity(BaseEntity):
    # if called should consider taking action
    is_subclass = True
    def __init__(self, template: BaseEntity):
        super().__init__(**template.__dict__)
        
        self.template = template

    def __call__(self):
        pass

    def update_template(self):
        self.template.__init__(**self.db_atts()) # id stays the same :O

    def request_buy(self):
        pass

