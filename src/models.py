from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

class Profiles(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    hair_color = Column(String)
    bust = Column(Integer)
    waist = Column(Integer)
    hips = Column(Integer)
