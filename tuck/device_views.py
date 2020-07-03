from tuck.device_models import DeviceClass, Device
from flask.views import MethodView
from flask import request
from flask import make_response, jsonify

from sqlalchemy.exc import IntegrityError

import json


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

    def post(self):
        """ Create a new DeviceClass """
        try:
            data = json.loads(request.data)
        except Exception:
            rv = {"message": "Error with message body"}
            print("there was an error")
            return make_response(jsonify(rv)), 400

        # check to make sure all the required data is here
        fields = data.keys()

        rv = DeviceClass.checkFields(fields)
        if rv:
            return make_response(jsonify(rv)), 400

        rv = DeviceClass.checkUnknownFields(fields)
        if rv:
            return make_response(jsonify(rv)), 400

        # actually create the device class
        try:
            deviceclass = DeviceClass(**data)
            deviceclass.save("charlesr")
            return make_response(deviceclass.serialize()), 200
        except IntegrityError:
            rv = {"message": "Duplicate Device Class"}
            return make_response(jsonify(rv)), 400
        except Exception:
            rv = {"message": "Generic Error"}
            return make_response(jsonify(rv)), 400

    def patch(self, id):
        deviceClass = DeviceClass.query.filter(DeviceClass.id == id).first()
        if deviceClass is None:
            response = {"message": "object not found"}
            return make_response(jsonify(response)), 404
        else:
            try:
                data = json.loads(request.data)
            except Exception:
                rv = {"message": "Error with message body"}
                print("there was an error")
                return make_response(jsonify(rv)), 400

            fields = data.keys()
            rv = DeviceClass.checkFields(fields)
            if rv:
                return make_response(jsonify(rv)), 400

            rv = DeviceClass.checkUnknownFields(fields)
            if rv:
                return make_response(jsonify(rv)), 400

            deviceClass.update(data)

            try:
                deviceClass.save("charlesr")
                return make_response(jsonify(deviceClass.serialize()))
            except Exception as e:
                rv = {"message": f"Generic Error: {e}"}
                return make_response(jsonify(rv)), 400

    def delete(self, id):
        deviceClass = DeviceClass.query.filter(DeviceClass.id == id).first()
        if deviceClass is None:
            response = {"message": "object not found"}
            return make_response(jsonify(response)), 404
        else:
            deviceClass.delete()
            return make_response(), 202


class DeviceView(MethodView):
    def get(self, mac):
        if mac is None:
            rv = []
            for device in Device.query.all():
                rv.append(device.serialize())
            return make_response(jsonify(rv)), 200

        else:
            device = Device.query.filter(Device.mac == mac).first()
            if device is None:
                response = {"message": "object not found"}
                return make_response(jsonify(response)), 404
            else:
                return make_response(jsonify(device.serialize())), 200

    def post(self):
        print("Here")
        try:
            data = json.loads(request.data)
        except Exception:
            rv = {"message": "Error with message body"}
            print("there was an error")
            return make_response(jsonify(rv)), 400

        # check to make sure all the required data is here
        fields = data.keys()

        rv = Device.checkFields(fields)
        if rv:
            return make_response(jsonify(rv)), 400

        rv = Device.checkUnknownFields(fields)
        if rv:
            return make_response(jsonify(rv)), 400

        # actually create the device class
        deviceClass = DeviceClass.query.filter(
            DeviceClass.id == data["device_class_id"]
        ).first()
        if deviceClass is None:
            return make_response(jsonify({"message": "Invalid DeviceClass id"})), 400
        del data["device_class_id"]
        data["device_class"] = deviceClass
        device = Device(**data)
        print(device)
        try:
            device.save("charlesr")
            return make_response(device.serialize()), 200
        except IntegrityError:
            rv = {"message": "Duplicate Device"}
            return make_response(jsonify(rv)), 400
        except Exception as e:
            rv = {"message": f"Generic Error {e}"}
            return make_response(jsonify(rv)), 400

    def patch(self, mac):
        device = Device.query.filter(Device.mac == mac).first()
        if device is None:
            response = {"message": "object not found"}
            return make_response(jsonify(response)), 404
        else:
            try:
                data = json.loads(request.data)
            except Exception:
                rv = {"message": "Error with message body"}
                print("there was an error")
                return make_response(jsonify(rv)), 400

            fields = data.keys()
            rv = Device.checkFields(fields)
            if rv:
                return make_response(jsonify(rv)), 400

            rv = Device.checkUnknownFields(fields)
            if rv:
                return make_response(jsonify(rv)), 400

            device.update(data)

            try:
                device.save("charlesr")
                return make_response(jsonify(device.serialize()))
            except Exception as e:
                rv = {"message": f"Generic Error: {e}"}
                return make_response(jsonify(rv)), 400

    def delete(self, mac):
        device = Device.query.filter(Device.mac == mac).first()
        if device is None:
            response = {"message": "object not found"}
            return make_response(jsonify(response)), 404
        else:
            device.delete()
            return make_response(), 202
