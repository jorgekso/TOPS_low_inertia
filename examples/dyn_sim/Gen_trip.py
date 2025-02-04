if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    import n45_functions as func
    #iterates over the different kinetic energy scenarios
    for i in range(100,400,50):
        func.gen_trip('3359',1400,1400,i*1e3,str(i)+'MWs')