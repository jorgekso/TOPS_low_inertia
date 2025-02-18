if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import init_N45 as func
    #iterates over the different kinetic energy scenarios
    import tops.ps_models.n45_with_controls_HVDC as n45
    ps = func.init_n45(model_data=n45,display_pf=True)
    # func.run_sensitivity(ps,'r',[3.5,3,2.5,2,1.5],foldername = 'r_sensitivity/')
    func.gen_trip(ps=ps,folderandfilename = 'TGOV_tuning/T_3=10')
    
