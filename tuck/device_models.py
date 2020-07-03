from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from tuck.db import Base
from tuck.modelbase import ModelBase


class DeviceClass(Base, ModelBase):
    __tablename__ = "device_class"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    vlan_id = Column(Integer, nullable=False)
    desc = Column(String(255))
    devices = relationship("Device", back_populates="device_class")

    required = ["vlan_id", "name"]
    optional = ["desc"]

    def __init__(self, name, vlan_id, desc=None):
        self.name = name
        self.vlan_id = vlan_id
        self.desc = desc

    def __repr__(self):
        return f"<DeviceClass {self.name}>"

    def checkFields(fields):
        return ModelBase.checkFields(DeviceClass, fields)

    def checkUnknownFields(fields):
        return ModelBase.checkUnknownFields(DeviceClass, fields)

    def serialize(self):
        rv = super(DeviceClass, self).serialize()
        rv["name"] = self.name
        rv["desc"] = self.desc
        rv["vlan_id"] = self.vlan_id

        return rv

    def update(self, data):
        # assume the keys are sanitized
        for (key, value) in data.items():
            self.__setattr__(key, value)


class Device(Base, ModelBase):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True)
    mac = Column(String(18), nullable=False)
    desc = Column(String(255), nullable=False)
    device_class_id = Column(Integer, ForeignKey("device_class.id"), nullable=False)
    device_class = relationship("DeviceClass", back_populates="devices")

    required = ["mac", "desc", "device_class_id"]
    optional = []

    def __init__(self, mac, desc, device_class):
        self.mac = mac
        self.desc = desc
        self.device_class = device_class

    def __repr__(self):
        return f"<Device {self.mac}>"

    def checkFields(fields):
        return ModelBase.checkFields(DeviceClass, fields)

    def serialize(self):
        rv = super(Device, self).serialize()
        rv["desc"] = self.desc
        rv["mac"] = self.mac
        rv["device_class"] = self.device_class_id

        return rv
