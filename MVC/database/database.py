from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from MVC.model.model import Base

DATABASE_URL = 'sqlite:///gestao_de_estoque.db'


engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    session = sessionmaker(bind=engine)
    try:
        yield session
    finally:
        session.close()

Base.metadata.create_all(engine)
