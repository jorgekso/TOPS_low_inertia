import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import time
sys.path.append('//Users/noralillelien/Documents/TOPS_low_inertia/')  # Corrected path to dyn_sim module
import dyn_sim.n45_functions as n45_functions
import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)
import numpy as np 
sys.path.append('/Users/noralillelien/Documents/TOPS_low_inertia/')
import inertia_sim.utility_functions_NJ as uf

if __name__ == '__main__':
    ps = n45_functions.init_n45()
    ps.init_dyn_sim()

    t = 0
    t_end = 50

    event_flag = True

    x_0 = ps.x_0.copy()

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x_0, t_end, max_step=5e-3)

    # Initialize simulation
    t = 0
    res = defaultdict(list)
    t_0 = time.time()

    while t < t_end:
        sys.stdout.write("\r%d%%" % (t/(t_end)*100))
        if 30 <= t and event_flag:
                event_flag = False
        result = sol.step()
        x = sol.y
        v = sol.v
        t = sol.t
        dx = ps.ode_fun(0, ps.x_0)
        res['t'].append(t)
        res['gen_speed'].append(ps.gen['GEN'].speed(x, v).copy())
        res['v'].append(v.copy())
        res['gen_I'].append(ps.gen['GEN'].I(x, v).copy())
        res['gen_P'].append(ps.gen['GEN'].P_e(x, v).copy())
        res['load_P'].append(ps.loads['Load'].P(x, v).copy())
        res['load_Q'].append(ps.loads['Load'].Q(x, v).copy())
    
    res['bus_names'].append(ps.buses['name'])
    res['gen_name'].append(ps.gen['GEN'].par['name'])
    print('Simulation completed in {:.2f} seconds.'.format(time.time() - t_0))
    uf.read_to_file(res, 'Results/Base/gen_trip.json')

