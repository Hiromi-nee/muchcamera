import sys
sys.path.insert(0, '../')
from calc.ExpCalc import ExpCalc

def diff_exposures(exposure_1, exposure_2):
    # takes 2 exposure objects and find which attribute is different
    # current, target
    flags = [0,0,0] # exposure time, aperture, iso
    if exposure_1.exp_time != exposure_2.exp_time:
    	# target faster
        if exposure_1.exp_time > exposure_2.exp_time: 
    		flags[0] = 1
    	else: # target slower shutter speed
    		flags[0] = -1
    if exposure_1.f_no != exposure_2.f_no:
    	# target larger aperture
    	if exposure_1.f_no > exposure_2.f_no:
			flags[1] = 1
		else:
			flags[1] = -1
    if exposure_1.iso != exposure_2.iso:
    	# target slower iso
        if exposure_1.iso > exposure_2.iso:
        	flags[2] = -1
        else:
        	flags[2] = 1

    return flags