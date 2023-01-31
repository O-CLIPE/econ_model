from abc import ABC, abstractmethod

from econ.table_classes import BaseEntity, Entity
from econ import table_classes as tbl


class ModelEntity(BaseEntity, ABC):
    """Class in which all model entities should inherit.

    Abstract methods::

        __call__(self) -> None
        assess_buys(self) -> None
        assess_sell(self, buyer, product, quantity, price) -> bool

    .. :py:class:: ModelEntity

        .. :py:meth:: hello
            hello
    """
    needs = dict()  # depends on the existence of goods

    def __init__(self, table_obj: Entity):
        if not isinstance(table_obj, Entity):
            raise TypeError(f"template was {type(table_obj)}, expected Entity")
        super().__init__(**table_obj.__dict__)

        self.table_obj = table_obj

    def update_template(self):
        self.table_obj.__init__(**self.base_attributes())  # calling __init__ again does not change the id

    @classmethod
    def introduce_needs_to_market(cls):
        for need in cls.needs:
            create = True
            for good in tbl.Good:
                if good.name == need:
                    create = False
            if create:
                tbl.Good(need)

    def request_buy(self, product: tbl.Product, quantity: int, price=None):
        producer = product.find_instance(product.producer_id)
        if price is None:
            price = product.price
        if producer.assess_sell(self, product, quantity, price):
            self.table_obj.buy(product, quantity, price)

    @abstractmethod
    def __call__(self):
        self.assess_buys()

    @abstractmethod
    def assess_buys(self):
        pass

    @abstractmethod
    def assess_sell(self, buyer: Entity, product: tbl.Product, quantity: int, price: float) -> bool:
        if price < product.price:
            return False
        if quantity > product.quantity:
            return False
        return True
