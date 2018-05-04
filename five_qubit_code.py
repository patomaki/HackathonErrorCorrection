# S. Patomaki, May 2018 for coursework
import numpy as np
from pyquil.quil import Program
from pyquil.gates import H,CNOT,CZ,Z,X,MEASURE,SWAP
from pyquil.api import QVMConnection

#-----Function definitions-----#
def all_qubit_indices():
    '''
        Return a list of qubit indices that correspond to
        the working qubits on the 19Q Acorn chip (0-19, missing 3)
        '''
    return [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
# #
# #
def def_CY(p):
    '''
        Define a Control-Y gate to program p.
        The Y-gate is actually equal to I oplus -i*Y
        to avoid imaginary coefficients.
        '''
    new_p = p
    CY = np.array([[1.,0,0,0],
                   [0,1.,0,0],
                   [0,0,0,-1.j],
                   [0,0,1.j,0]])
    p.defgate("CY",CY)
# #
# #
def encode_five_to_one_quiltxt(code_indices,data_q_index,p):
    '''
        Return a quil plaintext which is
        p appended with encoding circuit for the perfect 5-qubit
        permutation code.
        Input code_indices: qubit indices used in encoding
        data_q_index: qubit index with possibly non-trivial
        initial state.
        p: pyquil program object
        '''
    indices = [i for i in code_indices if i != data_q_index]
    enc_p = p
    
    enc_p.inst([H(q) for q in indices])
    enc_p.inst(Z(indices[0]))
    enc_p.inst(Z(indices[-1]))
    
    enc_p.inst(CZ(indices[0],indices[1]))
    enc_p.inst(CZ(indices[0],indices[3]))
    enc_p.inst(("CY",indices[0],data_q_index))
    
    enc_p.inst(CZ(indices[1],indices[2]))
    enc_p.inst(CZ(indices[1],indices[3]))
    enc_p.inst(CNOT(indices[1],data_q_index))
    
    enc_p.inst(CZ(indices[2],indices[0]))
    enc_p.inst(CZ(indices[2],indices[1]))
    enc_p.inst(CNOT(indices[2],data_q_index))
    
    enc_p.inst(CZ(indices[3],indices[0]))
    enc_p.inst(CZ(indices[3],indices[2]))
    enc_p.inst(("CY",indices[3],data_q_index))
    return enc_p
# #
# #
def decode_five_to_one_quiltxt(code_indices,data_q_index,p):
    '''
        '''
    indices = [i for i in code_indices if i != data_q_index]
    dec_p = p
    dec_p.inst(("CY",indices[3],data_q_index))
    dec_p.inst(CZ(indices[3],indices[2]))
    dec_p.inst(CZ(indices[3],indices[0]))
    
    dec_p.inst(CNOT(indices[2],data_q_index))
    dec_p.inst(CZ(indices[2],indices[1]))
    dec_p.inst(CZ(indices[2],indices[0]))
    
    dec_p.inst(CNOT(indices[1],data_q_index))
    dec_p.inst(CZ(indices[1],indices[3]))
    dec_p.inst(CZ(indices[1],indices[2]))
    #
    dec_p.inst(("CY",indices[0],data_q_index))
    dec_p.inst(CZ(indices[0],indices[3]))
    dec_p.inst(CZ(indices[0],indices[1]))
    
    dec_p.inst(Z(indices[-1]))
    dec_p.inst(Z(indices[0]))
    dec_p.inst([H(q) for q in list(reversed(indices))])
    return dec_p
# #
# #
def five_logical_Z(code_indices,p):
    '''
        '''
    new_p = p
    new_p.inst([Z(q) for q in code_indices])
    return new_p
# #
# #
def five_logical_X(code_indices,p):
    '''
        '''
    new_p = p
    new_p.inst([X(q) for q in code_indices])
    return new_p
# #
# #
def five_logical_H(code_indices,p):
    '''
        Append p with a non-fault-tolerant logical Hadamard
        '''
    new_p = p
    new_p.inst([H(q) for q in code_indices])
    new_p.inst(SWAP(code_indices[0],code_indices[1]))
    new_p.inst(SWAP(code_indices[3],code_indices[4]))
    new_p.inst(SWAP(code_indices[1],code_indices[3]))
    return new_p
# #
# #
def define_matrix_logical_H(p):
    dim = np.power(2,5)
    Hbar = np.zeros((dim,dim))
    for i in range(dim):
        for j in range(dim):
            if (i == j and i < dim/2) or (i == dim - j):
                Hbar(i,j) = 1.0/np.sqrt(2.0)
            elif i == j:
                Hbar(i,j) = -1.0/np.sqrt(2.0)
    print(Hbar)
    p.defgate("Hbar",Hbar)
# #
# #
def five_q_stabilizer_control_quiltxt(ancilla_indices,code_indices,p):
    '''
        Return a quil plaintext which
        appends p with a stabilizer measurement circuit
        for the 5-qubit code.
        Input ancilla_indices: indices of new measurement ancillas that
        act as controls and are measured.
        code_indices: 5 codeword qubit indices of a logical qubit
        p: pyquil program object
        '''
    
    new_p = p
    new_p.inst([H(q) for q in ancilla_indices])
    for offset in range(0,4):
        new_p.inst(CNOT(ancilla_indices[offset],code_indices[(0+offset)%5]))
        new_p.inst(CZ(ancilla_indices[offset],  code_indices[(1+offset)%5]))
        new_p.inst(CZ(ancilla_indices[offset],  code_indices[(2+offset)%5]))
        new_p.inst(CNOT(ancilla_indices[offset],code_indices[(3+offset)%5]))
    new_p.inst([H(q) for q in ancilla_indices])
    return new_p
# #
# #
def five_q_stabilizer_measurement_quiltxt(ancilla_indices,p):
    new_p = p
    new_p.measure_all(*[(q,q) for q in ancilla_indices])
    return new_p
# #
# #





