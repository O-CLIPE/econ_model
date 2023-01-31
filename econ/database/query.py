import mysql.connector  # mysql-connector-python

from econ.database import to_sql
from exceptions import EmptyTableError, MissingArgumentsError
from utils import print_in_file


def create_func(obj, table: str, unique: str | tuple[str] = "", *, return_=True, kwargs=None) -> int | None:
    """Insert data into specified table.

    Query an INSERT statement with information provided by the arguments
    personalized for {table}

    Keyword arguments:
    unique: Column/columns that hold the primary key. If empty, unique = {table}_id.
    table: The database table in which to to_sql.insert information.
    kwargs: Information specified based on the columns present on {table}.
    """
    if unique == "":
        unique = f"{table}_id"
    if not isinstance(table, str):
        raise TypeError(f"Expected str, got {type(table)}.")
    if not isinstance(unique, (str, tuple)):
        raise TypeError(f"Expected str, got {type(unique)}.")
    if isinstance(unique, str):
        unique = tuple(unique, )

    with mysql.connector.connect(host=obj.host, user=obj.user, password=obj.password) as database:
        query = to_sql.insert(table, kwargs)
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()

        if return_:
            with database.cursor() as cursor:
                cursor.execute(to_sql.select(table, {k: v for k, v in kwargs.items() if k in kwargs}, unique))
                return cursor.fetchone()[0]


def get_func(obj, table: str, where: dict = None, get_info: str | tuple[str] = None, *, infile=False,
             where_is_id=False) -> dict | list[dict]:
    """Get information from the database related to the specified table.

    return a list[dict] if where_is_id=False, else return a dict.
    If there are no arguments (besides table), return all entities information as dictionaries.

    Keyword arguments:
    table: The table in which to get info from.
    where: Identification or common info from rows.
    get_info: What you want from the entities that 'where' specifies. If default returns all.
    """
    if not isinstance(where, dict):
        raise TypeError(f"Expected dict, got {type(where)}")
    if not isinstance(table, str):
        raise TypeError(f"Expected str, got {type(table)}.")
    if get_info is None:
        get_info = tuple()
    if not isinstance(get_info, tuple):
        get_info = tuple((get_info,))

    with mysql.connector.connect(host=obj.host, user=obj.user, password=obj.password) as database:
        with database.cursor(dictionary=True) as cursor:
            if not where and not get_info:
                query = to_sql.select(table)
                cursor.execute(query)
                info = cursor.fetchall()  # list[dict]
            elif isinstance(where, dict):
                query = to_sql.select(table, where, get_info)
                cursor.execute(query)
                if where_is_id:
                    info = cursor.fetchone()  # dict
                else:
                    info = cursor.fetchall()  # list[dict]
            if infile:
                if isinstance(info, list):
                    try:
                        line = info[0]
                    except IndexError:
                        raise EmptyTableError("There is no info to print infile.")
                    result = []
                    for d in info:
                        result.append(tuple([v for v in d.values()]))
                else:  # isinstance(info, dict)
                    line = info
                    result = [tuple([v for v in info.values()])]
                headings = tuple([key for key in line])
                print_in_file(table, result, 27, headings)
            return info


def _set_and_del_func(obj, call, table: str, identifier_options: dict[str, type] = tuple(), identifier=None,
                      kwargs=None):
    if not isinstance(table, str):
        raise TypeError(f"Expected str, got {type(table)}.")

    identifier_dict = dict()
    for key, type_ in identifier_options:
        value = kwargs.get(key, None)
        if value:
            identifier_dict[key] = value
            del kwargs[key]

        if isinstance(identifier, type_):
            identifier_dict[key] = identifier
    if not isinstance(identifier, dict):
        identifier = identifier_dict

    for dictionary in (identifier, kwargs):
        for key, value in dictionary.copy().items():
            if value is None:
                del kwargs[key]

    if not identifier:
        raise MissingArgumentsError("There's nothing left on identifier. Assert there is one")

    with mysql.connector.connect(host=obj.host, user=obj.user, password=obj.password) as database:
        query = call(table, kwargs, identifier)
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()


def set_func(obj, table: str, identifier_options: dict[str, type] = tuple(), identifier=None, kwargs=None) -> None:
    """Set information in the database to the specified table.

    query an UPDATE statement with information provided by the arguments
    personalized for {table}
    All arguments are REQUIRED.

    Keyword arguments:
    table: The table in which to set information to.
    identifier_options: state possible types of identifier with corresponding column-keys.
    identifier: set values where identifier.
    kwargs: The information to update the table.
    """
    _set_and_del_func(obj, to_sql.update, table, identifier_options, identifier, kwargs)


def delete_func(obj, table: str, identifier_options: dict[str, type] = tuple(), identifier=None) -> None:
    _set_and_del_func(obj, to_sql.delete, table, identifier_options, identifier)
