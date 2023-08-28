# test a model on a new images

import os
import numpy as np
import torch
import SimpleITK as sitk

from UNET import UnetReduced

# Define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define the path to the model
dir_model = ''
dir_data = ''
dir_data_simu = ''
dir_output = ''

# Import the model
model_name = [i for i in os.listdir(dir_model) if i.endswith('.pt')]
print(model_name)
model = UnetReduced(in_channels=1, classes=1).to(device)
model.load_state_dict(torch.load(dir_model + model_name[0], map_location=device))

# Import the data '
data = sitk.GetArrayFromImage(sitk.ReadImage(dir_data))
print(data.shape)
data = torch.from_numpy(data)
data = data.type(torch.FloatTensor).unsqueeze(0).unsqueeze(0).to(device)
model.eval()
with torch.no_grad():
    pred = model(data)
    pred = pred.squeeze(0)
    pred = pred.squeeze(0)
    
# Convert the prediction tensor to a numpy array
pred = pred.cpu().numpy()

# Normalize the prediction
pred = (pred - np.min(pred)) / (np.max(pred) - np.min(pred))

# Scale the prediction to the range [0, 255]
pred = pred * 255

# Convert the prediction to uint8 data type
pred = pred.astype(np.uint8)

# Create the SimpleITK image from the numpy array
pred = sitk.GetImageFromArray(pred)

print(pred.GetSize())
print(data.shape)
print(pred[65,175,175])
print(pred[65,:,:].GetSize())

# Save the prediction
sitk.WriteImage(pred, dir_output + 'prediction.nii.gz')
print('Prediction done')

# Import simulated data
data = sitk.GetArrayFromImage(sitk.ReadImage(dir_data_simu))
print(data.shape)
data = torch.from_numpy(data)
data = data.type(torch.FloatTensor).unsqueeze(0).unsqueeze(0).to(device)
model.eval()
with torch.no_grad():
    pred = model(data)
    pred = pred.squeeze(0)
    pred = pred.squeeze(0)

# Convert the prediction tensor to a numpy array
pred = pred.cpu().numpy()

# Normalize the prediction
pred = (pred - np.min(pred)) / (np.max(pred) - np.min(pred))

# Scale the prediction to the range [0, 255]
pred = pred * 255

# Convert the prediction to uint8 data type
pred = pred.astype(np.uint8)

# Create the SimpleITK image from the numpy array
pred = sitk.GetImageFromArray(pred)

# Save the prediction
sitk.WriteImage(pred, dir_output+'prediction_simu.nii.gz')
print('Prediction done')
