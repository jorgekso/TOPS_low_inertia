if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import init_N45 as func
    #iterates over the different kinetic energy scenarios
    import tops.ps_models.n45_with_controls_HVDC as n45
    func.gen_trip(fault_bus = '7000',fault_Sn = 1400,fault_P=1400,kinetic_energy_eps=300*1e3, 
                  folderandfilename= 'PSS/NoPSS',t=0,t_end=70,t_trip=37.6,event_flag=True,model_data=n45)
    
