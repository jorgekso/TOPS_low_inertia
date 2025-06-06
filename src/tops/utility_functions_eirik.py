import numpy as np
import pandas as pd

# This file contains utility functions made for the master thesis of 2024.
# This is made for more readability


def HYGOV_to_simplified(ps):
    '''

    Function to convert original HYGOV model into a simplified model.
    As the original HYGOV is bugged.
    '''
    Hygov_name = ps['gov']['HYGOV'][0].index('name')
    Hygov_gen = ps['gov']['HYGOV'][0].index('gen')
    Hygov_R = ps['gov']['HYGOV'][0].index('R')
    Hygov_r = ps['gov']['HYGOV'][0].index('r')
    Hygov_D = ps['gov']['HYGOV'][0].index('D_turb')
    Hygov_Tf = ps['gov']['HYGOV'][0].index('T_f')
    Hygov_Tr = ps['gov']['HYGOV'][0].index('T_r')
    Hygov_Tg = ps['gov']['HYGOV'][0].index('T_g')
    Hygov_Tw = ps['gov']['HYGOV'][0].index('T_w')

    TGov_name = 0  # ps['gov']['TGOV1'][0].index('name')
    TGov_gen = 1  # ps['gov']['TGOV1'][0].index('gen')
    TGov_R = 2  # ps['gov']['TGOV1'][0].index('R')
    TGov_D = 3  # ps['gov']['TGOV1'][0].index('D_t')
    TGov_T1 = 4  # ps['gov']['TGOV1'][0].index('T_1')
    TGov_T2 = 5  # ps['gov']['TGOV1'][0].index('T_2')
    TGov_T3 = 6  # ps['gov']['TGOV1'][0].index('T_3')
    TGOV_T4 = 7
    TGov_Tg = 8
    TGov_Vmin = 9  # ps['gov']['TGOV1'][0].index('V_min')
    TGov_Vmax = 10  # ps['gov']['TGOV1'][0].index('V_max')
    # HYGOV ['name', 'gen', 'R', 'r', 'T_f', 'T_r', 'T_g', 'A_t', 'T_w', 'q_nl', 'D_turb', 'G_min', 'V_elm', 'G_max', 'P_N']
    # TGOV ['name', 'gen', 'R', 'D_t', 'V_min', 'V_max', 'T_1', 'T_2', 'T_3']
    ps['gov']['HYGOV_simple'] = [['name', 'gen', 'R', 'D_t', 'T_1', 'T_2', 'T_3', 'T_4', 'T_g', 'V_min', 'V_max']]
    for HYGOV in ps['gov']['HYGOV'][1:]:
        new_gov = ['', '', 0, 0, 0, 0, 0, 0, 0, 0, 0]  # ps['gov']['TGOV1'][-1].copy()
        new_gov[TGov_name] = HYGOV[Hygov_name]
        new_gov[TGov_gen] = HYGOV[Hygov_gen]
        new_gov[TGov_R] = HYGOV[Hygov_R] 
        new_gov[TGov_D] = HYGOV[Hygov_D] 
        new_gov[TGov_Tg] = HYGOV[Hygov_Tg]
        new_gov[TGov_T2] = HYGOV[Hygov_Tr]
        new_gov[TGov_T1] = HYGOV[Hygov_Tw] / 2
        new_gov[TGov_T3] = (HYGOV[Hygov_r] + new_gov[TGov_R]) * new_gov[TGov_T2] / new_gov[TGov_R]
        new_gov[TGOV_T4] = - new_gov[TGov_T1] * 2
        new_gov[TGov_Vmin] = 0
        new_gov[TGov_Vmax] = 1.5
        ps['gov']['HYGOV_simple'].append(new_gov)
    del ps['gov']['HYGOV']


