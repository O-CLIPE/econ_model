import econ, econdb

                    # Interactions
def new_entity(entity_id: int) -> econ.Entity:
    entity_info = econdb.get_entity(where=entity_id)
    print(entity_info)
    return econ.Entity(**entity_info)

def update_entity(entity: econ.Entity):
    atts = entity.__dict__
    for key in atts:
        if key not in ['entity_id', 'name', 'income', 'expenses', 'value']:
            del atts[key]
    econdb.set_entity(**atts)



 


