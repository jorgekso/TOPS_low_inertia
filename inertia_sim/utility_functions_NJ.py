import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
import json


def read_to_file(result, file_path):
    """
    Reads the results to a .json files.

    Parameters:
    results : dictionary
        Dictionary containing simulation results.
    file_path : string  
        Path to save the file.

    """

    for key, value in result.items():
        for i, item in enumerate(value):
            if isinstance(item, np.ndarray): #check if item is a numpy array
                result[key][i] = item.tolist()
    
    #Convert comeplex numbers to strings
    for key, value in result.items():
        try:
            if (isinstance(value[0][0], complex)): #check if item is a complex number
                result[key] = [[str(x) for x in sublist] for sublist in value] #convert complex numbers to strings
        except:
            pass
    
    with open(file_path, 'w') as file:
        json.dump(result, file, indent=4)
    
    print('Results saved to:', file_path)




def format_results(path):
    """
    Reads and formats the results from .json files in a folder.

    Parameters:
    path : string
        Path to the folder containing simulation results.
    """

    results = []
    file_names = []

    #Open all json files in the folder
    folder_path = Path(path)

    for file in sorted(folder_path.iterdir()):
        if file.suffix == '.json':
            with open(file, 'r') as f:
                results.append(json.load(f)) 
                file_names.append(file)
    
    
    #Format complex strings to complex values
    for res in results:
        for key, list in res.items(): 
            try:
                res[key] = [[complex(x) for x in sublist] for sublist in list]
            except:
                pass
    return results, file_names



def plot_freq(results, file_names, rocof=False):
    """
    Plot frequency results from simulation.

    Parameters:
    results : list of dictionaries
        List of dictionaries containing simulation results.
    rocof : bool, optional
        If True, plot ROCOF. Default is False.

    """

    #Plot frequency
    plt.figure()
    it = 0  
    for res in results:
        plt.plot(res['t'], 50 + 50*np.mean(res['gen_speed'], axis=1), label = file_names[it].stem)
        it += 1
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.grid()  
    plt.legend()

    #Plot ROCOF
    if rocof:
        plt.figure()
        it = 0   
        for res in results:
            plt.plot(res['t'], np.gradient(50 + 50*np.mean(res['gen_speed'], axis=1), res['t']), label = file_names[it].stem)
            it += 1
        plt.xlabel('Time [s]')
        plt.ylabel('ROCOF [Hz/s]')
        plt.grid()
        plt.legend()
            



    return None

def plot_power_VSC(results, file_names, VSC_name):
    """
    Plot power and voltage results from simulation.

    Parameters:
    results : list of dictionaries
        List of dictionaries containing simulation results.
    file_names : list of strings
        List of file names.
    VSC_name : string
        Name of the VSC to plot.
    """
    plt.figure()
    for res in results:
        plt.plot(res['t'], np.abs(res[VSC_name]), label = VSC_name)
    plt.xlabel('Time [s]')
    plt.ylabel('Power [MW]')
    plt.grid()
 
    
def plot_gen_speed(results, file_names, gen_name=None):
    """
    Plot generator speed results from simulation.

    Parameters:
    results : list of dictionaries
        List of dictionaries containing simulation results.
    file_names : list of strings
        List of file names.
    gen_name : string, optional
        Name of the generator to plot. If None, plot all generators.
    """
    plt.figure()
    it = 0   
    for res in results:
        if gen_name:
            plt.plot(res['t'], np.array(res['gen_speed'])[:, res['gen_name'][0].index(gen_name)], label=gen_name+' ' + file_names[it].stem)
            it += 1
        else:
            for gen in res['gen_name']:
                plt.plot(res['t'], np.array(res['gen_speed'])[:, res['gen_name'].index(gen)], label=gen)
    plt.xlabel('Time [s]')
    plt.ylabel('Speed [p.u.]')
    plt.grid()
    plt.legend()
    


