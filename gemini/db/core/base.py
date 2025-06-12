from typing import Any

from sqlalchemy import select, delete
from sqlalchemy import TIMESTAMP, JSON, DATE
from sqlalchemy import MetaData, text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy.dialects.postgresql import insert as pg_insert, JSONB

from gemini.manager import GEMINIManager, GEMINIComponentType
from gemini.db.core.engine import DatabaseEngine
from gemini.db.config import DatabaseConfig


db_config_settings = GEMINIManager().get_component_settings(GEMINIComponentType.DB)
db_config = DatabaseConfig(
    database_url=f"postgresql://{db_config_settings['GEMINI_DB_USER']}:{db_config_settings['GEMINI_DB_PASSWORD']}@{db_config_settings['GEMINI_DB_HOSTNAME']}:{db_config_settings['GEMINI_DB_PORT']}/{db_config_settings['GEMINI_DB_NAME']}"
)
metadata_obj = MetaData(schema="gemini")
db_engine = DatabaseEngine(db_config)


class BaseModel(DeclarativeBase, SerializeMixin):

    __abstract__ = True
    metadata = metadata_obj


    @classmethod
    def set_engine(cls, engine: DatabaseEngine):
        global db_engine
        db_engine = engine


    @classmethod
    def unique_fields(cls):
        unique_fields = []
        for constraint in cls.__table__.constraints:
            if isinstance(constraint, UniqueConstraint):
                for column in constraint.columns:
                    unique_fields.append(column.name)


        return unique_fields
    

    @classmethod
    def validate_fields(cls, **kwargs):
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
        kwargs = cls.validate_fields(**kwargs)
        instance = cls(**kwargs)
        with db_engine.get_session() as session:
            session.add(instance)
        return instance
    

    @classmethod
    def exists(cls, **kwargs):
        kwargs = cls.validate_fields(**kwargs)
        if kwargs == {}:
            return False
        instance = cls.get_by_parameters(**kwargs)
        if instance:
            return True
        return False


    @classmethod
    def all(cls):
        query = select(cls)
        with db_engine.get_session() as session:
            result = session.execute(query).scalars().all()
        return result
    

    @classmethod
    def get(cls, id):
        query = select(cls).where(cls.id == id)
        with db_engine.get_session() as session:
            result = session.execute(query).scalar_one_or_none()
        return result
    

    @classmethod
    def get_by_parameters(cls, **kwargs):
        query = select(cls)
        kwargs = cls.validate_fields(**kwargs)
        if kwargs == {}:
            return None
        for key, value in kwargs.items():
            attribute = getattr(cls, key)
            if isinstance(attribute.type, JSON):
                query = query.where(attribute.contains(value))
            elif isinstance(attribute.type, TIMESTAMP):
                query = query.where(attribute == value)
            else:
                query = query.where(attribute == value)
        with db_engine.get_session() as session:
            result = session.execute(query).scalars().first()
        return result
    

    @classmethod
    def update(cls, instance, **kwargs):
        with db_engine.get_session() as session:
            kwargs = cls.validate_fields(**kwargs)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.add(instance)
        return instance
    
    @classmethod
    def get_or_update(cls, instance, **kwargs):
        unique_fields = cls.unique_fields()
        kwargs = cls.validate_fields(**kwargs)
        unique_kwargs = {key: value for key, value in kwargs.items() if key in unique_fields}
        if unique_kwargs == {}:
            return instance
        existing_instance = cls.get_by_parameters(**unique_kwargs)
        if existing_instance:
            return existing_instance
        # If no existing instance found, update the current instance
        if not instance:
            instance = cls(**kwargs)
        else:
            # Update the existing instance with new values
            instance = cls.update(instance, **kwargs)


    @classmethod
    def get_or_create(cls, **kwargs):
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
        try:
            with db_engine.get_session() as session:
                session.delete(instance)
            return True
        except Exception as e:
            print(f"Error deleting instance: {e}")
            return False
    
    @classmethod
    def get_model_from_table_name(cls, table_name):
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
    def update_parameter(cls, instance, parameter_name, parameter_value):
        # Check if parameter_name is a valid column in the table
        if parameter_name not in cls.__table__.columns:
            raise ValueError(f"{parameter_name} is not a valid column in {cls.__tablename__}")
        with db_engine.get_session() as session:
            # Update the parameter value
            setattr(instance, parameter_name, parameter_value)
            session.add(instance)
        return instance
        
        
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
                elif isinstance(attribute.type, DATE):
                    query = query.where(attribute == value)  
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
                elif isinstance(attribute.type, DATE):
                    query = query.filter(attribute == value)
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
            elif isinstance(attribute.type, DATE):
                query = query.where(attribute == value)
            else:
                query = query.where(attribute == value)
        query = query.execution_options(yield_per=1000)
        with db_engine.get_session() as session:
            for partition in session.execute(query).scalars().partitions():
                for instance in partition:
                    yield instance


    @classmethod
    def rawstream(cls, **kwargs):
        query = select(cls)
        kwargs = cls.validate_fields(**kwargs)
        for key, value in kwargs.items():
            attribute = getattr(cls, key)
            if isinstance(attribute.type, JSON):
                query = query.where(attribute.contains(value))
            elif isinstance(attribute.type, TIMESTAMP):
                query = query.where(attribute >= value)
            elif isinstance(attribute.type, DATE):
                query = query.where(attribute == value)
            else:
                query = query.where(attribute == value)
        query = query.execution_options(yield_per=50)
        with db_engine.get_engine().connect() as conn:
            result = conn.execute(query).scalars().partitions()
            for partition in result:
                for instance in partition:
                    yield instance



class ViewBaseModel(BaseModel):

    __abstract__ = True


class MaterializedViewBaseModel(BaseModel):

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
    

    @classmethod
    def all(cls, limit=100):
        query = select(cls).limit(limit)
        with db_engine.get_session() as session:
            result = session.execute(query).scalars().all()
        return result
        
