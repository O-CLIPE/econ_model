import mysql.connector  # mysql-connector-python
from getpass import getpass
from time import sleep  # Some queries are slower than python code, and without sleep could cause unexpected errors.

from econ.database import query
from utils import list_all_args
from exceptions import MissingArgumentsError


class EconDatabase:
    """Automate connection to the database. Instances represent different connections/schemas."""
    def __init__(self, schema='market', host="localhost", user="root", password=None, *, pass_in_file=False):
        self.password = password
        self.host = host
        self.user = user
        self.schema = schema

        if pass_in_file:
            with open(password) as f:
                self.password = f.read()
        if not password:
            self.password = getpass('password: ')

    def build(self, sql_script: str):
        """Build the market database querying market_and_entities.sql"""
        with mysql.connector.connect(host=self.host, user=self.user, password=self.password) as db:
            query = sql_script.replace('market', self.schema)
            with db.cursor() as cursor:
                cursor.execute(query, multi=True)
        sleep(0.1)

    def drop(self):
        """Drops the name database (deletes it)."""
        with mysql.connector.connect(host=self.host, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute(f"DROP SCHEMA `{self.schema}`")
                db.commit()
        sleep(0.1)

    def schema_exists(self) -> bool:
        """Checks if the schema attributed to this instance exists"""
        with mysql.connector.connect(host=self.host, user=self.user, password=self.password) as db:
            with db.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{self.schema}';")
                result = cursor.fetchone()
                return True if result else False

    @list_all_args
    def create_entity(self, entity_id, name, **kwargs) -> int:
        """Inserts Entity information to database."""
        return query.create_func(self, 'entity', unique='entity_id', kwargs=kwargs['all'])

    def get_entity(self, where: int | str | dict = None, get_info: str | tuple[str] = None) -> dict | list:
        """Selects Entity information from database."""
        id_ = True
        if isinstance(where, str):   where = {'name': where}
        elif isinstance(where, int): where = {'entity_id': where}
        else:                        id_ = False
        return query.get_func(self, 'entity', where, get_info, where_is_id=id_)

    def set_entity(self, identifier: int | str = None, **kwargs):
        """Updates Entity information to database"""
        return query.set_func(self, 'entity', {'entity_id': int, 'name': str}, identifier, kwargs)

    @list_all_args
    def create_product(self, product_id: int, producer_id: int, good_id: int, name: str, **kwargs) -> int:
        """Inserts Product information to database."""
        return query.create_func(self, 'product', unique='product_id', kwargs=kwargs['all'])

    def get_product(self, where: int | str | dict = None, get_info: str | tuple[str] = None) -> dict | list:
        """Selects Product information from database."""
        id_ = True
        if isinstance(where, str):   where = {'name': where}
        elif isinstance(where, int): where = {'product_id': where}
        else:                        id_ = False
        return query.get_func(self, 'product', where, get_info, where_is_id=id_)

    def set_product(self, identifier: int | str, **kwargs):
        """Updates Product information to database."""
        return query.set_func(self, 'product', {'product_id': int, 'name': str}, identifier, **kwargs)

    @list_all_args
    def create_good(self, good_id: int, name: str, **kwargs) -> int:
        """Inserts Good information to database."""
        return query.create_func(self, 'good', unique='good_id', kwargs=kwargs['all'])

    def get_good(self, where: int | str | dict = None, get_info: str | tuple[str] = None) -> dict | list:
        """Selects Product information from database."""
        id_ = True
        if isinstance(where, str):   where = {'name': where}
        elif isinstance(where, int): where = {'good_id': where}
        else:                        id_ = False
        return query.get_func(self, 'good', where, get_info, where_is_id=id_)

    def set_good(self, identifier: int | str, **kwargs):
        """Updates Good information to database."""
        return query.set_func(self, 'good', {'name': str, 'good_id': int}, identifier, kwargs)

    # Consume -> Buy
    @list_all_args
    def create_buy(self, index: int, entity_id: int, product_id: int, quantity: int, price: float, **kwargs) -> int:
        """Inserts Buy information to database."""
        return query.create_func(self, 'buy', unique='index', kwargs=kwargs['all'], is_asset=quantity)

    def get_buy(self, where: int | dict = None, get_info: str | tuple[str] = None) -> dict | list[tuple] | None:
        """Selects Buy information from database."""
        id_ = True
        if isinstance(where, int): where = {'index': where}
        else:                      id_ = False
        return query.get_func(self, 'buy', where, get_info, where_is_id=id_)

    def set_buy(self, index: int, **kwargs):
        """Updates Buy information to database"""
        return query.set_func(self, 'buy', {'index': int}, index, kwargs)

    # Production goods
    @list_all_args
    def create_production_good(self, higher_good_id: int, lesser_good_id: int, quantity=1, **kwargs) -> int:
        """Inserts ProductionGoods information to database"""
        return query.create_func(self, 'production_good', unique=('higher_good_id', 'lesser_good_id'),
                                 kwargs=kwargs['all'])

    def get_production_good(self, where: int | dict = None, get_info: tuple[str] = None) -> dict | list[tuple] | None:
        """Selects ProductionGoods information from database."""
        id_ = True
        if isinstance(where, int): where = {'higher_good_id': where}
        else:                      id_ = False
        return query.get_func(self, 'production_good', where, get_info, where_is_id=id_)

    def set_production_good(self, index: int = None, higher_good_id: int = None, **kwargs):
        """Updates ProductionGoods information to database"""
        identifier = dict()
        identifier['index'] = index
        identifier['higher_good_id'] = higher_good_id
        if not identifier:
            raise MissingArgumentsError
        return query.set_func(self, 'production_good', identifier={'index': index, 'higher_good_id': higher_good_id},
                              kwargs=kwargs)

    # Good alternatives
    @list_all_args
    def create_good_alternative(self, good_id: int, alternative_id: int, **kwargs):
        """Insert GoodAlternative information to database"""
        return query.create_func(self, 'good_alternative', unique='alternative_id', kwargs=kwargs['all'])

    def delete_good_alternative(self, alternative_id: int):
        """Deletes GoodAlternative row on the database"""
        return query.delete_func(self, 'good_alternative', {'alternative_id': int}, alternative_id)
