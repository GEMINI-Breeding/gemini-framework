from gemini.models.base_model import _BaseModel
from gemini.models.db import session
from sqlalchemy.sql import text

class ViewBaseModel(_BaseModel):
  
  __abstract__ = True

  @classmethod
  def refresh(cls):
    """
    Refreshed the Materialized View.
    """
    try:
      query = f'REFRESH MATERIALIZED VIEW {cls.__table__.name}'
      query = text(query)
      session.execute(query)
      session.commit()
    except Exception as e:
      session.rollback()
      raise e
    
  @classmethod
  def get_all(cls):
    cls.refresh()
    return super().get_all()
  
  @classmethod
  def search(cls, **kwargs):
    cls.refresh()
    return super().search(**kwargs)
  
  @classmethod
  def stream(cls, **kwargs):
    cls.refresh()
    return super().stream(**kwargs)
  
  @classmethod
  def paginate(cls, order_by: str, page_number: int, page_limit: int, **kwargs):
    return super().paginate(order_by, page_number, page_limit, **kwargs)
  
  @classmethod
  def get_by_parameters(cls, **kwargs):
    cls.refresh()
    return super().get_by_parameters(**kwargs)
  
