from typing import ClassVar
from dataclasses import dataclass

from econ.table_classes import tableObject
from utils import track_instances
from econ import table_classes as tbl


@track_instances
@dataclass
class Good(tableObject):
    """Represents the good table.

    Attributes:
    name, good_id, work, production_goods
    """
    obj_id: ClassVar[str] = 'good_id'
    name: str                      #
    good_id: int = None            # IN DATABASE
    work: float = None             #
    production_goods: list = None  # list[tuple[Good, int]]
    alternative: list = None       # list[Good]

    def __post_init__(self):
        for good in Good:
            if self.name == good.name:
                good.add_alternative(self)
                tbl.GoodAlternative(good.good_id, self.good_id)

    def __str__(self) -> str:
        """str(self)"""  # repr is really annoying to read
        string = "<"
        if isinstance(self.good_id, int) :
            string += str(self.good_id) + "."
        string += f"{self.name}"
        if self.production_goods:
            string += " from "
            substr = []
            for good, qnt in self.production_goods:
                substr.append(f"({qnt} {good.name})")
            string += ", ".join(substr)
        string += f" with work={self.work}"

        string += f""
        if self.alternative:
            string+= ", alternatives=["
            substr = []
            for alternative in self.alternative:
                substr.append(str(alternative))
            string += ", ".join(substr) + "]"
        string += ">"
        return string

    def add_alternative(self, good):
        if not isinstance(self.alternative, list):
            self.alternative = list()
        self.alternative.append(good)

    def update_production_goods(self):
        """Updates and creates ProductionGoods with self, using the production_goods attribute"""
        for ref in self.production_goods:  # ref: list[Good, int]
            exists_ = False
            for obj in tbl.ProductionGoods:
                if obj.higher_good_id == self.good_id and obj.lesser_good_id == ref[0].good_id:
                    obj.quantity = ref[1]
                    exists_ = True
                    break
            if not exists_:
                tbl.ProductionGoods(higher_good_id=self.good_id, lesser_good_id=ref[0].good_id, quantity=ref[1])

    @classmethod
    def update_ProductionGoods(cls):
        """Updates and creates all possible ProductionGoods with every instance of Good, using update_production_goods
        """
        for inst in cls:
            inst.update_production_goods()

    @property
    def products(self) -> list:
        products = []
        id_ = self.good_id
        for product in tbl.Product:
            if product.good_id == id_:
                products.append(product)
        return products

    def _average_product_attr(self, product_attr: str) -> float:
        values = []
        for product in self.products:
            values.append(getattr(product, product_attr))
        average_attr = sum(values) / len(values)
        return average_attr

    @property
    def price(self) -> float:
        return self._average_product_attr('price')

    @property
    def cost(self) -> float:
        return self._average_product_attr('cost')

    @property
    def profit(self) -> float:
        return self._average_product_attr('profit')

    @property
    def total_chain_work(self) -> float:
        total_work = int(self.work)
        if self.production_goods:
            for good_quantity in self.production_goods:
                total_work += good_quantity[0].total_chain_work * good_quantity[1]
        return total_work
