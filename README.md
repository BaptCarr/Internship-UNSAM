# Internship at UNSAM

Welcome on my git repository on my internship at the UNSAM.
This internship was about the implementation of Partial Volume Correction (PVC) methods for a Positron Emission Tomography (PET).


# Sommaire

1. [Introduction](#introduction)
    - [Context](#context)
    - [Objectives](#objectives)

2. [Organization of the repository](#organization-of-the-repository)
    - [PET PVC from UCL](#pet-pvc-from-ucl)
    - [Artificial Intelligence](#artificial-intelligence)
    - [Data Simulations](#data-simulations)

3. [PET PVC from UCL](#pet-pvc-from-ucl)
    - [Overview](#overview)

4. [Artificial Intelligence](#artificial-intelligence)
    - [Overview](#overview)

5. [Data Simulations](#data-simulations)
    - [Overview](#overview)

# Introduction

## Contexte

This repo is the result of my internship at the UNSAM (Universidad Nacional de San Martin) in Argentina. This internship was about the implementation of Partial Volume Correction (PVC) methods for a Positron Emission Tomography (PET). The PVC methods are used to correct the partial volume effect (PVE) which is a phenomenon that occurs in PET images. The PVE is due to the limited spatial resolution of the PET scanner. This effect causes a loss of contrast and a bias in the quantification of the PET images. PVC methods are used to correct this effect.

## Objectives

The objective of this internship was to implement PVC methods in Python. The PVC methods are based on the use of a functional image (PET) with or without a structural image (MRI). The implemented solutions are : 
    - GitHub Library : PET PVC from UCL
    - Artificial Intelligence : U-Net structure


# Organization of the repository

## PET PVC from UCL

[This folder](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/) contains a fork of the PET PVC from UCL library. This library is a C++ library that implements PVC methods. The fork is a Python wrapper of the C++ library. The wrapper is made with the pybind11 library. Then there are 3 repo : 
    - PETPVC : The fork repo from the UCL.
    - [The Mask Repo](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/Mask_PETPVC_UCL) : This repo contains python scripts to produce masks for the PVC methods.
    - [The Test and Plot Repo](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/UCL_PlotOrCompute) : This repo contains python scripts to use the PVC methods from the and to plot the results.

## Artificial Intelligence

[This folder](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Artificial_Intelligence/) contains a U-Net structure. This structure is used to extract characteristics from the PET images then reconstruct the PET images with PVC. The U-Net structure is implemented with the PyTorch library. There is also a script to train the U-Net structure, a script to test the U-Net structure and a script to plot the results.

## Data Simulations

[This folder](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/) contains a script to simulate PET images. The script uses the APIRL library to simulate PET images. The script can simulate PET images with or without PVC. The script can also simulate PET images with or without a structural image (MRI). There are 2 subrepo :
    - [Simulation for testing the PVC methods](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/Simulation_Test) : This repo contains a MATLAB script to simulate PET images for testing the PVC methods.
    - [Simulation for training the U-Net structure](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/Simulation_Dataset) : This repo contains a MATLAB script to simulate PET images for training the U-Net structure and a python script to augment the dataset.

# PET PVC from UCL

## Overview

For this repo, you need to follow the installation instructions from the [PET PVC from UCL](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/PETPVC/) repo. Then you can use the scripts from the [Mask Repo](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/Mask_PETPVC_UCL) on you sgmented data. Finally you can use the scripts from the [Test and Plot Repo](https://github.com/BaptCarr/Internship-UNSAM/tree/main/PET_PVC_UCL/UCL_PlotOrCompute).

Becareful, you will surely need to change the paths in the scripts.

# Artificial Intelligence

## Overview

For this repo, you need to install the PyTorch library. Then you can use the scripts from the [Artificial Intelligence](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Artificial_Intelligence/) repo on you data. To use the scripts, you need to first use the TrainUNET.py script to train the U-Net structure. Then you can use the T[Result repo](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Artificial_Intelligence/Result/) to test the U-Net structure and plot the loss and the results.

Becareful, you will surely need to change the paths in the scripts.

# Data Simulations

## Overview

For this repo, you need to install the APIRL library. Then you can use the scripts from the [Data Simulations](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/) repo to simulate PET images. The use of this repo will depend on the repo you will want to use after. You can either use the [Simulation for testing the PVC methods](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/Simulation_Test) if you want to simulate only one image to test the UCL PETPVC library or the [Simulation for training the U-Net structure](https://github.com/BaptCarr/Internship-UNSAM/tree/main/Data_Simulations/Simulation_Dataset) if you want to simulate a dataset to train the U-Net structure.

