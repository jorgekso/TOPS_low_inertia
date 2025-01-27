import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
import json

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
            except ValueError:
                pass
    return results, file_names



def plot_freq(results, file_names, rocof=False):
    """
    Plot frequency results from simulation.

    Parameters:
    results : list of dictionaries
        List of dictionaries containing simulation results.
    file_names : list of strings
        List of file names.
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
            

    plt.show()

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
    plt.show()
    



