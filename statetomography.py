from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.api import QPUConnection
from pyquil.api import get_devices
from pyquil.gates import *
from pyquil.paulis import *
import numpy as np
from grove.tomography.state_tomography import do_state_tomography
from grove.tomography.process_tomography import do_process_tomography
from grove.tomography.utils import notebook_mode
import matplotlib.pyplot as plt
import grove.tomography.utils as ut


"""
qvm = QVMConnection()
acorn = get_devices(as_dict=True)['19Q-Acorn']
qpu = QVMConnection(acorn)  #QVM with QPU noise
#qpu = QPUConnection(acorn)
"""

def state_tomography(Program, NumSamples, qubits, QVMorQPU):
    """Inputs:
                Program = The program/circuit 
                NumSamples = Number of Samples in tomography
                qubits = qubit(s) to perform tomgraphy on, as a list
                QVMorQPU = 0 or 1 to decide which device to run on
        Outputs:
                Array and graph showing the tomography
                Estimate of fidelity compared to perfect/noiseless case 
        Suggestion: 
                    Use NumSamples = 1000
    """
    if(QVMorQPU == 0):
        state_tomography_qvm, _, _ = do_state_tomography(
                Program, NumSamples, qvm, qubits)
        print('The estimated density matrix is: \n',state_tomography_qvm.rho_est)
        state_tomography_qvm.plot()
        
    if(QVMorQPU == 1):
        state_tomography_qpu, _, _ = do_state_tomography(
                Program, NumSamples, qpu, qubits)
        state_tomography_qvm, _, _ = do_state_tomography(
                Program, 2000, qvm, qubits)
        print('The estimated density matrix is: \n',state_tomography_qpu.rho_est)
        state_tomography_qpu.plot()
        state_fidelity = state_tomography_qpu.fidelity(
                state_tomography_qvm.rho_est)
        print('The estimated state fidelity is:', state_fidelity)
    plt.show()

def process_tomography(Program, NumSamples, qubits, QVMorQPU):
    """Inputs:
                Program = The program/circuit 
                NumSamples = Number of Samples in tomography
                qubits = qubit(s) to perform tomgraphy on, as a list
                QVMorQPU = 0 or 1 to decide which device to run on
        Outputs:
                Array and graph showing the tomography
                Estimate of fidelity compared to perfect/noiseless case 
                
        Suggestion: 
                    Use NumSamples = 500
    """
    if(QVMorQPU == 0):
        process_tomography_qvm, _, _ = do_process_tomography(
                Program, NumSamples, qvm, qubits)
        process_tomography_qvm.plot()
        
    if(QVMorQPU == 1):
        process_tomography_qvm, _, _ = do_process_tomography(
                Program, 1000, qvm, qubits)
        process_tomography_qpu, _, _ = do_process_tomography(
                Program, NumSamples, qpu, qubits)     
        process_tomography_qpu.plot()
        print('Chi matrix:', process_tomography_qpu.to_chi())
        process_fidelity = process_tomography_qpu.process_fidelity(
                process_tomography_qvm.r_est)
        gate_fidelity = process_tomography_qpu.avg_gate_fidelity(
                process_tomography_qvm.r_est)
        print('The estimate process fidelity is:', process_fidelity)
        print('The estimate gate fidelity is:', gate_fidelity)
    plt.show()
    
"""
prog= Program([H(0), X(0), Z(0), X(0), H(0)])
state_tomography(prog,1000,[0],1)
process_tomography(prog,500,[0],1)
"""