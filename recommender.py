from camera import Camera
from pipeline import Pipeline
from calc.ExpCalc import ExpCalc
from calc.DofCalc import DofCalc
import PIL.Image
import PIL.ExifTags

class Recommender:
    
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


    def rec_settings(self, style, camera, exif_data=[]):
        settings = []
        if len(exif_data) == 0:
            #no exif, suggest full settings for given style
            return -1 
        else:
            pass
            #search style db
            #find most similar exposure setting
            #calc EV, make same EV
            #return settings

        return settings


if __name__ == '__main__':
    image_file_path = "/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3075.jpg"
    #exif = Recommender().extract_exif(image_file_path)
    #print(exif)

    a, b = Recommender().rec_style(image_file_path)
    print(a)
    print(b)