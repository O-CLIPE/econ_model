from typing import ClassVar
from dataclasses import dataclass

from econ.table_classes import tableObject
from utils import track_instances
from econ import table_classes as tbl


@track_instances
@dataclass
class Product(tableObject):
    obj_id: ClassVar[str] = 'product_id'

    name: str               #
    good_id: int            #
    producer_id: int        #
    product_id: int = None  # IN DATABASE
    cost: float = None      #
    value: float = None     #
    price: float = None     #
    quantity: int = None    #

    @property
    def good(self):
        id_ = self.good_id
        for good in tbl.Good:
            if good.good_id == id_:
                return good

    @good.setter
    def good(self, value: tbl.Good):
        self.good_id = value.good_id

    @property
    def producer(self):
        id_ = self.producer_id
        for entity in tbl.Entity:
            if entity.entity_id == id_:
                return entity

    @producer.setter
    def producer(self, value: tbl.Entity):
        self.producer_id = value.entity_id

    @property
    def profit(self):
        return self.price - self.cost
