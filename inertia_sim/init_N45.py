import sys
from collections import defaultdict
import time
from config import system_path
sys.path.append(system_path)  # Corrected path to dyn_sim module
import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)
import numpy as np 
import utility_functions_NJ as uf
import tops.utility_functions_eirik as MThesis
import tops.ps_models.n45_with_controls_HVDC as model_data
importlib.reload(dps)
import pandas as pd
import pandas as pd



def init_n45(model_data, display_pf, fault_bus = '3359',fault_Sn = 1400,fault_P = 1400,kinetic_energy_eps = 300e3):
    """
    Initializes the Nordic 45 system from "N45_case_data" folder with the specified fault bus, fault Sn, fault P and kinetic energy of the EPS.

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

    """
    #data_path = 'inertia_sim/N45_case_data/'
    data_path = 'inertia_sim/N45_case_data_NordLink/'
    #Accessing the case data and saving it in Dataframe format
    ENTSOE_gen_data, ENTSOE_load_data, ENTSOE_exchange_data = MThesis.Import_data_ENTSOE(data_path)
    # List of international power links: Should be updated if added links or using another model than N45
    international_links = {'L5230-1': 'NO_2-DE', 'L5240-2': 'NO_2-GB', 'L5210-1': 'NO_2-DK',
                           'L3360-1': 'SE_3-DK', 'L8600-1': 'SE_4-DK', 'L8700-1': 'SE_4-PL',
                           'L8600-2': 'SE_4-DE', 'L8700-2': 'SE_4-LT', 'L7020-1': 'FI-EE',
                           'L3020-1': 'SE_3-FI', 'L7010-1': 'FI-SE_3', 'L5220-1': 'NO_2-NL',
                           'L7020-2': 'FI-RU'}
    #Initializing the model from the load data in n45_with_controls
    model = model_data.load()

    # ------------------------------ Reparameterization to fit specific time-senario -----------------------------------
    index_area = model['buses'][0].index('Area')
    area_mapping = {24: 'SE_4', 23: 'SE_3', 22: 'SE_2', 21: 'SE_1', 11: 'NO_1', 12: 'NO_2', 13: 'NO_3',
        14: 'NO_4', 15: 'NO_5', 31: 'FI'} #integers from original N45, strings from Transparency platform
    #Change from numbers to strings from area_mapping to have consistent area names
    for bus in model['buses'][1:]:
        area = bus[index_area]
        if area in area_mapping:
            bus[index_area] = area_mapping[area]
        else:
            print(f"ERROR: Unknown price area {area}")

    
    # Making dictionary to map bus to area
    area_by_bus = {} #From bus find area
    bus_by_area = {} #From area find buses
    index_bus_name = model['buses'][0].index('name')
    index_area = model['buses'][0].index('Area')
    for bus in model['buses'][1:]:
        area = bus[index_area]
        area_by_bus[bus[index_bus_name]] = area
        if area not in bus_by_area:
            bus_by_area[area] = [bus[index_bus_name]]
        else:
            bus_by_area[area].append(bus[index_bus_name])
    fault_area = area_by_bus.get(fault_bus)



    #------------------------------Updating the Power generation in the n45_with_controls model-----------------------------------
    #To retrieve total specified power generation in an area
    # Initialize a list to store specified power generation by area code
    PowerGen_by_area = {}
    # Iterate through the 'GEN' data and extract 'bus' and 'P' columns
    index_bus_name = model['generators']['GEN'][0].index('bus')
    index_gen = model['generators']['GEN'][0].index('name')
    index_P = model['generators']['GEN'][0].index('P')


    all_gen = set()
    for row in model['generators']['GEN'][1:]:
        bus_name = row[index_bus_name]
        gen_name = row[index_gen]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        if area not in PowerGen_by_area:
            PowerGen_by_area[area] = 0
        PowerGen_by_area[area] = PowerGen_by_area[area] + P_specified
        all_gen.add(gen_name)


    #------------------------------Updating the Power consumption in the n45_with_controls model-----------------------------------
    PowerCon_by_area = {}
    PowerExc_by_country = {} #Used for scaling when mulitple export/import power links between countries
    index_name = model['loads'][0].index('name')
    index_bus_name = model['loads'][0].index('bus')
    index_P = model['loads'][0].index('P')
    load_sum = 0.0
    added = set() #To not count interconnectors multiple times
    for row in model['loads'][1:]:
        bus_name = row[index_bus_name]
        load_name = row[index_name]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        load_sum += P_specified
        if load_name not in international_links.keys(): #If load inside model
            if area not in PowerCon_by_area:
                PowerCon_by_area[area] = 0.0
            PowerCon_by_area[area] = PowerCon_by_area[area] + P_specified

        elif load_name in international_links.keys(): #if import/export cable
            transfer_code = international_links[load_name]
            from_count = transfer_code[:2]
            to_count = transfer_code[-2:]
            for other_load_name, other_transfer in international_links.items():
                other_from_count = other_transfer[:2]
                other_to_count = other_transfer[-2:]
                if from_count == other_from_count and to_count == other_to_count \
                        and transfer_code != other_transfer and transfer_code not in added:
                    if from_count not in PowerExc_by_country:
                        PowerExc_by_country[from_count] = 0.0
                    PowerExc_by_country[from_count] = PowerExc_by_country[from_count] + P_specified
                    added.add(transfer_code)
                elif from_count == other_to_count and to_count == other_from_count \
                        and transfer_code != other_transfer and transfer_code not in added:
                    if from_count not in PowerExc_by_country:
                        PowerExc_by_country[from_count] = 0.0
                    PowerExc_by_country[from_count] = PowerExc_by_country[from_count] - P_specified
                    added.add(transfer_code)


    
    # ------------------------------Updating generators' specified powers----------------------------------------------
    index_bus_name = model['generators']['GEN'][0].index('bus')
    index_gen = model['generators']['GEN'][0].index('name')
    index_P = model['generators']['GEN'][0].index('P')
    index_Sn = model['generators']['GEN'][0].index('S_n')
    for row in model['generators']['GEN'][1:]:
        bus_name = row[index_bus_name]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        gen_name = row[index_gen]
        row[index_P] = (P_specified * ENTSOE_gen_data['Power generation'].loc[area] / PowerGen_by_area.get(area))
        row[index_Sn] = row[index_Sn] * ENTSOE_gen_data['Power generation'].loc[area] / PowerGen_by_area.get(area)



    # ------------------------------Updating loads' active and reactive power consumptions------------------------------
    index_name = model['loads'][0].index('name')
    index_bus_name = model['loads'][0].index('bus')
    index_P = model['loads'][0].index('P')
    index_Q = model['loads'][0].index('Q')

    for row in model['loads'][1:]:
        bus_name = row[index_bus_name]
        load_name = row[index_name]
        area = area_by_bus.get(bus_name)
        cot_phi = row[index_Q] / row[index_P] if not -1 < row[index_P] < 1 else 0
        if row[index_name] in international_links.keys(): #if international link
            area_transfer = international_links.get(load_name)
            split = area_transfer.split('-')
            if area_transfer in ENTSOE_exchange_data['Power transfer'].keys(): #Only one link out of country
                P_new = ENTSOE_exchange_data['Power transfer'].loc[area_transfer]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
            elif split[1]+'-'+split[0] in ENTSOE_exchange_data['Power transfer'].keys():
                #reversed_transfer = split[1]+'-'+split[0]
                P_new = - ENTSOE_exchange_data['Power transfer'].loc[split[1]+'-'+split[0]]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
            else: #elif area_transfer not in ENTSOE_exchange_data['Power transfer'].keys(): #Might be multiple links out of country, need for disaggregation
                #export/import data is not retrieved
                P_new = row[index_P]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
                '''area_transfer = area_transfer[:2] + '-' + area_transfer[-2:]
                P_new = (ENTSOE_exchange_data['Power transfer'].loc[area_transfer]/
                         PowerExc_by_country.get(area[:2])*row[index_P])
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]'''

        else: #national loads
            P_new = row[index_P] * ENTSOE_load_data['Power consumption'].loc[area] / PowerCon_by_area.get(area)
            row[index_P] = P_new
            row[index_Q] = P_new * cot_phi


    #Adds a virtual line with generator to be disconnected
    MThesis.add_virtual_line(model, fault_bus)
    add_virtual_gen = MThesis.add_virtual_gen(model, fault_bus, fault_P, fault_Sn)
    # ------------------------------Updating the inertia of the system based on the kinetic energy of the EPS-----------------------------------
    area_by_bus['Virtual bus'] = model['buses'][-1][index_area] #adding to mapping
    index_H = model['generators']['GEN'][0].index('H')
    S_EPS = 0 #Nominal power of EPS
    H_EPS = 0 #Inertia time constant of EPS
    Ek_EPS = 0 #Kinetic energy of EPS
    # updating S_n
    for row in model['generators']['GEN'][1:]:
        #row[index_H] * = 1
        S_EPS += row[index_Sn]
        Ek_EPS += row[index_Sn] * row[index_H]
    H_EPS = Ek_EPS/S_EPS #Intertia time constant
    scaling = kinetic_energy_eps/Ek_EPS

    # updating S_n and scaling inertia
    for row in model['generators']['GEN'][1:]:
        row[index_H] *= scaling  # Apply the scaling factor to the inertia constant

    #Frequency bias:
    index_droop = model['gov']['HYGOV'][0].index('R')
    Freq_bias = MThesis.calc_frequency_bias(model)

    #Freeing up memory. These are not needed anymore
    del index_P, index_Sn 
    del index_area, from_count, cot_phi, load_name, index_Q, index_H, added
    del other_from_count, other_load_name, other_to_count, other_transfer, area_transfer
    del to_count, transfer_code, fault_Sn, fault_P, P_new, P_specified

    ps = dps.PowerSystemModel(model=model)
    ps.use_numba = True

    if display_pf:
        display_power_flow(ps, model, international_links, fault_bus, PowerExc_by_country)

    if display_pf:
        display_power_flow(ps, model, international_links, fault_bus, PowerExc_by_country)
    return ps

