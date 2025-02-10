import sys
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/')
import inertia_sim.utility_functions_NJ as uf
import matplotlib.pyplot as plt

if __name__ == '__main__':  
    folder_path = '//Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/Results/H_EPS/'
    results,file_names = uf.format_results(folder_path)
    uf.plot_freq(results, file_names)
    #uf.plot_gen(results, file_names)
    #uf.plot_gen_speed(results, file_names,'G3000-1')
  

    # uf.plot_power_VSC(results, file_names, 'FI-EE' )
    # uf.plot_power_VSC(results, file_names, 'NO_2-GB' )
    # uf.plot_power_VSC(results, file_names, 'NO_2-DE' )
    # uf.plot_power_VSC(results, file_names, 'SE_4-LT' )

    plt.show()

