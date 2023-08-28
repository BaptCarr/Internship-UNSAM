# This script use all PVC methods on the real image.

import subprocess

# Save the directory of the different files
dir_Image = ''
dir_GroundTruth = ''
dir_Mask = ''
output_dir = ''
dir_python=""

Methods = ["GTM","LABBE","RL","VC","RBV","LABBE+RBV","RBV+VC","RBV+RL","LABBE+RBV+VC","LABBE+RBV+RL", "MTC" ,"LABBE+MTC", "MTC+VC", "MTC+RL","LABBE+MTC+VC","LABBE+MTC+RL","IY","IY+VC", "IY+RL","MG", "MG+VC" ,"MG+RL"]

for i in Methods:

    # Define the command with the desired options
    command = "petpvc -i "+dir_Image+" -m "+dir_Mask+" -o "+output_dir+"Result_SIMU_PVC_"+i+".nii --pvc "+i+" -x 5.0 -y 5.0 -z 5.0 "
   

    if "IY" in i :
        command+=" -n 3"
    if "RL" in i : 
        command += " -k 3"
    if "VC" in i : 
        command+=" -k 3"
    
     # Run the command and wait for it to complete
    subprocess.run(command, shell=True)

    
    # Define the command with the desired options
    command = "python3 "+dir_python+"Error.py -i "+output_dir+"Result_SIMU_PVC_"+i+".nii -o" +i

        # Run the command and wait for it to complete
    subprocess.run(command, shell=True)