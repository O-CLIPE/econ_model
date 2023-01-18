from econ import *
import econdb as db

                    # Interactions
def new_entity(entity_id: int) -> BaseEntity:
    info = db.get_entity(where=entity_id)
    return BaseEntity(**info)

def commit_entity(entity: BaseEntity):
    atts = entity.db_atts()
    db.set_entity(**atts)

def new_good(good_id: int) -> Good:
    info = db.get_good(where=good_id)
    return Good(**info)

def commit_good(good: Good):
    atts = good.__dict__
    db.set_good(**atts)
    
def new_product(product_id: int) -> Product:
    info = db.get_product(where=product_id)
    return Product(**info)

def commit_product(product: Product):
    atts = product.__dict__
    db.set_product(**atts)

def commit_buys():
    for buy in BaseEntity.buys:
        db.create_buy(*buy)

def commit_all():
    for good in Good.instances:
        commit_good(good)
    for product in Product.instances:
        commit_product(product)
    for entity in BaseEntity.get_instances():
        commit_entity(entity)
    commit_buys()
    
def obj_database() -> tuple:
    objects = []
    for func, class_ in ((db.get_entity, BaseEntity), (db.get_good, Good), (db.get_product, Product)):
        for item in func():
            objects.append(class_(**item))

    return tuple(objects)
