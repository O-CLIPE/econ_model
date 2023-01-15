from econobj import *

def test_obj():
    a = new_entity(1)
    print(a)
    a.name = 'Bro hello'
    print(a)
    update_entity(a)
    econdb.get_entity()
    a.name = 'Cleen Water Company'
    update_entity(a)