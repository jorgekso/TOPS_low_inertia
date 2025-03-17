import sys
from collections import defaultdict
import time

from config import system_path
sys.path.append(system_path)  # Corrected path to dyn_sim module

import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)


import utility_functions_NJ as uf
import numpy as np 

import matplotlib.pyplot as plt


from FFR import activate_FFR


def gen_trip(ps,folderandfilename, fault_bus = '7000',fault_Sn = 1400,fault_P = 1400,kinetic_energy_eps = 300e3,
             t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False, FFR = False, FFR_vsc_names = None):
    """
    Simulates a generator trip in the Nordic 45 system.
    Parameters:
    model_data : dictionary
        Dictionary containing the model data.
    fault_bus : string
        The bus number of the fault.
    fault_Sn : float
        The nominal power of the fault.
    fault_P : float
        The active power of the fault.
    kinetic_energy_eps : float
        The kinetic energy of the EPS.
    folderandfilename : string
        The folder and filename of the results.
    t : float
        The initial time of the simulation.
    t_end : float
        The end time of the simulation.
    t_trip : float
        The time of the generator trip.
    event_flag : bool
        If True, the generator trip event is triggered.
    VSC : bool
        If True, the VSC results are included in the simulation.
    """
    
    ps.power_flow()
    ps.init_dyn_sim()
    x0 = ps.x0.copy()
    v0 = ps.v0.copy()




    x_0 = ps.x_0.copy()

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x_0, t_end, max_step=5e-3)

    # Initialize simulation
    t = 0
    res = defaultdict(list)
    t_0 = time.time()

        
    FFR_activated = False
    while t < t_end:
        sys.stdout.write("\r%d%%" % (t/(t_end)*100))

        if t > t_trip and event_flag:
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
        if(VSC):
            res['VSC_p'].append(ps.vsc['VSC_SI'].p_e(x, v).copy())
            res['VSC_Sn'].append(ps.vsc['VSC_SI'].par['S_n'])
            res['VSC_name'].append(ps.vsc['VSC_SI'].par['name'])
    
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
    uf.read_to_file(res, 'Results/'+folderandfilename+'.json')


def HVDC_cable_trip(ps,folderandfilename,t=0,t_end=50,t_trip = 17.6,event_flag = True, link_name = 'NO_2-DE', FFR = False, FFR_sources = None):
    ''''
    Simulates a trip of a HVDC cable in the Nordic 45 system.
    Parameters:
    ps : PowerSystemModel
        The power system model.
    folderandfilename : string
        The folder and filename of the results.
    t : float
        The initial time of the simulation.
    t_end : float
        The end time of the simulation.
    t_trip : float
        The time of the trip.
    event_flag : bool
        If True, the trip event is triggered.
    line : string
        The name of the line that should trip.
    '''
    
    ps.power_flow()
    ps.init_dyn_sim()
    x0 = ps.x0.copy()
    v0 = ps.v0.copy()




    x_0 = ps.x_0.copy()

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x_0, t_end, max_step=5e-3)

    # Initialize simulation
    t = 0
    res = defaultdict(list)
    t_0 = time.time()
    print(max(abs(ps.state_derivatives(0, ps.x_0, ps.v_0))))

    FFR_activated = False
    t_FFR = 0
       
    
    while t < t_end:
        sys.stdout.write("\r%d%%" % (t/(t_end)*100))

        if t > t_trip and event_flag:
            event_flag = False
            #find the index of the vsc corresponding to the name load 
            #ps.vsc['VSC_SI'].par['name'] is an ndarray
            index_vsc = np.where(ps.vsc['VSC_SI'].par['name'] == link_name)[0]
            ps.vsc['VSC_SI'].set_input('p_ref', 0,index_vsc)
        result = sol.step()
        x = sol.y
        v = sol.v
        t = sol.t
        


        if FFR_sources != None:
            mean_freq = 50 + 50*np.mean(ps.gen['GEN'].speed(x,v))
           
            FFR_activated, t_FFR = activate_FFR(ps, mean_freq,t, FFR_sources, FFR_activated, t_FFR,x,v)
            
            

       
                


        dx = ps.ode_fun(0, ps.x_0)
        res['t'].append(t)
        res['gen_speed'].append(ps.gen['GEN'].speed(x, v).copy())
        res['v'].append(v.copy())
        res['gen_I'].append(ps.gen['GEN'].I(x, v).copy())
        res['gen_P'].append(ps.gen['GEN'].P_e(x, v).copy())
        res['load_P'].append(ps.loads['Load'].P(x, v).copy())
        res['load_Q'].append(ps.loads['Load'].Q(x, v).copy())
        res['VSC_p'].append(ps.vsc['VSC_SI'].p_e(x, v).copy())
    res['VSC_Sn'].append(ps.vsc['VSC_SI'].par['S_n'].copy())
    res['VSC_name'].append(ps.vsc['VSC_SI'].par['name'].copy())
    res['gen_name'].append(ps.gen['GEN'].par['name'].copy())
    res['bus_names'].append(ps.buses['name'].copy())
    res['load_names'].append(ps.loads['Load'].par['name'].copy())

    print('Simulation completed in {:.2f} seconds.'.format(time.time() - t_0))
    uf.read_to_file(res, 'Results/'+folderandfilename+'.json')