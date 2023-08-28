## This script define the Dataset class.

import os
import numpy as np
import torch
from torch.utils.data import DataLoader,Dataset
import SimpleITK as sitk



# Create the dataset class
class DATASET(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.file_list = [file for file in os.listdir(root_dir) if ((file.endswith('.nii.gz') or file.endswith('.nii')) and file.startswith('DATA') and not(file.startswith('DATAA')))]
        #print(self.file_list)

    def __len__(self):
        return len(self.file_list)
    
    #return the size of the data
    def get_data_size(self):
        file_path = os.path.join(self.root_dir, self.file_list[0])
        data = sitk.GetArrayFromImage(sitk.ReadImage(file_path))
        return data.shape
    
    def __getitem__(self, idx):
        file_path = os.path.join(self.root_dir, self.file_list[idx])
        data = sitk.GetArrayFromImage(sitk.ReadImage(file_path))
        label = sitk.GetArrayFromImage(sitk.ReadImage(file_path.replace('DATA','LABEL')))
        mri = sitk.GetArrayFromImage(sitk.ReadImage(file_path.replace('DATA','MRI')))

        # Min-max normalization for the data
        data_min = np.min(data)
        data_max = np.max(data)
        data = (data - data_min) / (data_max - data_min)

        # Min-max normalization for the MRI
        mri_min = np.min(mri)
        mri_max = np.max(mri)
        mri = (mri - mri_min) / (mri_max - mri_min)

        # Min-max normalization for the label
        label_min = np.min(label)
        label_max = np.max(label)
        label = (label - label_min) / (label_max - label_min)

        # Cut the data to the same size [127,256,256]
        data = data[:, 44:300, 44:300]
        label = label[:, 44:300, 44:300]
        mri = mri[:, 44:300, 44:300]

        # Add a channel dimension and transform to tensor
        data = torch.from_numpy(data)
        data = data.type(torch.FloatTensor).unsqueeze(0)
        label = torch.from_numpy(label)
        label = label.type(torch.FloatTensor).unsqueeze(0)
        mri = torch.from_numpy(mri)
        mri = mri.type(torch.FloatTensor).unsqueeze(0)
        
        
        return {'data': data, 'label': label, 'MRI': mri}