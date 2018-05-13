from general_helpers import *
from simple_state_tomography import *
from steane_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection,get_devices,QPUConnection

#-----Function definitions-----#
LambdaM = np.array([[1.,0.,0.,1.],
                    [0.,1.,1.,0.],
                    [0.,1.,-1.,0.],
                    [1.,0.,0.,-1.]])/2
sigmaX = np.array([[0.,1.],
                   [1.,0.]])
sigmaY = np.array([[0.,-1.j],
                   [1.j,0.]])
sigmaZ = np.array([[1.,0.],
                   [0.,-1.]])
Id2 = np.array([[1.,0.],
                [0.,1.]])

#-----Main function-----#
def main():
    data_q_index = 1
    ancilla_index = 7
    n_runs = 50
    info_str = date_str()
    info_str += '_nruns_' + str(n_runs)
    name_str = 'qpu_process_tomo_data_q_'+str(data_q_index)
    data_folder = 'data_11_5/'
    acorn = get_devices(as_dict=True)['19Q-Acorn']
    # qvmn = QVMConnection(acorn)
    # qvm = QVMConnection()
    qpu = QPUConnection(acorn)
    qhardware = qpu
    # Prepare states |psi_k><psi_k| from 1-d^2
    # Prepare |0><0|: (do nothing)
    p = Program()
    p.inst(I(data_q_index))
    p.inst(X(data_q_index))
    trrho1 = one_qubit_state_tomography(p,qhardware,n_runs,data_q_index,ancilla_index)
    rho1 = (trrho1[0]*Id2 + trrho1[1]*sigmaX +
            trrho1[2]*sigmaY + trrho1[3]*sigmaZ)/2.0
    
    # Prepare |1><1|:
    p = Program()
    p.inst(X(data_q_index))
    p.inst(X(data_q_index))
    trrho2 = one_qubit_state_tomography(p,qhardware,n_runs,data_q_index,ancilla_index)
    rho2 = (trrho2[0]*Id2 + trrho2[1]*sigmaX +
            trrho2[2]*sigmaY + trrho2[3]*sigmaZ)/2.0
    
    # Prepare |+><+|:
    p = Program()
    p.inst(H(data_q_index))
    p.inst(X(data_q_index))
    trrho3 = one_qubit_state_tomography(p,qhardware,n_runs,data_q_index,ancilla_index)
    rho3 = (trrho3[0]*Id2 + trrho3[1]*sigmaX +
            trrho3[2]*sigmaY + trrho3[3]*sigmaZ)/2.0
    
    # Prepare |-><-|:
    p = Program()
    p.inst(H(data_q_index))
    p.inst(PHASE(np.pi/2,data_q_index))
    p.inst(X(data_q_index))
    trrho4 = one_qubit_state_tomography(p,qhardware,n_runs,data_q_index,ancilla_index)
    rho4 = (trrho4[0]*Id2 + trrho4[1]*sigmaX +
            trrho4[2]*sigmaY + trrho4[3]*sigmaZ)/2.0

    print(trrho1)
    print(trrho2)
    print(trrho3)
    print(trrho4)
    header_str = ('H process tomography raw, qs '+str(data_q_index)+','
                  +str(ancilla_index))
    print(header_str)
    save_np_data(np.array([trrho1,
                           trrho2,
                           trrho3,
                           trrho4]),
                 data_folder,
                 name_str+'_X_raw'+info_str,
                 header_str)
    # rhoprime matrices rho1p, etc
    # follow the convention of N & C exactly
    rho1p = rho1
    rho4p = rho2
    rho2p = rho3 - 1.j*rho4 - (1. - 1.j)*(rho1p+rho4p)/2.0
    rho3p = rho3 + 1.j*rho4 - (1. + 1.j)*(rho1p+rho4p)/2.0

    rhoM = np.array([[rho1p[0,0],rho1p[0,1],rho2p[0,0],rho2p[0,1]],
                     [rho1p[1,0],rho1p[1,1],rho2p[1,0],rho2p[1,1]],
                     [rho3p[0,0],rho3p[0,1],rho4p[0,0],rho4p[0,1]],
                     [rho3p[1,0],rho3p[1,1],rho4p[1,0],rho4p[1,1]]])
                      
    chi = LambdaM*rhoM*LambdaM
    print('chi matrix:')
    print(chi)
    header_str = ('H process tomography chi, qs '+str(data_q_index)+','
                  +str(ancilla_index))
    print(header_str)
    save_np_data(chi,
                 data_folder,
                 name_str+'_X_chi'+info_str,
                 header_str)
# #
# #

if __name__ == '__main__':
    main()
