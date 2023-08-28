import os
import numpy as np
import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split
from torch.utils.data import DataLoader
import SimpleITK as sitk
# import matplotlib.pyplot as plt
import math
import time
import csv

from Dataset import DATASET
from UNET import UnetReduced


def training_UNET(input_channel): 


    if input_channel > 2:
        print('Error : input_channel must be 1 or 2')
        return 1

    #Initiate the GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device : ',device)

    result_dir = ''

    in_channels = input_channel
    out_channels = 1
    model = UnetReduced(in_channels, out_channels)

    # Create the dataset
    Data_dir = ''
    Dataset = DATASET(root_dir=Data_dir)


    # Print the model architecture
    print('---------------Model Unet--------------- \n\n\n')
    print(model)
    print('\n\n\n----------------------------------------')


    print([len(Dataset),len(Dataset[0]),len(Dataset[0]['data']),len(Dataset[0]['data'][0]),len(Dataset[0]['data'][0][0]),len(Dataset[0]['data'][0][0][0])])

    ######################## TRAINING PARAMETERS ###############
    batchSize = 1
    epochs = 100
    learning_rate = 0.00005
    printStep_epochs = 1
    plotStep_epochs = 5
    printStep_batches = 40
    plotStep_batches = math.inf
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    model.to(device)


    ######################## CREATING THE DATASETS ###############

    #Dataset.to(device)
    Dataset_Train, Dataset_Val, Dataset_Test = random_split(Dataset, [495, 100, 65])

    train_loader = DataLoader(Dataset_Train, batch_size=batchSize, drop_last = True)
    val_loader = DataLoader(Dataset_Val, batch_size=batchSize, drop_last = True)
    test_loader = DataLoader(Dataset_Test, batch_size=batchSize, drop_last = True)


######################## TRAINING ###############

    print('\n\nBeginning of the training ')

    losses_train, losses_val, losses_test = [], [],[]
    times_train, times_val = [], []
    running_loss_test = 0.0

    for epoch in range(epochs):
        running_loss_train, running_loss_val = 0.0, 0.0
        start_time_train = time.time()

        for i, data in enumerate(train_loader, 0):
            images, MRI, labels = data['data'], data['MRI'], data['label']
            if input_channel == 2:
                images = torch.cat((data, MRI), dim=1)
            optimizer.zero_grad()
            outputs = model(images.to(device))
            loss = criterion(outputs, labels.to(device))
            loss.backward()
            optimizer.step()
            running_loss_train += loss.item()


        running_loss_train = running_loss_train / 440
        print(f'training loss de fin d epoch {str(epoch+1)} is : ' + str(running_loss_train))
        losses_train.append(running_loss_train)

        # Record ending time for training loop
        end_time_train = time.time()
        time_taken_train = end_time_train - start_time_train
        print(f'Training time for epoch {epoch + 1}: {time_taken_train:.2f} seconds')
        times_train.append(time_taken_train)
        
        with torch.no_grad():
            # Record starting time for validation loop
            start_time_val = time.time()

            for i, data in enumerate(val_loader, 0):
                images, MRI, labels = data['data'], data['MRI'], data['label']
                if input_channel == 2:
                    images = torch.cat((data, MRI), dim=1)
                outputs = model(images.to(device))
                loss = criterion(outputs, labels.to(device))
                running_loss_val += loss.item()


            running_loss_val = running_loss_val / 100
            print(f'validation loss de fin d epoch {str(epoch+1)} is : ' + str(running_loss_val))
            losses_val.append(running_loss_val)

            # Record ending time for validation loop
            end_time_val = time.time()
            time_taken_val = end_time_val - start_time_val
            print(f'Validation time for epoch {epoch+1}: {time_taken_val:.2f} seconds')
            times_val.append(time_taken_val)
            
            
    for i, data in enumerate(test_loader, 0):
        
        images, MRI, labels = data['data'], data['MRI'], data['label']
        if input_channel == 2:
            images = torch.cat((data, MRI), dim=1)
        outputs = model(images.to(device))
        loss = criterion(outputs, labels.to(device))
        running_loss_test += loss.item()

    running_loss_test = running_loss_test / 60
    print(f'validation loss is nb {str(i // printStep_batches)} : ' + str(running_loss_test))
    losses_test.append(running_loss_test)

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    # Save the losses to CSV files in the "result" directory after each epoch
    with open(os.path.join(result_dir, '{}_{}_losses_train_only_PET.csv'.format(timestamp, epochs)), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(losses_train)

    with open(os.path.join(result_dir, '{}_{}_losses_val_only_PET.csv'.format(timestamp, epochs)), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(losses_val)

    with open(os.path.join(result_dir, '{}_{}_losses_test_only_PET.csv'.format(timestamp, epochs)), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(losses_test)

    model_path = os.path.join(result_dir, '{}_{}_UNET_only_PET.pt'.format(timestamp, epochs))
    torch.save(model.state_dict(), model_path)

    return 0

