This repository is a fork of Eirik Stendshorne Sanden's GitHub, which itself is a copy of the TOPS model originally developed by Hallvar Haugdal: https://github.com/hallvar-h/TOPS/

This version has been modified to study the Nordic 45 model (N45), which represents the Nordic Synchronous Area. The N45 model used here is an adapted version from Martin G. Teignes. It has been further extended to include: Voltage Source Converter (VSC) HVDC transmission, Wind power modeled as VSCs, Power System Stabilizers (PSS). With these additional features, the N45 model has been appropriately tuned.

Inspired by Eirik Stendshorne Sanden’s master's thesis, a new initialization function has been implemented. This function reads load, generation, and exchange data, ensuring their proper distribution. Additionally, it allows updating the energy mix, enabling the redistribution of power generation among different generators.



# Original readme:

# TOPS (**T**iny **O**pen **P**ower System **S**imulator)
**Note**: This repository was previously called DynPSSimPy.


This is a package for performing dynamic power system simulations in Python. The aim is to provide a simple and lightweight tool which is easy to install, run and modify, to be used by researchers and in education. Performance is not the main priority. The only dependencies are numpy, scipy, pandas and matplotlib (the core functionality only uses numpy and scipy).

The package is being developed as part of ongoing research, and thus contains experimental features. Use at your own risk!

Some features:
- Newton-Rhapson power flow
- Dynamic time domain simulation (RMS/phasor approximation)
- Linearization, eigenvalue analysis/modal analysis

# Installation
The package can be installed using pip, as follows:

`pip install tops`

# Citing
If you use this code for your research, please cite [this paper](https://arxiv.org/abs/2101.02937).

# Example notebooks
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hallvar-h/TOPS/HEAD?filepath=examples%2Fnotebooks)

# Contact
[Hallvar Haugdal](mailto:hallvhau@gmail.com)
