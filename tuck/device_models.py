from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from tuck.db import Base
from tuck.modelbase import ModelBase


class DeviceClass(Base, ModelBase):
    __tablename__ = "device_class"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    vlan_id = Column(Integer, nullable=False)
    desc = Column(String(255))
    devices = relationship("Device", back_populates="device_class")

    def __init__(self, name, vlan_id, desc=None):
        self.name = name
        self.vlan_id = vlan_id
        self.desc = desc

    def __repr__(self):
        return f"<DeviceClass {self.name}>"


class Device(Base, ModelBase):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True)
    mac = Column(String(18), nullable=False)
    desc = Column(String(255), nullable=False)
    device_class_id = Column(Integer, ForeignKey("device_class.id"), nullable=False)
    device_class = relationship("DeviceClass", back_populates="devices")

    def __init__(self, mac, desc, device_class):
        self.mac = mac
        self.desc = desc
        self.device_class = device_class

    def __repr__(self):
        return f"<Device {self.mac}>"
