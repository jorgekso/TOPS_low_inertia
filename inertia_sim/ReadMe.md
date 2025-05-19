# TOPS

This is a fork of Eirik Stenshorne Sanden's fork of Hallvard Haugdal's TOPS. 

# Low Inertia Power System Simulation

This project contains power system simulations focusing on low inertia scenarios in the Nordic power grid.

## Project Description

Analysis of power system stability and frequency response in scenarios with reduced system inertia due to increased renewable energy penetration.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## File Structure

```
tops_low_inertia/
├── src/
│   └── tops/
│       └── ps_models/      # Power system models
│           └── n45_2030.py # Nordic 45-bus system
├── inertia_sim/           # Simulation scripts
└── results/              # Simulation results
```

## Running Simulations

1. Configure simulation parameters in the model file
2. Run the simulation:
   ```bash
   python run_sim.py
   ```

## Model Parameters

The N45 2030 model includes:
- 45 buses representing Nordic power system
- Hydro and thermal governors
- Automatic voltage regulators
- Power system stabilizers
- VSC-based HVDC links and wind power plants

## Dependencies

- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- TOPS Power System Library

