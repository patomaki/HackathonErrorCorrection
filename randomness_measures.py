from math import floor
import random
import numpy as np
from scipy.special import erfc,gammainc
#-----Function definitions-----#
def convert_01_to_np(sample):
    '''
    Convert from {0,1} to {-1,+1}
    '''
    if sample == 0:
        return -1
    elif sample == 1:
        return +1
    else:
        return 0
# #
# #
def monobit_test(bit_sequence,quiet=False):
    '''
    Estimates whether there are an equal number of 0s and 1s 
    in bit_sequence
    '''
    if not quiet:
        print('Running monobit test...')
    np_sequence = [convert_01_to_np(int(r)) for r in bit_sequence]
    S = sum(np_sequence)
    sobs = np.abs(S)/np.sqrt(len(bit_sequence))
    pval = erfc(sobs/np.sqrt(2))
    if not quiet:
        print('Sum: ',S)
        print('test statistic: ',sobs)
        print('P-value: ',pval,' (non-random for p < 0.01)')
    if (pval >= 0.01) and (not quiet):
        print('According to monobit test, input sequence is random.')
    elif not quiet:
        print('According to monobit test, input sequence is not random.')
    return [S,sobs,pval]
# #
# #
def runs_test(bit_sequence,quiet=False):
    '''
    Evaluates the number of runs (subsequent 0s or 1s) in bit_sequence,
    estimates whether 0/1 runs oscillate "too slow or fast", indicated
    by small or large values of test statistic V.
    '''
    print('Running runs test...')
    ones = [int(r) for r in bit_sequence if int(r) == 1]
    pi = len(ones)/len(bit_sequence)
    # [S,sobs,pval] = monobit_test(bit_sequence,quiet=True)
    if np.abs(pi - 0.5) >= 2.0/np.sqrt(len(bit_sequence)):
        print('Prerequisite test not passed. Returning')
        return 0.0
    else:
        V = 0
        for i in range(len(bit_sequence)-1):
            if int(bit_sequence[i+1]) != int(bit_sequence[i]):
                V = V + 1
        V = V + 1
        pval = erfc(np.abs(V - 2*len(bit_sequence)*pi*(1-pi))
                    /(2*np.sqrt(2)*len(bit_sequence)*pi*(1-pi)))
        if not quiet:
            print('pi value: ',pi)
            print('V statistic: ',V)
            print('P-value: ',pval)
        if (pval >= 0.01) and (not quiet):
            print('According to runs test, input sequence is random.')
        elif not quiet:
            print('According to runs test, input sequence is not random.')
        return pval
# #
# #
def binary_matrix_rank_test(bit_sequence,quiet=False):
    '''
    Check for linear dependence among fixed length substrings.
    Binary rank of a matrix:
    '''
    nrows = 32 # NISQ test suite value; other values require alterations
    ncols = 32 # NISQ test suite value; other values require alterations
    nblocks = floor(len(bit_sequence)/(nrows*ncols))
    print('Number of blocks: ',nblocks)
    bit_sequence = bit_sequence[0:nblocks*nrows*ncols]
    bit_sequences = np.array_split(bit_sequence,nblocks)
    bit_matrices = []
    binary_ranks = []
    for subsequence in bit_sequences:
        bit_matrices.append(subsequence.reshape((nrows,ncols)))
        binary_ranks.append(np.linalg.matrix_rank(bit_matrices[-1]))
        #print(binary_ranks[-1])
    FM = len([j for j in range(len(binary_ranks))
              if binary_ranks[j] == nrows])
    FMm1 = len([j for j in range(len(binary_ranks))
                if binary_ranks[j] == nrows-1])
    # probabilities
    r = 32
    product = 1
    for i in range(r):
        product *= (((1.0-np.power(2,1.0*(i-32)))*(1.0-np.power(2,1.0*(i-32))))
                    /(1.0-np.power(2,1.0*(i-r))))
    p_32 = np.power(2,1.0*(r*(32+32-r)-32*32))*product
                
    r = 31
    product = 1
    for i in range(r):
        product *= (((1.0-np.power(2,1.0*(i-32)))*(1.0-np.power(2,1.0*(i-32))))
                   /(1.0-np.power(2,1.0*(i-r))))
    p_31 = np.power(2,1.0*(r*(32+32-r)-32*32))*product
    p_30 = 1 - (p_32+p_31)

    chi2 = (np.power(FM-p_32*nblocks,2)/(p_32*nblocks)
           + np.power(FMm1-p_31*nblocks,2)/(p_31*nblocks)
           + np.power(nblocks-FM-FMm1-p_30*nblocks,2)/(p_30*nblocks))
    print('Chi squared: ',chi2)
    pval = np.exp(-chi2/2.0)
    print('P-value: ',pval)
    if (pval > 0.01) and (not quiet):
        print('According to the binary matrix rank test, ')
        print('input sequence is random.')
    elif not quiet:
        print('According to the binary matrix rank test, ')
        print('input sequence is not random.')
    return [chi2,pval]
# #
# #
#-----Main function-----#
def main():
    # Compare with python's pseudorandom numbers
    n_samples = 10000
    print('Basic randomness tests on pythons random prns:')
    rands = np.zeros(n_samples)
    for i in range(n_samples):
        rands[i] = random.randint(0,1)
    monobit_test(rands)
    runs_test(rands)
    binary_matrix_rank_test(rands)

    print('Basic randomness tests on physical-H induced rns:')
    file_name = 'data_9_5/qpu_rn_data_q_1_physical_H_2018-05-09__13-04-33_nruns_100000.txt'
    #file_name = 'data_9_5/qpu_rn_data_q_1_physical_H_2018-05-09__13-03-10_nruns_10000.txt'
    qpu_physical_H = np.loadtxt(file_name)
    monobit_test(qpu_physical_H)
    runs_test(qpu_physical_H)
    binary_matrix_rank_test(qpu_physical_H)

    print('Basic randomness tests on Steane-H induced rns:')
    file_name = 'data_9_5/qpu_rn_data_q_1_Steane_H_2018-05-09__13-02-50_nruns_10000.txt'
    qpu_Steane_H = np.loadtxt(file_name)[:,0]
    monobit_test(qpu_Steane_H)
    runs_test(qpu_Steane_H)
    binary_matrix_rank_test(qpu_Steane_H)



# #
# #
if __name__ == '__main__':
    main()
