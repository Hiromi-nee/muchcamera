class DofCalc:

    def calc_coc(ff_fl, actual_fl=0, coc_35=0.030):
        # 35mm format circle of confusion is 0.025 - 0.035 mm
        # CoC = (CoC for 35mm format) / (Digital camera lens focal length multiplier)
        # Multiplier = (35mm equivalent lens focal length) / (Actual lens focal length)
        if actual_fl == 0:
            actual_fl = ff_fl
        multiplier = ff_fl / actual_fl
        return coc_35 / (multiplier)

    def calc_dof(f_no, fl, coc, f_distance):
        # http://www.dofmaster.com/equations.html
        #i = DofCalc.get_n(f_no)
        n = f_no
        hyperfocal_dist = ((fl ** 2) / (n * coc)) + fl
        print("HPD (m):",hyperfocal_dist/1000)
        temp_1 = (f_distance*1000 * (hyperfocal_dist - fl))
        near_dist_sharp = temp_1 / (hyperfocal_dist + f_distance*1000 - 2 * fl)
        far_dist_sharp = temp_1 / (hyperfocal_dist - f_distance*1000)
        in_front_subj = (f_distance*1000 - near_dist_sharp)/1000
        behind_subj = (far_dist_sharp - f_distance*1000)/1000
        #print("In front of subject in focus (m):", in_front_subj)
        #print("Behind of subject in focus (m):",behind_subj)
        return near_dist_sharp/1000, far_dist_sharp/1000