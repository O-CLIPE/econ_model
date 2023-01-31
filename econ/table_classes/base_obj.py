class tableObject:
    """ market.tables represented in Python.

    Subclasses keep track of all instances if wrapped @track_instances.
    Objects represent market.table rows.
    Foreign keys should make properties.
    """

    obj_id = 'econobj_id'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        for attr in self.__annotations__:
            if not hasattr(self, attr):
                setattr(self, attr, None)

    def __setattr__(self, name, value):
        for attr, type_ in self.__annotations__.items():
            if name == attr:
                if type_ is float:
                    type_ = (float, int)
                if not isinstance(value, type_) and value is not None:
                    raise TypeError(f"{attr} expected {type_}, got {type(value)}.")
                super().__setattr__(name, value)

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        info = self.__dict__

        return f"{cls_name}({', '.join(f'{key}={value!r}' for key, value in info.items())})"

# the track_instances higher-order-function stole most of the job of this class :(
