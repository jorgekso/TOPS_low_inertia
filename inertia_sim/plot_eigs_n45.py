'''
This script is used to plot the eigenvalues of the N45 system.
This script is copied from Sjur Foyen's script plot_eigs_v2, and modified to work with the future N45 2030 system.
'''


import tops.dynamic as dps
import tops.modal_analysis as dps_mdl
import tops.plotting as dps_plt
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/examples/')  # Corrected path to dyn_sim module
import init_N45 as n45_functions
import sys
from collections import defaultdict
import time

from config import system_path
sys.path.append(system_path)  # Corrected path to dyn_sim module

import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)



if __name__ == '__main__':
    import tops.ps_models.n45_2_0 as n45
    import init_N45 as init
    energy_mix_2030 = {'FI': {'Wind': 0.7, 'Hydro': 0.1, 'Nuclear': 0.2, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_1': {'Wind': 0.5, 'Hydro': 0.5, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_2': {'Wind': 0.4, 'Hydro': 0.6, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_3': {'Wind': 0.4, 'Hydro': 0.6, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_4': {'Wind': 0.5, 'Hydro': 0.5, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_5': {'Wind': 0.0, 'Hydro': 1.0, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_1': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_2': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_3': {'Wind': 0.6, 'Hydro': 0.0, 'Nuclear': 0.4, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_4': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0}}
    
    ps = init.init_n45(model_data=n45,energy_mix= energy_mix_2030, 
                       data_path= 'inertia_sim/2030_scenario/',
                       spinning_reserve=1.2)
    ps.power_flow()
    ps.init_dyn_sim()

    # Perform system linearization
    ps_lin = dps_mdl.PowerSystemModelLinearization(ps)
    ps_lin.linearize()
    ps_lin.eigenvalue_decomposition()

    # Plot eigenvalues
    dps_plt.plot_eigs(ps_lin.eigs, xlim=(-50, 1))
    
    print(' ')
    print('state description: ')
    print(ps.state_desc)
    print(' ')
    print('Eigenvalues = ')
    print(ps_lin.eigs)
    print(' ')
    print('Speed states: ')
    speedstates = ps.gen['GEN'].state_idx_global['speed']
    print(speedstates)
    # Get mode shape for electromechanical modes
    print(' ')
    damplim = 0.0
    dampl = input('Specify damping threshold (%) : ')
    damplim = 0.01* float(dampl)
    mode_idx = ps_lin.get_mode_idx(['em'], damp_threshold=damplim)
    print('Mode indices with damping less than', dampl,'% :',mode_idx)
    # mode_idx = [14, 12, 10]
    rev = ps_lin.rev
    # Selecting mode shapes to print
    maxmode=0.0
    Gennumber=0
    tellermax=0
    critmode = int(input('Specify mode index for printing generator speed MODE SHAPES : '))
    for tellerx in speedstates:
        if abs(rev[tellerx, critmode]) > maxmode:
            maxmode = abs(rev[tellerx, critmode])
            tellermax=tellerx
            Gennumber= int((tellerx-speedstates[0]+6)/6)

    print(' ')
    print('Selected eigenvalue = ')
    print(ps_lin.eigs[critmode])
    print(' ')
    print('Gen with highest mode shape = ', Gennumber)
    print(ps.state_desc[tellermax])
    print('Mode shape magnitude = ', maxmode )
    # printing eigenvectors
    print('Right eigenvectors = ')
    gen_number = 0
    for tellerx in speedstates:
        gen_number =gen_number + 1
        print('mode ', critmode, ' gen',gen_number,' =', rev[tellerx, critmode] / (maxmode))
    # Plotting selected mode shape
    # mode_shape = rev[np.ix_(ps.gen['GEN'].state_idx_global['speed'], mode_idx)]
    mode_shape = rev[np.ix_(ps.gen['GEN'].state_idx_global['speed'], [critmode, critmode+1])]
    fig, ax = plt.subplots(1, mode_shape.shape[1], subplot_kw={'projection': 'polar'})
    labels = ps.gen['GEN'].par['name']
    for ax_, ms in zip(ax, mode_shape.T):
        dps_plt.plot_mode_shape(ms, ax=ax_, normalize=True,labels=labels)

    plt.show()