from copy import deepcopy
from general_helpers import *
from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection,get_devices,QPUConnection

#-----Function definitions-----#
def apply_CY(c,t,p):
    '''
    '''
    new_p = p
    new_p.inst(RZ(np.pi/2.0,t))
    new_p.inst(CNOT(c,t))
    new_p.inst(RZ(-np.pi/2.0,t))
    return new_p
# #
# #
def initialize_state(code_index,Pauli,p):
    '''
    Initialize to a given state (here, ground state)
    '''
    new_p = p
    new_p.inst(Pauli(code_index))
    return new_p
# #
# #
def measure_one_qubit_pauli(Pauli,code_index,ancilla_index,p,qvm):
    '''
    Single-Pauli measurement using the "Phase-kickback trick"
    '''
    new_p = p
    new_p.inst(H(ancilla_index))
    if Pauli == 'I':
        new_p.inst(I(ancilla_index))
    elif Pauli == 'X':
        new_p.inst(CNOT(ancilla_index,code_index))
    elif Pauli == 'Y':
        new_p = apply_CY(ancilla_index,code_index,p)
    elif Pauli == 'Z':
        new_p.inst(CZ(ancilla_index,code_index))
    new_p.inst(H(ancilla_index))
    #ket_results = qvm.wavefunction(p)
    #print('state after measurement circuit')
    #print(ket_results)
    new_p.measure_all(*[(q,q) for q in [ancilla_index,code_index]])
    return new_p
# #
# #
def observable_average(np_list):
    '''
    Takes averages of qvm/qpu-returned measurement list
    converting 0 to +1, 1 to -1
    '''
    avg = 0
    for i in range(len(np_list)):
        if np_list[i] == 0:
            avg = avg + 1
        elif np_list[i] == 1:
            avg = avg - 1
    return avg / len(np_list)
# #
# #
def one_qubit_state_tomography(initial_p,qvm,n_runs,code_index,ancilla_index):
    '''
    '''
    c = ancilla_index
    t = code_index
    p = deepcopy(initial_p)
    print('State initialized with:')
    print(initial_p)
    #ket_results = qvm.wavefunction(p)
    #print('Initial state:')
    #print(ket_results)

    p = measure_one_qubit_pauli('I',t,c,p,qvm)
    # ancilla returns always 0 because every state is
    # a +1 eigenstate of I
    run_results = qvm.run(p,[c,t],n_runs)
    trIrho = observable_average(np.array(run_results)[:,0])

    # X component
    p = deepcopy(initial_p)
    #p = Program()
    #p = initialize_state(t,Initial_Pauli,p)
    p = measure_one_qubit_pauli('X',t,c,p,qvm)
    run_results = qvm.run(p,[c,t],n_runs)
    trXrho = observable_average(np.array(run_results)[:,0])
    
    # Y component
    p = deepcopy(initial_p)
    #p = Program()
    #p = initialize_state(t,Initial_Pauli,p)
    p = measure_one_qubit_pauli('Y',t,c,p,qvm)
    run_results = qvm.run(p,[c,t],n_runs)
    trYrho = observable_average(np.array(run_results)[:,0])
    
    # Z component
    p = deepcopy(initial_p)
    #p = Program()
    #p = initialize_state(t,Initial_Pauli,p)
    p = measure_one_qubit_pauli('Z',t,c,p,qvm)
    run_results = qvm.run(p,[c,t],n_runs)
    trZrho = observable_average(np.array(run_results)[:,0])
    return [trIrho,trXrho,trYrho,trZrho]
# #
# #
#-----Main function-----#
def main():
    print('Performing state tomography on a single qubit...')
    #---Constants---#
    code_index    = 0
    ancilla_index = 1
    # Indices for Steane code
    code_indices    = [1,7,12,17,11,6,16]
    data_q_index    = 1
    ancilla_indices = [6,10,5,0]
    additional_ancilla_index = 16
    n_runs = 10000
    info_str = date_str()
    info_str += '_nruns_' + str(n_runs)
    name_str = 'qvmn_state_tomo_data_q_'+str(data_q_index)
    
    print('Number of runs: ',n_runs)
    acorn = get_devices(as_dict=True)['19Q-Acorn']
    qvm = QVMConnection(acorn)
    # qvm = QVMConnection()
    
    # Physical Hadamard
    p = Program()
    Initial_Pauli = H
    p = initialize_state(code_index,Initial_Pauli,p)
    trrho = one_qubit_state_tomography(p,
                                       qvm,
                                       n_runs,
                                       code_index,
                                       ancilla_index)
    header_str = 'Physical Hadamard state tomography I,X,Y,Z'
    print(header_str)
    print(np.array(trrho)/2.0)
    
    save_np_data(np.array(trrho)/2.0,
                 'data_9_5/',
                 name_str+'_physical_H_'+info_str,
                 header_str)

    # Steane code logical Hadamard
    p = Program()
    p = encode_steane_code_qubit(code_indices,data_q_index,p)
    p = steane_logical_H(code_indices,p)
    p = decode_steane_code_qubit(code_indices,data_q_index,p)
    trrho = one_qubit_state_tomography(p,
                                       qvm,
                                       n_runs,
                                       data_q_index,
                                       ancilla_indices[0])
    header_str = 'Steane Logical Hadamard (encoding, Hbar, decoding) state tomography I,X,Y,Z'
    print(header_str)
    print(np.array(trrho)/2.0)
    save_np_data(np.array(trrho)/2.0,
                 'data_9_5/',
                 name_str+'_Steane_H_'+info_str,
                 header_str)
    print('Everything went better than expected!')

if __name__ == '__main__':
    main()
