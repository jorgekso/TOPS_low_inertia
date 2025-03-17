import numpy as np 


# def activate_FFR(ps, mean_freq,t, vsc_names,activated):
    
#     threshold = 49.7
   
#     if (mean_freq <= threshold) and activated == False:
#         activated = True
#         print(f'FFR activated at t = {t}')
#         P_FFR = 50 #Max FFR 50 MW

#         for name in ps.vsc['VSC_SI'].par['name']:

#             if name in vsc_names:
#                 idx = np.where(ps.vsc['VSC_SI'].par['name'] == name)[0][0]
#                 p_pre = ps.vsc['VSC_SI'].par['p_ref'][idx]
#                 p_new = p_pre + P_FFR/ps.vsc['VSC_SI'].par['S_n'][idx]

#                 if p_new > ps.vsc['VSC_SI'].par['S_n'][idx]:
#                     p_new = ps.vsc['VSC_SI'].par['S_n'][idx]
#                 ps.vsc['VSC_SI'].set_input('p_ref', p_new, idx)

#                 # print(f'FFR activated at {name}')
#                 # print(f'power injected = {P_FFR + p_pre*ps.vsc['VSC_SI'].par['S_n'][idx]} MW')
#     return activated       


def activate_FFR(ps, local_freq, t, FFR_sources, activated, t_FFR, x,v, t_duration = 30):
    
    threshold = 49.7
    P_FFR = 200 #MW
    
    t_delay = 1.3
    


    FFR_type = check_FFR_type(ps, FFR_sources)
    

    if (local_freq <= threshold) and activated == False:
        activated = True
        t_FFR = t + t_delay
        print(round_timestep(t_FFR))
        print(round_timestep(t_FFR + t_duration) )

    
   
    if activated == True:
        if FFR_type == 'Load':
        
                if (round_timestep(t) == round_timestep(t_FFR) ):
                    print('checkpoint')
                    for name in FFR_sources:
                        idx = np.where(ps.loads['Load'].par['name'] == name)[0][0]
                        print(f'Before FFR is activated {ps.loads['Load'].par['P'][idx]}')
                        
                        #ps.loads['Load'].activate_FFR(P_FFR, idx)
                        ps.loads['Load'].set_input('P', ps.loads['Load'].par['P'][idx] - P_FFR, idx)
            
                        print(f'After FFR is activated {ps.loads['Load'].par['P'][idx]}')
                    
                if round_timestep(t) == round_timestep(t_FFR + t_duration):
                    
                    print(round_timestep(t_FFR + t_duration))
                    for name in FFR_sources:
                        idx = np.where(ps.loads['Load'].par['name'] == name)[0][0]
                        ps.loads['Load'].set_input('P', ps.loads['Load'].par['P'][idx] + P_FFR, idx)
                        #ps.loads['Load'].activate_FFR(-P_FFR, idx)
                       
                   
            
            
        elif FFR_type == 'VSC':
            for name in ps.vsc['VSC_SI'].par['name']:
                idx = np.where(ps.vsc['VSC_SI'].par['name'] == name)[0][0]
                if  t <= (t + t_duration):
                    activated = True
                    ps.vsc['VSC_SI'].activate_FFR(P_FFR, idx)
                else:
                    activated = False
                    ps.vsc['VSC_SI'].activate_FFR(-P_FFR, idx)
                
    return activated, t_FFR



def check_FFR_type(ps, FFR_providers):

    for provider in FFR_providers:
        if provider in ps.loads['Load'].par['name']:
            FFR_type = 'Load'
        else:
            FFR_type = 'VSC'
    return FFR_type 

def round_timestep(value):
    return round(value/0.005)*0.005
            

if __name__ == '__main__':
    
    import init_N45 as init
    import tops.ps_models.n45_tuned as n45

    from inertia_sim.fault_events import gen_trip, HVDC_cable_trip



    SE_4 = ['WG8500-1', 'WG8500-2']
    SE3 = ['WG3000-1', 'WG3000-2', 'WG3300-1', 'WG3300-2', 'WG3359-1', 'WG3359-2']
    SE2 = ['WG3100-1', 'WG3100-2', 'WG3100-3', 'WG3245-1', 'WG3245-2', 'WG3245-3']
    SE1 = ['WG3115-1', 'WG3249-1', 'WG3249-2'] 
    NO_1 =  ['WG5120-1']
    NO_2 = ['WG5230-1', 'WG5230-2']
    NO_3 = ['WG5320-1']
    NO_4 = ['WG5420-1', 'WG5420-1']
    FI = ['WG7000-1', 'WG7000-2', 'WG7000-3', 'WG7100-1', 'WG71000-2', 'WG71000-3']

    Load = ['L3100-1', 'L3000-3','L3300-2']

    FFR_sources= Load

    

    #Kladd for energimix fordeling
    #Energy mix for different areas

    # #Energy mix for Nordlink 
    # energy_mix = {'FI': {'Wind': 0.218, 'Hydro': 0.334, 'Nuclear': 0.448, 'Solar': 0.0, 'Fossil': 0.0},
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
    energy_mix = {'FI': {'Wind': 0.7, 'Hydro': 0.1, 'Nuclear': 0.2, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_1': {'Wind': 0.5, 'Hydro': 0.5, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_2': {'Wind': 0.4, 'Hydro': 0.6, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_3': {'Wind': 0.4, 'Hydro': 0.6, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_4': {'Wind': 0.5, 'Hydro': 0.5, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'NO_5': {'Wind': 0.0, 'Hydro': 1.0, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_1': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_2': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_3': {'Wind': 0.6, 'Hydro': 0.0, 'Nuclear': 0.4, 'Solar': 0.0, 'Fossil': 0.0},
                'SE_4': {'Wind': 0.95, 'Hydro': 0.05, 'Nuclear': 0.0, 'Solar': 0.0, 'Fossil': 0.0}}


    ps = init.init_n45(model_data=n45,display_pf=False,energy_mix= energy_mix, 
                       data_path= 'inertia_sim/2030_scenario/',
                       virtual_gen=False,spinning_reserve=1.2)
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    #func.gen_trip(ps=ps,fault_bus = '5230',fault_Sn = 792,fault_P = 792,kinetic_energy_eps = 300e3, 
    # folderandfilename = 'NordLink/test1',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False)
    # func.gen_trip(ps=ps,folderandfilename = '2030_scenario/test', fault_bus = '5230',fault_Sn = 1400,
    #               fault_P = 1400,event_flag=True, VSC=True, t_trip = 10.81)

    HVDC_cable_trip(ps=ps,folderandfilename = 'FFR/FFR_test1',
                            t_trip=10.81,event_flag=True,t_end=50, FFR_sources=FFR_sources)

    
                






