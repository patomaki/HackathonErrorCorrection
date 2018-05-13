from copy import deepcopy
from general_helpers import *
from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection,get_devices,QPUConnection

#-----Function definitions-----#
def measure_two_qubit_pauli(Pauli1,Pauli2,code_indices,ancilla_index,p,qvm):
    '''
    Single-Pauli measurement using the "Phase-kickback trick"
    '''
    new_p = p
    new_p.inst(H(ancilla_index))
    if Pauli1 == 'I':
        new_p.inst(I(ancilla_index))
    elif Pauli1 == 'X':
        new_p.inst(CNOT(ancilla_index,code_indices[0]))
    elif Pauli1 == 'Y':
        new_p = apply_CY(ancilla_index,code_indices[0],p)
    elif Pauli1 == 'Z':
        new_p.inst(CZ(ancilla_index,code_indices[0]))

    if Pauli2 == 'I':
        new_p.inst(I(ancilla_index))
    elif Pauli2 == 'X':
        new_p.inst(CNOT(ancilla_index,code_indices[1]))
    elif Pauli2 == 'Y':
        new_p = apply_CY(ancilla_index,code_indices[1],p)
    elif Pauli2 == 'Z':
        new_p.inst(CZ(ancilla_index,code_indices[1]))

    new_p.inst(H(ancilla_index))
    #ket_results = qvm.wavefunction(p)
    #print('state after measurement circuit')
    #print(ket_results)
    new_p.measure_all(*[(q,q) for q in [ancilla_index,code_indices]])
    return new_p
# #
# #
def two_qubit_state_tomography(initial_p,qvm,n_runs,code_indices,ancilla_index):
    '''
    '''
    c = ancilla_index
    t = code_indices
    p = deepcopy(initial_p)
    print('State initialized with:')
    print(initial_p)
    #ket_results = qvm.wavefunction(p)
    #print('Initial state:')
    #print(ket_results)
    
    Paulilist = ['I','X','Y','Z']
    trrho = np.zeros((4,4))
    for i in range(len(Paulilist)):
        for j in range(len(Paulilist)):
            p = deepcopy(initial_p)
            p = measure_two_qubit_pauli(Paulilist[i],
                                        Paulilist[j],
                                        code_indices,
                                        ancilla_index,
                                        p,
                                        qvm)
            run_results = qvm.run(p,[code_incides,ancilla_index],n_runs)
            print(run_results)
            trrho[i,j] = observable_average(np.array(run_results)[:,0])
    return [trrho]
# #
# #

#-----Main function-----#
def main():
    code_indices = [11,6]
    ancilla_indices = [1,16]
    n_runs = 10
    qvm = QVMConnection()
    qhardware = qvm
    p = Program()
    p.inst(I(code_indices[0]))
    p.inst(I(code_indices[1]))
    trrho = two_qubit_state_tomography(p,
                                       qhardware,
                                       n_runs,
                                       code_indices,
                                       ancilla_indices[0])


# #
# #
if __name__ == '__main__':
    main()
