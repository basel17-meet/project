from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String , File
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)


class Post(Base):
	__tablename__ = 'post'
	__table_args__ = {'extend_existing':True}
	id = Column(Integer, primary_key=True)
	userid = Column(Integer , ForeignKey("user.id"))
	user = relationship ("User")
	title = Column(String)
	descreption = Column(String)
	file = Column(File)


