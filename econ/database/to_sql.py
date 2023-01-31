def select(schema: str, table: str, condition: dict = None, columns: tuple[str] = ()) -> str:
    """Return a SELECT statement in SQL for querying.

    SELECT columns | '*' FROM table WHERE condition ; -- condition is optional
    """
    if condition is None:
        condition = {}
    query = ["SELECT", None, "FROM", None, "WHERE", None, ";"]
    temp = []
    if not columns:
        query[1] = "*"
    else:
        for column in columns:
            temp.append(f"`{column}`")
        query[1] = ", ".join(temp)
    query[3] = f"`{schema}`.`{table}`"
    temp.clear()
    if not condition:
        query[4:6] = "", ""
    else:
        for key, value in condition.items():
            temp.append(f"`{key}` = {value!r}")
        query[5] = " AND ".join(temp)

    return " ".join(query)


def insert(schema: str, table: str, info: dict) -> str:
    """Return an INSERT statement in SQL for querying.

    INSERT INTO table (info.keys) VALUES (info.values) ;
    """
    query = ["INSERT INTO", None, None, "VALUES", None, ";"]

    query[1] = f"`{schema}`.`{table}`"
    keys, values = [], []
    for key, value in info.items():
        keys.append(f"`{key}`")
        values.append(repr(value))

    query[2] = f"""({", ".join(keys)})"""
    query[4] = f"""({", ".join(values)})"""
    return " ".join(query)


def update(schema: str, table: str, info: dict, condition: dict = None) -> str:
    """Return an UPDATE statement in SQL for querying.

    UPDATE table SET info WHERE condition ;
    """
    if condition is None:
        condition = {}
    query = ["UPDATE", None, "SET", None, "WHERE", None, ";"]

    query[1] = f"`{schema}`.`{table}`"
    temp = []
    for key, value in info.items():
        temp.append(f"`{key}` = {repr(value)}")
    query[3] = ", ".join(temp)
    temp.clear()

    for key, value in condition.items():
        temp.append(f"`{key}` = {repr(value)}")
    query[5] = " AND ".join(temp)

    return " ".join(query)


def delete(schema: str, table: str, condition: dict) -> str:
    """Return a DELETE statement in SQL for querying.

    DELETE FROM table WHERE condition ;
    """
    query = ["DELETE FROM", None, "WHERE", None, ";"]

    query[1] = f"`{schema}`.`{table}`"

    temp = []
    for column, value in condition:
        temp.append(f"`{column}`={value}")
    query[3] = " AND ".join(temp)

    return " ".join(query)
