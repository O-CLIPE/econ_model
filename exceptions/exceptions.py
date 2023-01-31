class NoSufficientSupplyError(Exception):
    """Buy action failed because there were no sufficient items"""
    def __init__(self, supply: int, quantity: int, msg: str = None):
        self.supply = supply
        self.quantity = quantity
        if msg is None: msg = f"Buy called for {quantity} items, but there are only {supply}."
        super().__init__(msg)


class EmptyTableError(Exception):
    """Action couldn't be done because table is empty"""


class ObjectAlreadyExistsError(Exception):
    """Object with unique specified info already exists"""
    def __init__(self, unique_info: dict, old: object, new: object, msg: str = None):
        self.matching_info = {k: v for k, v in unique_info.items() if getattr(old, k) == unique_info[k]}
        all_none = True
        for key in self.matching_info:
            if self.matching_info[key] is not None:
                all_none = False
        if all_none:
            msg = "All of the matching_info items are None, and that may have raised this incorrectly."

        self.old = old
        self.new = new
        if msg is None:
            msg = f"""New {type(new)} has {', '.join(f"{k}: {repr(v)}" for k, v in self.matching_info.items())} """\
                  f"attributes that are in  common with {old} and could not be initiated."

        super().__init__(msg)


class MissingArgumentsError(Exception):
    """IDE didn't see it coming, buy you should have"""


class ClassIsNotIterable(Exception):
    """Could not iterate class. Probably because it is not decorated with @track_instances."""


