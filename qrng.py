# S. Patomaki, April 2018 Quantum Hackathon for rigetti
import time
import datetime
import numpy as np
from pyquil.quil import Program
from pyquil.gates import H, CNOT, CCNOT, X, MEASURE
from pyquil.api import QVMConnection,QPUConnection,get_devices,CompilerConnection

#-----Function definitions-----#
def date_str():
    '''
    Return a date-string to add to e.g. filename
    '''
    # src timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
    time_stamp = time.time()
    time_stamp_str = str(datetime.datetime.fromtimestamp(time_stamp).isoformat())
    time_stamp_str = time_stamp_str.split(':',1)[0]
    return time_stamp_str
# #
# #
def all_qubit_indices():
    '''
    Return a list of qubit indices
    '''
    return [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
# #
# #
def quil_qrng_txt(n_qubits,p):
    '''
    Return a quil plaintext which
    appends p with Hadamard operations to n_bits qubits and measure_all
    Input n_bits: number of qubits to apply Hadamards to
          p: pyquil program object
    '''
    qrng_p = p
    indices = all_qubit_indices()
    indices = indices[0:n_qubits-1]
    qrng_p.inst([H(q) for q in indices])
    qrng_p.measure_all(*[(q,q) for q in indices])
    return qrng_p
# #
# #
def def_logical_hadamard(p):
    '''
    Logical hadamard in repetition code
    '''
    Hbar = 1.0/np.sqrt(2)*np.array([[1,0,0,0,0,0,0,1],
                                    [0,1,0,0,0,0,1,0],
                                    [0,0,1,0,0,1,0,0],
                                    [0,0,0,1,1,0,0,0],
                                    [0,0,0,1,-1,0,0,0],
                                    [0,0,1,0,0,-1,0,0],
                                    [0,1,0,0,0,0,-1,0],
                                    [1,0,0,0,0,0,0,-1]])
    p.defgate("Hbar",Hbar)
# #
# #
def enc1(prog,q1,i,j): #takes single qubit, specify which ancillas to use
    enc1 = prog
    return enc1.inst(CNOT(q1,i)).inst(CNOT(q1,j))
# #
# #
def meas1(prog): #measures first 3 qubits
    results = qvm.run_and_measure(prog, qubits=range(3), trials=10)
    return results
# #
# #
def qpumeas1(prog): #measures first 3 qubits
    results = qpu.run_and_measure(prog, qubits=range(3), trials=10)
    return results
# #
# #
def meas2(prog): #measures first 9
    results = qvm.run_and_measure(prog, qubits=range(9), trials=10)
    return results
# #
# #
def enc2(prog): #takes 3 bit rep
    enc2 = prog
    return enc2.inst(CNOT(0,1)).inst(CNOT(0,2)).inst(CNOT(3,4)).inst(CNOT(3,5)).inst(CNOT(6,7)).inst(CNOT(6,8))
# #
# #
def enc(prog): #concatenated repetition code for qubit 1
    encoded = enc1(prog,3,6)
    conc = enc2(encoded)
    return conc
# #
# #
def decode1(enc,q1,q2,q3): #decode 3bitflip
    dec = enc
    return dec.inst(CNOT(q1,q2)).inst(CNOT(q1,q3))
# #
# #
def zpar(prog, i, j, k):
    return  prog.inst(CNOT(i,k),CNOT(j,k))
# #
# #
def xpar(prog, i, j, k):
    return  prog.inst(H(i),H(j),CNOT(i,k),CNOT(j,k),H(i),H(j))
# #
# #
def correctphas(prog,q1,q2,q3,a1,a2):
    xpar(prog,q1,q2,a1)
    xpar(prog,q2,q3,a2)
    return prog.inst(H(q2),CCNOT(a1,a2,q2),H(q2),H(q1),X(a2)
                     ,CCNOT(a1,a2,q1),X(a2),H(q1),H(q3),X(a1),CCNOT(a1,a2,q3),H(q3),X(a1))
# #
# #
def correctbit(prog,q1,q2,q3,a1,a2):
    zpar(prog,q1,q2,a1)
    zpar(prog,q2,q3,a2)
    return prog.inst(CCNOT(a1,a2,q2),X(a2),CCNOT(a1,a2,q1),X(a2),X(a1),CCNOT(a1,a2,q3),X(a1))
# #
# #
def encphas(prog,q1,i,j): #takes single qubit, specify which ancillas to use
    enc1 = prog
    return enc1.inst(CNOT(q1,i)).inst(CNOT(q1,j)).inst(H(q1)).inst(H(i)).inst(H(j))
# #
# #
def decodephas1(enc,q1,q2,q3): #decode 3phaseflip
    dec = enc
    return dec.inst(H(q1)).inst(H(q2)).inst(H(q3)).inst(CNOT(q1,q2)).inst(CNOT(q1,q3))
# #
# #
def quil_qrng_error_corrected(n_qubits,p):
    '''
    '''
    indices = [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15]
    qrng_p = p
    enc1(qrng_p,0,6,11)
    enc1(qrng_p,1,7,12)
    enc1(qrng_p,13,19,14)
    def_logical_hadamard(qrng_p)
    qrng_p.inst(("Hbar",0,6,11))
    qrng_p.inst(("Hbar",1,7,12))
    qrng_p.inst(("Hbar",13,19,14))
    correctbit(qrng_p,0,6,11,  16,5)
    correctbit(qrng_p,1,7,12,  17,18)
    correctbit(qrng_p,13,19,14,4,9)
    decode1(qrng_p,0,6,11)
    decode1(qrng_p,1,7,12)
    decode1(qrng_p,13,19,14)
    qrng_p.measure_all(*[(q,q) for q in indices])
                #[MEASURE(10,11),
#                 MEASURE(12,13),
#                 MEASURE(14,15),
#                 MEASURE(0,0),
#                 MEASURE(4,4),
#                 MEASURE(7,7)])
    return qrng_p
# #
# #
def sample_int(n_qubits,p,qpu,indices,n_samples=1):
    '''
    Return an integer sampled from a quantum random number generator
    Input n_bits: the number of bits to sample
          p: pyquil Program
          qpu: {QVM,QPU}Connection object
          indices: qubit indices to use
          n_samples: the number of integers to return (default 1)
    Return numbers: list of integers
    '''
    qrng_p = p
    output_bits = indices
    numbers = np.zeros(n_samples)
    qrng_p = quil_qrng_txt(n_qubits,qrng_p)
    for sample in range(n_samples):
        run_result = qpu.run(qrng_p,indices)
        int_result = int("".join([str(b) for b in run_result[0]]),2)
        numbers[sample] = 1.0*int_result # /2**n_qubits
    return numbers
# #
# #
def sample_int_compiled(n_qubits,p,qpu,compiler,indices,n_samples=1):
    '''
    Same as sample_int, but pre-compiled
    (DOES NOT WORK AS OF NOW; compiler cannot ignore qubit 3)
    '''
    qrng_p = p
    output_bits = indices
    numbers = np.zeros(n_samples)
    qrng_p = quil_qrng_txt(n_qubits,qrng_p)
    compiled_qrng_p = compiler.compile(qrng_p)
    for sample in range(n_samples):
        run_result = qpu.run(qrng_p,indices)
        int_result = int("".join([str(b) for b in run_result[0]]),2)
        numbers[sample] = 1.0*int_result #/2**n_qubits
    return numbers
# #
# #
def save_numbers(numbers,info_str):
    '''
    Save a list to the folder the
    '''
    np.savetxt('numbers_'+info_str+'.txt', np.array(numbers))
# #
# #

#-----Main function-----#
#def main():
#    n_bits = 19
#    n_samples = 5
#    
#    p = Program()
#    qvm = QVMConnection()
#    devices = get_devices()
#    acorn = '19Q-Acorn'
#    qpu = QPUConnection(acorn)
#    print(date_str())
#    print(all_qubit_indices())
#    qrng_p = quil_qrng_txt(n_bits,p)
#    print(qrng_p)
#    print(sample_int(n_bits,p,qvm))
#    print(sample_int(n_bits,p,qvm,n_samples))
#
#if __name__ == '__main__':
#    main()
