# S. Patomaki, April 2018 Quantum Hackathon for rigetti
import time
import datetime
import numpy as np
from pyquil.quil import Program
from pyquil.gates import H, CNOT
from pyquil.api import QVMConnection,QPUConnection,get_devices,CompilerConnection
from qrng import *
from plot import basic_plot,matrix_plot
from quality_testing import monobit_test,within_block_test

#-----Main function-----#
def main():
    #---Constants---#
    n_qubits = 15
    n_samples = 10 # 1000
    indices = all_qubit_indices()
    indices = indices[0:n_qubits-1]
    info_str = date_str()
    info_str += '_' + str(n_samples) + '_' + str(n_qubits)
    
    #---Program/connection initialization---#
    p = Program()
    qvm = QVMConnection()
    devices = get_devices(as_dict=True)
    print(devices)
    acorn = devices['19Q-Acorn']
    qpu = QPUConnection(acorn)
    compiler = CompilerConnection(acorn)
    
    #---Random number generation---#
    qrng_p = quil_qrng_error_corrected(n_qubits,p)
    #a_number = sample_int(n_qubits,p,qvm,indices)
    print(qrng_p)
    indices = [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15]
    numbers = np.zeros(n_samples)
    for sample in range(n_samples):
        run_result = qpu.run(qrng_p,indices)
        raw_run_result = [run_result[0][0],run_result[0][3],run_result[0][6]]
        #print(raw_run_result)
        #print(raw_run_result[0])
        int_result = int("".join([str(b) for b in run_result[0]]),2)
        numbers[sample] = 1.0*int_result # /2**n_qubits
    print(numbers)
#    numbers = sample_int(n_qubits,p,qvm,indices,n_samples)
#    print(numbers)
#    # numbers_2 = sample_int_compiled(n_qubits,p,qvm,compiler,indices,n_samples)
#    # print(numbers_2)
#    
    save_numbers(numbers,'qpu_error_corrected_numbers_'+info_str+'.txt')
#    
#    basic_plot(numbers,'numbers_'+info_str+'.pdf')
#    matrix_plot(numbers,'number_matrix'+info_str+'.pdf')

if __name__ == '__main__':
    main()
