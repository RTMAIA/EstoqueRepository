from sqlalchemy import select

class BaseRepository():
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def criar(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def buscar_todos(self):
        obj = self.session.scalars(select(self.model)).all()
        return obj
    
    def buscar_por_id(self, id):
        obj = self.session.scalars(select(self.model).where(self.model.id == id)).all()
        return obj
    
    def update(self, id, **kwargs):
        obj = self.buscar_por_id(id)
        self.session.add(obj)
        self.commit()
        return obj

    def delete(self, id):
        obj = self.buscar_por_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
      