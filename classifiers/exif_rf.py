import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder,LabelBinarizer,MinMaxScaler,OneHotEncoder
from sklearn.decomposition import TruncatedSVD,NMF,PCA,FactorAnalysis
from sklearn.feature_selection import SelectFromModel,SelectPercentile,f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

class ExifRF:
    ss_pattern = re.compile("^\d/.*")
    encode_cols = ["ExposureCompensation"]
    classifier_locations = {'LK':'', 'MB':'', 'SD':''}

    def eval_shutterspeed(self,shutterspeed):
        if self.ss_pattern.match(shutterspeed):
            return 1/int(shutterspeed[2:])
        else:
            return shutterspeed

    def classify(self, classifier, data):
        clr = self.load_c(self.classifier_locations[classifier])
        df = pd.DataFrame.from_records(data,columns=["ExposureTime","FNumber","FocalLengthIn35mmFormat","ISO","ExposureCompensation"])
        for c in self.encode_cols:
            df[c] = LabelEncoder().fit_transform(df[c].values)

        df['ExposureTime'] = df.apply(lambda row: self.eval_shutterspeed(row['ExposureTime']),axis=1)
        outcome = clr.predict(df)
        print("Class: ", outcome )
        #outcome2 = classifier.predict_log_proba(data)
        #print("Class log prob: ",outcome2)
        outcome3 = classifier.predict_proba(df)
        print("Class prob: ",outcome3)

        return outcome, outcome3

    def load_c(self, fname):
        return joblib.load(fname)


if __name__ == '__main__':
    data = [["30", 22, 30,"100","0"],["1/250",5.6,200,"800","0"],["1/500",2.8, 50,"400","0"],["1/50",1.4,50,"400","0"],["1",1.4,50,"1600","-1/2"],["1/40", 2, 23, "3200", "0"],["25", 16, 23, "200", "0"]]
    ret = ExifRF.classify("LK", data)
    print(ret)