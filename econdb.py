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

                    # 2. Entity functions
def create_entity(name, **kwargs) -> int:
    # keywords -> name, income, expenses, value
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        kwargs['name'] = name
        keys, values = list(), list(); 

        for key, value in kwargs.items():
            keys.append(key)
            values.append(value)

        keys = repr(keys); 
        values = repr(values)

        keys = keys[1:-1]; 
        keys = keys.replace("'", "`")
        values = values[1:-1] 

        query = f"INSERT INTO `market`.`entity` ({keys}) VALUES ({values});"
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()
        
        with database.cursor() as cursor:
            cursor.execute(f"SELECT `entity_id` FROM `market`.`entity` WHERE `name`={repr(name)}")
            return cursor.fetchone()[0]

def set_entity(identifier=None, **kwargs):
    # identifier -> name or id
    # keywords -> income, expenses, value
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        query = ["UPDATE `market`.`entity` SET "]

        for key, value in kwargs.copy().items():
            if value is None:
                del kwargs[key]
            elif key == 'entity_id':
                del kwargs[key]
                identifier = value

        for idx, [key, value] in enumerate(kwargs.items()):
            query.append(f"`{key}` = {repr(value)} ")
            if len(kwargs) != idx + 1:
                query.append(", ") 

        if isinstance(identifier, str):
            query.append(f"WHERE `name` = {repr(identifier)};")
        else:
            query.append(f"WHERE `entity_id` = {repr(identifier)};")

        query = "".join(query)

        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()
            
def get_entity(*columns, where=None) -> int | dict | list:
    # columns -> id, name, income, expenses, value
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        query = ["SELECT "]
        if not columns: 
            query.append("* ")
        else:
            for idx, value in enumerate(columns):
                query.append(f"`{value}` ")
                if len(columns) != idx + 1:
                    query.append(", ")
        query.append("FROM `market`.`entity` ")

        if where is None:
            query = "".join(query)
            with database.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print_in_file("database", result, 27)
        elif isinstance(where, int):
            query.append(f"WHERE `entity_id` = {where}; ")
            query = "".join(query)
            with database.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchone()
        elif isinstance(where, str):
            query.append(f"WHERE `name` = {repr(where)}; ")
            query = "".join(query)
            with database.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0]
        elif isinstance(where, dict):
            query.append(" WHERE ")
            for idx, [key, value] in enumerate(where.items()):
                query.append(f"`{key}` = {repr(value)} ")
                if len(where) != idx + 1:
                    query.append("AND ")
            query = "".join(query)
            with database.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result



                    # 3.Product funcitons
def create_product(producer_id: int, good_id: int, **kwargs):
    # keywords -> name, income, expenses, value
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        kwargs['producer_id'] = producer_id
        kwargs['good_id'] = good_id

        keys, values = list(), list(); 

        for key, value in kwargs.items():
            if isinstance(value, int):
                value = float(value)
            keys.append(key)
            values.append(value)

        keys_repr = repr(keys)[1:-1].replace("'", "`"); 
        values_repr = repr(values)[1:-1]

        query = f"INSERT INTO `market`.`product` ({keys_repr}) VALUES ({values_repr});"
        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()



                    # 4.Good functions
def create_good(name: str, **kwargs):
    # keywords -> name, value, price
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        kwargs['name'] = name

        keys, values = list(), list()
        for key, value in kwargs.items():
            if isinstance(value, int):
                value = float(value)
            keys.append(repr(key).replace("'", "`"))
            values.append(repr(value))

        keys = ", ".join(keys)
        values = ", ".join(values)
        query = [f"INSERT INTO `market`.`good` ({keys}) VALUES ({values});"]

        with database.cursor() as cursor:
            cursor.execute(query)
            database.commit()

def get_good_id(**kwargs) -> list | None:
    # keywords -> id, name, income, expenses, value
    with mysql.connector.connect(host=host, user=user, password=password) as database:
        query = ["SELECT `entity_id`, `name` FROM `market`.`entity` WHERE "]
        for idx, [key, value] in enumerate(kwargs.items()):
            query.append(f"`{key}` = {repr(value)} ")
            if len(kwargs) != idx + 1:
                query.append("AND ")

        query = "".join(query)

        with database.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result



                    # 5.Utility
def print_in_file(filename: str, data: list, column_size_limit: int, headings=['entity_id', 'name', 'income', 'expenses', 'value']):
    with open(f"{filename}.dbr", "w") as f:
        f.write("-- This was an automatically generated file. --\nDatabase data: ")
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