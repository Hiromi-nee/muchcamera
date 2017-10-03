from camera import Camera
from pipeline import Pipeline
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc
import PIL.Image
import PIL.ExifTags
import sqlite3
import helper.exp_helper as exp_helper


class Recommender:
    exif_db_path = "/media/Kyou/FYP_DATA/flickr_dl/scripts/muchcamera/exif_db/"
    styles_db_path = {
                    "SM":"exif_0.db",
                    "SD":"exif_1.db",
                    "DT":"exif_2.db",
                    "HK":"exif_3.db",
                    "MB":"exif_4.db",
                    "LK":"exif_7.db"
                    }
 

    def extract_exif(self, image_file_path):
        #["1/250",5.6,200,"800","0"]
        exif = ["",0,0,"",""]
        img = PIL.Image.open(image_file_path)
        try:
            exif_dict = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
        except Exception:
            return []
        try:
            exif[0] = str(exif_dict['ExposureTime'][0]) + "/" + str(exif_dict['ExposureTime'][1])
            exif[1] = exif_dict['FNumber'][0]/exif_dict['FNumber'][1]
            exif[2] = int(exif_dict['FocalLength'][0]/exif_dict['FocalLength'][1])
            exif[3] = str(exif_dict['ISOSpeedRatings'])
            exif[4] = str(exif_dict['ExposureBiasValue'][0]/exif_dict['ExposureBiasValue'][1])
        except Exception:
            return [] # no exif
        return [exif]

    def rec_style(self, image_file_path):
        exif_data = self.extract_exif(image_file_path)
        a_styles, class_probs = Pipeline().execute(image_file_path, exif_data)
        return a_styles, class_probs

    def rec_settings_wo_image(self, style, camera, target_ev):
            #no exif, suggest full settings for given style
            #search style db, find something with similar EV
            #reject things like bright sun -> want to do long exposure

            # i want to shoot [insert style]
            # choose EV (estimate)
            # suggest settings
            # take pict
            # detect style
            # give feedback
        if style in self.styles_db_path:
            conn = sqlite3.connect(self.exif_db_path + self.styles_db_path[style])
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT ExposureTime,FNumber,FocalLength,ISO FROM t WHERE EV=:ev",{"ev":str(int(target_ev))})
            results = cur.fetchall()
            if len(results) == 0:
                return []
            else:
                final_results = self.filter_for_camera_limits(camera, results)
                return final_results
        else:
            return []
        

    def rec_settings_w_image(self, style, camera, image_file_path):
        exif_data = self.extract_exif(image_file_path)[0]
        if len(exif_data) == 0:
            return []
        else:
            stmt_base = "SELECT DISTINCT ExposureTime,FNumber,FocalLength,ISO FROM t WHERE "
            expo = ExpCalc(eval(exif_data[0]),int(exif_data[3]),float(exif_data[1]))
            expc = expo.get_exposure_val()

            try:
                if style in self.styles_db_path:
                    conn = sqlite3.connect(self.exif_db_path + self.styles_db_path[style])
                    cur = conn.cursor()
                    if style == "SM":
                        cur.execute(stmt_base + "CAST(EV AS INTEGER) >= :evlow AND CAST(EV AS INTEGER) <= :evhigh", {"evlow":expc-2.5, "evhigh":expc+2.5})
                    elif style == "SD":
                        cur.execute(stmt_base + "CAST(FNumber AS INTEGER) <= :f_no", {"f_no":6.3})
                    elif style == "DT":
                        cur.execute(stmt_base + "CAST(EV AS INTEGER) >= :evlow AND CAST(EV AS INTEGER) <= :evhigh", {"evlow":expc-3, "evhigh":expc+3})
                    elif style == "HK":
                        cur.execute(stmt_base + "CAST(EV AS INTEGER) >= :evlow AND CAST(EV AS INTEGER) <= :evhigh", {"evlow":expc-2, "evhigh":expc+2.5})
                    elif style == "MB":
                        cur.execute(stmt_base + "CAST(ISO AS INTEGER)<=:iso AND CAST(EV AS INTEGER)<=:ev", {"iso":int(exif_data[3]),"ev":8})
                    elif style == "LK":
                        cur.execute(stmt_base + "CAST(EV AS INTEGER) >= :evlow AND CAST(EV AS INTEGER) <= :evhigh", {"evlow":expc-2.5, "evhigh":expc+2})
                    
                    results = cur.fetchall()
                    if len(results) == 0:
                        return []
                    else:
                        final_results = self.filter_for_camera_limits(camera, results)
                        print(final_results)
                        return final_results
            except Exception as e:
                print(e)
                return []
            #search style db
            #find most similar exposure setting
            #calc EV, make same EV
            #return settings


    def sanity_check_settings(self, style, settings):
        pass

    def filter_for_camera_limits(self, camera, settings):
        #check if settings are within camera limits
        final_settings = []
        for setting in settings:
            #check exptime
            try:

                if float(setting[0]) > camera.max_shutter_speed or float(setting[0]) < camera.min_shutter_speed:
                    continue
                if float(setting[1]) > camera.max_aperture or float(setting[1]) < camera.min_aperture:
                    continue
                if float(setting[2]) > camera.max_fl or float(setting[2]) < camera.min_fl:
                    continue
                if int(setting[3]) > camera.max_iso or int(setting[3]) < camera.min_iso:
                    continue
            except Exception:
                continue
            final_settings.extend([setting])
        return final_settings

    def check_within_camera_limits(self, camera, settings):
        pass

    def recommend_filter(self, camera, settings, target_settings):
        # exp_time, iso, f_no
        target_exp = ExpCalc(eval(target_settings[0]),int(target_settings[1]),float(target_settings[2]))
        current_exp = ExpCalc(eval(settings[0]),int(settings[1]),float(settings[2]))
        # larger EV = brighter scene
        no_stop_diff = current_exp.get_exposure_val() - target_exp.get_exposure_val()
        # diff settings see which setting change
        flags = exp_helper.diff_exposures(current_exp, target_exp)
        if flags[0] != 0:
            # exposure changed
            # if fastest shutter speed but still overexposed -> ND Filter
            # if slower shutter speed but still under exposed -> suggest raising ISO
            if flags[0] == 1: # current slower shutter speed than target
                if no_stop_diff > 0: # current scene brighter than target scene
                    # raise ISO
                    return {"Action" : "Raise ISO", "Value (stops)" : no_stop_diff}
                else: # current scene darker than target scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff}
            else: # current faster shutter speed than target
                if no_stop_diff < 0: # current scene darker than target scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff} # rec ND Filter
                else: # current scene brighter than target scene
                    return {"Action" : "Raise ISO", "Value (stops)" : no_stop_diff}
        if flags[1] != 0:
            # aperture changed
            # if aperture change to smaller num but still under exposed, warn amount, suggest raising ISO
            # if larger num -> use ND Filter
            if flags[1] == 1: # current smaller aperture than target
                if no_stop_diff > 0: # current scene brighter than target scene
                    return {"Action" : "Raise ISO", "Value (stops)" : no_stop_diff}
                else: # target scene brighter than current scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff}
            else: # target smaller aperture than current
                if no_stop_diff < 0: # target scene brighter than current scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff}
                else: # current scene brighter than target scene
                    return {"Action" : "Raise ISO", "Value (stops)" : no_stop_diff}
        if flags[2] != 0: 
            # iso changed
            if flags[2] == 1: # target higher iso
                if no_stop_diff < 0: # target scene brighter than current scene
                    return {"Action" : "Decrease Shutter Speed or Aperture", "Value (stops)" : no_stop_diff}
                else: # current scene brighter than target scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff}
            else: # target lower iso
                if no_stop_diff > 0: # current scene brighter than target scene
                    return {"Action" : "ND Filter", "Value (stops)" : no_stop_diff}
                else: # target scene brighter than current scene
                    return {"Action" : "Decrease Shutter Speed or Aperture", "Value (stops)" : no_stop_diff}
        # set to min or max of the other settings before checking if need to apply filter
        # if need to apply filter, suggest how many stops


if __name__ == '__main__':
    image_file_path = "/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3075.jpg"
    #exif = Recommender().extract_exif(image_file_path)
    #print(exif)

    a, b = Recommender().rec_style(image_file_path)
    print(a)
    print(b)
    print("Rec settings without image.")
    camera = Camera()
    res = Recommender().rec_settings_wo_image("SM", camera, "10")
    print(res)

    print("Rec settings with image.")
    res2 = Recommender().rec_settings_w_image("SM", camera, image_file_path)
    print(res2)