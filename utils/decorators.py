from functools import wraps
import inspect
from typing import ClassVar

from exceptions import ObjectAlreadyExistsError, ClassIsNotIterable


def list_all_args(func=None):
    """List all function arguments to all in function call

    Access it with kwargs['all']
    """
    if func and inspect.isfunction(func):

        @wraps(func)
        def decorator(f):
            var_names = f.__code__.co_varnames
            kwargs_idx = var_names.index('kwargs')
            parameters = var_names[:kwargs_idx]

            def new_func(*args, **kwargs):
                all_args = dict(kwargs)
                for arg, parameter_name in zip(args, parameters):
                    all_args[parameter_name] = arg
                kwargs['all'] = all_args
                return f(*args, **kwargs)
            return new_func
        return decorator(func)
    return list_all_args


class IterateClassMeta(type):
    """Supports iterating the class itself, by returning the __instances__ class attribute"""
    def __iter__(cls):
        if hasattr(cls, '__instances__'):
            return iter(getattr(cls, '__instances__'))
        else:
            raise ClassIsNotIterable

    def __len__(cls):
        if hasattr(cls, '__instances__'):
            return len(getattr(cls, '__instances__'))


def track_instances(class_=None, *, new_track=False):
    """Tracks instances of class_.

    @track_instances -> default.
    @track_instances(new_track=True) -> Adds __new_instances__ property. Use new=True in __init__.
    """
    if class_ is not None and callable(class_):

        @wraps(class_, updated=())
        class TrackInstances(class_, metaclass=IterateClassMeta):
            __instances__: ClassVar[list] = list()
            obj_id: ClassVar[str] = 'name' if not hasattr(class_, 'obj_id') else getattr(class_, 'obj_id')

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if self not in self.__instances__:
                    self.__instances__.append(self)

            @classmethod
            def find_instance(cls, value, attr=None) -> object:
                if not attr:
                    attr = cls.obj_id
                for instance in cls.__instances__:
                    if getattr(instance, attr) == value:
                        return instance

            @classmethod
            def auto_generate_id_atts(cls, attr: str):
                ids = list()
                for inst in cls:
                    ids.append(getattr(inst, attr))
                for inst in cls:
                    inst.auto_define_id_attr(attr, ids)

            def auto_define_id_attr(self, attr: str, ids: list[int] = None):
                if hasattr(self, attr) and getattr(self, attr) is not None:
                    return
                if not ids:
                    ids = list()
                    for inst in type(self):
                        ids.append(getattr(inst, attr))
                id_num = type(self).__instances__.index(self) + 1
                if id_num in ids:
                    i = id_num
                    while True:
                        i += 1
                        if getattr(self, attr) not in ids:
                            setattr(self, attr, i)
                else:
                    setattr(self, attr, id_num)
        return TrackInstances
    elif new_track:
        @wraps(class_)
        def new_track_wrapper(class_):
            # old_init_ = deepcopy(class_.__init__)

            @wraps(class_, updated=())
            class NewTrackInstances(class_):
                __new_instances__ = list()

                def __init__(self, *args, new=False, **kwargs):
                    super().__init__(*args, **kwargs)

                    if new:
                        self.__new_instances__.append(self)

                @classmethod
                def find_new_instance(cls, object_id) -> object:
                    for instance in cls.__instances__:
                        if getattr(instance, cls.obj_id) == object_id:
                            return instance

            return NewTrackInstances

        @wraps(class_)
        def inside_wrap(class_):
            return new_track_wrapper(track_instances(class_))  # class_ is inside track_instances

        return inside_wrap
    return track_instances


# currently not using this
def check_if_object_already_exists(self):
    new_id = getattr(self, self.obj_id)

    for instance in type(self).__instances__:
        if getattr(instance, instance.obj_id) == new_id and new_id is not None:
            raise ObjectAlreadyExistsError({self.obj_id: new_id}, instance, self)
