from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection
#-----Main function-----#
def main():
    #---Constants---#
<<<<<<< HEAD
    # dead: 2,3,15,18
    # code_indices = [1,7,12,17,11,6,16]
    code_indices    = [0,1,4,5,6,7,8]
    data_q_index    = 1
    ancilla_indices = [9,10,11,12,13,14]
    
    qvm = QVMConnection()
    # acorn = get_devices(as_dict=True)['19Q-Acorn']
    # qvm = QVMConnection(acorn)  #QVM with QPU noise

    # syndrome_table = []
    # for e in range(2*len(code_indices)):
    p = Program()
    p = encode_steane_code_qubit(code_indices,data_q_index,p)
    p = steane_logical_H(code_indices,p)
    # if e < 7:
    #     p.inst(X(code_indices[e%7]))
    # else:
    #     p.inst(Z(code_indices[e%7]))
    #p = syndrome_circuit(ancilla_indices,code_indices,p)
    #p = decode_steane_code_qubit(code_indices,data_q_index,p)
    #p.measure_all(*[(q,q) for q in ancilla_indices])
    run_results = qvm.run(p,ancilla_indices)
    ket_results = qvm.wavefunction(p)
    # syndrome_table.append(run_results)
    print(ket_results)

=======
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
>>>>>>> d81524b6c7ec54e4373175e938561791c1b1dede
# #
# #
if __name__ == '__main__':
    main()
