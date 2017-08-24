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

    def eval_shutterspeed(self,shutterspeed):
        if self.ss_pattern.match(shutterspeed):
            return 1/int(shutterspeed[2:])
        else:
            return shutterspeed

    def classify(self, classifier,data):
        
        data['ExposureTime'] = data.apply(lambda row: self.eval_shutterspeed(row['ExposureTime']),axis=1)
        outcome = classifier.predict(data)
        print("Class: ", outcome )
        outcome2 = classifier.predict_log_proba(data)
        print("Class log prob: ",outcome2)
        outcome3 = classifier.predict_proba(data)
        print("Class prob: ",outcome3)

    def load_c(fname):
        return joblib.load(fname)