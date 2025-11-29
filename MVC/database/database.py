from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from MVC.model.model import Base
import os

DATABASE_URL = 'sqlite:///gestao_de_estoque.db'


engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    session = sessionmaker(bind=engine)
    try:
        yield session
    finally:
        session.close()
if not os.path.exists('gestao_de_estoque.db'):
    Base.metadata.create_all(engine)

