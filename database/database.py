from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from model.model import Base
import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.join(os.path.dirname(sys.executable), 'data')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(BASE_DIR, exist_ok=True)

DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR, "gestao_de_estoque.db")}'


engine = create_engine(DATABASE_URL, echo=True)

# if not os.path.exists('gestao_de_estoque.db'):
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

def get_session():
    Session = session
    try:
        yield Session()
    finally:
        Session.close_all()
        

