from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask.ext.jsonpify import jsonify
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc
from fractions import Fraction
from recommender import Recommender
import os, uuid

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = "images/"

# EXPOSURE API
exposures = []
image_paths = []

#Fraction(new_exp_time).limit_denominator()

class Exposure(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp = {"ExposureTime": str(Fraction(exposures[exp_id].exp_time).limit_denominator()),
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

class ExposureValueById(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('exposure_id', type=int, help="exp_id")
        args = parser.parse_args()
        exp_id = args['exposure_id']
        args = parser.parse_args()
        evs = exposures[exp_id].get_exposure_val()

        return jsonify({"EV":round(evs,0)})


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
            "EV": round(ev,0),
            "ExposureTime": str(Fraction(exp_obj.exp_time).limit_denominator()),
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
            exp = {"ExposureTime": str(Fraction(exposures[exp_id].exp_time).limit_denominator())}
        except Exception as e:
            exp = {"Error": "Exposure not found."}

        return jsonify(exp)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            parser.add_argument('ExposureTime', help="Aperture Value.")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp_obj = exposures[exp_id]
            exp_time = float(args['ExposureTime'])
            ev = exp_obj.set_exp_time(exp_time)
            res = {
            "EV": round(ev,0),
            "ExposureTime": str(Fraction(exp_obj.exp_time).limit_denominator()),
            "ISO": exp_obj.iso,
            "Aperture": exp_obj.f_no
            }

        except Exception:
            res = {"Error": "Exposure not found."}

        return jsonify(res)


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
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('exposure_id', type=int, help="exp_id")
            parser.add_argument('ISO', help="Aperture Value.")
            parser.add_argument('change', help="Setting to adjust. et or f_no")
            args = parser.parse_args()
            exp_id = args['exposure_id']
            exp_obj = exposures[exp_id]
            iso = int(args['ISO'])
            if args['change'] == "f_no":
                ev = exp_obj.set_iso_fixed_et(iso)
            elif args['change'] == "et":
                ev = exp_obj.set_iso_fixed_fno(iso)
            res = {
            "EV": round(ev,0),
            "ExposureTime": str(Fraction(exp_obj.exp_time).limit_denominator()),
            "ISO": exp_obj.iso,
            "Aperture": exp_obj.f_no
            }

        except Exception as e:
            res = {"Error": "Exposure not found."}
            print(e)

        return jsonify(res)

# END EXPOSURE API


# DOF API

class CalcDOF(Resource):
    def get(self):
        # f_no, fl, coc, f_distance
        parser = reqparse.RequestParser()
        parser.add_argument('Aperture', help="Aperture")
        parser.add_argument('FocalLength', help="FocalLength Value.")
        parser.add_argument('coc', help="coc")
        parser.add_argument('SubjDist', help="Focus distance")
        args = parser.parse_args()
        hyperfocal_dist, near_dist_sharp, far_dist_sharp, in_front_subj, behind_subj = DofCalc.calc_dof( 
            float(args['Aperture']),
            float(args['FocalLength']),
            float(args['coc']),
            float(args['SubjDist'])
            )
        res = {
            "hyperfocal_distance": hyperfocal_dist/1000,
            "near_dist_sharp": near_dist_sharp/1000,
            "far_dist_sharp": far_dist_sharp/1000,
            "in_front_subj": in_front_subj,
            "behind_subj": behind_subj
        }
        return jsonify(res)

class CalcCOC(Resource):
    def get(self):
        #ff_fl, actual_fl=0, coc_35=0.030
        parser = reqparse.RequestParser()
        parser.add_argument('FFFocalLength', help="35mm equiv. FL")
        parser.add_argument('FocalLength', help="FocalLength Value.")
        args = parser.parse_args()
        coc = DofCalc.calc_coc(float(args['FFFocalLength']), float(args['FocalLength']))

        return jsonify({"COC": coc})
# END DOF API

# IMAGE UPLOAD

class UploadImage(Resource):
    def post(self):
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(UPLOAD_FOLDER, f_name))
        image_paths.append(f_name)

        return jsonify({'image_id':(len(image_paths)-1)})

# END IMAGE UPLOAD

# EXIF

class Exif(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image_id', type=int, help="Photo id")
        args = parser.parse_args()
        exif = Recommender().extract_exif(UPLOAD_FOLDER+image_paths[args['image_id']])[0]
        # et, fno, fl ,iso, ev bias
        img_exif = {"ExposureTime": exif[0],
        "Aperture": exif[1],
        "FocalLength":exif[2],
        "ISO":exif[3],
        "ExposureCompensation": exif[4]
        }

        return jsonify(img_exif)

# END EXIF

# RECOMMENDER

class RecStyle(Resource):
    pass

class RecSettingsWOImage(Resource):
    pass


class RecSettingsWImage(Resource):
    pass


# END RECOMMENDER

# CAMERA

# END CAMERA

# EXPOSURE ROUTES
api.add_resource(Exposure, '/exposure')
api.add_resource(ExposureValue, '/ev')
api.add_resource(ExposureValueById, '/ev_by_id')
api.add_resource(Aperture, '/aperture')
api.add_resource(ExposureTime, '/exposure_time')
api.add_resource(Iso, '/iso')

# DOF ROUTES
api.add_resource(CalcDOF, '/calc_dof')
api.add_resource(CalcCOC, '/calc_coc')

#EXIF ROUTES

api.add_resource(Exif, '/get_exif')

# IMAGE UPLOAD ROUTES

api.add_resource(UploadImage, '/upload_image')

# RECOMMENDER ROUTES

api.add_resource(RecStyle, '/recommend_style')
api.add_resource(RecSettingsWOImage, '/recommend_settings_wo_image')
api.add_resource(RecSettingsWImage, '/recommend_settings_w_image')

if __name__ == '__main__':
     app.run(port='5002')