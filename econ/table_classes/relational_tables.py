from typing import ClassVar
from dataclasses import dataclass

from econ.table_classes import tableObject
from utils import track_instances
from econ import table_classes as tbl


@track_instances(new_track=True)
@dataclass
class Buy(tableObject):
    obj_id: ClassVar[str] = 'index'
    entity_id: int
    producer_id: int
    price: float = None
    quantity: int = 1
    is_asset: int = None
    index: int = None

    def __post_init__(self):
        if self.is_asset is None:
            self.is_asset = self.quantity

    def __repr__(self) -> str:
        info = self.__dict__
        del info['index']
        return f"Buy(index={self.index} {', '.join(f'{name}={repr(value)}' for name, value in info.items())})"


@track_instances
@dataclass
class ProductionGoods(tableObject):
    obj_id: ClassVar[str] = 'index'

    higher_good_id: int     #
    lesser_good_id: int     #
    quantity_per_unit: int  # IN DATABASE
    index: int = None       #

    @classmethod
    def update_Good(cls):
        for inst in cls.__instances__:
            inst.send_to_Good()

    def send_to_Good(self):
        self.higher_good.production_goods.append(self.lesser_good, self.quantity_per_unit)

    @property
    def higher_good(self):
        for good in tbl.Good:
            if good.good_id == self.higher_good_id:
                return good

    @property
    def lesser_good(self):
        for good in tbl.Good:
            if good.good_id == self.lesser_good_id:
                return good


@track_instances
@dataclass
class GoodAlternative(tableObject):
    obj_id = 'alternative_id'

    good_id: int
    alternative_id: int
