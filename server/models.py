from server import db
import enum

db.Model.metadata.reflect(db.engine)


class User(db.Model):
    __table__ = db.Model.metadata.tables['user']

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Project(db.Model):
    __table__ = db.Model.metadata.tables['project']

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Application(db.Model):
    __table__ = db.Model.metadata.tables['application']

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

