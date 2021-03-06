from calc.ExpCalc import ExpCalc

class Camera:

    def __init__(self, ff_fl="50", orig_fl = "50", model="Nikon D750", sensor_size="FF", 
        max_aperture = 20, min_aperture = 2.8, max_shutter_speed = 30, min_shutter_speed = 1/4000,
        max_iso = 6400, min_iso = 100, max_fl = 70, min_fl = 28, multiplier=1):

        #self.exposure = exposure
        self.ff_focal_length = ff_fl
        self.orig_focal_length = orig_fl
        self.model = model
        self.multiplier = multiplier
        self.sensor_size = sensor_size
        self.max_aperture = max_aperture
        self.min_aperture = min_aperture
        self.max_shutter_speed = max_shutter_speed
        self.min_shutter_speed = min_shutter_speed
        self.max_iso = max_iso
        self.min_iso = min_iso
        self.max_fl = max_fl
        self.min_fl = min_fl


    def calc_ff_focal_length(self):
        if self.ff_focal_length == self.orig_focal_length:
            return self.ff_focal_length
        else:
            self.ff_focal_length = self.orig_focal_length*self.multiplier
            return self.ff_focal_length