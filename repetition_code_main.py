from repetition_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection,get_devices

def main():
    # dead qubits: 2,3,15,18
    code_indices = [0,1,2]
    data_q_index = 0
    ancilla_indices = [4,5]
    qvm = QVMConnection()
    p = Program()
    p = encode_repetition_code_qubit(code_indices,data_q_index,p)
    # p = repetition_logical_X(code_indices,p)
    p = repetition_logical_H(code_indices,data_q_index,p)
    #p = repetition_logical_X(code_indices,p)
    #p = repetition_logical_Z(code_indices,p)
    # p.inst([H(q) for q in code_indices])
    # p = decode_repetition_code_qubit(code_indices,data_q_index,p)
    run_results = qvm.run(p,code_indices)
    ket_results = qvm.wavefunction(p)
    print(ket_results)
# #
# #
if __name__ == '__main__':
    main()
