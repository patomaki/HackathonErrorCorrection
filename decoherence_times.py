import numpy as np
from pyquil.quil import Program, Pragma
from pyquil.api import QVMConnection, QPUConnection, get_devices, CompilerConnection
from pyquil.gates import I, H, X
from matplotlib import pyplot as plt
from grove.tomography.state_tomography import do_state_tomography
from scipy.optimize import curve_fit
from pdb import set_trace


def initialize_in_plus(qubit):

    p = Program(H(qubit))

    return p


def initialize_in_1(qubit):

    p = Program(X(qubit))

    return p


def add_identities(p, qubit, num_identities):

    set_trace()
    p.inst(Pragma("PRESERVE_BLOCK"))
    p.inst((I(qubit),)*num_identities)
    p.inst(Pragma("END_PRESERVE_BLOCK"))

    return p


def compile_program(p, acorn):
   
    compiler = CompilerConnection(acorn)
    compiledProg = compiler.compile(p)
   
    return compiledProg


def straight_line(x, m, c):

    return m*x + c


def measure_T1(qubit, acorn, QPUFlag=False):

    qvm = QVMConnection(acorn)
    qpu = QPUConnection(acorn)

    populations = []

    for num_identities in range(1, 1000):
        print("Num identities = {}".format(num_identities))

        p = initialize_in_1(qubit)
        p = add_identities(p, qubit, num_identities)
        p = compile_program(p, acorn)

        if QPUFlag:
            state_tomography_qpu, _, _ = do_state_tomography(p, 1000, qpu, [qubit]) 
            rho = state_tomography_qpu.rho_est
        else:
            state_tomography_qvm, _, _ = do_state_tomography(p, 1000, qvm, [qubit]) 
            rho = state_tomography_qvm.rho_est

        excited_population = rho[1,1]
        populations.append(excited_population)

    logged_populations = np.log(populations)
    times = range(1, 1000)
    popt, pcov = curve_fit(straight_line, times, logged_populations)
    m, c = popt
    T1 = -1/m

    plt.semilogy(times, logged_populations, label = "Data")
    plt.semilogy(times, np.exp(m*logged_populations + c), label = "Fit: T1 = {}".format(T1))
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("Excited population")
    plt.legend(loc="best")
    plt.show()
    plt.savefig("T1_times.pdf")


def measure_T2(qubit, acorn):

    qpu = QPUConnection(acorn)

    populations = []

 

if __name__ == "__main__":

    acorn = get_devices(as_dict=True)["19Q-Acorn"]
    measure_T1(1, acorn, False)
