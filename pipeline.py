from classifiers/cnnwrap import CNNWrap
from classifiers/exif_rf import ExifRF

class Pipeline:

	def use_exif(self, exif_data, type_to_detect):
		predicted_class, probability = ExifRF.classify(type_to_detect, exif_data)
		return predicted_class

	def use_cnn(self, image_file_path):
		pass

	def execute(self):
		cnn_ret = self.use_cnn(image_file_path)
		
		#find most probable class
		#find 2nd most probable class, use RF detect if possible.
		# see rf detector probabilty to determine is it exists.
		#return detected style

