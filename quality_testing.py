# S. Patomaki, April 2018 Quantum Hackathon for rigetti
# tests from NIST Statistical test suite
import numpy as np
from scipy.special import erfc,gammainc

#-----Function definitions-----#
def monobit_test(numbers):
    '''
    Return the sums, stats, pvals
    sums: list of sums, where a single sum for the 
          bit string 01011 is equal to -1+1-1+1+1
    '''
    n_bits = 3
    bit_strings = []
    bit_list = []
    sums  = np.zeros(len(numbers))
    stats = np.zeros(len(numbers))
    pvals = np.zeros(len(numbers))
    for i in range(len(numbers)):
        b3 = str(bin(numbers[i])[2:].zfill(n_bits))
        bit_strings.append(b3)
        sum = 0
        for j in range(n_bits):
            if int(bit_strings[-1][j]) == 0:
                sum += -1
            else:
                sum += 1
        sums[i] = sum
        stats[i] = np.abs(sum)/np.sqrt(len(bit_strings[i]))
    pvals[i] = erfc(stats[i]) # random if pval >= 0.01
    return sums, stats, pvals
# #
# #
def within_block_test(numbers):
    '''
    Return chi-squared statistics for the generated numbers
    '''
    n_bits = 3
    bit_strings = []
    M = len(str(bin(numbers[0])[2:].zfill(n_bits)))
    N = len(numbers)
    pi = np.zeros(len(numbers))
    chi2 = 0
    for i in range(N):
        bit_strings.append(str(bin(numbers[i])[2:].zfill(n_bits)))
        sum = 0
        for j in range(M):
            pi[i] += int(bit_strings[-1][j])
        pi[i] = pi[i]/M
        chi2 += 4*M*np.power(pi[i] - 0.5,2)
    pval = gammainc(1.0*N/2.0, chi2/2.0)
    return chi2, pval
