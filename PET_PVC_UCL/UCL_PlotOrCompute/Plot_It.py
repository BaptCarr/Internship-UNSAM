# Plot the differente stat for different number of iteration for a PVC algorithm
# 

import matplotlib.pyplot as plt
import csv
import numpy as np
import SimpleITK as sitk

# Save the directory of the different files
stat_csv_path = ''
dir_Image = ''
dir_GroundTruth = ''
dir_Mask = ''
output_dir = ''

# Read the CSV file 
mean_values = {}
MaxError_values = {}
StdError_values = {}
Bias_values = {}
Bias_WM_values = {}
Bias_void_values = {}
Bias_GM_values = {}


with open(stat_csv_path, "r") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",")  # Set delimiter as tab ("\t")
    for row in reader:
        label = int(row["Output"])
        mean = float(row["Mean error"])
        MaxError = float(row["Max error"])
        StdError = float(row["Standard deviation"])
        Bias = float(row["Bias"])
        Bias_WM = float(row["Bias WM"])
        #Bias_void = float(row["Bias void"])
        Bias_GM = float(row["Bias GM"])
        mean_values[label] = mean
        MaxError_values[label] = MaxError
        StdError_values[label] = StdError
        Bias_values[label] = Bias
        Bias_WM_values[label] = Bias_WM
        #Bias_void_values[label] = Bias_void
        Bias_GM_values[label] = Bias_GM


# Define the length of the plot
Length = len(mean_values.keys())

# Compute the statistics of the original image
pet_data = sitk.GetArrayFromImage(sitk.ReadImage(dir_Image))
pet_data2 = sitk.GetArrayFromImage(sitk.ReadImage(dir))
mask = sitk.ReadImage(dir_Mask)
mask_data = sitk.GetArrayFromImage(mask)

error = np.mean(abs(pet_data - pet_data2))
bias = np.mean(abs(pet_data - pet_data2)) / np.mean(pet_data)
MaxError = np.max(abs(pet_data - pet_data2))
StdError = np.std(abs(pet_data - pet_data2))
bias_WM = np.mean(abs(pet_data[mask_data == 0] - pet_data2[mask_data == 0])) / np.mean(pet_data[mask_data == 0])
bias_GM = np.mean(abs(pet_data[mask_data == 2] - pet_data2[mask_data == 2])) / np.mean(pet_data[mask_data == 2])


# plot the different stat of each images and save it
plt.figure(1)
plt.plot(list(mean_values.keys()), list(mean_values.values()), label="PETPVC")
#plt.plot([0, Length], [error, error], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Mean error")
plt.title("Mean error in function of the number of iteration")
plt.savefig(output_dir+ "Mean_error.png")

plt.figure(2)
plt.plot(list(MaxError_values.keys()), list(MaxError_values.values()), label="PETPVC")
#plt.plot([0, Length], [MaxError, MaxError], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Max error")
plt.title("Max error in function of the number of iteration")
plt.savefig(output_dir+ "Max_error.png")

plt.figure(3)
plt.plot(list(StdError_values.keys()), list(StdError_values.values()), label="PETPVC")
#plt.plot([0, Length], [StdError, StdError], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Standard deviation")
plt.title("Standard deviation in function of the number of iteration")
plt.savefig(output_dir+ "Standard_deviation.png")

plt.figure(4)
plt.plot(list(Bias_values.keys()), list(Bias_values.values()), label="PETPVC")
#plt.plot([0, Length], [bias, bias], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Bias")
plt.title("Bias in function of the number of iteration")
plt.savefig(output_dir+ "Bias.png")

plt.figure(5)
plt.plot(list(Bias_WM_values.keys()), list(Bias_WM_values.values()), label="PETPVC")
#plt.plot([0, Length], [bias_WM, bias_WM], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Bias WM")
plt.title("Bias WM in function of the number of iteration")
plt.savefig(output_dir+ "Bias_WM.png")

"""
plt.figure(6)
plt.plot(list(Bias_void_values.keys()), list(Bias_void_values.values()))
plt.xlabel("Number of iteration")
plt.ylabel("Bias void")
plt.title("Bias void in function of the number of iteration")

"""

plt.figure(7)
plt.plot(list(Bias_GM_values.keys()), list(Bias_GM_values.values()), label="PETPVC")
#plt.plot([0, Length], [bias_GM, bias_GM], label="Original image")
plt.xlabel("Number of iteration")
plt.ylabel("Bias GM")
plt.title("Bias GM in function of the number of iteration")
plt.savefig(output_dir+ "Bias_GM.png")



plt.show()

