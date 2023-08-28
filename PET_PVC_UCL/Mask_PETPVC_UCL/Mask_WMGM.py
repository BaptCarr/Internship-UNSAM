## This mask willbe omly used with the Muller-Gartner method
## This script is used to convert a segmented image to a binary mask for the white matter and gray matter
## The white matter is represented by the value 2 and 41 and the gray matter by the value 42 and 3

import SimpleITK as sitk
import numpy as np

# def directory
input_dir = ""
output_dir = ""

# List of labels to keep (GM and WM)
labels_to_keep = [41,42,2,3]

# Load the segmented image
segmented_image = sitk.ReadImage(input_dir + "/aseg.nii")

# Convert the image to a NumPy array for manipulation
segmentation_data = sitk.GetArrayFromImage(segmented_image)

#Compute the max of the nifti image
max_label = np.max(segmentation_data)

# Create a mask for the labels to keep
mask = np.isin(segmentation_data, labels_to_keep)

# Apply the mask to keep only the specified labels
segmentation_data[~mask] = max_label + 1

#set all values to 10 execpt the ones we want to keep
segmentation_data[segmentation_data == 0] = max_label + 1

# Replace the segmentation values
segmentation_data[np.logical_or(segmentation_data == 41, segmentation_data == 2)] = 2  # Combine white matter into label 3
segmentation_data[np.logical_or(segmentation_data == 42, segmentation_data == 3)] = 0 # Combine gray matter into label 2

# Create a new SimpleITK image from the modified array
modified_segmentation_img = sitk.GetImageFromArray(segmentation_data)
modified_segmentation_img.CopyInformation(segmented_image)

# Save the GM and WM masks
sitk.WriteImage(modified_segmentation_img, output_dir + '/GM_WM_mask.nii')

##~/home/carrolaggi/Desktop/Internship/PatientCeunim/aseg.nii


