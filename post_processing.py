# S. Patomaki, April 2018 Quantum Hackathon for rigetti
import os
import sys
import numpy as np
from quality_testing import monobit_test,within_block_test
from scipy.special import erfc,gammainc

#-----Function definitions-----#
def read_data():
    data = []
    this_dir = os.getcwd()
    file_list = os.listdir(this_dir)
        #for file_name in file_list:
        #if ((file_name.find('numbers_2018-04-07T') != -1)
        #   and (file_name.find('txt') != -1)):
    file_name = 'numbers_2018-04-07T15_1000_19.txt'
        #file_name = 'numbers_2018-04-07T17_1000_19.txt'
        #file_name = 'numbers_error_corrected_numbers_2018-04-07T18_35_1000_15.txt'
    data = np.append(data,np.loadtxt(file_name))
    return data
# #
# #
def convert_to_3bit(number):
    '''
    Drop last bit
    '''
    n_bits = 3
    b4 = bin(number)[2:].zfill(4)
    b3 = b4[:-1]
    return int(b3,2)
# #
# #
#-----Script-----#
data = read_data()
numbers = data
n_bits = 3
bit_strings = []
bit_list = []
sums  = np.zeros(len(numbers))
stats = np.zeros(len(numbers))
pvals = np.zeros(len(numbers))
for i in range(len(numbers)):
    b3 = str(bin(int(data[i]))[2:].zfill(n_bits))
    print(b3)
    bit_strings.append(b3)
    sum = 0
    for j in range(n_bits):
        print(int(bit_strings[i][j]))
        if int(bit_strings[i][j]) == 0:
            sum += -1
        else:
            sum += 1
        sums[i] = sum
        stats[i] = np.abs(sum)/np.sqrt(len(bit_strings[i]))
    pvals[i] = erfc(stats[i])
print(np.mean(sums))
print(np.mean(pvals))

#data_b3 = []
#for i in range(len(data)):
#    #data_b3.append(convert_to_3bit(int(data[i])))
#    data_b3.append(int(data[i]))
##print(data_b3)
#monobit_sums, monobit_stats, monobit_pvals = monobit_test(data)
#print(np.mean(monobit_sums))
#print(np.mean(monobit_stats))
#print(np.mean(monobit_pvals))
#chi2,block_pval = within_block_test(data_b3)
#print(chi2)
#print(block_pval)

import matplotlib.pyplot as plt
dx = 20
dy = 50
number_matrix = np.array(data).reshape((dx,dy))
plt.figure()
plt.matshow(number_matrix)
plt.savefig('qpu_uncorrected_19_1000.pdf')


