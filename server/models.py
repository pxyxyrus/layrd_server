from server import db
from datetime import datetime


db.Model.metadata.reflect(db.engine)


class RootModel(db.Model):
    __abstract__ = True

    def to_dict(self):
       return {c.name: self.datetime_to_unix(getattr(self, c.name)) for c in self.__table__.columns}

    @staticmethod
    def datetime_to_unix(value):
        # check if value is in datetime type, if not just return its value
        if isinstance(value, datetime):
            return int(value.timestamp())
        else:
            return value
        
class User(RootModel):
    __table__ = db.Model.metadata.tables['user']


class Project(RootModel):
    __table__ = db.Model.metadata.tables['project']


class Application(RootModel):
    __table__ = db.Model.metadata.tables['application']
