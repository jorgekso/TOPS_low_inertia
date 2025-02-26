if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import init_N45 as func
    #iterates over the different kinetic energy scenarios
    import tops.ps_models.n45_with_controls_HVDC as n45
    ps = func.init_n45(model_data=n45,display_pf=True,data_path='2030_scenario/',kinetic_energy_eps=150e3)
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    #func.gen_trip(ps=ps,fault_bus = '5230',fault_Sn = 792,fault_P = 792,kinetic_energy_eps = 300e3, folderandfilename = 'NordLink/test1',t=0,t_end=50,t_trip = 17.6,event_flag = True,VSC=False)
    # func.gen_trip(ps=ps,folderandfilename = '2030_scenario/test', fault_bus = '5230',fault_Sn = 1400,
    #               fault_P = 1400,event_flag=True, VSC=True, t_trip = 10.81)
    func.HVDC_cable_trip(ps=ps,folderandfilename = '2030_scenario/test_HVDC_trip',line = 'L5230-1')