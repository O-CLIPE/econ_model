from econ.table_classes import *
from econ.database import EconDatabase


# Interactions
class TablesAndDatabase(EconDatabase):
    def new_entity(self, entity_id: int) -> Entity:
        info = self.get_entity(where=entity_id)
        return Entity(**info)

    def commit_entity(self, entity: Entity):
        atts = entity.base_attributes()
        self.set_entity(**atts)

    def new_good(self, good_id: int) -> Good:
        info = self.get_good(where=good_id)
        return Good(**info)

    def commit_good(self, good: Good):
        atts = good.__dict__
        identifier = atts['good_id']
        del atts['good_id']
        self.set_good(identifier, **atts)

    def new_product(self, product_id: int) -> Product:
        info = self.get_product(where=product_id)
        return Product(**info)

    def commit_product(self, product: Product):
        atts = product.__dict__
        identifier = atts['product_id']
        del atts['product_id']
        self.set_product(identifier, **atts)

    def new_buy(self, index: int):
        info = self.get_buy(where=index)
        return Buy(**info)

    def commit_buys(self, ):
        for buy in Entity.buys:
            self.create_buy(*buy)

        Buy.__new_instances__.clear()

    def commit_all(self):
        for good in Good.instances:
            self.commit_good(good)
        for product in Product.instances:
            self.commit_product(product)
        for entity in Entity.__instances__:
            self.commit_entity(entity)
        self.commit_buys()

    def obj_database(self) -> tuple:
        """Return a tuple representing the database as table objects."""
        objects = []
        for func, class_ in ((self.get_entity, Entity), (self.get_good, Good), (self.get_product, Product), (self.get_buy, Buy)):
            for item in func():
                objects.append(class_(**item))

        return tuple(objects)
