from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, User , Post 

engine = create_engine('sqlite:///crudlab.db')
Base.metadata.create_all(engine)
#Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine,autoflush=False)
session = DBSession()

session.query(User).delete()
session.query(Post).delete()
session.commit()

