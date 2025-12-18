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
    
    def gerar_sku(self, **kwargs) -> str:
            variacao = 'N01'
            # for i in kwargs:
                # if not len(kwargs[i]) >= 3:
                    # raise ValueError(f'O campo "{i}" Deve maior ou igual a 3.')
                
            sku = (kwargs['produto'][0:3] + '-' + kwargs['marca'][0:3] + '-' + kwargs['categoria'][0:3] + '-' + variacao).upper()
            obj = self.session.scalar(select(self.model).where(self.model.sku == sku))
            if not obj:
                return sku
            
            sku = f'{sku[13:15] + 1}'.zfill(2)
            print(sku)
            
            