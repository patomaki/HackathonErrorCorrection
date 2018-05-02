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

"""
qvm = QVMConnection()

acorn = get_devices(as_dict=True)['19Q-Acorn']
qvm = QVMConnection(acorn)  #QVM with QPU noise
"""


def state_tomography(Program, NumSamples, qubits, QVMorQPU):
    """Inputs:
                Program = The program/circuit 
                NumSamples = Number of Samples in tomography
                qubits = qubit(s) to perform tomgraphy on
                QVMorQPU = 0 or 1 to decide which device to run on
        Outputs:
                Array and graph showing the tomography
                Estimate of fidelity compared to perfect/noiseless case               
    """
    if(QVMorQPU == 0):
        state_tomography_qvm, _, _ = do_state_tomography(
                Program, NumSamples, qvm, qubits)
        print('The estimated density matrix is: \n',state_tomography_qvm.rho_est)
        state_tomography_qvm.plot()
        
    if(QVMorQPU == 1):
        state_tomography_qpu, _, _ = do_state_tomography(
                Program, NumSamples, qpu, qubits)
        print('The estimated density matrix is: \n',state_tomography_qpu.rho_est)
        state_tomography_qpu.plot()
        state_fidelity = state_tomography_qpu.fidelity(
                state_tomography(Program,NumSamples,qvm,qubits))
        print('The estimated state fidelity is:', state_fidelity)
    plt.show()

def process_tomography(Program, NumSamples, qubits, QVMorQPU):
    """Inputs:
                Program = The program/circuit 
                NumSamples = Number of Samples in tomography
                qubits = qubit(s) to perform tomgraphy on
                QVMorQPU = 0 or 1 to decide which device to run on
        Outputs:
                Array and graph showing the tomography
                Estimate of fidelity compared to perfect/noiseless case               
    """
    if(QVMorQPU == 0):
        process_tomography_qvm, _, _ = do_process_tomography(
                Program, NumSamples, qvm, qubits)
        process_tomography_qvm.plot()
        
    if(QVMorQPU == 1):
        process_tomography_qpu, _, _ = do_process_tomography(
                Program, NumSamples, qvm, qubits)
        process_tomography_qpu.plot()
        process_fidelity = process_tomography_qpu.avg_gate_fidelity(
                process_tomography_qvm.r_est)
        print('The estimate process fidelity is:', process_fidelity)        
    plt.show()
