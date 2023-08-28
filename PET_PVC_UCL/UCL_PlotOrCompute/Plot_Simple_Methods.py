# This script plot the different histograms of the different methods

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
methods = {}
mean_values = {}
MaxError_values = {}
StdError_values = {}
Bias_values = {}
Bias_WM_values = {}


# Add the stats of the original image
pet_data = sitk.GetArrayFromImage(sitk.ReadImage(dir_Image))
pet_data2 = sitk.GetArrayFromImage(sitk.ReadImage(dir_GroundTruth))
mask_data = sitk.GetArrayFromImage(sitk.ReadImage(dir_Mask))
error = np.mean(abs(pet_data - pet_data2))
bias = np.mean(abs(pet_data - pet_data2)) / np.mean(pet_data)
MaxError = np.max(abs(pet_data - pet_data2))
StdError = np.std(abs(pet_data - pet_data2))
bias_WM = np.mean(abs(pet_data[mask_data == 0] - pet_data2[mask_data == 0])) / np.mean(pet_data[mask_data == 0])
methods[0] = "Original"
mean_values[0] = error
MaxError_values[0] = MaxError
StdError_values[0] = StdError
Bias_values[0] = bias
Bias_WM_values[0] = bias_WM



with open(stat_csv_path, "r") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",")  # Set delimiter as tab ("\t")
    label = 0
    for row in reader :
        if "+RL" in row["Output"] or "MG" in row["Output"] :
            # Skip this method
            continue
        label += 1
        method = row["Output"]
        mean = float(row["Mean error"])
        MaxError = float(row["Max error"])
        StdError = float(row["Standard deviation"])
        Bias = float(row["Bias"])
        Bias_WM = float(row["Bias WM"])

        methods[label] = method
        mean_values[label] = mean
        MaxError_values[label] = MaxError
        StdError_values[label] = StdError
        Bias_values[label] = Bias
        Bias_WM_values[label] = Bias_WM

print(methods.values())

# Plot the different histograms of each images and save it
# Plot and save histogram for Mean error
plt.figure()
plt.bar(list(methods.keys()), list(mean_values.values()), color='g')
plt.xticks(list(methods.keys()), list(methods.values()), rotation=45, ha='right', fontsize=8)
plt.ylabel("Mean error")
plt.title("Histogram of Mean Error")
plt.tight_layout()
plt.savefig(output_dir + "/Mean_error.png")
plt.close()

# Plot and save histogram for Max error
plt.figure()
plt.bar(list(methods.keys()), list(MaxError_values.values()), color='g')
plt.xticks(list(methods.keys()), list(methods.values()), rotation=45, ha='right', fontsize=8)
plt.ylabel("Max error")
plt.title("Histogram of Max Error")
plt.tight_layout()
plt.savefig(output_dir + "/Max_error.png")
plt.close()

# Plot and save histogram for Standard deviation
plt.figure()
plt.bar(list(methods.keys()), list(StdError_values.values()), color='g')
plt.xticks(list(methods.keys()), list(methods.values()), rotation=45, ha='right', fontsize=8)
plt.ylabel("Standard deviation")
plt.title("Histogram of Standard Deviation")
plt.tight_layout()
plt.savefig(output_dir + "/Standard_deviation.png")
plt.close()

# Plot and save histogram for Bias
plt.figure()
plt.bar(list(methods.keys()), list(Bias_values.values()), color='g')
plt.xticks(list(methods.keys()), list(methods.values()), rotation=45, ha='right', fontsize=8)
plt.ylabel("Bias")
plt.title("Histogram of Bias")
plt.tight_layout()
plt.savefig(output_dir + "/Bias.png")
plt.close()

# Plot and save histogram for Bias WM
plt.figure()
plt.bar(list(methods.keys()), list(Bias_WM_values.values()), color='g')
plt.xticks(list(methods.keys()), list(methods.values()), rotation=45, ha='right', fontsize=8)
plt.ylabel("Bias WM")
plt.title("Histogram of Bias GM")
plt.tight_layout()
plt.savefig(output_dir + "/Bias_WM.png")
plt.close()



"""
# Check if methods dictionary is empty
if not methods:
    print("No data found in the CSV file. Exiting...")
    exit()

# Plot the different histograms of each images and save it
plt.figure(1)
plt.bar(methods.keys(), mean_values.values(), color='g')
plt.xticks(methods.keys(), methods.values(), rotation='vertical')
plt.ylabel("Mean error")
plt.savefig("/home/carrolaggi/Desktop/Internship/Github/Result/Plot/Mean_error.png")

plt.figure(2)
plt.bar(methods.keys(), MaxError_values.values(), color='g')
plt.xticks(methods.keys(), methods.values(), rotation='vertical')
plt.ylabel("Max error")
plt.savefig("/home/carrolaggi/Desktop/Internship/Github/Result/Plot/Max_error.png")

plt.figure(3)
plt.bar(methods.keys(), StdError_values.values(), color='g')
plt.xticks(methods.keys(), methods.values(), rotation='vertical')
plt.ylabel("Standard deviation")
plt.savefig("/home/carrolaggi/Desktop/Internship/Github/Result/Plot/Standard_deviation.png")

plt.figure(4)
plt.bar(methods.keys(), Bias_values.values(), color='g')
plt.xticks(methods.keys(), methods.values(), rotation='vertical')
plt.ylabel("Bias")
plt.savefig("/home/carrolaggi/Desktop/Internship/Github/Result/Plot/Bias.png")

plt.figure(5)
plt.bar(methods.keys(), Bias_WM_values.values(), color='g')
plt.xticks(methods.keys(), methods.values(), rotation='vertical')
plt.ylabel("Bias WM")
plt.savefig("/home/carrolaggi/Desktop/Internship/Github/Result/Plot/Bias_WM.png")

plt.show()

#"""