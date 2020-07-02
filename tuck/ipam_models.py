from sqlalchemy import Column, Integer, String

from tuck.db import Base
from tuck.modelbase import ModelBase


class VLAN(Base, ModelBase):
    __tablename__ = "vlan"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))

    def __init__(self, vlan_id, name=None):
        self.id = vlan_id
        self.name = name

    def __repr__(self):
        return f"<VLAN {self.id}:{self.name}>"
