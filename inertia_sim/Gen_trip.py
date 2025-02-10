if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import n45_functions as func
    #iterates over the different kinetic energy scenarios
    
    func.gen_trip('7000',1400,1400,300*1e3,'pf_tests/negative_flow_with_fault',0,70,37.6,True, True)