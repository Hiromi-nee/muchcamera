from DofCalc import DofCalc
import ExpCalc
from fractions import Fraction

def test_set_f_no():
    a = ExpCalc.ExpCalc(1/4000,100,2.8)
    ev = round(a.get_exposure_val(),0)
    new_ev = round(a.set_f_no(2),0)
    if new_ev != ev:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV NEQ")
        return 1
    else:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV EQ. F_NO Test pass.")
        return 0

def test_set_exp_time():
    a = ExpCalc.ExpCalc(1/4000,1600,2.8)
    ev = round(a.get_exposure_val(),0)
    new_ev = round(a.set_exp_time(1/8000),0)
    if new_ev != ev:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV NEQ")
        return 1
    else:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV EQ. ET Test pass.")
        return 0

def test_set_iso_fixed_et():
    a = ExpCalc.ExpCalc(1/4000,100,1.4)
    ev = round(a.get_exposure_val(),0)
    new_ev = round(a.set_iso_fixed_et(400),0)
    if new_ev != ev:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV NEQ")
        return 1
    else:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV EQ. ISO Test pass.")
        return 0

def test_set_iso_fixed_fno():
    a = ExpCalc.ExpCalc(1/4000,100,1.4)
    ev = round(a.get_exposure_val(),0)
    new_ev = round(a.set_iso_fixed_fno(400),0)
    if new_ev == ev:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV EQ. ISO Test pass.")
        return 0
    elif new_ev > ev:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("Suggested ET:",Fraction(a.exp_time).limit_denominator())
        print("EV NEQ. Overexposure.") 
    else:
        print("EV:", ev)
        print("NEV:", new_ev)
        print("EV NEQ")
        return 1
        

def test_expcalc():
    test_set_f_no()
    test_set_exp_time()
    test_set_iso_fixed_et()
    test_set_iso_fixed_fno()


def test_calc_coc():
    ff_fl = 50
    coc = DofCalc.calc_coc(ff_fl)
    print("COC:", coc)

def test_calc_dof():
    f_no = 2
    fl = 50
    coc = DofCalc.calc_coc(fl)
    f_distance = 10
    print("Aperture: ",f_no)
    print("Focal length (mm): ",fl)
    print("Circle of Confusion: ",coc)
    print("Focal dist. (m): ", f_distance)
    nd, fd = DofCalc.calc_dof(f_no, fl, coc, f_distance)
    print("Near distance sharp:",nd)
    print("Far distance sharp:",fd)

def test_dofcalc():
    test_calc_coc()
    test_calc_dof()

def main():
    #test_expcalc()
    test_dofcalc()

if __name__ == '__main__':
    main()
    #Photo_id,Model,Make,Software,ExposureTime,FNumber,FocalLength,FocalLengthIn35mmFormat,ISO,ExposureCompensation,Flash,Class