def init_VSC(ps):
    """
    Initializes the VSC-HVDC transmission in the Nordic 45 system from N45_case_data folder.

    Parameters:
    ps : PowerSystemModel
        The power system model.
    """

    
    vsc_international_links = {'L5230-1': 'NO_2-DE', 'L5240-2': 'NO_2-GB','L8700-2': 'SE_4-LT', 'L7020-1': 'FI-EE'} #Load names of international links with VSC-HVDC
    
    vsc_power_exchange = {'NO_2-DE': 0.0, 'NO_2-GB': 0.0, 'SE_4-LT': 0, 'FI-EE': 0.0} #Power exchange with VSC-HVDC

    path = 'inertia_sim/N45_case_data_NordLink/'
    ENTSOE_gen_data, ENTSOE_load_data, ENTSOE_exchange_data = MThesis.Import_data_ENTSOE(path)

    for link, load in ENTSOE_exchange_data.iterrows():
        if link in vsc_power_exchange.keys():
            vsc_power_exchange[link] = load['Power transfer']

    for row in ps.model['vsc']['VSC_SI']:
        if row[0] == 'name':
            continue
        else:
            link = row[0]
            if link in vsc_power_exchange.keys():
                row[2] = -vsc_power_exchange[link]/ps.vsc['VSC_SI'].par['S_n']

    ps2 = dps.PowerSystemModel(model=ps.model)
    return ps2
    # for name in ps.loads['Load'].par['name']:
    #     if name in vsc_international_links.keys():
    #         ps.loads['Load'].y_load = 0 #Disconnecting the load
            
        
    # for name, load in vsc_power_exchange.items():
    #     for index in range(len(ps.vsc['VSC_SI'].par['name'])):
    #         if name == ps.vsc['VSC_SI'].par['name'][index]:
    #             power = -load/ps.vsc['VSC_SI'].par['S_n']
    #             ps.vsc['VSC_SI'].set_input('p_ref', power)
    
            

