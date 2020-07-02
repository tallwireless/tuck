from tuck.device_models import DeviceClass, Device
from flask.views import MethodView

from flask import make_response, jsonify


class DeviceClassView(MethodView):
    def get(self, id):
        if id is None:
            rv = []
            for deviceClass in DeviceClass.query.all():
                rv.append(deviceClass.serialize())
            return make_response(jsonify(rv)), 200

        else:
            deviceClass = DeviceClass.query.filter(DeviceClass.id == id).first()
            if deviceClass is None:
                response = {"message": "object not found"}
                return make_response(jsonify(response)), 404
            else:
                return make_response(jsonify(deviceClass.serialize())), 200


class DeviceView(MethodView):
    def get(self, id):
        if id is None:
            rv = []
            for device in Device.query.all():
                rv.append(device.serialize())
            return make_response(jsonify(rv)), 200

        else:
            device = Device.query.filter(Device.id == id).first()
            if device is None:
                response = {"message": "object not found"}
                return make_response(jsonify(response)), 404
            else:
                return make_response(jsonify(device.serialize())), 200
