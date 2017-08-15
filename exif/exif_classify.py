import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder,LabelBinarizer,MinMaxScaler,OneHotEncoder
from sklearn.decomposition import TruncatedSVD,NMF,PCA,FactorAnalysis
from sklearn.feature_selection import SelectFromModel,SelectPercentile,f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

ss_pattern = re.compile("^\d/.*")

def eval_shutterspeed(shutterspeed):
    if ss_pattern.match(shutterspeed):
        return 1/int(shutterspeed[2:])
    else:
        return shutterspeed

def test(rfc, test, columns):
    X_t10 = test[columns].values
    accuracy = rfc.score(X_t10, test["Class"])
    print("Mean accuracy: %f." % accuracy)
    return accuracy

def train(est, train_data, train_target):
    rfc = RandomForestClassifier(n_estimators=est)
    rfc.fit(train_data, list(train_target.values.ravel()))
    return rfc

def classify(classifier,data):
    data['ExposureTime'] = data.apply(lambda row: eval_shutterspeed(row['ExposureTime']),axis=1)
    outcome = classifier.predict(data)
    print("Class: ", outcome )
    outcome2 = classifier.predict_log_proba(data)
    print("Class log prob: ",outcome2)
    outcome3 = classifier.predict_proba(data)
    print("Class prob: ",outcome3)

def save_c(classifier, fname):
    joblib.dump(classifier, fname+'.pkl') 
    print("Saved to %s.pkl" % fname)

def load_c(fname):
    return joblib.load(fname)

def save_df(df, fname):
    df.to_csv(fname)
    print("Saved dataframe to file.")

no_est_rf = 100
#0 = test, 1 = classify
test_or_classify = 0

data_path = "/media/Kyou/FYP_DATA/flickr_dl/data/exif/exif_csv_v2/"
#data_path = "/media/Kyou/FYP_DATA/flickr_dl/data/exif/exif_csv_v2/"
#dataset_highkey = pd.read_csv(data_path+'cleanT_clean_exif_3.db.csv')
#dataset_lowkey = pd.read_csv(data_path+'cleanT_clean_exif_7.db.csv')

#dataset_symmetry = pd.read_csv(data_path+'cleanT_clean_exif_0.db.csv')
#dataset_shallowdof = pd.read_csv(data_path+'cleanT_clean_exif_1.db.csv')
#dataset_duotones = pd.read_csv(data_path+'cleanT_clean_exif_2.db.csv')
dataset_motionblur = pd.read_csv(data_path+'cleanT_clean_exif_4.db.csv')
dataset_goodlight = pd.read_csv(data_path+'cleanT_clean_exif_5.db.csv')
#dataset_vividcolour = pd.read_csv(data_path+'cleanT_clean_exif_6.db.csv')



#msk = np.random.rand(len(dataset_highkey)) < 0.8
#train_highkey = dataset_highkey[msk]
#test_highkey = dataset_highkey[~msk]

#msk = np.random.rand(len(dataset_lowkey)) < 0.8
#train_lowkey = dataset_lowkey[msk]
#test_lowkey = dataset_lowkey[~msk]

#change here
train_lowkey, test_lowkey = train_test_split(dataset_goodlight, test_size =0.2) 
train_highkey, test_highkey = train_test_split(dataset_motionblur, test_size=0.2)
#end change here

traind = pd.concat([train_highkey,train_lowkey])
testd = pd.concat([test_lowkey,test_highkey])

data = pd.concat([traind,testd])

encode_cols = ["ExposureCompensation"]
for c in encode_cols:
    data[c] = LabelEncoder().fit_transform(data[c].values)
traind = data[:traind.shape[0]]
testd = data[traind.shape[0]:]

#Photo_id,Model,Make,Software,ExposureTime,FNumber,FocalLength,FocalLengthIn35mmFormat,"ISO","ExposureCompensation","Flash",Class
train_labels = traind['Class']
train_target = train_labels.rename(None).to_frame() #labels
orig_train = traind
del traind['Photo_id']
del traind['Model']
del traind['Make']
del traind['Software']
del traind['FocalLength']
del traind['Class']
del traind['Flash']
#del traind['ExposureCompensation']
#del traind['FocalLengthIn35mmFormat'] #uncomment this line to train with only ExposureTime and FNumber

columns = traind.columns.tolist()
print("Train data length %d, width %d" %traind.shape)
classifier = train(no_est_rf, traind, train_target)
accuracy = test(classifier, testd, columns)
if accuracy > 0.885986:
    save_c(classifier, "MB_GL_RFClassifier")
    save_df(orig_train, "train_MB_GL.csv")
    save_df(testd, "test_MB_GL.csv")

sample_data = [["30", 22, 30,"100","0"],["1/250",5.6,200,"800","0"],["1/500",2.8, 50,"400","0"],["1/50",1.4,50,"400","0"],["1",1.4,50,"1600","-1/2"],["1/40", 2, 23, "3200", "0"],["25", 16, 23, "200", "0"]]
sample_data1 = [["30", 22, 30,"100"],["1/250",5.6,200,"800"],["1/500",2.8, 50,"400"],["1/50",1.4,50,"400"],["1",1.4,50,"1600"],["1/40", 2, 23, "3200"],["25", 16, 23, "200"]]
sample_data2 = [["30", "22"],["0.0001","5.6"],["0.00025","2.8"],["0.5","1.4"],["1","1.4"]] #use this if training with 2 feats only
sample_data3 = [["30", "22", "30"],["0.0001","5.6","200"],["0.00025","2.8", "50"],["0.5","1.4","50"],["1","1.4","50"]]


no_ec = 0 # 0 if 5 feats, 1 if 4 feats
if no_ec == 0:
    df = pd.DataFrame.from_records(sample_data,columns=["ExposureTime","FNumber","FocalLengthIn35mmFormat","ISO","ExposureCompensation"])
    for c in encode_cols:
        df[c] = LabelEncoder().fit_transform(df[c].values)
else:
    df = pd.DataFrame.from_records(sample_data1,columns=["ExposureTime","FNumber","FocalLengthIn35mmFormat","ISO"])
classify(classifier,df)
#for s_data in df:
#    print(s_data)
#    classify(classifier,[s_data])