def gen_trip(ps, fault_bus = '7000',fault_Sn = 1400,fault_P = 1400,kinetic_energy_eps = 300e3, folderandfilename = 'Base/300MWs',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False):
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
        If True, the VSC is included in the simulation.
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

def run_sensitivity(powersystem, sens_par=str, sens_vars=list,foldername = str):
    for sens_var in sens_vars:
        powersystem.gov['HYGOV'].par[sens_par] = sens_var  # Sensitivity analysis
        #how to get the index of the parameter in the model
        index = powersystem.model['gov']['HYGOV'][0].index(sens_par)
        #updating the model as well as the powersystem
        for row in powersystem.model['gov']['HYGOV']:
            #Skip the first row
            if row[0] == 'name':
                continue
            else:
                row[index] = sens_var
        ps2 = dps.PowerSystemModel(model=powersystem.model)
        gen_trip(ps=ps2, folderandfilename=foldername+str(sens_par)+'_'+str(sens_var), t_end=50, t_trip=17.6, event_flag=True)



def display_power_flow(ps, model, international_links, fault_bus, PowerExc_by_country):
    """
    Displays the power flow in the Nordic 45 system.
    Parameters:
    model_data : dictionary
        Dictionary containing the model data.
    """
    
    ps.init_dyn_sim()
    x0 = ps.x0.copy()
    v0 = ps.v0.copy()
    
    Flows = {'NO_1-NO_2': 0.0, 'NO_1-NO_5': 0.0, 'NO_5-NO_2': 0.0, 'NO_1-NO_3': 0.0, 'NO_4-NO_3': 0.0, 'NO_5-NO_3': 0.0,
             'NO_1-SE_3': 0.0, 'NO_3-SE_2': 0.0, 'NO_4-SE_1': 0.0, 'NO_4-SE_2': 0.0, 'NO_4-FI': 0.0, 'SE_1-FI': 0.0,
             'SE_1-SE_2': 0.0, 'SE_2-SE_3': 0.0, 'SE_3-SE_4': 0.0, 'SE_3-FI': 0.0}
    
    # Making dictionary to map bus to area
    area_by_bus = {} #From bus find area
    bus_by_area = {} #From area find buses
    index_bus_name = model['buses'][0].index('name')
    index_area = model['buses'][0].index('Area')
    for bus in model['buses'][1:]:
        area = bus[index_area]
        area_by_bus[bus[index_bus_name]] = area
        if area not in bus_by_area:
            bus_by_area[area] = [bus[index_bus_name]]
        else:
            bus_by_area[area].append(bus[index_bus_name])

    
    s_base = ps.s_n

    #Flow along lines
    for from_bus, to_bus, p_to, p_from in zip(
        ps.lines['Line'].par['from_bus'], ps.lines['Line'].par['to_bus'],
        ps.lines['Line'].p_to(x0, v0).copy(), ps.lines['Line'].p_from(x0, v0).copy()):

        from_area = area_by_bus.get(from_bus)
        to_area = area_by_bus.get(to_bus)
        if from_area + '-' + to_area in Flows:
            Flows[from_area + '-' + to_area] -= p_to * s_base
        elif to_area + '-' + from_area in Flows:
            Flows[to_area + '-' + from_area] -= p_from * s_base
    
    #Flow along Transformer-lines
    for fbus, tbus, p_to, p_from in zip(
            ps.trafos['Trafo'].par['from_bus'], ps.trafos['Trafo'].par['to_bus'],\
            ps.trafos['Trafo'].p_to(x0, v0).copy(), ps.trafos['Trafo'].p_from(x0, v0).copy()):
        #S_base = model['base_mva']
        from_area = area_by_bus.get(fbus)
        to_area = area_by_bus.get(tbus)
        if from_area + '-' + to_area in Flows:
            Flows[from_area + '-' + to_area] -= p_to * s_base
        elif to_area + '-' + from_area in Flows:
            Flows[to_area + '-' + from_area] -= p_from * s_base

    #Checking if flow matches production - consumption:
    generation = {'FI': 0.0, 'NO_1': 0.0, 'NO_2': 0.0, 'NO_3': 0.0, 'NO_4': 0.0, 'NO_5': 0.0,
                  'SE_1': 0.0, 'SE_2': 0.0, 'SE_3': 0.0, 'SE_4': 0.0} #Generation in each area
    consumption = generation.copy() #Consumption in each area
    power_out = generation.copy() #Simulated power output from each area
    export = generation.copy() #Export data

    for bus, P in zip(ps.gen['GEN'].par['bus'], ps.gen['GEN'].P_e(x0, v0).copy()):
            area = area_by_bus.get(bus)
            generation[area] += P
    
    total_cons_test = export.copy()
    for name, bus, P in zip(ps.loads['Load'].par['name'], ps.loads['Load'].par['bus'], ps.loads['Load'].p(x0, v0).copy()):
        area = area_by_bus.get(bus)
        reverse = international_links[name].split('-') if name in international_links else None
        if reverse is None:  # name not in international_links.keys():
            consumption[area] += P * s_base
        elif international_links[name] in Flows.keys():
            Flows[international_links[name]] += P * s_base
        elif reverse[1] + '-' + reverse[0] in Flows.keys():
            Flows[reverse[1] + '-' + reverse[0]] += P * s_base
        else:
            export[area] += P * s_base
        total_cons_test[area] += P * s_base
    
        #This is the power exchange from simulation:
    for key, val in Flows.items():
        #Flow_filtered = [(key, value) for key, value in Flows.items() if area in key]
        from_to = key.split('-')
        power_out[from_to[0]] += val
        power_out[from_to[1]] -= val
    
    for name, power, s_b in zip(
        ps.vsc['VSC_SI'].par['name'],ps.vsc['VSC_SI'].par['p_ref'], ps.vsc['VSC_SI'].par['S_n']): 
        area = name.split('-')[0]
    
        if area in export.keys():
  
            export[area] += power * s_b
           

    



    print(pd.DataFrame({'Transfer': list(Flows.keys()), 'Power [MW]': list(Flows.values())}))
    print(pd.DataFrame({'Area': list(generation.keys()), 'Generation': list(generation.values())}))
    print(pd.DataFrame({'Area': list(consumption.keys()), 'Consumption': list(consumption.values())}))
    print(pd.DataFrame({'Transfer': list(export.keys()), 'exchange': list(export.values())}))
    print(pd.DataFrame({'Area': list(total_cons_test.keys()), 'total cons': list(total_cons_test.values())}))
    print(pd.DataFrame({'Area export': list(PowerExc_by_country.keys()), 'exchange': list(PowerExc_by_country.values())}))
    for area, gen, con, pflow, exc in zip(
            generation, generation.values(), consumption.values(), power_out.values(), export.values()):
        print('Area:', area, ' Generation - consumption: ', round(gen-con), ' After simulation: ', round(pflow+exc))

    #This should give the same
    total_loss = (ps.lines['Line'].p_loss_tot(x0, v0) + ps.trafos['Trafo'].p_loss_tot(x0, v0)) * s_base
    print('Balance:',sum(generation.values())-sum(consumption.values()) - sum(export.values()))
    print('Losses: ', total_loss)


    #Checking balance
    print('FI-SE_3',ps.loads['Load'].par['name'][-12], ps.loads['Load'].p(x0, v0).copy()[-12]*s_base)
    print('SE_3-FI',ps.loads['Load'].par['name'][3], ps.loads['Load'].p(x0, v0).copy()[3]*s_base)
    print(sum(ps.gen['GEN'].par['S_n']))

    path = '/Users/noralillelien/Documents/TOPS_low_inertia/'

    #Open the Excel file in append mode using openpyxl engine. To save for printing initial power flow
    # with pd.ExcelWriter(path + 'dataframes_DynPSSimPy.xlsx',
    #                     engine='openpyxl') as writer:

    #     # Save the new DataFrame to the existing sheet (if it doesn't exist, it will create a new sheet)
    #     pd.DataFrame({'Area': list(generation.keys()), 'Generation': list(generation.values())}) \
    #         .to_excel(writer, sheet_name='DynPSS_Gen', index=True)

    #     pd.DataFrame({'Area': list(consumption.keys()), 'Consumption': list(consumption.values())}) \
    #         .to_excel(writer, sheet_name='DynPSS_Con', index=True)

    #     pd.DataFrame({'Transfer': list(Flows.keys()), 'Power [MW]': list(Flows.values())}) \
    #         .to_excel(writer, sheet_name='DynPSS_trans', index=True)

    #     pd.DataFrame({'Link': list(export.keys()), 'exchange': list(export.values())}) \
    #         .to_excel(writer, sheet_name='DynPSS_export', index=True)

    #     print('Excel writing complete')


