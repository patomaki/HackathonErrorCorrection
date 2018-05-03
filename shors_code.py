from pyquil.gates import H,CNOT,X,Z,CZ

#-----Function definitions-----#
def encode_shors_code_quiltxt(indices,p):
    '''
        Return a quil plaintext which
        appends p with encoding circuit to Shor's code.
        Input code_indices
    '''
    enc_p = p
    enc_p.inst(CNOT(indices[0],indices[0+3]))
    enc_p.inst(CNOT(indices[3],indices[3+3]))
    enc_p.inst(H(indices[0]))
    enc_p.inst(H(indices[3]))
    enc_p.inst(H(indices[6]))
    enc_p.inst(CNOT(indices[0],indices[1]))
    enc_p.inst(CNOT(indices[0],indices[2]))
    enc_p.inst(CNOT(indices[3],indices[3+1]))
    enc_p.inst(CNOT(indices[3],indices[3+2]))
    enc_p.inst(CNOT(indices[6],indices[6+1]))
    enc_p.inst(CNOT(indices[6],indices[6+2]))
    return enc_p
# #
# #
def decode_shors_code_quiltxt(indices,p):
   enc_p = p
   enc_p.inst(CNOT(indices[6],indices[6+2]))
   enc_p.inst(CNOT(indices[6],indices[6+1]))
   enc_p.inst(CNOT(indices[3],indices[3+2]))
   enc_p.inst(CNOT(indices[3],indices[3+1]))
   enc_p.inst(CNOT(indices[0],indices[2]))
   enc_p.inst(CNOT(indices[0],indices[1]))
   enc_p.inst(H(indices[6]))
   enc_p.inst(H(indices[3]))
   enc_p.inst(H(indices[0]))
   enc_p.inst(CNOT(indices[3],indices[3+3]))
   enc_p.inst(CNOT(indices[0],indices[0+3]))
   return enc_p
# #
# #
def logical_Z_quiltxt(indices,p):
    '''
        Append p with a logical Z onto qubits labelled with "indices".
        Note that physically the logical Z consists of Xs.
    '''
    new_p = p
    new_p.inst([X(indices[q]) for q in range(len(indices))])
    return new_p
# #
# #
def logical_X_quiltxt(indices,p):
    '''
        Append p with a logical X onto qubits labelled with "indices".
        Note that physically the logical Z consists of Zs.
        '''
    new_p = p
    new_p.inst([Z(indices[q]) for q in range(len(indices))])
    return new_p
# #
# #
def logical_H_quiltxt(indices,p):
    '''
        Append p with a logical H onto qubits labelled with "indices".
    '''
    new_p = p
    new_p.inst([H(indices[q]) for q in range(len(indices))])
    return new_p
# #
# #
def stabilizer_quiltxt(index,indices,p):
    '''
        Append p with a Shor's code stabilizer number "index"
    '''
    new_p = p
    if index == 1:
        new_p.inst(X(indices[0])).inst(X(indices[1])).inst(X(indices[2]))
        new_p.inst(X(indices[3])).inst(X(indices[4])).inst(X(indices[5]))
    elif index == 2:
        new_p.inst(X(indices[0])).inst(X(indices[1])).inst(X(indices[2]))
        new_p.inst(X(indices[6])).inst(X(indices[7])).inst(X(indices[8]))
    elif index == 3:
        new_p.inst(Z(indices[0])).inst(Z(indices[1]))
    elif index == 4:
        new_p.inst(Z(indices[0])).inst(Z(indices[2]))
    elif index == 5:
        new_p.inst(Z(indices[0+3])).inst(Z(indices[1+3]))
    elif index == 6:
        new_p.inst(Z(indices[0+3])).inst(Z(indices[2+3]))
    elif index == 7:
        new_p.inst(Z(indices[0+6])).inst(Z(indices[1+6]))
    elif index == 8:
        new_p.inst(Z(indices[0+6])).inst(Z(indices[2+6]))
    else:
        pass
    return new_p
# #
# #
def stabilizer_circuit_quiltxt(ancilla_indices,code_indices):
    '''
        Append p with stabilizer control circuit (everything but final
        measurements)
    '''
    new_p = p
    new_p.inst([H(q) for q in ancilla_indices])
    new_p.inst(CNOT(ancilla_indices[0],code_indices[0]))
    new_p.inst(CNOT(ancilla_indices[0],code_indices[1]))
    new_p.inst(CNOT(ancilla_indices[0],code_indices[2]))
    new_p.inst(CNOT(ancilla_indices[0],code_indices[3]))
    new_p.inst(CNOT(ancilla_indices[0],code_indices[4]))
    new_p.inst(CNOT(ancilla_indices[0],code_indices[5]))
    
    new_p.inst(CNOT(ancilla_indices[1],code_indices[0]))
    new_p.inst(CNOT(ancilla_indices[1],code_indices[1]))
    new_p.inst(CNOT(ancilla_indices[1],code_indices[2]))
    new_p.inst(CNOT(ancilla_indices[1],code_indices[6]))
    new_p.inst(CNOT(ancilla_indices[1],code_indices[7]))
    new_p.inst(CNOT(ancilla_indices[1],code_indices[8]))

    new_p.inst(CZ(ancilla_indices[2],code_indices[0]))
    new_p.inst(CZ(ancilla_indices[2],code_indices[1]))

    new_p.inst(CZ(ancilla_indices[3],code_indices[0]))
    new_p.inst(CZ(ancilla_indices[3],code_indices[2]))

    new_p.inst(CZ(ancilla_indices[4],code_indices[3]))
    new_p.inst(CZ(ancilla_indices[4],code_indices[4]))

    new_p.inst(CZ(ancilla_indices[5],code_indices[3]))
    new_p.inst(CZ(ancilla_indices[5],code_indices[5]))

    new_p.inst(CZ(ancilla_indices[6],code_indices[6]))
    new_p.inst(CZ(ancilla_indices[6],code_indices[7]))

    new_p.inst(CZ(ancilla_indices[7],code_indices[6]))
    new_p.inst(CZ(ancilla_indices[7],code_indices[8]))
    new_p.inst([H(q) for q in ancilla_indices])
