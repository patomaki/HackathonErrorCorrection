# S. Patomaki, May 2018 for coursework
import numpy as np
from argparse import ArgumentParser
from pyquil.quil import Program
from pyquil.api import QVMConnection,QPUConnection,get_devices,CompilerConnection
from five_qubit_code import *

#-----Main function-----#
def main():
    #---Constants---#
    # Note the order of labeling in kets:
    # | q_{n} q_{n-1} ... q_{m+1} q_{m} >
    code_indices    = [16,11,10,5,0]
    data_q_index    = 11
    ancilla_indices = [12,7,6,1]
    #---Cmd-line argument parsing---#
    parser = ArgumentParser()
    parser.add_argument('--hardware',type=str,action='store')
    args = parser.parse_args()
    hardware_str = args.hardware if args.hardware else None
    print('Using hardware',hardware_str)
    #---Initialization---#
    if hardware_str.lower() == 'qpu':
        devices = get_devices(as_dict=True)
        acorn = devices['19Q-Acorn']
        qpu = QPUConnection(acorn)
    else:
        qvm = QVMConnection()
    #---Quiltxt definitions---#
    p = Program()
    print('defining CY...')
    def_CY(p)
    print('appending encoding...')
    define_matrix_logical_H(p)
    p = encode_five_to_one_quiltxt(code_indices,data_q_index,p)
    # print('appending logical Hadamard...')
    # p = qrng_quiltxt(code_indices,p)
    # p.inst([X(q) for q in code_indices])
    ket_results = qvm.wavefunction(p)
    print('state after encoding')
    print(ket_results)
    print('appending logical Hadamard...')
    p = five_logical_H(code_indices,p)
    ket_results = qvm.wavefunction(p)
    print(ket_results)
    # print('appending stabilizer control circuits...')
    # p = five_q_stabilizer_control_quiltxt(ancilla_indices,code_indices,p)
    # print('decoding...')
    p = decode_five_to_one_quiltxt(code_indices,data_q_index,p)
    print('state after decoding...')
    ket_results = qvm.wavefunction(p)
    print(ket_results)
    # print('measuring stabilizers...')
    # p = five_q_stabilizer_measurement_quiltxt(ancilla_indices,p)
    # p.inst(MEASURE(data_q_index,data_q_index))
    # p.measure_all(*[(q,q) for q in ancilla_indices+code_indices])
    #---Running---#
    # run_results = qvm.run(p,ancilla_indices+code_indices)
    # ket_results = qvm.wavefunction(p)
    # print(run_results)
    # print(ket_results)
# #
# #
if __name__ == '__main__':
    main()
