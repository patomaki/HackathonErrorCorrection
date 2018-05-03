from pyquil.gates import H,CNOT,X,Z,CZ,CCNOT
import numpy as np

#-----Function definitions-----#

def def_CCCNOT(p):
    '''
        Define a triple control not gate to program p
    '''
    CCCNOT = np.array([[1.,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,1.,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,1.,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,1.,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,1.,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,1.,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,1.,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,1.,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,1.,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,1.,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,1.,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,1.,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,1.,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,1.,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.,0]])
    p.defgate("CCCNOT",CCCNOT)

def def_CCCZ(p):
    '''
        Define a triple control not gate to program p
    '''
    CCCZ = np.array([[1.,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,1.,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,1.,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,1.,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,1.,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,1.,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,1.,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,1.,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,1.,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,1.,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,1.,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,1.,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,1.,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,1.,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1.]])
    p.defgate("CCCZ",CCCZ)

def encode_steane_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with Steane code encoding circuit for qubits
    with indices code_indices, and data qubit with index
    data_q_index.
    '''
    ancilla_indices = [i for i in code_indices if i!=data_q_index]
    enc_p = p
    enc_p.inst([H(q) for q in ancilla_indices[3:6]])
    enc_p.inst(CNOT(data_q_index,ancilla_indices[0]))
    enc_p.inst(CNOT(data_q_index,ancilla_indices[1]))
    enc_p.inst(CNOT(ancilla_indices[5],ancilla_indices[0]))
    enc_p.inst(CNOT(ancilla_indices[5],ancilla_indices[2]))
    enc_p.inst(CNOT(ancilla_indices[5],data_q_index))
    enc_p.inst(CNOT(ancilla_indices[4],ancilla_indices[1]))
    enc_p.inst(CNOT(ancilla_indices[4],ancilla_indices[2]))
    enc_p.inst(CNOT(ancilla_indices[4],data_q_index))
    enc_p.inst(CNOT(ancilla_indices[3],ancilla_indices[0]))
    enc_p.inst(CNOT(ancilla_indices[3],ancilla_indices[1]))
    enc_p.inst(CNOT(ancilla_indices[3],ancilla_indices[2]))
    return enc_p
# #
# #
def decode_steane_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with Steane code decoding circuit for qubits
    with indices code_indices and data qubit with index
    data_q_index.
    '''
    ancilla_indices = [i for i in code_indices if i!=data_q_index]
    dec_p = p
    dec_p.inst(CNOT(ancilla_indices[3],ancilla_indices[2]))
    dec_p.inst(CNOT(ancilla_indices[3],ancilla_indices[1]))
    dec_p.inst(CNOT(ancilla_indices[3],ancilla_indices[0]))
    dec_p.inst(CNOT(ancilla_indices[4],data_q_index))
    dec_p.inst(CNOT(ancilla_indices[4],ancilla_indices[2]))
    dec_p.inst(CNOT(ancilla_indices[4],ancilla_indices[1]))
    dec_p.inst(CNOT(ancilla_indices[5],data_q_index))
    dec_p.inst(CNOT(ancilla_indices[5],ancilla_indices[2]))
    dec_p.inst(CNOT(ancilla_indices[5],ancilla_indices[0]))
    dec_p.inst(CNOT(data_q_index,ancilla_indices[1]))
    dec_p.inst(CNOT(data_q_index,ancilla_indices[0]))
    dec_p.inst([H(q) for q in ancilla_indices[3:6]])
    return dec_p
# #
# #
def logical_X(code_indices,p):
    '''
    Steane code logical X
    '''
    new_p = p
    new_p.inst([X(q) for q in code_indices])
    return new_p
# #
# #
def logical_Z(code_indices,p):
    '''
    Steane code logical Z
    '''
    new_p = p
    new_p.inst([Z(q) for q in code_indices])
    return new_p
# #
# #
def logical_H(code_indices,p):
    '''
    Steane code logical H
    '''
    new_p = p
    new_p.inst([H(q) for q in code_indices])
    return new_p
# #
# #
def stabilizer(stabilizer_index,code_indices,p):
    '''
    Steane code stabilizer of index stabilizer_index (0-5)
    '''
    new_p = p
    if stabilizer_index == 0:
        new_p.inst([X(q) for q in code_indices[3:7]])
    elif stabilizer_index == 1:
        new_p.inst([X(code_indices[0]),X(code_indices[1])])
        new_p.inst([X(code_indices[4]),X(code_indices[5])])
    elif stabilizer_index == 2:
        new_p.inst([X(q) for q in code_indices if q%2==0])
    elif stabilizer_index == 3:
        new_p.inst([Z(q) for q in code_indices[3:7]])
    elif stabilizer_index == 4:
        new_p.inst([Z(code_indices[0]),Z(code_indices[1])])
        new_p.inst([Z(code_indices[4]),Z(code_indices[5])])
    elif stabilizer_index == 5:
        new_p.inst([Z(q) for q in code_indices if q%2==0])
    return new_p
