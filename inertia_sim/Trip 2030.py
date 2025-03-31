if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import init_N45 as init
    import fault_events as fault
    
    #iterates over the different kinetic energy scenarios
    import tops.ps_models.n45_2030 as n45

    #Kladd for energimix fordeling
    #Energy mix for different areas

    # #Energy mix for Nordlink 
    # energy_mix_NordLink = {'FI': {'Wind': 0.218, 'Hydro': 0.334, 'Nuclear': 0.448, 'Solar': 0.0, 'Fossil': 0.0},
    #             'NO_1': {'Wind': 0.083, 'Hydro': 0.917, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'NO_2': {'Wind': 0.084, 'Hydro': 0.916, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'NO_3': {'Wind': 0.140, 'Hydro': 0.860, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'NO_4': {'Wind': 0.139, 'Hydro': 0.861, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'NO_5': {'Wind': 0.0, 'Hydro': 1.0, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'SE_1': {'Wind': 0.158, 'Hydro': 0.842, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'SE_2': {'Wind': 0.212, 'Hydro': 0.788, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
    #             'SE_3': {'Wind': 0.233, 'Hydro': 0.195, 'Nuclear': 0.572, 'Solar': 0.0, 'Fossil': 0.0},
    #             'SE_4': {'Wind': 0.8, 'Hydro': 0.2, 'Nuclear': 0, 'Solar': 0.0, 'Fossil': 0.0}}
    #Energy mix for 2030 worst case scenario
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
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    #func.gen_trip(ps=ps,fault_bus = '5230',fault_Sn = 792,fault_P = 792,kinetic_energy_eps = 300e3, 
    # folderandfilename = 'NordLink/test1',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False)
    # func.gen_trip(ps=ps,folderandfilename = '2030_scenario/test', fault_bus = '5230',fault_Sn = 1400,
    #               fault_P = 1400,event_flag=True, VSC=True, t_trip = 10.81)

    fault.HVDC_cable_trip(ps=ps,folderandfilename = 'Combining FFR and SI/400MW FFR and K_SI=0.05', 
                            event_flag=True, FFR_sources=['L3000-1','L3100-1','L5120-1','L7000-1'])


