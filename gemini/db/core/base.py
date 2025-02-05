from typing import Any
import pprint

from sqlalchemy import select, insert, delete, update
from sqlalchemy import TIMESTAMP, JSON, DATE, String
from sqlalchemy import MetaData, text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy.dialects.postgresql import insert as pg_insert, JSONB

from gemini import global_manager
from gemini.db.core.engine import DatabaseEngine
from gemini.config.settings import GEMINISettings

db_config = global_manager.get_settings().get_database_config()
metadata_obj = MetaData(schema="gemini")
db_engine = DatabaseEngine(db_config)


class BaseModel(DeclarativeBase, SerializeMixin):
    __abstract__ = True
    metadata = metadata_obj

    # def __repr__(self) -> str:
    #     dict_repr = self.to_dict()
    #     return pprint.pformat(dict_repr)

    @classmethod
    def set_engine(cls, engine: DatabaseEngine):
        global db_engine
        db_engine = engine

    @classmethod
    def unique_fields(cls):
        """
        Get the unique fields of the class.
        """
        unique_fields = []
        for constraint in cls.__table__.constraints:
            if isinstance(constraint, UniqueConstraint):
                for column in constraint.columns:
                    unique_fields.append(column.name)
        return unique_fields
    
    @classmethod
    def validate_fields(cls, **kwargs):
        """
        Validate the fields of the class.
        """
        # Remove None values from the kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        # Remove empty dicts from the kwargs
        kwargs = {k: v for k, v in kwargs.items() if v != {}}
        # Remove Items that are not columns in the table
        columns = cls.__table__.columns.keys()
        kwargs = {k: v for k, v in kwargs.items() if k in columns}
        return kwargs
    
    @classmethod
    def create(cls, **kwargs):
        """
        Create a new instance of the class.
        """
        kwargs = cls.validate_fields(**kwargs)
        instance = cls(**kwargs)
        with db_engine.get_session() as session:
            session.add(instance)
        return instance
    
    @classmethod
    def all(cls):
        """
        Get all instances of the class.
        """
        query = select(cls)
        with db_engine.get_session() as session:
            result = session.execute(query).scalars().all()
        return result
    
    @classmethod
    def get(cls, id):
        """
        Get an instance of the class by ID.
        """
        query = select(cls).where(cls.id == id)
        with db_engine.get_session() as session:
            result = session.execute(query).scalar_one_or_none()
        return result
    
    @classmethod
    def get_by_parameters(cls, **kwargs):
        """
        Get instances of the class by multiple
        parameters.
        """
        query = select(cls)
        kwargs = cls.validate_fields(**kwargs)
        if kwargs == {}:
            return None
        for key, value in kwargs.items():
            attribute = getattr(cls, key)
            if isinstance(attribute.type, JSON):
                query = query.where(attribute.contains(value))
            elif isinstance(attribute.type, TIMESTAMP):
                query = query.where(attribute >= value)
            else:
                query = query.where(attribute == value)
        with db_engine.get_session() as session:
            result = session.execute(query).scalars().first()
        return result
    
    @classmethod
    def update(cls, instance, **kwargs):
        """
        Update an instance of the class.
        """
        with db_engine.get_session() as session:
            kwargs = cls.validate_fields(**kwargs)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.add(instance)
        return instance

    # @classmethod
    # def update_or_get(cls, instance, **kwargs):
    #     """
    #     Update an existing instance or create a new one.
    #     """
    #     try:
    #         unique_fields = cls.unique_fields()
    #         kwargs = cls.validate_fields(**kwargs)
    #         unique_kwargs = {key: value for key, value in kwargs.items() if key in unique_fields}
    #         if unique_kwargs == {}:
    #             return None
    #         instance = cls.update(instance, **kwargs)
    #         return instance
    #     except Exception as e:
    #         return None


    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Get an existing instance or create a new one.
        """
        unique_fields = cls.unique_fields()
        kwargs = cls.validate_fields(**kwargs)
        unique_kwargs = {key: value for key, value in kwargs.items() if key in unique_fields}
        if unique_kwargs == {}:
            return None
        instance = cls.get_by_parameters(**unique_kwargs)
        if instance:
            return instance
        else:
            instance = cls.create(**kwargs)
            return instance
        
    @classmethod
    def delete(cls, instance):
        """
        Delete an instance of the class.
        """
        with db_engine.get_session() as session:
            session.delete(instance)
        return True
    


    @classmethod
    def get_model_from_table_name(cls, table_name):
        """
        Get the model by table name
        """
        return cls.metadata.tables[f"{cls.metadata.schema}.{table_name}"]
        
    @classmethod
    def insert_bulk(cls, constraint, data):
        with db_engine.get_session() as session:
            table = cls.__table__
            stmt = pg_insert(table).on_conflict_do_nothing(constraint=constraint).returning(table.c.id)
            inserted_records = session.execute(stmt, data, execution_options={"populate_existing": True})
            inserted_ids = [record.id for record in inserted_records]
            return inserted_ids
        
        
        
    @classmethod
    def update_bulk(cls, constraint, upsert_on, data):
        with db_engine.get_session() as session:
            table = cls.__table__
            stmt = pg_insert(table).on_conflict_do_update(constraint=constraint, set_={upsert_on: stmt.excluded[upsert_on]}).returning(table.c.id)
            inserted_records = session.execute(stmt, data, execution_options={"populate_existing": True})
            inserted_ids = [record.id for record in inserted_records]
            return inserted_ids
        

    @classmethod
    def delete_bulk(cls, data):
        with db_engine.get_session() as session:
            table = cls.__table__
            stmt = delete(table).where(table.c.id.in_(data))
            session.execute(stmt)
            return True
        
        
    @classmethod
    def update_or_create(cls, constraint, **kwargs):
        unique_fields = cls.unique_fields()
        kwargs = cls.validate_fields(**kwargs)
        unique_kwargs = {key: value for key, value in kwargs.items() if key in unique_fields}
        if unique_kwargs == {}:
            return None
        instance = cls.get_by_parameters(**unique_kwargs)
        if instance:
            instance = cls.update(instance, **kwargs)
            return instance
        else:
            instance = cls.create(**kwargs)
            return instance
        
        
        
    @classmethod
    def search(cls, **kwargs):
        with db_engine.get_session() as session:
            query = select(cls)
            kwargs = cls.validate_fields(**kwargs)
            for key, value in kwargs.items():
                attribute = getattr(cls, key)
                if isinstance(attribute.type, JSONB):
                    query = query.where(attribute.contains(value))
                elif isinstance(attribute.type, TIMESTAMP):
                    query = query.where(attribute >= value)
                else:
                    query = query.where(attribute == value)
            result = session.execute(query).scalars().all()
        return result
        
    @classmethod
    def paginate(cls, order_by, page_number, page_limit, **kwargs):
        with db_engine.get_session() as session:
            query = session.query(cls)
            kwargs = cls.validate_fields(**kwargs)
            for key, value in kwargs.items():
                attribute = getattr(cls, key)
                if isinstance(attribute.type, JSON):
                    query = query.filter(attribute.contains(value))
                elif isinstance(attribute.type, TIMESTAMP):
                    query = query.filter(attribute >= value)
                else:
                    query = query.filter(attribute == value)
            number_of_records = query.count()
            number_of_pages = number_of_records // page_limit
            if page_number > 0:
                query = query.offset((page_number - 1) * page_limit)
            query = query.limit(page_limit)
            query_result = query.all()
        return number_of_records, number_of_pages, query_result
    
    @classmethod
    def stream(cls, **kwargs):
        query = select(cls)
        kwargs = cls.validate_fields(**kwargs)
        for key, value in kwargs.items():
            attribute = getattr(cls, key)
            if isinstance(attribute.type, JSON):
                query = query.where(attribute.contains(value))
            elif isinstance(attribute.type, TIMESTAMP):
                query = query.where(attribute >= value)
            else:
                query = query.where(attribute == value)
        query = query.execution_options(yield_per=1000)
        with db_engine.get_session() as session:
            for partition in session.execute(query).scalars().partitions():
                for instance in partition:
                    yield instance


class ViewBaseModel(BaseModel):

    __abstract__ = True

    @classmethod
    def refresh(cls):
        with db_engine.get_session() as session:
            query = text(f"REFRESH MATERIALIZED VIEW {cls.__table__.name}")
            session.execute(query)
        
    @classmethod
    def get(cls):
        cls.refresh()
        return super().get()
    
    @classmethod
    def all(cls):
        cls.refresh()
        return super().all()
    
    @classmethod
    def get_by_parameters(cls, **kwargs):
        cls.refresh()
        return super().get_by_parameters(**kwargs)
    
    @classmethod
    def search(cls, **kwargs):
        cls.refresh()
        return super().search(**kwargs)
    
    @classmethod
    def paginate(cls, order_by, page_number, page_limit, **kwargs):
        cls.refresh()
        return super().paginate(order_by, page_number, page_limit, **kwargs)
    
    @classmethod
    def stream(cls, **kwargs):
        cls.refresh()
        return super().stream(**kwargs)
    
class ColumnarBaseModel(BaseModel):

    __abstract__ = True
    

