# Compute the best number of iteration for the PVC algorithm

import subprocess

# Save the directory of the different files
dir_Image = ''
dir_GroundTruth = ''
dir_Mask = ''
output_dir = ''
dir_python = ""

for i in range(1,50):

    # Define the command with the desired options
    command = "petpvc -i "+dir_Image+"Reconstructed_Image.nii -m "+dir_Mask+"WM_GM_Mask4D_Sim.nii -o "+output_dir+"Result_SIMU_PVC_RL.nii --pvc RL -x 5.0 -y 5.0 -z 5.0 -k "
    command += str(i)

    # Run the command and wait for it to complete
    subprocess.run(command, shell=True)

    # Define the command with the desired options
    command = "python3 "+dir_python+"Error.py -i "+output_dir+"Result_SIMU_PVC_RL.nii -o "
    command += str(i)

    # Run the command and wait for it to complete
    subprocess.run(command, shell=True)




