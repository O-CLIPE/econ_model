from econ.table_classes import *
from exceptions.exceptions import *

import pytest


def test_Good():
    potato = Good('potato')
    assert potato.name == 'potato'
    assert potato.good_id is None
    assert potato.__dict__ == {'good_id': None, 'name': 'potato', 'price': None, 'production_goods': None}

    tomato = Good('tomato', good_id=2, price=12.00)
    assert tomato.name == 'tomato'
    assert tomato.good_id == 2
    assert tomato.price == 12.0

    assert tomato.get_instances() == [potato, tomato]
    assert tomato.__instances__[0].name == 'potato'
    assert repr(tomato) == "Good(name='tomato', good_id=2, price=12.0, production_goods=None)"

    with pytest.raises(TypeError):
        Good()
        Good(price=12)
        Good(name=1)
        Good("a", price="10")
        Good("a", price=11, good_id=12.0)

    tomato.price = 13.0
    assert tomato.price == 13.0


def test_Product():
    potato = Product('potato', 1, 2)
    assert potato.name == 'potato'
    assert potato.good_id == 1
    assert potato.producer_id == 2
    assert potato.product_id is None
    assert potato.value is None
    assert potato.price is None
    assert potato.quantity is None

    tomato = Product('tomato', good_id=10, producer_id=3, price=12.00, value=10.00, quantity=100, product_id=1)
    assert tomato.name == 'tomato'
    assert tomato.good_id == 10
    assert tomato.producer_id == 3
    assert tomato.price == 12.0
    assert tomato.value == 10.0
    assert tomato.quantity == 100
    assert tomato.product_id == 1

    assert tomato.__instances__ == [potato, tomato]

    assert tomato.__repr__() == "Product(name='tomato', good_id=10, producer_id=3, product_id=1, value=10.0, "\
                                "price=12.0, quantity=100)"

    with pytest.raises(TypeError) as e:
        Product()
        Product(price=12)
        Product('potato', 1, 2, price='10')
        Product('potato', 1, 2, quantity=12.2)

    tomato.price = 13.0
    assert tomato.price == 13.0

    with pytest.raises(ObjectAlreadyExistsError):
        Product('no1', 1, 2, product_id=1)

    tomato.quantity = 12
    assert tomato.quantity == 12


def test_BaseEntity():
    ghost = Entity('ghost')
    company = Entity('company')
    assert company.name == 'company'
    assert company.entity_id is None
    assert company.value is None
    assert company.cash is None

    buyer = Entity(name='buyer', entity_id=2, cash=100.0, value=120.00)
    assert buyer.name == 'buyer'
    assert buyer.entity_id == 2
    assert buyer.cash == 100.0
    assert buyer.value == 120.00

    assert buyer.__instances__ == [ghost, company, buyer]

    assert buyer.__repr__() == "BaseEntity(name='buyer', entity_id=2, cash=100.0, value=120.0)"

    with pytest.raises(TypeError):
        Entity()
        Entity(price=12)
        Entity('hello', value='10')
        Entity('potato', entity_id=12.2)

    buyer.value = 130.0
    assert buyer.value == 130.0

    with pytest.raises(ObjectAlreadyExistsError):
        Entity('buyer')

    buyer.name = 'jonas'
    assert buyer.name == 'jonas'
    company.entity_id = 1
    company.cash = 10_000.00
    # tomato = Good('tomato', good_id=2, price=12.00)
    co_tomatoes = Product('co_tomato', good_id=2, producer_id=1, price=12.00, value=10.00, quantity=100, product_id=32)
    buyer.buy(co_tomatoes, 2)
    assert buyer.cash == 76.00
    assert company.cash == 10_024.00
    assert co_tomatoes.quantity == 98


def test_Entity():
    pass