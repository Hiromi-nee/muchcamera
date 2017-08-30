import pandas as pd
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

class ExifRF:
    ss_pattern = re.compile("^\d/.*")
    encode_cols = ["ExposureCompensation"]
    labels_file = "/media/Kyou/FYP_DATA/flickr_dl/scripts/muchcamera/classifiers/data/exif_classes.txt"
    rfclr_root_path="/media/Kyou/FYP_DATA/flickr_dl/scripts/muchcamera/classifiers/exif_rf_models/"
    classifier_locations = {
                    'HK':'HK_LK_RFClassifier.pkl',
                    'LK':'LK_GL_RFClassifier.pkl', 
                    'MB':'MB_HK_RFClassifier.pkl', 
                    'SD':'SD_SYM_RFClassifier.pkl'
                    }

    def eval_shutterspeed(self,shutterspeed):
        if self.ss_pattern.match(shutterspeed):
            return 1/int(shutterspeed[2:])
        else:
            return shutterspeed

    def classify(self, classifier, data):
        clr = self.load_c(self.rfclr_root_path + self.classifier_locations[classifier])
        df = pd.DataFrame.from_records(
            data,
            columns=["ExposureTime","FNumber","FocalLengthIn35mmFormat","ISO","ExposureCompensation"]
            )
        for c in self.encode_cols:
            df[c] = LabelEncoder().fit_transform(df[c].values)

        df['ExposureTime'] = df.apply(lambda row: self.eval_shutterspeed(row['ExposureTime']),axis=1)
        outcome = clr.predict(df)
       # print("Class: ", outcome )
        #outcome2 = classifier.predict_log_proba(data)
        #print("Class log prob: ",outcome2)
        outcome3 = clr.predict_proba(df)
        #print("Class prob: ",outcome3)
        labels = np.loadtxt(self.labels_file, str, delimiter='\t')
        return labels[outcome[0]], outcome3

    def load_c(self, fname):
        return joblib.load(fname)


if __name__ == '__main__':
    data = [
        ["30", 22, 30,"100","0"],
        ["1/250",5.6,200,"800","0"],
        ["1/500",2.8, 50,"400","0"],
        ["1/50",1.4,50,"400","0"],
        ["1",1.4,50,"1600","-1/2"],
        ["1/40", 2, 23, "3200", "0"],
        ["25", 16, 23, "200", "0"]
        ]
    ret1, ret2 = ExifRF().classify("SD", [data[1]])
    print(ret1)
    print(ret2)