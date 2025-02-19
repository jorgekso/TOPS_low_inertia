import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)

def run_sensitivity(powersystem, sens_par=str, sens_vars=list,foldername = str):
    for sens_var in sens_vars:
        powersystem.gov['HYGOV'].par[sens_par] = sens_var  # Sensitivity analysis
        #how to get the index of the parameter in the model
        index = powersystem.model['gov']['HYGOV'][0].index(sens_par)
        #updating the model as well as the powersystem
        for row in powersystem.model['gov']['HYGOV']:
            #Skip the first row
            if row[0] == 'name':
                continue
            else:
                row[index] = sens_var
        ps2 = dps.PowerSystemModel(model=powersystem.model)
        gen_trip(ps=ps2, folderandfilename=foldername+str(sens_par)+'_'+str(sens_var), t_end=50, t_trip=17.6, event_flag=True)