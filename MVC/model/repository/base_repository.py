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
        obj = self.session.execute(select(self.model)).scalars().all()
        return obj
    
    def buscar_por_id(self, id):
        obj = self.session.execute(select(self.model).where(self.model.id == id).scalar_one_or_none())
        return obj

    def delete(self, id):
        obj = self.buscar_por_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()


