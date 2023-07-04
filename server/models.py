from server import db


db.Model.metadata.reflect(db.engine)


class RootModel(db.Model):
    __abstract__ = True

    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(RootModel):
    __table__ = db.Model.metadata.tables['user']


class Project(RootModel):
    __table__ = db.Model.metadata.tables['project']


class Application(RootModel):
    __table__ = db.Model.metadata.tables['application']
