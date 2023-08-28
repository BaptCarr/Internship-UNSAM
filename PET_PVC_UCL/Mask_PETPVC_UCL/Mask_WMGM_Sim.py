# This script  is used to convert 2 mask (GM and WM) to a segmented image
# 

import SimpleITK as sitk
import numpy as np

# def directory
input_dir = ""
output_dir = ""

# Load the segmented image
segmented_image = sitk.ReadImage(input_dir + "gmMask.nii")
segmented_image2 = sitk.ReadImage(input_dir + "wmMask.nii")

# Convert the image to a NumPy array for manipulation
segmentation_data = sitk.GetArrayFromImage(segmented_image)
segmentation_data2 = sitk.GetArrayFromImage(segmented_image2)

# give to the background of both images the value 3
segmentation_data[np.logical_and(segmentation_data == 0 , segmentation_data2 == 0)] = 10

# Give the value 0 to the GM
segmentation_data[segmentation_data == 1] = 0

# Give the value 2 to the WM which is in the segmentation_data2 but in the segmentation_data
segmentation_data[segmentation_data2 == 1] = 2

# Create a new SimpleITK image from the modified array
modified_segmentation_img = sitk.GetImageFromArray(segmentation_data)
modified_segmentation_img.CopyInformation(segmented_image)

# Save the GM and WM masks
sitk.WriteImage(modified_segmentation_img, output_dir + 'GM_WM_mask_Sim.nii')





