from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from model.model import Base
import os

DATABASE_URL = 'sqlite:///gestao_de_estoque.db'


engine = create_engine(DATABASE_URL, echo=True)

if not os.path.exists('gestao_de_estoque.db'):
    Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

def get_session():
    Session = session
    try:
        yield Session()
    finally:
        Session.close_all()
        

