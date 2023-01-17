import mysql.connector # mysql-connector-python
from getpass import getpass

                    # 1. Defining database access and querying the market_and_entities.sql
def access_info():
    global host, user, password

    host = "localhost"; print(host)
    user = "root"; print(user)
    password = getpass("password: ")
access_info()

def query_schema():
    with mysql.connector.connect(
        host=host,
        user=user,
        password=password
    ) as db:

        with open("market_and_entities.sql") as query:
            with db.cursor() as cursor:
                cursor.execute(query.read(), multi=True)
query_schema()

                    # 2. Generalization
def create_func(table: str, ordered_not_null_variables: tuple[str], *args, **kwargs) -> int:
    """Insert data into the market.{table} table.
    
    Query an INSERT statement with information provided by the arguments
    personalized for {table}
    Only kwargs isn't required.

    Keyword arguments:
    table: The table in wich to insert info.
    ordered_not_null_variables: Keys that can't be null in kwargs. Ordered for the purpose of args
    args: Information especified in ordered_not_null_variable declared in the same order.
    kwargs: Information especified with a key.
    """
    with mysql.connector.connect(host=host, user=user, password=password) as database:

        for idx, var in enumerate(ordered_not_null_variables):
            kwargs[var] = args[idx - 1]

        query = insert(table, kwargs)
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()
        
        with database.cursor() as cursor:
            print({key: value for key, value in kwargs.items() if key in ordered_not_null_variables})
            cursor.execute(select(table, {key: value for key, value in kwargs.items() if key in ordered_not_null_variables}, (f'{table}_id',)))
            return cursor.fetchone()[0]

def get_func(table: str, where={}, info=()) -> dict | list[tuple] | None:
    """Get information from the database related to the market.{table} table.
    
    If identification is given, return dict from a single {table}.
    Else return a list containing one tuple for each matching {table}.
    If there are no arguments (besides table), print all entities information in file.

    Keyword arguments:
    table: The table in wich to get info from.
    where: Identification* or a common info** from entities. *int | str, return dict. **dict, return a list.
    info: What you want from the entities that where specifies.
    """
    if not isinstance(info, tuple):
        info = tuple((info,))
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        if not where and not info:
            query = select(table)
            with database.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                foo = cursor.fetchall()
                headings = tuple([key for key in foo[0]])
                result = []
                for d in foo:
                    result.append(tuple([v for v in d.values()]))
                print_in_file(table, result, 27, headings)
        elif isinstance(where, int):
            query = select(table, {f'{table}_id': where}, info)
            with database.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchone()
        elif isinstance(where, str):
            query = select(table, {'name': where}, info)
            with database.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchone()
        elif isinstance(where, dict):
            query = select(table, where, info)
            with database.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result


def set_func(table: str, identifier: str | int = None, **kwargs):
    """Set information in the database to the market.{table} table.
    
    Query an UPDATE statement with information provided by the arguments
    personalized for {table}
    All arguments are REQUIRED.

    Keyword arguments:
    table: The table in wich to set info to.
    identifier: 'name' if string, '{table}_id' if int.
    kwargs: The information to update the table.
    """
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        for key, value in kwargs.copy().items():
            if value is None:
                del kwargs[key]
            elif key == f'{table}_id':
                del kwargs[key]
                identifier = value

        if isinstance(identifier, str):
            type_ = 'name'
        else:
            type_ = f'{table}_id'

        print(identifier)
        query = update(table, kwargs, {type_: identifier})
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()

                    # 3.Table/Class especific
def create_entity(name, **kwargs) -> int:
    """Call create_func with table='entity'.

    Keywords -> name, income, expenses, value"""
    create_func('entity', ('name',), name, **kwargs)

def set_entity(identifier: int | str = None, **kwargs):
    # identifier -> name or id
    # keywords -> income, expenses, value
    set_func('entity', identifier, **kwargs)
            
def get_entity(where={}, info=()) -> dict | list | None:
    # columns -> id, name, income, expenses, value
    get_func('entity', where, info)


def create_product(producer_id: int, good_id: int, **kwargs):
    """Call create_func with table='entity'.

    Keywords -> name, income, expenses, value"""
    # keywords -> name, income, expenses, value
    create_func('product', ('producer_id', 'good_id'), producer_id, good_id, **kwargs)

