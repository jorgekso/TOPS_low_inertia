import numpy as np 


def activate_FFR(ps, mean_freq,t, ffr_names,activated,v,t_FFR,t_end_FFR):
    
    threshold = 49.7
    t_delay = 1.2
   
    if (mean_freq <= threshold) and activated == False:
        activated = True
        t_FFR = t+t_delay
        t_end_FFR = t_FFR+30
        print(f'FFR detected at t = {t}')
    P_FFR = 50 #Max FFR 50 MW
    if activated == True and t_end_FFR >= t >= t_FFR:
        for load_name in ps.loads['DynamicLoad'].par['name']:
            if load_name in ffr_names:
                index = np.where(ps.loads['DynamicLoad'].par['name'] == load_name)[0]
                v0 = ps.loads['DynamicLoad'].v0(index)
                P = (ps.loads['DynamicLoad'].par['P'][index]-P_FFR)/ps.loads['DynamicLoad'].sys_par['s_n']
                Q = ps.loads['DynamicLoad'].par['Q'][index]/ps.loads['DynamicLoad'].sys_par['s_n']
                z = np.conj(1/(P+1j*Q))
                y = 1/z
                g = y.real
                b = y.imag
                ps.loads['DynamicLoad'].set_input('g_setp', g, index)
                ps.loads['DynamicLoad'].set_input('b_setp', b, index)
    else:
        for load_name in ps.loads['DynamicLoad'].par['name']:
            if load_name in ffr_names:
                index = np.where(ps.loads['DynamicLoad'].par['name'] == load_name)[0]
                v0 = ps.loads['DynamicLoad'].v0(index)
                P = ps.loads['DynamicLoad'].par['P'][index]/ps.loads['DynamicLoad'].sys_par['s_n']
                Q = ps.loads['DynamicLoad'].par['Q'][index]/ps.loads['DynamicLoad'].sys_par['s_n']
                z = np.conj(1/(P+1j*Q))
                y = 1/z
                g = y.real
                b = y.imag
                ps.loads['DynamicLoad'].set_input('g_setp', g, index)
                ps.loads['DynamicLoad'].set_input('b_setp', b, index)


        
    return activated,t_FFR,t_end_FFR     

            

if __name__ == '__main__':
    
    import init_N45 as func
    import tops.ps_models.n45_2030 as n45

    from inertia_sim.fault_events import gen_trip, HVDC_cable_trip


    energy_mix = {'FI': {'Wind': 0.7, 'Hydro': 0.1, 'Nuclear': 0.2, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_1': {'Wind': 0.6, 'Hydro': 0.4, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_2': {'Wind': 0.6, 'Hydro': 0.4, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_3': {'Wind': 0.4, 'Hydro': 0.6, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_4': {'Wind': 0.5, 'Hydro': 0.5, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_5': {'Wind': 0.0, 'Hydro': 1.0, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_1': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_2': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_3': {'Wind': 0.6, 'Hydro': 0.0, 'Nuclear': 0.4, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_4': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0}}


    ps = func.init_n45(model_data=n45,display_pf=False,energy_mix= energy_mix, 
                       data_path='inertia_sim/2030_scenario/',
                       kinetic_energy_eps=150e3,virtual_gen=False,spinning_reserve=4)
    
    
    SE_4 = ['WG8500-1', 'WG8500-2']
    SE3 = ['WG3000-1', 'WG3000-2', 'WG3300-1', 'WG3300-2', 'WG3359-1', 'WG3359-2']
    SE2 = ['WG3100-1', 'WG3100-2', 'WG3100-3', 'WG3245-1', 'WG3245-2', 'WG3245-3']
    SE1 = ['WG3115-1', 'WG3249-1', 'WG3249-2'] 
    NO_1 =  ['WG5120-1']
    NO_2 = ['WG5230-1', 'WG5230-2']
    NO_3 = ['WG5320-1']
    NO_4 = ['WG5420-1', 'WG5420-1']
    FI = ['WG7000-1', 'WG7000-2', 'WG7000-3', 'WG7100-1', 'WG71000-2', 'WG71000-3']

    FFR_sources= ['WG7000-1']

    
    HVDC_cable_trip(ps,folderandfilename = 'FFR_FI/50 MW',t=0,t_end=50,t_trip = 17.6,event_flag = True, 
                    link_name = 'NO_2-DE',FFR = True, FFR_sources = FFR_sources)
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    #func.gen_trip(ps=ps,fault_bus = '5230',fault_Sn = 792,fault_P = 792,kinetic_energy_eps = 300e3, 
    # folderandfilename = 'NordLink/test1',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False)
    # func.gen_trip(ps=ps,folderandfilename = '2030_scenario/test', fault_bus = '5230',fault_Sn = 1400,
    #               fault_P = 1400,event_flag=True, VSC=True, t_trip = 10.81)

    # func.HVDC_cable_trip(ps=ps,folderandfilename = 'Spinning reserves/2030 0,76',
    #                      link_name = 'NO_2-DE',t_trip=10.81,event_flag=False,t_end=50)
    

    
                






