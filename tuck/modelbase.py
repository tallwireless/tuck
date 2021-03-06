from tuck.db import db_session
from sqlalchemy import DateTime, String, Column

from flask import g

import arrow


class ModelBase(object):
    createdBy = Column(String(50), nullable=False)
    created = Column(DateTime, nullable=False)
    updatedBy = Column(String(50), nullable=False)
    updated = Column(DateTime, nullable=False)

    def __init__(self):
        pass

    def save(self, who=None):
        print(type(self))
        if self._sa_instance_state.modified:
            if who is None:
                who = g.user.username
            # The row is brand new, need to say who created it
            if self.createdBy is None:
                self.createdBy = who
                self.created = arrow.utcnow().datetime

            # Update who updated it and when
            self.updatedBy = who
            self.updated = arrow.utcnow().datetime

            db_session.add(self)
            db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "createdBy": self.createdBy,
            "created": arrow.get(self.created).strftime("%Y/%d/%m %H:%M UTC"),
            "updatedBy": self.updatedBy,
            "updated": arrow.get(self.updated).strftime("%Y/%d/%m %H:%M UTC"),
        }

    def checkFields(self, fields):
        for req in self.required:
            if req not in fields:
                return {"message": f"Missing required field: {req}"}

    def checkUnknownFields(self, fields):
        all_fields = self.required + self.optional
        for req in fields:
            if req not in all_fields:
                return {"message": f"Unknown Field: {req}"}

        return False

    def update(self, data):
        # assume the keys are sanitized
        for (key, value) in data.items():
            self.__setattr__(key, value)
