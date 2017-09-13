from math import log2, sqrt, inf, log, log10
from fractions import Fraction


class ExpCalc:
    """Class for calculating exposure"""
    expt_lut = [
        1 / 8000, 1 / 6400, 1 / 5000, 1 / 4000, 1 / 3200, 1 / 2500, 1 / 2000,
        1 / 1600, 1 / 1250, 1 / 1000, 1 / 800, 1 / 640, 1 / 500,
        1 / 400, 1 / 320,
        1 / 250, 1 / 200, 1 / 160, 1 / 125, 1 / 100, 1 / 80, 1 / 60,
        1 / 50, 1 / 40, 1 / 30, 1 / 25, 1 / 20, 1 / 15, 1 / 13, 1 / 10,
        1 / 8, 1 / 6, 1 / 5, 1 / 4,
        0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5]
    f_no_lut = [
        0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8,
        2, 2.2, 2.5, 2.8, 3.2, 3.5, 4, 4.5, 5.0, 5.6,
        6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20,
        22, 27, 32, 38, 45, 54, 64]
    iso_lut = [
        50, 100, 125, 160, 200, 250, 320, 400, 500, 640,
        800, 1000, 1250, 1600, 2000, 2500, 3200,
        4000, 5000, 6400, 12800, 25600]

    def __init__(self, exp_time, iso, f_no):
        self.exp_time = exp_time
        self.iso = iso
        self.f_no = f_no

    def inc_stop(self, type, amt):
        if type == "f_no":
            cur_idx = self.f_no_lut.index(self.f_no)
            new_idx = int(cur_idx - amt * 3)
            if new_idx < 0:
                stops_over = 0 - new_idx
                new_idx = cur_idx
                print("Over limits by %d stops." % stops_over)
            try:
                new_f_no = self.f_no_lut[new_idx]
            except Exception:
                print("Error incrementing aperture")
            self.f_no = new_f_no
            return new_f_no

        elif type == "exp_time":
            cur_idx = self.expt_lut.index(self.exp_time)
            new_idx = int(cur_idx + amt * 3)
            #print("new_idx:", new_idx)
            #print("cur_idx:", cur_idx)
            if new_idx >= len(self.expt_lut):
                stops_over = new_idx - (len(self.expt_lut) - 1) 
                new_idx = cur_idx
                print("Over limits by %d stops" % stops_over)
            try:
                new_exp_time = self.expt_lut[new_idx]
            except Exception:
                print("Err incrementing exp_time")
            self.exp_time = new_exp_time
            return new_exp_time

        elif type == "iso":
            cur_idx = self.iso_lut.index(self.iso)
            new_idx = int(cur_idx + amt * 3)
            if new_idx >= len(self.iso_lut):
                stops_over = new_idx - (len(self.iso_lut) - 1) 
                new_idx = cur_idx
                print("Over limits by %d stops" % stops_over)
            try:
                new_iso = self.iso_lut[new_idx]
            except Exception:
                print("Err incrementing iso")
            self.iso = new_iso
            return new_iso

        else:
            print("Type error.")
            return -1

    def dec_stop(self, type, amt):
        if type == "f_no":
            cur_idx = self.f_no_lut.index(self.f_no)
            new_idx = int(cur_idx + amt * 3)
            if new_idx >= len(self.f_no_lut):
                stop_underexposed = new_idx - (len(self.f_no_lut) - 1)
                new_idx = 0
                print("Over camera limits by: %d stops" % stop_underexposed)
            try:
                new_f_no = self.f_no_lut[new_idx]
            except Exception:
                print("Err decrementing f_no")
            self.f_no = new_f_no
            return new_f_no

        elif type == "exp_time":
            cur_idx = self.expt_lut.index(self.exp_time)
            new_idx = int(cur_idx-amt*3)
            #print("new_idx:", new_idx)
            #print("cur_idx:", cur_idx)
            if new_idx <0:
                new_idx = 0
                print("Exceeds Camera capabilities")
                #return new_idx
            try:
                new_exp_time = self.expt_lut[new_idx]
            except Exception:
                print("Err decrementing exp_time")
            self.exp_time = new_exp_time
            return new_exp_time

        elif type == "iso":
            cur_idx = self.iso_lut.index(self.iso)
            new_idx = int(cur_idx-amt*3)
            if new_idx <0:
                new_idx = 0
            try:
                new_iso = self.iso_lut[new_idx]
            except Exception:
                print("Err decrementing iso")
            self.iso = new_iso
            return new_iso
        else:
            print("Type error.")
            return -1

    def get_ev(self):
        return log2((1/self.f_no ** 2) / self.exp_time)

    def get_exposure_val(self):
        # EV = log2(N**2 / t) where N = f-number
        # and t = exposure time in seconds.
        # EVS = EV100 + log2(S / 100) where S = desired ISO.
        #ev = log2(((1/self.f_no) ** 2) / self.exp_time)
        #evs = ev + log2(self.iso / 100)
        evs2 = log2(100 * (self.f_no ** 2) / (self.iso*self.exp_time))
        return evs2  # good to round this value



