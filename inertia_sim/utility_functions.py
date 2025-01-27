import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
import json


def plot_freq(path, rocof=False):
    """
    Plot frequency results from simulation.

    Parameters:
    path : string
        Path to the folder containing simulation results.
    rocof : bool
        Flag to plot ROCOF.

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


    #Plot frequency
    fig = plt.figure()

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



