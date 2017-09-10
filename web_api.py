from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc

app = Flask(__name__)
api = Api(app)


# EXPOSURE API
exposures = []

class Exposure(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp = {"ExposureTime": exposures[exp_id].exp_time,
            "ISO": exposures[exp_id].iso,
            "Aperture": exposures[exp_id].f_no}
        except Exception as e:
            exp = {"Error": "Exposure not found."}
            exp = e

        return jsonify(exp)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ExposureTime', help="Exposure Time/Shutterspeed")
        parser.add_argument('ISO', help="ISO")
        parser.add_argument('Aperture', help="Aperture of lens")
        args = parser.parse_args()
        exposure_obj = ExpCalc(eval(args['ExposureTime']), int(args['ISO']), float(args['Aperture']))
        exposures.append(exposure_obj)
        return jsonify( {"exposure_id": str(len(exposures)-1)} )

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exposures[exp_id] = None
        except Exception as e:
            exp = {"Error": "Exposure not found."}
            exp = e

        return jsonify(exp)



class ExposureValue(Resource):
    def get(self):
       parser = reqparse.RequestParser()
       parser.add_argument('ExposureTime', help="Exposure Time/Shutterspeed")
       parser.add_argument('ISO', help="ISO")
       parser.add_argument('Aperture', help="Aperture of lens")
       args = parser.parse_args()
       exposure_obj = ExpCalc(eval(args['ExposureTime']), int(args['ISO']), float(args['Aperture']))
       evs = exposure_obj.get_exposure_val()

       return jsonify({"EV":evs})


class Aperture(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp = {"Aperture": exposures[exp_id].f_no}
        except Exception as e:
            exp = {"Error": "Exposure not found."}

        return jsonify(exp)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            parser.add_argument('Aperture', help="Aperture Value.")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp_obj = exposures[exp_id]
            f_no = float(args['Aperture'])
            ev = exp_obj.set_f_no(f_no)
            res = {
            "EV": ev,
            "ExposureTime": exp_obj.exp_time,
            "ISO": exp_obj.iso,
            "Aperture": exp_obj.f_no
            }

        except Exception:
            res = {"Error": "Exposure not found."}

        return jsonify(res)


class ExposureTime(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp = {"ExposureTime": exposures[exp_id].exp_time}
        except Exception as e:
            exp = {"Error": "Exposure not found."}

        return jsonify(exp)

    def post(self):
        pass


class Iso(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp = {"ISO": exposures[exp_id].iso}
        except Exception as e:
            exp = {"Error": "Exposure not found."}

        return jsonify(exp)

    def post(self):
        pass

# END EXPOSURE API



api.add_resource(Exposure, '/exposure')
api.add_resource(ExposureValue, '/ev')
api.add_resource(Aperture, '/aperture')
api.add_resource(ExposureTime, '/exposure_time')
api.add_resource(Iso, '/iso')

if __name__ == '__main__':
     app.run(port='5002')