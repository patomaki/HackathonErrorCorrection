from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection
#-----Main function-----#
def main():
    #---Constants---#
    code_indices    = [0,1,2,4,5,6,7]
    data_q_index    = 0
    ancilla_indices = [8,9,10,11,12,13]
    p = Program()
    qvm = QVMConnection()
    def_CCCNOT(p)
    def_CCCZ(p)
    p.inst(X(0))
    p = encode_steane_code_qubit(code_indices,data_q_index,p)
    #p.inst(Z(code_indices[2]))
    p = syndrome_circuit(ancilla_indices,code_indices,p)
    p = conditional_error_correction(ancilla_indices,code_indices,p)
    p = decode_steane_code_qubit(code_indices,data_q_index,p)
    p.measure_all(*[(q,q) for q in code_indices+ancilla_indices])
    #p.measure_all(*[(q,q) for q in code_indices])
    #run_results = qvm.run(p,code_indices)
    run_results = qvm.run(p,code_indices+ancilla_indices)
    ket_results = qvm.wavefunction(p)
    print('state after decoding:')
    print(ket_results)
    print('measurement results:')
    print(run_results)
# #
# #
if __name__ == '__main__':
    main()
