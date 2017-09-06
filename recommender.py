from camera import Camera
from pipeline import Pipeline
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc
import PIL.Image
import PIL.ExifTags
import sqlite3

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
        exif_dict = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        try:
            exif[0] = str(exif_dict['ExposureTime'][0]) + "/" + str(exif_dict['ExposureTime'][1])
            exif[1] = exif_dict['FNumber'][0]/exif_dict['FNumber'][1]
            exif[2] = int(exif_dict['FocalLength'][0]/exif_dict['FocalLength'][1])
            exif[3] = str(exif_dict['ISOSpeedRatings'])
            exif[4] = str(exif_dict['ExposureBiasValue'][0]/exif_dict['ExposureBiasValue'][1])
        except Exception:
            return [-1] # no exif
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
                    return -1
                else:
                    return results
            else:
                return -1
        

    def rec_settings_w_image(self, style, camera, exif_data=[]):
        settings = []
        if len(exif_data) == 0:
            return [-1] 
        else:
            pass
            #search style db
            #find most similar exposure setting
            #calc EV, make same EV
            #return settings

        return settings

    def search_exif(self, style, exif_data=[], ev=100):
        
        if ev == 100:
            # user choose style
            pass
        elif len(exif_data) != 0:
            pass
            # Search style db
            # find similar exp
            
        pass


if __name__ == '__main__':
    image_file_path = "/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3075.jpg"
    #exif = Recommender().extract_exif(image_file_path)
    #print(exif)

    a, b = Recommender().rec_style(image_file_path)
    print(a)
    print(b)