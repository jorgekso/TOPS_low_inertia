import sys
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/')
import inertia_sim.utility_functions_NJ as uf
import matplotlib.pyplot as plt
if __name__ == '__main__':  
    folder_path = '/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/Results/HVDC/'
    results,file_names = uf.format_results(folder_path)
    uf.plot_freq(results, file_names)
    #uf.plot_gen_speed(results, file_names,'G3000-1')
    plt.show()