def Import_data_ENTSOE(path):
    '''
    Retrieving data from Transparency platform
    Arguments
        path -- path to folder with case data
    '''
    # path = 'C:/Users/eirik/OneDrive - NTNU/Master/'
    # Retrieving data from Transparency platform
    # Reading the aggregated generation data from excel file
    ENTSOE_gen_data = pd.read_excel(
        path + 'dataframes_transparency.xlsx', sheet_name='Aggr_generation', index_col=0)
    # Reading the aggregated load data from excel file
    ENTSOE_load_data = pd.read_excel(
        path + 'dataframes_transparency.xlsx', sheet_name='Aggr_load', index_col=0)

    # Reading the aggregated exchange data from excel file (power links)
    ENTSOE_exchange_data = pd.read_excel(
        path + 'powerflow_Statnett.xlsx', sheet_name='aggr_exchange', index_col=0)
    return ENTSOE_gen_data, ENTSOE_load_data, ENTSOE_exchange_data

def Import_actual_data(path):
    '''
    path should be to a xlsx file
    '''
    #path = 'C:/Users/eirik/OneDrive - NTNU/Master/faktiske hendelser/utfall Olkiluoto.xlsx'
    return pd.read_excel(path)

def find_gen_wihtout_gov(model, all_gen):
    '''
    Returning a set containing names of generators without governor (TGOV or HYGOV)
    '''
    gen_withGov = set()
    # index_droop = model['gov']['HYGOV'][0].index('R')
    index_name_hygov = model['gov']['HYGOV'][0].index('gen')
    index_name_tgov = model['gov']['TGOV1'][0].index('gen')
    for row_gov in model['gov']['HYGOV'][1:]:
        gen_withGov.add(row_gov[index_name_hygov])
    for row_gov in model['gov']['TGOV1'][1:]:
        gen_withGov.add(row_gov[index_name_tgov])
    return all_gen.difference(gen_withGov)

def scale_impedance(model, impedance_scale, only_R=True):
    '''
    Scale line impedances of the model. Made for tuning of transmission lines.
    '''
    #impedance_scale = 1
    index_R = model['lines'][0].index('R')
    for row in model['lines'][1:]:
        row[index_R] *= impedance_scale
    index_R = model['transformers'][0].index('R')
    for row in model['transformers'][1:]:
        row[index_R] *= impedance_scale
    if not only_R:
        index_X = model['lines'][0].index('X')
        for row in model['lines'][1:]:
            row[index_X] *= impedance_scale
        index_X = model['transformers'][0].index('X')
        for row in model['transformers'][1:]:
            row[index_X] *= impedance_scale

def add_virtual_line(model, fault_bus):
    '''
    Adding virtual line to simulate generator disconnection. Should therefore be used with add_virtual_gen
    '''
    index_bus_name = model['buses'][0].index('name')
    for bus_info in model['buses'][1:]:
        if bus_info[index_bus_name] == fault_bus:
            new_bus = bus_info.copy()
            new_bus[index_bus_name] = 'Virtual bus'
            model['buses'].append(new_bus)
            break

    mapping_for_line = {
        'name': 'Virtual line',
        'from_bus': 'Virtual bus',
        'to_bus': fault_bus,
        'length': 1,
        'S_n': 0,
        'V_n': 0,
        'unit': 'p.u',
        'R': 1e-6,
        'X': 1e-6,
        'B': 0
    }
    mapping_for_gov = {
        'name': 'Virtual gov',
        'gen': 'Virtual gen',
        'R': 1,
        'D_t': 0.02,
        'V_min': 0,
        'V_max': 2,
        'T_1': 0.1,
        'T_2': 0.1,
        'T_3': 0.3
    }
    new_line = [mapping_for_line[element] for element in model['lines'][0]]
    model['lines'].append(new_line)

