from typing import ClassVar

from econ.table_classes import tableObject
from utils import track_instances
from exceptions import NoSufficientSupplyError
from econ import table_classes as tbl


class BaseEntity(tableObject):
    """Superclass of all entities."""
    obj_id: ClassVar[str] = 'entity_id'

    entity_id: int  #
    name: str       #
    cash: float     # IN DATABASE
    value: float    #

    def __init__(self, name: str, **kwargs):
        self.name = name

        super().__init__(**kwargs)

    def base_attributes(self) -> dict:
        return {
            'entity_id': self.entity_id,
            'name': self.name,
            'cash': self.cash,
            'value': self.value
        }


@track_instances
class Entity(BaseEntity):
    """Represents the Entity table."""
    def buy(self, product, quantity: float, price=None):
        if isinstance(product, int):
            product = tbl.Product.find_instance(product, 'product_id')
        if product.quantity < quantity:
            raise NoSufficientSupplyError(product.quantity, quantity)

        tbl.Buy(self.entity_id, product.producer_id, quantity, price, new=True)
        cash = product.price * quantity
        self.cash -= cash
        self.find_instance(product.producer_id).cash += cash
        product.quantity -= quantity

    def make_product(self, good, name: str):
        if isinstance(good, tbl.Good):
            good = good.good_id
        elif isinstance(good, str):
            good = tbl.Good.find_instance(good, 'name').good_id
        elif not isinstance(good, int):
            raise TypeError(f"Expected int, got {type(good).__name__}")
        tbl.Product(name, entity_id=self.entity_id, good_id=good)
