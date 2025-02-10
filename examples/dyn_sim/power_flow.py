
import tops.ps_models.n45_with_controls_HVDC as model_data 
from n45_functions import init_n45 
import pandas as pd


        
    
    







if __name__ == '__main__':

    ps = init_n45()

    print(ps.gen['GEN'].par['name'])

    



    


    

    
   
    
    