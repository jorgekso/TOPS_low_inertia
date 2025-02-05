import sys
sys.path.append('/Users/noralillelien/Documents/TOPS_low_inertia/')
import inertia_sim.utility_functions_NJ as uf

if __name__ == '__main__':  
    folder_path = '/Users/noralillelien/Documents/TOPS_low_inertia/Results'
    results,file_names = uf.format_results(folder_path)
    uf.plot_freq(results, file_names)