# #
# #
def syndrome_circuit(ancilla_indices,code_indices,p):
    '''
    Circuit for 1-qubit error detection in the Steane code
    '''
    syn_p = p
    syn_p.inst([H(q) for q in ancilla_indices])
    syn_p.inst([CNOT(ancilla_indices[0],q)
                for q in code_indices[3:7]])
    syn_p.inst([CNOT(ancilla_indices[1],code_indices[1]),
                CNOT(ancilla_indices[1],code_indices[2])])
    syn_p.inst([CNOT(ancilla_indices[1],code_indices[5]),
                CNOT(ancilla_indices[1],code_indices[6])])
    #syn_p.inst([CNOT(ancilla_indices[2],q) for q in range(len(code_indices)) if q%2==0])
    syn_p.inst([CNOT(ancilla_indices[2],code_indices[0]),
                CNOT(ancilla_indices[2],code_indices[2])])
    syn_p.inst([CNOT(ancilla_indices[2],code_indices[4]),
                CNOT(ancilla_indices[2],code_indices[6])])

    syn_p.inst([CZ(ancilla_indices[3],q)
                for q in code_indices[3:7]])
    syn_p.inst([CZ(ancilla_indices[4],code_indices[1]),
                CZ(ancilla_indices[4],code_indices[2])])
    syn_p.inst([CZ(ancilla_indices[4],code_indices[5]),
                CZ(ancilla_indices[4],code_indices[6])])
    #syn_p.inst([CZ(ancilla_indices[5],q) for q in range(len(code_indices)) if q%2==0])
    syn_p.inst([CZ(ancilla_indices[5],code_indices[0]),
                CZ(ancilla_indices[5],code_indices[2])])
    syn_p.inst([CZ(ancilla_indices[5],code_indices[4]),
                CZ(ancilla_indices[5],code_indices[6])])
    syn_p.inst([H(q) for q in ancilla_indices])
    return syn_p
# #
# #
def conditional_error_correction(ancilla_indices,code_indices,p):
    '''
    '''
    new_p = p

    # 1-qubit X-errors
    #new_p.inst(CNOT(ancilla_indices[3],code_indices[3]))
    #new_p.inst(CNOT(ancilla_indices[4],code_indices[1]))
    #new_p.inst(CNOT(ancilla_indices[5],code_indices[0]))
    new_p.inst(("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[6]))
    new_p.inst(X(ancilla_indices[3]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[2]),X(ancilla_indices[3]))
    new_p.inst(X(ancilla_indices[4]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[4]),X(ancilla_indices[4]))
    new_p.inst(X(ancilla_indices[5]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[5]),X(ancilla_indices[5]),)
    new_p.inst(X(ancilla_indices[3]),X(ancilla_indices[4]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[0]),X(ancilla_indices[3]),X(ancilla_indices[4]))
    new_p.inst(X(ancilla_indices[3]),X(ancilla_indices[5]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[1]),X(ancilla_indices[3]),X(ancilla_indices[5]))
    new_p.inst(X(ancilla_indices[4]),X(ancilla_indices[5]),("CCCNOT",ancilla_indices[3],ancilla_indices[4],ancilla_indices[5],code_indices[3]),X(ancilla_indices[4]),X(ancilla_indices[5]))

    # 1-qubit Z-errors
    #new_p.inst(CZ(ancilla_indices[0],code_indices[3]))
    #new_p.inst(CZ(ancilla_indices[1],code_indices[1]))
    #new_p.inst(CZ(ancilla_indices[2],code_indices[0]))
    new_p.inst(("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[6]))
    new_p.inst(X(ancilla_indices[0]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[2]),X(ancilla_indices[0]))
    new_p.inst(X(ancilla_indices[1]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[4]),X(ancilla_indices[1]))
    new_p.inst(X(ancilla_indices[2]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[5]),X(ancilla_indices[2]),)
    new_p.inst(X(ancilla_indices[0]),X(ancilla_indices[1]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[0]),X(ancilla_indices[0]),X(ancilla_indices[1]))
    new_p.inst(X(ancilla_indices[0]),X(ancilla_indices[2]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[1]),X(ancilla_indices[0]),X(ancilla_indices[2]))
    new_p.inst(X(ancilla_indices[1]),X(ancilla_indices[2]),("CCCZ",ancilla_indices[0],ancilla_indices[1],ancilla_indices[2],code_indices[3]),X(ancilla_indices[1]),X(ancilla_indices[2]))
    
    return new_p


