if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import init_N45 as func
    #iterates over the different kinetic energy scenarios
    import tops.ps_models.n45_NordLink as n45

    data_path = 'inertia_sim/N45_case_data_NordLink/'
    ps = func.init_n45(model_data=n45, data_path= data_path, display_pf=True)
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    #func.gen_trip(ps=ps,fault_bus = '5230',fault_Sn = 792,fault_P = 792,kinetic_energy_eps = 300e3, folderandfilename = 'NordLink/test1',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False)
    func.gen_trip(ps=ps,folderandfilename = 'NordLink/base_fault', fault_bus = '5230',fault_Sn = 792,fault_P = 792,event_flag=True, VSC=True, t_trip = 10)
