from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

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
	photo = Column(String)


engine = create_engine('sqlite:///project.db')


Base.metadata.create_all(engine)


