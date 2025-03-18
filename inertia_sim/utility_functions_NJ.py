import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
import json
import pandas as pd 
import os


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

def plot_gen_power(results, file_names, gen_name=None):
    """
    Plot generator power output results from simulation.

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
            plt.plot(res['t'], np.array(res['gen_P'])[:, res['gen_name'][0].index(gen_name)], label=gen_name+' ' + file_names[it].stem)
            it += 1
        else:
            for gen in res['gen_name']:
                plt.plot(res['t'], np.array(res['gen_P'])[:, res['gen_name'].index(gen)], label=gen)
    plt.xlabel('Time [s]')
    plt.ylabel('Power [MW]')
    plt.grid()
    plt.legend()


def import_powerflow_data(path):
    """
    Retrievies data from .xlsx files

    Parameter:
    path : string
        String to folder path 
    """
  
    # Reading the aggregated generation data from excel file
    ENTSOE_gen_data = pd.read_excel(
        path + 'dataframes_transparency.xlsx', sheet_name='Aggr_generation', index_col=0)
    # Reading the aggregated load data from excel file
    ENTSOE_load_data = pd.read_excel(
        path + 'dataframes_transparency.xlsx', sheet_name='Aggr_load', index_col=0)

    # Reading the aggregated exchange data from excel file (power links)
    ENTSOE_exchange_data = pd.read_excel(
        path + 'powerflow_Statnett.xlsx', sheet_name='aggr_exchange', index_col=0)
    return ENTSOE_gen_data, ENTSOE_load_data, ENTSOE_exchange_data



def plot_freq(results, file_names, rocof=False, scenario = None, gen = None):
    """
    Plot frequency results from simulation.

    Parameters:
    results : list of dictionaries
        List of dictionaries containing simulation results.
    rocof : bool, optional
        If True, plot ROCOF. Default is False.

    """
    # plt.rcParams.update({

    #     "font.family": "Dejavu serif",

    #     "font.serif": ["Computer Modern Roman"],
    #     "font.size": 12,           # Default font size
    #     "axes.titlesize": 14,      # Font size for axes titles
    #     "axes.labelsize": 14,      # Font size for x and y labels
    #     "xtick.labelsize": 12,     # Font size for x tick labels
    #     "ytick.labelsize": 12,     # Font size for y tick labels
    #     "legend.fontsize": 12,     # Font size for legend
    #     "figure.titlesize": 16     # Font size for figure title
    # })

    #Plot frequency
    if gen is not None:
        plt.figure()
        it = 0
        for res in results:
            gen_index = res['gen_name'].index(gen)
            plt.plot(res['t'], 50 + 50*np.array(res['gen_speed'])[:,gen_index], label = file_names[it].stem)
            it += 1


    else:
        plt.figure()
        it = 0  
        for res in results:
            plt.plot(res['t'], 50 + 50*np.mean(res['gen_speed'], axis=1), label = file_names[it].stem)
            it += 1

        if scenario == 'NordLink':

            from plot_NordLink_data import import_NordLink_data
            from config import system_path
            path = system_path+'inertia_sim/N45_case_data_NordLink/Case-Norlink.xlsx'
            data = import_NordLink_data(path)


            # Check if the necessary columns exist
            required_columns = ['Timestamp', 'Frequency: FI', 'Frequency: NO1', 'Frequency: NO2', 'Frequency: NO3']
            if not all(col in data.columns for col in required_columns):
                print("Error: Required columns are missing from the data.")
            else:
                data['mean_freq'] = data[['Frequency: FI', 'Frequency: NO1', 'Frequency: NO2', 'Frequency: NO3']].mean(axis=1)
                plt.plot(data['Seconds'], data['Frequency: FI'], label='FI')
                # plt.plot(data['Seconds'], data['Frequency: NO1'], label='NO1')
                # plt.plot(data['Seconds'], data['Frequency: NO2'], label='NO2')
                # plt.plot(data['Seconds'], data['Frequency: NO3'], label='NO3')
                # plt.plot(data['Seconds'], data['mean_freq'], label='Average frequency')
    #Add a dotted line at 49.1 Hz
    plt.axhline(y=49.1, color='r', linestyle='--', label='49.1 Hz')
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
    index = 0
    for name in results[0]['VSC_name'][0]:
        if(name == VSC_name):
            break
        else:
            index += 1
    it = 0
    for res in results:
        
        plt.plot(res['t'], ([row[index] for row in res['VSC_p']]), label = file_names[it].stem)# label = res['VSC_name'][0][index]+' '+file_names[i].stem)
        it += 1
    plt.xlabel('Time [s]')
    plt.legend()
    plt.ylabel('Power [MW]')
    #plt.title(f'Active power output from {res['VSC_name'][0][index]}')
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
        if gen_name is not None:
            plt.plot(res['t'], np.array(res['gen_speed'])[:, res['gen_name'][0].index(gen_name)], label=gen_name+' ' + file_names[it].stem)
            it += 1
        else:
            for gen in res['gen_name']:
                plt.plot(res['t'], np.array(res['gen_speed'])[:, res['gen_name'].index(gen)], label=gen)
    plt.xlabel('Time [s]')
    plt.ylabel('Speed [p.u.]')
    plt.grid()
    plt.legend()

def plot_local_freq(results, file_names, load_name, gen_name,  mean_freq = False):
    plt.figure()
    it = 0
    for res in results:
        plt.plot(res['t'], np.array(res['freq_est'])[:, res['load_name'][0].index(load_name)], label=load_name+' ' + file_names[it].stem)
    
        if gen_name is not None:
            plt.plot(res['t'], 50 +  50*np.array(res['gen_speed'])[:, res['gen_name'][0].index(gen_name)], label=gen_name+' ' + file_names[it].stem)
        it += 1
    if mean_freq == True:
        plt.plot(res['t'], 50 + 50*np.mean(res['gen_speed'], axis=1),label = 'mean_freq')
    plt.xlabel('Time [s]')
    plt.ylabel('Freq [Hz]')
    plt.grid()
    plt.legend()
    


