# S. Patomaki, April 2018 Quantum Hackathon for rigetti
import time
import datetime
import numpy as np
from pyquil.quil import Program
from pyquil.gates import H
from pyquil.api import QVMConnection,QPUConnection,get_devices,CompilerConnection
from qrng import date_str,all_qubit_indices,quil_qrng_txt,sample_int,sample_int_compiled,save_numbers
from plot import basic_plot,matrix_plot
from quality_testing import monobit_test,within_block_test

#-----Main function-----#
def main():
    #---Constants---#
    n_qubits = 19
    n_samples = 1 # 1000
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
    qrng_p = quil_qrng_txt(n_qubits,p)
    a_number = sample_int(n_qubits,p,qpu,indices)
    print(a_number)
    numbers = sample_int(n_qubits,p,qpu,indices,n_samples)
    print(numbers)
    # numbers_2 = sample_int_compiled(n_qubits,p,qvm,compiler,indices,n_samples)
    # print(numbers_2)

    save_numbers(numbers,info_str)

    basic_plot(numbers,'qvm_numbers_'+info_str+'.pdf')
    matrix_plot(numbers,'qvm_number_matrix'+info_str+'.pdf')

if __name__ == '__main__':
    main()
