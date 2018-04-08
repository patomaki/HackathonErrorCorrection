from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.api import QPUConnection
from pyquil.api import get_devices, Job
from pyquil.gates import *
from pyquil.paulis import *
import numpy as np
from grove.tomography.state_tomography import do_state_tomography
from grove.tomography.utils import notebook_mode
import matplotlib.pyplot as plt


qvm = QVMConnection()
#qpu = QPUConnection()
def state_tomography(Program, NumSamples, qubits, QVMorQPU):
    if(QVMorQPU == 0):
        state_tomography_qvm, _, _ = do_state_tomography(Program, NumSamples, qvm, qubits)
    if(QVMorQPU == 1):
        state_tomography_qpu, _, _ = do_state_tomography(Program, NumSamples, qpu, qubits)
    state_tomography_qvm.plot();
    print(state_tomography_qvm.rho_est())
    plt.show()


prog = Program(H(0))


state_tomography(prog,10,[0],0)



prog.measure(0,0)
results = qvm.run(prog, [0], 10)
print(results)


