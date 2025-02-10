if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import n45_functions as func
    #iterates over the different kinetic energy scenarios
    
    func.test_init_VSC('7000',1400,1400,300*1e3,'test_vsc/test1',0,70)