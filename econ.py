class Good:
    def __init__(self, name, **kwargs):
        self.good_id = None     #
        self.name = name        #  IN DATABASE
        self.price = None       #
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(name, str):
            raise ValueError("name must be a string")

class Product:
    def __init__(self, name, good_id, entity_id, **kwargs):
        pass


class Entity: # a market is just a relation between entities
    def __init__(self, name, **kwargs):
        self.entity_id = None   # 
        self.name = name        # 
        self.income = None      #  IN DATABASE
        self.expenses = None    #
        self.value = None       #

        for key, value in kwargs.items():
            setattr(self, key, value)
        if not isinstance(self.name, str):
            raise ValueError("The name must be a name.")

    def __repr__(self) -> str:
        return f"<Entity n.{self.entity_id} '{self.name}'>"

    def set_ebit(self):
        self.ebit = self.income - self.expenses

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def add_provider(self, consumer):
        self.providers.append(consumer)
