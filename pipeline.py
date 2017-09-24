from classifiers.cnnwrap import CNNWrap
from classifiers.exif_rf import ExifRF

class Pipeline:
    rf_lut = {'Symmetry':'SD',
            'Shallow_DOF':'SD',
            'Duotones':False,
            'High_Key':'HK',
            'Motion_Blur':'MB',
            'Low_Key':'LK'
            }

    def use_exif(self, type_to_detect, exif_data):
        """
        Returns Predicted Class and probabilities (not in use).
        """
        predicted_class, probability = ExifRF().classify(type_to_detect, exif_data)
        return predicted_class #returned as class label

    def use_cnn(self, image_file_path):
        """
        Returns class probabilities. Python dict format.
        {'1 Shallow_DOF': 0.003380368, '4 Motion_Blur': 0.0076151602, '3 High_Key': 0.0087650334, '5 Good_Light': 0.015498164, '0 Symmetry': 0.95774382, '2 Duotones': 0.0069975234}

        """
        return CNNWrap.classify(image_file_path) #return as probabilities of all classes

    def execute(self, image_file_path, exif_data=[]):

        available_styles = []

        cnn_ret = self.use_cnn(image_file_path)

        #sorted class probabilities
        s = [(k, cnn_ret[k]) for k in sorted(cnn_ret, key=cnn_ret.get, reverse=True)]
        for i_class in s:
            if i_class[1] > 1 / len(s):
                #check rf

                if len(exif_data) != 0:
                    print(exif_data)
                    if self.rf_lut[i_class[0]]:
                        e_ret = self.use_exif(self.rf_lut[i_class[0]],exif_data)
                        if eval(e_ret).decode("utf-8") != i_class[0]:
                            break
                available_styles.extend([i_class])
        if len(available_styles) == 0:
            available_styles.extend([s[0]])
        return available_styles, s

        #find most probable class
        #find 2nd most probable class, use RF detect if possible.
        # see rf detector probabilty to determine is it exists.
        #return detected style
        #return CNN probabilities



if __name__ == '__main__':
    data = [
        ["30", 22, 30,"100","0"],
        ["1/250",5.6,200,"800","0"],
        ["1/500",2.8, 50,"400","0"],
        ["1/50",1.4,50,"400","0"],
        ["1",1.4,50,"1600","-1/2"],
        ["1/40", 2, 23, "3200", "0"],
        ["25", 16, 23, "200", "0"],
        ["1/75", 5.6, 23, "3200", "0"]
        ]
    ret1, ret2 = Pipeline().execute("/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3076.jpg", [data[7]])
    print(ret1)
    print(ret2)