def add_virtual_gen(model,fault_bus, fault_P, fault_Sn):
    '''
    Adding a virtual generator to be disconnected.
    Parameters:
        model: network model (N45)
        fault_bus: bus where faulty generator is located
        fault_P: active power to be disconnected
        fault_Sn: nominal power to be disconnected
    '''
    S_tot = 0.0
    P_tot = 0.0
    Num = 0
    relevant_gens = []
    index_bus_name = model['generators']['GEN'][0].index('bus')
    index_gen_name = model['generators']['GEN'][0].index('name')
    index_P = model['generators']['GEN'][0].index('P')
    index_Sn = model['generators']['GEN'][0].index('S_n')
    for row in model['generators']['GEN'][1:]:
        if row[index_bus_name] == fault_bus:
            S_tot += row[index_Sn]
            P_tot += row[index_P]
            Num += 1
            relevant_gens.append(row)
    new_gen = relevant_gens[0].copy()  # Arbitrarily choosing the first generators parameters
    new_gen[index_bus_name] = 'Virtual bus'
    new_gen[index_gen_name] = 'Virtual gen'
    new_gen[index_P] = fault_P
    new_gen[index_Sn] = fault_Sn
    model['generators']['GEN'].append(new_gen)
    for gen in relevant_gens:  # total Sn and P must be equal when adding virtual generator
        gen[index_P] = (P_tot - fault_P) / Num
        gen[index_Sn] = (S_tot - fault_Sn) / Num
    return True

def load_to_disconnect(model, load_name: str):
    '''
    Moving load to virtual buss to disconnect that single load
        model: network model (N45)
        fault_bus: bus where faulty load is located
        load_name: name of load
    '''
    index_bus_name = model['loads'][0].index('bus')
    index_load_name = model['loads'][0].index('name')
    for row in model['loads'][1:]:
        if row[index_load_name] == load_name:
            row[index_bus_name] = 'Virtual bus'
            break

def calc_frequency_bias(model):
    '''
    Calculate frequency bias.
    '''
    index_name_hygov = model['gov']['HYGOV'][0].index('gen') if 'HYGOV' in model['gov'] else None
    index_gen_name = model['generators']['GEN'][0].index('name')
    index_name_tgov = model['gov']['TGOV1'][0].index('gen') if 'TGOV1' in model['gov'] else None
    index_name_hygov_simple = model['gov']['HYGOV_simple'][0].index('gen') if 'HYGOV_simple' in model['gov'] else None
    index_Sn = model['generators']['GEN'][0].index('S_n')
    index_droop_HYGOV = model['gov']['HYGOV'][0].index('R') if 'HYGOV' in model['gov'] else None
    index_droop_simple = model['gov']['HYGOV_simple'][0].index('R') if 'HYGOV_simple' in model['gov'] else None
    index_droop_tgov = model['gov']['TGOV1'][0].index('R') if 'TGOV1' in model['gov'] else None
    Freq_bias = 0  # Inverse droop
    P_HYGOV = 0
    P_TGOV1 = 0
    for row_gen in model['generators']['GEN'][1:]:
        found_in_hygov = False
        found_in_hygov_simple = False
        if index_name_hygov is not None:
            for row_gov in model['gov']['HYGOV']:
                if row_gov[index_name_hygov] == row_gen[index_gen_name]:
                    # row_gov[index_droop] = 0.045
                    Freq_bias += 1 / row_gov[index_droop_HYGOV] * row_gen[index_Sn]
                    P_HYGOV += row_gen[index_Sn]
                    found_in_hygov = True
                    break
        if found_in_hygov:
            continue
        if index_name_hygov_simple is not None:
            for row_gov in model['gov']['HYGOV_simple']:
                if row_gov[index_name_hygov_simple] == row_gen[index_gen_name]:
                    Freq_bias += 1 / row_gov[index_droop_simple] * row_gen[index_Sn]
                    P_HYGOV += row_gen[index_Sn]
                    found_in_hygov_simple = True
                    break
        if found_in_hygov_simple:
            continue
        if index_name_tgov is not None:
            for row_gov in model['gov']['TGOV1']:
                if row_gov[index_name_tgov] == row_gen[index_gen_name]:
                    # row_gov[index_droop] = 0.25
                    Freq_bias += 1 / row_gov[index_droop_tgov] * row_gen[index_Sn]
                    P_TGOV1 += row_gen[index_Sn]
                    break
    Freq_bias = Freq_bias / model['f']
    #print('P_HYGOV',P_HYGOV,'P_TGOV', P_TGOV1)
    return Freq_bias
