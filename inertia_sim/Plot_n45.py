import sys

from config import system_path
sys.path.append(system_path)
import utility_functions_NJ as uf


import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

if __name__ == '__main__':  
    
    plt.rcParams.update({

        "font.family": "Dejavu serif",

        "font.serif": ["Computer Modern Roman"],
        "font.size": 12,           # Default font size
        "axes.titlesize": 14,      # Font size for axes titles
        "axes.labelsize": 14,      # Font size for x and y labels
        "xtick.labelsize": 12,     # Font size for x tick labels
        "ytick.labelsize": 12,     # Font size for y tick labels
        "legend.fontsize": 12,     # Font size for legend
        "figure.titlesize": 16     # Font size for figure title
    })


    folder_path = system_path+'Results/SC/'

    results,file_names = uf.format_results(folder_path)
    # uf.plot_freq(results, file_names, scenario = 'NordLink')
    uf.plot_freq(results, file_names)
    # results,file_names = uf.format_results(folder_path2)
    # uf.plot_freq(results, file_names)
    #uf.plot_gen(results, file_names)
    # uf.plot_gen_power(results, file_names,'G3249-1')
    # uf.plot_gen_power(results, file_names,'SC3249-1')
    # uf.plot_gen_speed(results, file_names,'G3249-1')
    # uf.plot_gen_speed(results, file_names,'G7000-1')
    # uf.plot_gen_speed(results, file_names,'G7100-1')
  
    # uf.plot_power_VSC(results, file_names, 'WG7100-1' )
    # uf.plot_power_VSC(results, file_names, 'FI-EE' )
    # uf.plot_power_VSC(results, file_names, 'NO_2-GB' )
    # uf.plot_power_VSC(results, file_names, 'NO_2-DE' )
    # uf.plot_power_VSC(results, file_names, 'SE_4-LT' )

    plt.show()