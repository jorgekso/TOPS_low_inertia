import tops.ps_models.n45_with_controls_HVDC as model_data

if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    from init_N45 import init_VSC, init_n45

    #iterates over the different kinetic energy scenarios
    
    ps = init_n45(model_data)
    init_VSC(ps)


