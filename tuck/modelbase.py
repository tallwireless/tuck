from tuck.db import db_session


class ModelBase(object):
    def __init__(self):
        pass

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
