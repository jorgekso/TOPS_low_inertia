import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import time
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/examples/')  # Corrected path to dyn_sim module
import dyn_sim.n45_functions as n45_functions
import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)
import numpy as np 
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/')  # Corrected path to inertia_sim module
import inertia_sim.utility_functions_NJ as uf

if __name__ == '__main__':
    ps = n45_functions.init_n45()
    ps.power_flow()
    ps.init_dyn_sim()
    x0 = ps.x0.copy()
    v0 = ps.v0.copy()
    t = 0
    t_end = 50

    event_flag = False

    x_0 = ps.x_0.copy()

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x_0, t_end, max_step=5e-3)

    # Initialize simulation
    t = 0
    res = defaultdict(list)
    t_0 = time.time()

    while t < t_end:
        sys.stdout.write("\r%d%%" % (t/(t_end)*100))
        if t > 17.6 and event_flag:
            event_flag = False
            ps.lines['Line'].event(ps, 'Virtual line', 'disconnect')
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
    
    disconnected_gen_idx = -1  # Index of the disconnected generator, should be the last one bc of the virtual generator added.
    # Deletes the disconnected generator from the results
    # Convert lists to numpy arrays before deleting elements
    for key in ['gen_speed', 'gen_I', 'gen_P']:
        res[key] = np.array(res[key])
        res[key] = np.delete(res[key], disconnected_gen_idx, axis=1)
        res[key] = res[key].tolist()  # Convert back to list for JSON serialization
    res['gen_name'] = np.array(ps.gen['GEN'].par['name'])
    res['gen_name'] = np.delete(res['gen_name'], disconnected_gen_idx)
    res['gen_name'] = res['gen_name'].tolist()  # Convert back to list for JSON serialization

    res['bus_names'].append(ps.buses['name'])
    print('Simulation completed in {:.2f} seconds.'.format(time.time() - t_0))
    uf.read_to_file(res, 'Results/Base/no_fault.json')

