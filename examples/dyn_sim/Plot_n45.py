import sys
sys.path.append('/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/')
import inertia_sim.utility_functions_NJ as uf

if __name__ == '__main__':  
    folder_path = '/Users/joerg/Documents/NTNU/Master/TOPS_low_inertia/Results/Base/'
    results,file_names = uf.format_results(folder_path)
    uf.plot_freq(results, file_names)
