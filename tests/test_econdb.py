import use_database.econdb as db
import time

db.log_info(auto=True)
if db.schema_exists('test_econdb'):
    db.drop(name='test_econdb')
    time.sleep(0.1)  # code runs too fast, faster than the queries.

db.build(name='test_econdb')
time.sleep(0.1)


def test_create_func():
    global cwc_id, wb_id, cwc_wb_id, bob_id
    cwc_id = db.create_entity('Cleen Water Company', cash=10_000, value=200_000)
    wb_id = db.create_good('bottled water')
    cwc_wb_id = db.create_product(cwc_id, wb_id, '100ml CWC water bottle', price=8.00, quantity=500)
    bob_id = db.create_entity('bob', cash=100.00)

    for id_ in [cwc_id, wb_id, cwc_wb_id, bob_id]:
        assert isinstance(id_, int)

    global mr_copy_value_id
    mr_copy_value_id = db.create_entity('Mr. Copy Value', cash=1_000_000, value=200_000)


def test_get_func():
    cwc = db.get_entity(cwc_id)
    wb_good = db.get_good(wb_id)
    cwc_wb = db.get_product(cwc_wb_id)
    bob = db.get_entity(bob_id)
    assert cwc == {'entity_id': 1, 'name': 'Cleen Water Company', 'cash': 10000.0, 'value': 200000.0}
    assert wb_good == {'good_id': 1, 'name': 'bottled water', 'price': None}
    assert cwc_wb == {'product_id': 1, 'good_id': 1, 'producer_id': 1, 'name': '100ml CWC water bottle', 'value': None,
                      'price': 8.0, 'quantity': 500}
    assert bob == {'entity_id': 2, 'name': 'bob', 'cash': 100.0, 'value': None}

    mr_copy_value = db.get_entity(mr_copy_value_id)
    assert db.get_entity(where={'value': 200_000}) == [cwc, mr_copy_value]
    assert db.get_entity('bob') == bob

def test_set_func():
    pass