def set_product(identifier: int | str, **kwargs):
    # identifier -> name or id
    # keywords -> name, value, price, supply
    set_func('product', identifier, **kwargs)

def get_product(where={}, info=()) -> dict | list | None:
    # columns -> good_id, entity_id, id, name, value, price, supply
    get_func('product', where, info)


def create_good(name: str, **kwargs):
    # keywords -> name, value, price
   create_func('good', ('name',), name, **kwargs)

def set_good(identifier: int | str, **kwargs):
    # identifier -> name or id
    # keywords -> name, price
    set_func('product', identifier, **kwargs)

def get_good(where={}, info=()) -> dict | list[tuple] | None:
    # columns -> id, name, income, expenses, value
    get_func('good', where, info)


                    # 4.Representation of data in file
def print_in_file(filename: str, data: list, column_size_limit: int, headings: tuple):
    """Writes in filename.dbtxt the data with headings and custom column_size"""
    with open(f"{filename}.dbtxt", "w") as f:
        f.write("-- This was an automatically generated file. --\nData: ")
        for idx, head in enumerate(headings):
            f.write(f"{head}")
            if idx != len(headings) - 1:
                f.write(", ")
            else:
                f.write(".")
        f.write('\n\n')
        data.insert(0, headings)
        for table in data:
            for idx, column in enumerate(table):
                text = str(column)
                if len(text) >= column_size_limit - 2:
                    text = abbreviate(text, column_size_limit - 1)
                f.write(text)
                for i in range(column_size_limit - len(text)):
                    f.write(' ')
            f.write('\n')

def abbreviate(text: str, limit: int) -> str:
    """Abbreviate text to fit in limit."""
    abbv = str(text)
    for (old, new) in (("Incorporated", "Inc."), ("Company", "Co."), ("Limited", "Ltd."),
        ("Association", "Assoc."), ("Brothers", "Bros."), ("Compagnie", "Cie."),
        ("Manufacturings", "Mfg."), ("Manufacturers", "Mfrs.")):
        abbv = abbv.replace(old, new)

    if " " in text and len(abbv) > limit:
        if abbv.count(" ") <= limit/3:
            m = abbv.split()
            for idx, item in enumerate(m):
                if len(m[idx]) > 3:
                    m[idx] = f"{item[:3]}."
            abbv = " ".join(m)
        else:
            m = abbv.split()
            for idx, item in enumerate(m):
                m[idx] = item[0]
            abbv = "".join(m)
    elif len(abbv) > limit:
        abbv = f"{text[:limit - 1]}."
    return abbv[:limit]


                    # 5.TO SQL
def select(table: str, condition: dict = {}, columns: tuple = ()) -> str:
    """Create a SELECT statement in SQL for querying."""
    query = ["SELECT", None, "FROM", None, "WHERE", None, ";"]
    temp = []
    if not columns:
        query[1] = "*"
    else:
        for column in columns:  
            temp.append(f"`{column}`")
        query[1] = ", ".join(temp)
    query[3] = f"`market`.`{table}`"
    temp.clear()
    if not condition:
        query[4:6] = "", ""
    else:
        for key, value in condition.items():
            temp.append(f"`{key}` = {value!r}")
        query[5] = ", ".join(temp)

    return " ".join(query)

def insert(table: str, info: dict) -> str:
    """Create an INSERT statement in SQL for querying."""
    query = ["INSERT INTO", None, None, "VALUES", None, ";"]

    query[1] = f"`market`.`{table}`"
    keys, values = [], []
    for key, value in info.items():
        keys.append(f"`{key}`")
        values.append(repr(value))

    query[2] = f"""({", ".join(keys)})"""
    query[4] = f"""({", ".join(values)})"""
    return " ".join(query)


def update(table: str, info: dict, condition: dict = {}) -> str:
    """Create an UPDATE statement in SQL for querying."""
    query = ["UPDATE", None, "SET", None, "WHERE", None, ";"]

    query[1] = f"`market`.`{table}`"
    temp = []
    for key, value in info.items():
        temp.append(f"`{key}` = {repr(value)}")
    query[3] = ", ".join(temp)
    temp.clear()
    if not condition:
        query[4:6] = "", ""
    else:
        for key, value in condition.items():
            temp.append(f"`{key}` = {repr(value)}")
        query[5] = ", ".join(temp)
    return " ".join(query)