def init_n45_with_VSC(model_data, display_pf, fault_bus = '7000',fault_Sn = 1400,fault_P = 1400,kinetic_energy_eps = 300e3):
    """
    Initializes the Nordic 45 system from "N45_case_data" folder with the specified fault bus, fault Sn, fault P and kinetic energy of the EPS.

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

    """
    #data_path = 'inertia_sim/N45_case_data/'
    data_path = 'inertia_sim/N45_case_data_NordLink/'

    #Accessing the case data and saving it in Dataframe format
    ENTSOE_gen_data, ENTSOE_load_data, ENTSOE_exchange_data = MThesis.Import_data_ENTSOE(data_path)
    # List of international power links: Should be updated if added links or using another model than N45
    international_links = {'L5230-1': 'NO_2-DE', 'L5240-2': 'NO_2-GB', 'L5210-1': 'NO_2-DK',
                           'L3360-1': 'SE_3-DK', 'L8600-1': 'SE_4-DK', 'L8700-1': 'SE_4-PL',
                           'L8600-2': 'SE_4-DE', 'L8700-2': 'SE_4-LT', 'L7020-1': 'FI-EE',
                           'L3020-1': 'SE_3-FI', 'L7010-1': 'FI-SE_3', 'L5220-1': 'NO_2-NL',
                           'L7020-2': 'FI-RU'}
    #Initializing the model from the load data in n45_with_controls
    model = model_data.load()

    # ------------------------------ Reparameterization to fit specific time-senario -----------------------------------
    index_area = model['buses'][0].index('Area')
    area_mapping = {24: 'SE_4', 23: 'SE_3', 22: 'SE_2', 21: 'SE_1', 11: 'NO_1', 12: 'NO_2', 13: 'NO_3',
        14: 'NO_4', 15: 'NO_5', 31: 'FI'} #integers from original N45, strings from Transparency platform
    #Change from numbers to strings from area_mapping to have consistent area names
    for bus in model['buses'][1:]:
        area = bus[index_area]
        if area in area_mapping:
            bus[index_area] = area_mapping[area]
        else:
            print(f"ERROR: Unknown price area {area}")

    
    # Making dictionary to map bus to area
    area_by_bus = {} #From bus find area
    bus_by_area = {} #From area find buses
    index_bus_name = model['buses'][0].index('name')
    index_area = model['buses'][0].index('Area')
    for bus in model['buses'][1:]:
        area = bus[index_area]
        area_by_bus[bus[index_bus_name]] = area
        if area not in bus_by_area:
            bus_by_area[area] = [bus[index_bus_name]]
        else:
            bus_by_area[area].append(bus[index_bus_name])
    fault_area = area_by_bus.get(fault_bus)



    #------------------------------Updating the Power generation in the n45_with_controls model-----------------------------------
    #To retrieve total specified power generation in an area
    # Initialize a list to store specified power generation by area code
    PowerGen_by_area = {}
    # Iterate through the 'GEN' data and extract 'bus' and 'P' columns
    index_bus_name = model['generators']['GEN'][0].index('bus')
    index_gen = model['generators']['GEN'][0].index('name')
    index_P = model['generators']['GEN'][0].index('P')


    all_gen = set()
    for row in model['generators']['GEN'][1:]:
        bus_name = row[index_bus_name]
        gen_name = row[index_gen]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        if area not in PowerGen_by_area:
            PowerGen_by_area[area] = 0
        PowerGen_by_area[area] = PowerGen_by_area[area] + P_specified
        all_gen.add(gen_name)


    #------------------------------Updating the Power consumption in the n45_with_controls model-----------------------------------
    PowerCon_by_area = {}
    PowerExc_by_country = {} #Used for scaling when mulitple export/import power links between countries
    index_name = model['loads'][0].index('name')
    index_bus_name = model['loads'][0].index('bus')
    index_P = model['loads'][0].index('P')
    load_sum = 0.0
    added = set() #To not count interconnectors multiple times
    for row in model['loads'][1:]:
        bus_name = row[index_bus_name]
        load_name = row[index_name]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        load_sum += P_specified
        if load_name not in international_links.keys(): #If load inside model
            if area not in PowerCon_by_area:
                PowerCon_by_area[area] = 0.0
            PowerCon_by_area[area] = PowerCon_by_area[area] + P_specified

        elif load_name in international_links.keys(): #if import/export cable
            transfer_code = international_links[load_name]
            from_count = transfer_code[:2]
            to_count = transfer_code[-2:]
            for other_load_name, other_transfer in international_links.items():
                other_from_count = other_transfer[:2]
                other_to_count = other_transfer[-2:]
                if from_count == other_from_count and to_count == other_to_count \
                        and transfer_code != other_transfer and transfer_code not in added:
                    if from_count not in PowerExc_by_country:
                        PowerExc_by_country[from_count] = 0.0
                    PowerExc_by_country[from_count] = PowerExc_by_country[from_count] + P_specified
                    added.add(transfer_code)
                elif from_count == other_to_count and to_count == other_from_count \
                        and transfer_code != other_transfer and transfer_code not in added:
                    if from_count not in PowerExc_by_country:
                        PowerExc_by_country[from_count] = 0.0
                    PowerExc_by_country[from_count] = PowerExc_by_country[from_count] - P_specified
                    added.add(transfer_code)


    
    # ------------------------------Updating generators' specified powers----------------------------------------------
    index_bus_name = model['generators']['GEN'][0].index('bus')
    index_gen = model['generators']['GEN'][0].index('name')
    index_P = model['generators']['GEN'][0].index('P')
    index_Sn = model['generators']['GEN'][0].index('S_n')
    for row in model['generators']['GEN'][1:]:
        bus_name = row[index_bus_name]
        P_specified = row[index_P]
        area = area_by_bus.get(bus_name)
        gen_name = row[index_gen]
        row[index_P] = (P_specified * ENTSOE_gen_data['Power generation'].loc[area] / PowerGen_by_area.get(area))
        row[index_Sn] = row[index_Sn] * ENTSOE_gen_data['Power generation'].loc[area] / PowerGen_by_area.get(area)



    # ------------------------------Updating loads' active and reactive power consumptions------------------------------
    index_name = model['loads'][0].index('name')
    index_bus_name = model['loads'][0].index('bus')
    index_P = model['loads'][0].index('P')
    index_Q = model['loads'][0].index('Q')

    for row in model['loads'][1:]:
        bus_name = row[index_bus_name]
        load_name = row[index_name]
        area = area_by_bus.get(bus_name)
        cot_phi = row[index_Q] / row[index_P] if not -1 < row[index_P] < 1 else 0
        if row[index_name] in international_links.keys(): #if international link
            area_transfer = international_links.get(load_name)
            split = area_transfer.split('-')
            if area_transfer in ENTSOE_exchange_data['Power transfer'].keys(): #Only one link out of country
                P_new = ENTSOE_exchange_data['Power transfer'].loc[area_transfer]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
            elif split[1]+'-'+split[0] in ENTSOE_exchange_data['Power transfer'].keys():
                #reversed_transfer = split[1]+'-'+split[0]
                P_new = - ENTSOE_exchange_data['Power transfer'].loc[split[1]+'-'+split[0]]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
            else: #elif area_transfer not in ENTSOE_exchange_data['Power transfer'].keys(): #Might be multiple links out of country, need for disaggregation
                #export/import data is not retrieved
                P_new = row[index_P]
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]
                '''area_transfer = area_transfer[:2] + '-' + area_transfer[-2:]
                P_new = (ENTSOE_exchange_data['Power transfer'].loc[area_transfer]/
                         PowerExc_by_country.get(area[:2])*row[index_P])
                row[index_P] = P_new if P_new != 0 else 0.01
                row[index_Q] = cot_phi * P_new if P_new != 0 else row[index_Q]'''

        else: #national loads
            P_new = row[index_P] * ENTSOE_load_data['Power consumption'].loc[area] / PowerCon_by_area.get(area)
            row[index_P] = P_new
            row[index_Q] = P_new * cot_phi


    #Adds a virtual line with generator to be disconnected
    MThesis.add_virtual_line(model, fault_bus)
    add_virtual_gen = MThesis.add_virtual_gen(model, fault_bus, fault_P, fault_Sn)
    # ------------------------------Updating the inertia of the system based on the kinetic energy of the EPS-----------------------------------
    area_by_bus['Virtual bus'] = model['buses'][-1][index_area] #adding to mapping
    index_H = model['generators']['GEN'][0].index('H')
    S_EPS = 0 #Nominal power of EPS
    H_EPS = 0 #Inertia time constant of EPS
    Ek_EPS = 0 #Kinetic energy of EPS
    # updating S_n
    for row in model['generators']['GEN'][1:]:
        #row[index_H] * = 1
        S_EPS += row[index_Sn]
        Ek_EPS += row[index_Sn] * row[index_H]
    H_EPS = Ek_EPS/S_EPS #Intertia time constant
    scaling = kinetic_energy_eps/Ek_EPS

    # updating S_n and scaling inertia
    for row in model['generators']['GEN'][1:]:
        row[index_H] *= scaling  # Apply the scaling factor to the inertia constant

    #Frequency bias:
    index_droop = model['gov']['HYGOV'][0].index('R')
    Freq_bias = MThesis.calc_frequency_bias(model)

    #Freeing up memory. These are not needed anymore
    del index_P, index_Sn 
    del index_area, from_count, cot_phi, load_name, index_Q, index_H, added
    del other_from_count, other_load_name, other_to_count, other_transfer, area_transfer
    del to_count, transfer_code, fault_Sn, fault_P, P_new, P_specified

    ps = dps.PowerSystemModel(model=model)
    ps.use_numba = True

    ps2 = init_VSC(ps)

    if display_pf:
        display_power_flow(ps, model, international_links, fault_bus, PowerExc_by_country)
    return ps2