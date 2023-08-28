## The script will finalise the dataset. 
## It will add random translations and elastic deformations to the data, labels and MRI.
## From one sample, it will create 10 samples with random translations.
## We have acces to a GPU

import SimpleITK as sitk
import numpy as np
import os


# Define the GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Path to the data
PATH = ''
OUTPATH = ''

# List the data keeping only the data and not the labels knowing that the data start with 'data' and the labels with 'label'
list = [x for x in os.listdir(PATH) if x.startswith('DATA')]
print(list)
print(len(list))

# Function to apply random translation and elastic deformation to the data
def apply_random_augmentation(data, label, mri):
    # Create a random translation
    translation = sitk.TranslationTransform(3)
    translation_offset = [float(offset) for offset in np.random.randint(-18, 18, 3)]
    translation.SetOffset(translation_offset)

    # Create a random rotation
    angles = np.random.randint(-40, 40, 3) * np.pi / 180
    rotation_center = [data.GetWidth() // 2, data.GetHeight() // 2, data.GetDepth() // 2]

    rotation_transform = sitk.Euler3DTransform(rotation_center, angles[0], angles[1], angles[2])

    # rotation_transform = sitk.Euler3DTransform(rotation_center, *angles)
    data = sitk.Resample(data, rotation_transform)
    mri = sitk.Resample(mri, rotation_transform)
    label = sitk.Resample(label, rotation_transform)

    # Apply the translation to the data and the labels
    data = sitk.Resample(data, translation)
    mri = sitk.Resample(mri, translation)
    label = sitk.Resample(label, translation)

    return data, label, mri

# Loop over the data
for i in range(len(list)):
    # Create 10 samples with random translations
    print('Init ' + str(i))
    for j in range(10):
        print('       '+ str(j))
        # Load the data and the labels
        data = sitk.ReadImage(PATH + list[i])
        label = sitk.ReadImage(PATH + list[i].replace('DATA', 'LABEL'))
        mri = sitk.ReadImage(PATH + list[i].replace('DATA', 'MRI'))

        # Convert the SimpleITK images to NumPy arrays
        data_np = sitk.GetArrayFromImage(data)
        label_np = sitk.GetArrayFromImage(label)
        mri_np = sitk.GetArrayFromImage(mri)

        # Apply random augmentation and get augmented data
        augmented_data, augmented_label, augmented_mri = apply_random_augmentation(data, label, mri)

        #Set up the right name
        list[i].replace('.nii', f'{str(j)}.nii.gz')
        info = list[i][4:8] if len(list[i]) == 12 else list[i][4:7]

        # Save the data and the labels
        sitk.WriteImage(augmented_data, OUTPATH + f'DATA_AUGMENTED'+info+f'_{str(j)}.nii.gz')
        sitk.WriteImage(augmented_label, OUTPATH + f'LABEL_AUGMENTED'+info+f'_{str(j)}.nii.gz')
        sitk.WriteImage(augmented_mri, OUTPATH + f'MRI_AUGMENTED'+info+f'_{str(j)}.nii.gz')

