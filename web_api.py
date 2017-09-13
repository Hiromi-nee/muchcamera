from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask.ext.jsonpify import jsonify
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc
from fractions import Fraction
from recommender import Recommender
import os, uuid
from camera import Camera

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = "images/"

# EXPOSURE API
exposures = []
image_paths = []
cameras = []

# Fraction(new_exp_time).limit_denominator()


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


class AperturePriority(Resource):
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


class ExposureTimePriority(Resource):
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


class IsoPriority(Resource):
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


class ManualExposure(Resource):
    pass

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
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image_id', type=int, help="Photo id")
        args = parser.parse_args()
        detected_styles, cnn_class_probs = Recommender().rec_style(image_paths[args['image_id']])
        res = {
        "detected_styles": [{i[0] : i [1]}for i in detected_styles],
        "class_probabilities": [{i[0] : i [1]}for i in cnn_class_probs]
        }
        return jsonify(res)


class RecSettingsWOImage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('style', help="style")
        parser.add_argument('target_ev', help="target_ev")
        # camera args
        parser.add_argument('ff_fl', help="Full Frame Focal Length")
        parser.add_argument('orig_fl', help="Original Focal Length")
        parser.add_argument('model', type=int, help="camera model")
        parser.add_argument('sensor_size', help="sensor size")
        parser.add_argument('max_aperture', help="max_aperture")
        parser.add_argument('min_aperture', help="min_aperture")
        parser.add_argument('max_shutter_speed', help="max_shutter_speed")
        parser.add_argument('min_shutter_speed', help="min_shutter_speed")
        parser.add_argument('max_iso', type=int, help="max_iso")
        parser.add_argument('min_iso', type=int, help="min_iso")
        parser.add_argument('max_fl', type=int, help="max focal length")
        parser.add_argument('min_fl', type=int, help="minimum focal length")
        parser.add_argument('multiplier', help="crop factor")
        # end camera args
        args = parser.parse_args()
        #ff_fl="50", orig_fl = "50", model="Nikon D750", sensor_size="FF", 
        #max_aperture = 20, min_aperture = 2.8, max_shutter_speed = 30, min_shutter_speed = 1/4000,
        #max_iso = 6400, min_iso = 100, max_fl = 70, min_fl = 28, multiplier=1
        camera = Camera(
            args['ff_fl'], args['orig_fl'],
            args['model'], args['sensor_size'],
            float(args['max_aperture']), float(args['min_aperture']),
            float(args['max_shutter_speed']), eval(args['min_shutter_speed']),
            args['max_iso'], args['min_iso'],
            args['max_fl'], args['min_fl'],
            float(args['multiplier'])
        )
        rec_res = Recommender().rec_settings_wo_image(args['style'], camera, args['target_ev'])
        res = {
        "recommended_settings": [{ "ExposureTime": str(Fraction(float(i[0])).limit_denominator()), 
                                "Aperture": i[1], 
                                "FocalLength": i[2], 
                                "ISO": i[3] } for i in rec_res]
        }

        return jsonify(res)


class RecSettingsWImage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('style', help="style")
        parser.add_argument('image_id', type=int, help="image_id")
        # camera args
        parser.add_argument('ff_fl', help="Full Frame Focal Length")
        parser.add_argument('orig_fl', help="Original Focal Length")
        parser.add_argument('model', type=int, help="camera model")
        parser.add_argument('sensor_size', help="sensor size")
        parser.add_argument('max_aperture', help="max_aperture")
        parser.add_argument('min_aperture', help="min_aperture")
        parser.add_argument('max_shutter_speed', help="max_shutter_speed")
        parser.add_argument('min_shutter_speed', help="min_shutter_speed")
        parser.add_argument('max_iso', type=int, help="max_iso")
        parser.add_argument('min_iso', type=int, help="min_iso")
        parser.add_argument('max_fl', type=int, help="max focal length")
        parser.add_argument('min_fl', type=int, help="minimum focal length")
        parser.add_argument('multiplier', help="crop factor")
        # end camera args
        args = parser.parse_args()
        camera = Camera(
            args['ff_fl'], args['orig_fl'],
            args['model'], args['sensor_size'],
            float(args['max_aperture']), float(args['min_aperture']),
            float(args['max_shutter_speed']), eval(args['min_shutter_speed']),
            args['max_iso'], args['min_iso'],
            args['max_fl'], args['min_fl'],
            float(args['multiplier'])
        )

        rec_res = Recommender().rec_settings_w_image(args['style'], camera, image_paths[args['image_id']])
        res = {
        "recommended_settings": [
            {
            "ExposureTime": str(Fraction(float(i[0])).limit_denominator()),
            "Aperture": i[1],
            "FocalLength": i[2],
            "ISO": i[3]
            } for i in rec_res]
        }

        return jsonify(res)

# END RECOMMENDER

# CAMERA


class CameraConfig(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ff_fl', help="Full Frame Focal Length")
        parser.add_argument('orig_fl', help="Original Focal Length")
        parser.add_argument('model', type=int, help="camera model")
        parser.add_argument('sensor_size', help="sensor size")
        parser.add_argument('max_aperture', help="max_aperture")
        parser.add_argument('min_aperture', help="min_aperture")
        parser.add_argument('max_shutter_speed', help="max_shutter_speed")
        parser.add_argument('min_shutter_speed', help="min_shutter_speed")
        parser.add_argument('max_iso', type=int, help="max_iso")
        parser.add_argument('min_iso', type=int, help="min_iso")
        parser.add_argument('max_fl', type=int, help="max focal length")
        parser.add_argument('min_fl', type=int, help="minimum focal length")
        parser.add_argument('multiplier', help="crop factor")
        args = parser.parse_args()
        camera = Camera(
            args['ff_fl'], args['orig_fl'],
            args['model'], args['sensor_size'],
            float(args['max_aperture']), float(args['min_aperture']),
            float(args['max_shutter_speed']), eval(args['min_shutter_speed']),
            args['max_iso'], args['min_iso'],
            args['max_fl'], args['min_fl'],
            float(args['multiplier'])
        )

        cameras.append(camera)

        return jsonify({"camera_id": (len(cameras) - 1)})

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('camera_id', type=int, help="camera_id")
        args = parser.parse_args()
        camera = cameras[args['camera_id']]
        res = {}

        return jsonify(res)

class ListCamera(Resource):
    def get(self):
        pass

# END CAMERA

# EXPOSURE ROUTES

api.add_resource(Exposure, '/exposure')
api.add_resource(ExposureValue, '/ev')
api.add_resource(ExposureValueById, '/ev_by_id')
api.add_resource(AperturePriority, '/aperture')
api.add_resource(ExposureTimePriority, '/exposure_time')
api.add_resource(IsoPriority, '/iso')
api.add_resource(ManualExposure, '/manual_exposure')

# DOF ROUTES
api.add_resource(CalcDOF, '/calc_dof')
api.add_resource(CalcCOC, '/calc_coc')

# EXIF ROUTES

api.add_resource(Exif, '/get_exif')

# IMAGE UPLOAD ROUTES

api.add_resource(UploadImage, '/upload_image')

# RECOMMENDER ROUTES

api.add_resource(RecStyle, '/recommend_style')
api.add_resource(RecSettingsWOImage, '/recommend_settings_wo_image')
api.add_resource(RecSettingsWImage, '/recommend_settings_w_image')

# CAMERA ROUTE

api.add_resource(CameraConfig, '/camera_config')
api.add_resource(ListCamera, '/list_camera')

if __name__ == '__main__':
     app.run(port='5002')