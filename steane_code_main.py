from general_helpers import *
from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection,get_devices,QPUConnection

# USER:
# Check that name_str and header_str refer
# to the correct qhardware (qvm or qpu),
# and indicate whether it is noisy

#-----Function definitions-----#
def physical_H_induced_rns(qhardware,data_q_index,n_runs):
    '''
    '''
    info_str = date_str()
    info_str += '_nruns_' + str(n_runs)
    name_str = 'qpu_rn_data_q_'+str(data_q_index)
    header_str = 'Physical H-induced random numbers on qpu. '
    header_str += 'data_q_index = '+str(data_q_index)
    print('header:')
    print(header_str)
    p = Program()
    p.inst(H(data_q_index))
    p.inst(MEASURE(data_q_index,data_q_index))
    run_results = qhardware.run(p,[data_q_index],n_runs)
    save_np_data(np.array(run_results),
                 'data_10_5/',
                 name_str+'_physical_H_'+info_str,
                 header_str)
# #
# #
def steane_H_induced_rns(qhardware,code_indices,data_q_index,n_runs):
    '''
    '''
    info_str = date_str()
    info_str += '_nruns_' + str(n_runs)
    name_str = 'qpu_rn_data_q_'+str(data_q_index)
    header_str = 'Steane Hbar-induced random numbers on qpu. '
    header_str += ('code_indices = '+str(code_indices)
                  +', data_q_index = '+str(data_q_index))
    print('header:')
    print(header_str)
    p = Program()
    p = encode_steane_code_qubit(code_indices,data_q_index,p)
    p = steane_logical_H(code_indices,p)
    p = decode_steane_code_qubit(code_indices,data_q_index,p)
    p.measure_all(*[(q,q) for q in code_indices])
    run_results = qhardware.run(p,code_indices,n_runs)
    save_np_data(np.array(run_results),
                 'data_10_5/',
                 name_str+'_Steane_H_'+info_str,
                 header_str)
# #
# #
#-----Main function-----#
def main():
    print('Generating Hadamard-induced random numbers...')
    #---Constants---#
    code_indices    = [1,7,12,17,11,6,16]
    data_q_index    = 1
    ancilla_indices = [6,10,5,0]
    n_runs = 10000
    print('Number of runs: ',n_runs)
    acorn = get_devices(as_dict=True)['19Q-Acorn']
    # qvm = QVMConnection(acorn)  #QVM with QPU noise
    # qvm = QVMConnection() # QVM without noise
    qpu = QPUConnection(acorn)
    qhardware = qpu
    
    physical_H_induced_rns(qhardware,data_q_index,n_runs)
    # steane_H_induced_rns(qhardware,code_indices,data_q_index,n_runs)

# Testing section
#    p.inst(X(code_indices[0]))
#    p.inst(X(code_indices[1]))
#    p.inst(X(code_indices[2]))
#    p.inst(X(code_indices[3]))
#
#    p = apply_CCCNOT(code_indices[0],
#                     code_indices[1],
#                     code_indices[2],
#                     code_indices[3],
#                     p)
#    ket_results = qvm.wavefunction(p)
#    print('state after CCCNOT')
#    print(ket_results)
#    def_CCCNOT(p)
#    def_CCCZ(p)
#    p.inst(X(0))
#    p = encode_steane_code_qubit(code_indices,data_q_index,p)
#    #p.inst(Z(code_indices[2]))
#    p = syndrome_circuit(ancilla_indices,code_indices,p)
#    p = conditional_error_correction(ancilla_indices,code_indices,p)
#    p = decode_steane_code_qubit(code_indices,data_q_index,p)
#    p.measure_all(*[(q,q) for q in code_indices+ancilla_indices])
#    #run_results = qvm.run(p,code_indices)
#    run_results = qvm.run(p,code_indices+ancilla_indices)
#    ket_results = qvm.wavefunction(p)
#    print('state after decoding:')
#    print(ket_results)
#    print('measurement results:')
#    print(run_results)
    print('Everything went better than expected!')
# #
# #
if __name__ == '__main__':
    main()
