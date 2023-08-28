# Compute the error between the orginal PET image and the PET image after a method of PVC 
# To call this script, use the following command line:
# python3 Error.py -i <input> -t <truth> -m <method> 
# with input the path to the input PET image, Truth the path to the GroundTruth image and method the method used for the PVC

import SimpleITK as sitk
import numpy as np
import os
import sys
import getopt
import csv


def ComputeError(argv) : 
    arg_input = ""
    arg_output = ""  
    arg_help = "{0} -i <input> -t <truth> -m <method> ".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hi:u:o:", ["help", "input=", "truth=", "output="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-i", "--input"):
            arg_input = arg
        elif opt in ("-i", "--truth"):
            arg_truth = arg
        elif opt in ("-m", "--method"):
            arg_method = arg
    

    # Save the directory of the different files
    dir_Mask = ''
    output_dir = ''


    # Load the PET image
    pet_image = sitk.ReadImage(arg_truth)
    pet_data = sitk.GetArrayFromImage(pet_image)
    pet_image2 = sitk.ReadImage(arg_input)
    pet_data2 = sitk.GetArrayFromImage(pet_image2)
    mask = sitk.ReadImage(dir_Mask)
    mask_data = sitk.GetArrayFromImage(mask)

    # Compute the mean error 
    error = np.mean(abs(pet_data - pet_data2))
    print("The mean error is : {:.2f}".format(error))

    # Compute the max error
    max_error = np.max(abs(pet_data - pet_data2))
    print("The max error is : {:.2f}".format(max_error))

    # Compute the min error
    min_error = np.min(pet_data - pet_data2)
    print("The min error is : {:.2f}".format(min_error))

    # Compute the standard deviation
    std_error = np.std(abs(pet_data - pet_data2))
    print("The standard deviation is : {:.2f}".format(std_error))

    # Compute the median error
    median_error = np.median(abs(pet_data - pet_data2))
    print("The median error is : {:.2f}".format(median_error))

    # Compute the difference of the mean activity between the two images
    mean_pet = np.mean(pet_data)
    mean_pet2 = np.mean(pet_data2)
    Error_Mean = abs(mean_pet - mean_pet2)
    print("The difference of the mean activity between the two images is : {:.2f}".format(Error_Mean))

    # Compute the Bias error
    Bias = Error_Mean / mean_pet
    print("The Bias error is : {:.2f}".format(Bias))
    
    # Compute the mean error in the WM
    error_WM = np.mean(abs(pet_data[mask_data == 0] - pet_data2[mask_data == 0]))
    print("The mean error in the WM is : {:.2f}".format(error_WM))

    # Compute the min and max error and bias in the WM
    min_error_WM = np.min(pet_data[mask_data == 0] - pet_data2[mask_data == 0])
    max_error_WM = np.max(abs(pet_data[mask_data == 0] - pet_data2[mask_data == 0]))
    bias_WM = np.mean(abs(pet_data[mask_data == 0] - pet_data2[mask_data == 0])) / np.mean(pet_data[mask_data == 0])
    print("The min error in the WM is : {:.2f}".format(min_error_WM))
    print("The max error in the WM is : {:.2f}".format(max_error_WM))
    print("The bias in the WM is : {:.2f}".format(bias_WM))

    # Compute the mean of the errors and the bias in the GM
    error_GM = np.mean(abs(pet_data[mask_data == 2] - pet_data2[mask_data == 2]))
    bias_GM = np.mean(abs(pet_data[mask_data == 2] - pet_data2[mask_data == 2])) / np.mean(pet_data[mask_data == 2])
    print("The mean error in the GM is : {:.2f}".format(error_GM))

    # Compute the error in the void
    error_void = np.mean(abs(pet_data[mask_data == 10] - pet_data2[mask_data == 10]))
    bias_void = np.mean(abs(pet_data[mask_data == 10] - pet_data2[mask_data == 10])) / np.mean(pet_data[mask_data == 10])
    print("The mean error in the void is : {:.2f}".format(error_void))

    # Create a csv file if it doesn't exist

    if not os.path.isfile(output_dir+"Error.csv"):
        with open(output_dir+"Error.csv", 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["Methods/Iterations", "Mean error", "Max error", "Min error", "Standard deviation", "Median error", "Error mean", "Bias", "Mean Error WM", "Min Error WM", "Max Error WM", "Bias WM", "Mean Error GM", "Bias GM", "Mean Error void", "Bias void"])

    # Save all value in a csv file by addinng the line with the output entered by the user

    with open(output_dir+"Error.csv", 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([arg_method, error, max_error, min_error, std_error, median_error, Error_Mean, Bias, error_WM, min_error_WM, max_error_WM, bias_WM, error_GM,  error_void])

if __name__ == "__main__":
    ComputeError(sys.argv)
