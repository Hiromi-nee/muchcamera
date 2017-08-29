import subprocess
import ast

class CNNWrap:
    def classify(input_file, gpu=False):
        python2_exe = "python2"
        py2_classifier_script="classifiers/cnn.py"
        path_to_image = input_file
        results = ""
        try:
            out = subprocess.run([python2_exe, py2_classifier_script, path_to_image], stdout=subprocess.PIPE)
            ret = out.stdout
            results = ast.literal_eval(ret.decode().split("\n")[1])
        except Exception as e:
            results = "Error calling CNN classifier"

        return results



if __name__ == '__main__':
    ret = CNNWrap.classify("/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3076.jpg")
    print(ret)