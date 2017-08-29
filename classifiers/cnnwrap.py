import subprocess

class CNNWrap:
    def classify(input_file, gpu=False):
        python2_exe = "python2"
        py2_classifier_script="cnn.py"
        path_to_image = input_file
        results = ""
        try:
            out = subprocess.run([python2_exe, py2_classifier_script, path_to_image], stdout=subprocess.PIPE)
            results = out.stdout
        except Exception:
            results = "Error calling CNN classifier"

        return results



if __name__ == '__main__':
    ret = CNNWrap().classify("image.jpg")
    print(ret)