import tops.ps_models.n45_with_controls as model_data

from init_N45 import init_n45

if __name__ == '__main__':
    #This code is used to generate a trip of a 1400MW generator in the 3359 bus of the Nordic 45 system.
    

    
    data_path = 'inertia_sim/N45_case_data/'


    ps = init_n45(model_data, data_path, False, VSC_HVDC=True)

    vsc_international_links = {'L5230-1': 'NO_2-DE', 'L5240-2': 'NO_2-GB','L8700-2': 'SE_4-LT', 'L7020-1': 'FI-EE'}

    for name, power in zip(ps.loads['Load'].par['name'], ps.loads['Load'].par['P']):
        if name in vsc_international_links.keys():
            if power != 0:
                print('Loads not deleted')
            else:
                print('Load deleted')


    # print(ps.vsc['VSC_SI'].par['p_ref'])
    
    
    # ps2 = init_n45(model_data, data_path, False, VSC_HVDC=True)

    # print(ps2.vsc['VSC_SI'].par['p_ref'])
    
    

    


