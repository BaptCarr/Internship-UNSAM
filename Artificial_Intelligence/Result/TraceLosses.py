import matplotlib.pyplot as plt
import numpy as np
import os

# define directory
input_dir = ''
output_dir = ''


# Scan the directory for the files
files = [i for i in os.listdir(input_dir) if i.endswith('.csv')]
print(files)    

# Load the data from the files
data_train = np.loadtxt(input_dir + files[2], delimiter=',')
data_val = np.loadtxt(input_dir + files[1], delimiter=',')
data_test = np.loadtxt(input_dir + files[0], delimiter=',')
#print(len(data_train))
#print(len(data_val))

# Plot the losses with the test lost as a line to compare
plt.figure(figsize=(10, 5))
plt.plot(data_train, label='Training loss')
plt.plot(data_val, label='Validation loss')
plt.axhline(y=data_test, color='r', linestyle='-', label='Test loss')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Losses of the Training Validation and Test Sets')
plt.savefig(input_dir+'losses.png')


# plot for each 10 epochs
for i in range(10, len(data_train), 10):
    epochs = [ k for k in range(i-10, i)]
    plt.figure(figsize=(10, 5))
    plt.plot(data_train[i-10:i], label='Training loss')
    plt.plot(data_val[i-10:i], label='Validation loss')
    plt.axhline(y=data_test, color='r', linestyle='-', label='Test loss')
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Losses of the Training, Validation and Test Sets' + str(i))
    plt.savefig(output_dir+'losses_' + str(i) + '.png')

plt.show()