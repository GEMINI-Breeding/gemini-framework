from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import TIMESTAMP, DATE, MetaData, JSON, String, or_, UniqueConstraint
from sqlalchemy import select, insert
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy_mixins.serialize import SerializeMixin
from datetime import datetime
from typing import List

# from psycopg2.errors import ProgrammingError
from sqlalchemy.exc import ProgrammingError
from gemini.models.db import session, engine


metadata_obj = MetaData(schema="gemini")


class _BaseModel(DeclarativeBase, SerializeMixin):
    __abstract__ = True
    metadata = metadata_obj

    def __repr__(self) -> str:
        return str(self.to_dict())


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
        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        # Remove values that are not columns in the table
        columns = cls.__table__.columns.keys()
        kwargs = {key: value for key, value in kwargs.items() if key in columns}

        return kwargs

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new instance of the class and add it to the database.
        """
        try:
            kwargs = cls.validate_fields(**kwargs)
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance if instance else None
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get_all(cls):
        """
        Get all instances of the class from the database.
        """
        try:
            query = select(cls)
            result = session.execute(query).scalars().all()
            return result if result else []
        except Exception as e:
            session.rollback()
            raise e
        
    @classmethod
    def get_by_id(cls, id):
        """
        Get an instance of the class by ID.
        """
        try:
            query = select(cls).where(cls.id == id)
            result = session.execute(query).scalar_one_or_none()
            return result
        except Exception as e:
            session.rollback()
            raise e
        
    @classmethod
    def get_by_parameters(cls, **kwargs):
        """
        Get instances of the class from the database by multiple parameters.
        """
        try:
            query = select(cls)
            kwargs = cls.validate_fields(**kwargs)
            if kwargs == {}:
                return None
            for key, value in kwargs.items():
                attribute = getattr(cls, key)
                if isinstance(attribute.type, JSONB):
                    query = query.where(attribute.contains(value))
                elif isinstance(attribute.type, TIMESTAMP):
                    query = query.where(attribute >= value)
                elif isinstance(attribute.type, DATE):
                    query = query.where(attribute == value)
                elif isinstance(attribute.type, String):
                    query = query.where(attribute == value)
                else:
                    query = query.where(attribute == value)
            result = session.execute(query).scalars().first()
            return result
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Get an existing instance from the database or create a new one if it doesn't exist.
        """
        try:
            # Remove non-unique fields from the kwargs
            unique_fields = cls.unique_fields()
            kwargs = cls.validate_fields(**kwargs)
            unique_kwargs = {key: value for key, value in kwargs.items() if key in unique_fields}        
            # If Unique Kwarg is empty, return None
            if unique_kwargs == {}:
                return None
            instance = cls.get_by_parameters(**unique_kwargs)
            if instance:
                return instance
            else:
                instance = cls(**kwargs)
                session.add(instance)
                session.commit()
                return instance
        except Exception as e:
            session.rollback()
            raise e


    @classmethod
    def update(cls, instance, **kwargs):
        """
        Update an instance of the class in the database.
        """
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
            return instance
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def update_or_get(cls, instance, **kwargs):
        """
        Update an existing instance from the database or create a new one if it doesn't exist.
        """
        try:
            instance = cls.update(instance, **kwargs)
            return instance
        except Exception as e:
            instance = cls.get_or_create(**kwargs)
            return instance

    @classmethod
    def search(cls, **kwargs):
        """
        Search for instances of the class in the database by multiple parameters.
        """
        try:
            query = select(cls)
            conditions = []
            kwargs = cls.validate_fields(**kwargs)
            for key, value in kwargs.items():
                attribute = getattr(cls, key)
                if isinstance(attribute.type, JSONB):
                    conditions.append(attribute.contains(value))
                elif isinstance(attribute.type, TIMESTAMP):
                    conditions.append(attribute >= value)
                elif isinstance(attribute.type, DATE):
                    conditions.append(attribute == value)
                elif isinstance(attribute.type, String):
                    conditions.append(attribute == value)
                else:
                    conditions.append(attribute == value)
            query = query.where(*conditions)
            result = session.execute(query).scalars().all()
            return result
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def stream(cls, **kwargs):
        """
        Stream data from the database by multiple parameters.
        """
        try:
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
                elif isinstance(attribute.type, String):
                    query = query.where(attribute == value)
                else:
                    query = query.where(attribute == value)
            query = query.execution_options(yield_per=1000)
            for partition in session.execute(query).scalars().partitions():
                for instance in partition:
                    yield instance 
        except ProgrammingError as e:
            session.rollback()
            pass
        except Exception as e:
            session.rollback()
            raise e
        
    @classmethod
    def stream_raw(cls, **kwargs):
        """
        Stream data using SQLAlchemy Core.
        """
        try:
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
                elif isinstance(attribute.type, String):
                    query = query.where(attribute == value)
                else:
                    query = query.where(attribute == value)
                query = query.execution_options(yield_per=1000)
            with engine.connect() as conn:
                result = conn.execute(query).scalars().partitions()
                for partition in result:
                    for instance in partition:
                        yield instance
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def update_or_create(cls, constraint: str, **kwargs):
        """
        Update an existing instance from the database or create a new one if it doesn't exist.
        """
        try:
            kwargs = cls.validate_fields(**kwargs)
            stmt = pg_insert(cls).values(**kwargs)
            do_update_stmt = stmt.on_conflict_do_update(
                constraint=constraint, set_=kwargs
            )
            session.execute(do_update_stmt)
            session.commit()
            instance = cls.get_by_parameters(**kwargs)
            return instance
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def delete(cls, instance) -> bool:
        """
        Delete an instance of the class from the database.
        """
        try:
            session.delete(instance)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

    @classmethod
    def save(self):
        """
        Save an instance of the class to the database.
        """
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def model_lookup_by_table_name(cls, table_name: str):
        """
        Get the model by table name
        """
        try:
            schema = cls.metadata.schema
            return cls.metadata.tables[f"{schema}.{table_name}"]
        except Exception as e:
            session.rollback()
            raise e
        
    @classmethod
    def insert_bulk(cls, constraint: str, data: List[dict]):
        try:
            table = cls.__table__
            stmt = pg_insert(table).on_conflict_do_nothing(constraint=constraint).returning(table.c.id)
            inserted_records = session.execute(stmt, data, execution_options={"populate_existing": True})
            inserted_ids = [record.id for record in inserted_records]
            session.commit()
            return inserted_ids
        except Exception as e:
            session.rollback()
            raise e


    @classmethod
    def upsert_bulk(cls, constraint: str, upsert_on: str, data: List[dict]):
        try:
            table = cls.__table__
            stmt = pg_insert(table)
            stmt = stmt.on_conflict_do_update(
                constraint=constraint, set_={upsert_on: stmt.excluded[upsert_on]}
            ).returning(table.c.id)
            inserted_records = session.execute(stmt, data, execution_options={"populate_existing": True})
            inserted_ids = [record.id for record in inserted_records]
            session.commit()
            return inserted_ids
        except Exception as e:
            session.rollback()
            raise e


class BaseModel(_BaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
   