# TODO: FIX ISO>100, adjust by stops. luts in 1/3 steps. 

    def update_f_no(self,old_ev):
        new_ev = self.get_exposure_val()
        print("new_ev:",new_ev)
        #if self.iso != 100:
        #    old_ev = old_ev - (self.iso/100)
        #f_no = sqrt(self.exp_time * (2**(old_ev + log2(self.iso / 100))))
        #print("F:",f_no)
        #new_f_no = self.round_to_list(round(f_no,1), self.f_no_lut)
        #print("nfno:",new_f_no)
        #new_ev = self.calc_ev(self.exp_time,self.iso,new_f_no)
        #print("NEW",new_ev)
        if new_ev > old_ev:
            dec_amt = round(new_ev,0) - round(old_ev,0)
            print("dec",dec_amt)
            new_f_no = self.inc_stop("f_no",dec_amt) ###
            print("New Fno:", new_f_no)
        elif new_ev < old_ev:
            inc_amt = round(old_ev,0) - round(new_ev,0)
            print("inc",inc_amt)
            new_f_no = self.dec_stop("f_no",inc_amt)
            print("New Fno:", new_f_no)

        self.f_no = new_f_no

    def update_exp_time(self,old_ev):
        #exp_time = (self.f_no * self.f_no) / (2 ** (old_ev + log2(self.iso / 100)))
        #print("ET:",Fraction(exp_time).limit_denominator())
        # do table rounding before converting to string
        #self.exp_time = str(self.round_to_list(Fraction(exp_time).limit_denominator(), self.expt_lut))
        #self.exp_time = float(Fraction(self.round_to_list(exp_time, self.expt_lut)).limit_denominator())
        #print(Fraction(self.exp_time).limit_denominator())
        new_ev = self.get_exposure_val()
        print("new_ev:",new_ev)
        if new_ev > old_ev:
            dec_amt = round(new_ev,0) - round(old_ev,0)
            print("dec",dec_amt)
            new_exp_time = self.inc_stop("exp_time",dec_amt)
        elif new_ev < old_ev:
            inc_amt = round(old_ev,0) - round(new_ev,0)
            print("inc",inc_amt)
            new_exp_time = self.dec_stop("exp_time",inc_amt)
        print("new_et:",Fraction(new_exp_time).limit_denominator())
        self.exp_time = new_exp_time
    
    def update_iso(self,old_ev):
        #iso = (2 ** (sqrt((self.f_no ** 2) / self.exp_time) - old_ev)) * 100
        #self.iso = self.round_to_list(round(iso), self.iso_lut)
        new_ev = self.get_exposure_val()
        print("new_ev:",new_ev)
        if new_ev > old_ev:
            dec_amt = round(new_ev,0) - round(old_ev,0)
            print("dec",dec_amt)
            new_iso = self.dec_stop("iso",dec_amt)
        elif new_ev < old_ev:
            inc_amt = round(old_ev,0) - round(new_ev,0)
            print("inc",inc_amt)
            new_iso = self.inc_stop("iso",inc_amt)
        print("new_iso:",new_iso)
        self.iso = new_iso

    def round_to_list(self, val, lst):
        if val < lst[0] or val > lst[len(lst) - 1]:
            return val
        best = val
        bestDiff = inf
        for lstval in lst:
            print("Best:",best)
            diff = abs(lstval - val)
            if diff <= bestDiff:
                best = lstval
                bestDiff = diff
            else:
                return best
        return best

#attr setters

    #aperture priority
    def set_f_no(self,f_no):
        old_evs = self.get_exposure_val()
        old_ev = self.get_ev()
        print("oet:",self.exp_time)
        print("oev:",old_ev)
        print("oevs:",old_evs)
        print("oiso:",self.iso)
        print("ofno:",self.f_no)
        self.f_no = f_no
        self.update_exp_time(old_evs)
        return self.get_exposure_val()

    #shutter priority
    def set_exp_time(self,et):
        old_evs = self.get_exposure_val()
        old_ev = self.get_ev()
        print("oet:",self.exp_time)
        print("oev:",old_ev)
        print("oevs:",old_evs)
        print("oiso:",self.iso)
        print("ofno:",self.f_no)
        self.exp_time = et
        self.update_f_no(old_evs)
        return self.get_exposure_val()

    def set_iso_fixed_et(self, iso):
        old_evs = self.get_exposure_val()
        old_ev = self.get_ev()
        print("oet:",self.exp_time)
        print("oev:",old_ev)
        print("oevs:",old_evs)
        print("oiso:",self.iso)
        print("ofno:",self.f_no)
        self.iso = iso
        self.update_f_no(old_evs)
        return self.get_exposure_val()

    def set_iso_fixed_fno(self,iso):
        old_evs = self.get_exposure_val()
        old_ev = self.get_ev()
        print("oet:",self.exp_time)
        print("oev:",old_ev)
        print("oevs:",old_evs)
        print("oiso:",self.iso)
        print("ofno:",self.f_no)
        self.iso = iso
        self.update_exp_time(old_evs)
        print("New ET:", self.exp_time)
        print("New f:", self.f_no)
        print("New iso:", self.iso)
        return self.get_exposure_val()