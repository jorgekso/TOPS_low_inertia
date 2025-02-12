import pandas as pd 
import matplotlib.pyplot as plt
from config import system_path


def import_NordLink_data(path):
    """
    Imports the NordLink data from a .xlsx file.
    
    Parameters:
    path : string
        Path to the .xlsx file.
    """

    data = pd.read_excel(path, sheet_name='Utfall-NordLink-2023-02-17-v2')
    print('Successfully imported NordLink data.')

    # Convert 'Timestamp' column to datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # Starting the time from 0
    start_time = data['Timestamp'].iloc[0]
    data['Seconds'] = (data['Timestamp'] - start_time).dt.total_seconds()

    return data

if __name__ == '__main__':

    path = system_path+'inertia_sim/N45_case_data_NordLink/Case-Norlink.xlsx'
    data = import_NordLink_data(path)

    # Check if the necessary columns exist
    if 'Timestamp' not in data.columns or 'Frequency: FI' not in data.columns:
        print("Error: Required columns are missing from the data.")
    else:

        plt.figure()
        plt.plot(data['Seconds'], data['Frequency: FI'], label='NordLink')
        plt.xlabel('Seconds')
        plt.ylabel('Frequency [Hz]')
        plt.legend()
        plt.grid()
        plt.show()


