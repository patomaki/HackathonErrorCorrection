from pyquil.gates import H,CNOT,X,Z,CZ
#-----Function definitions-----#
def encode_repetition_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with repetition encoding circuit for qubits labelled
    with code_indices, and data qubit at data_q_index.
    '''
    ancilla_indices = [q for q in code_indices if q != data_q_index]
    enc_p = p
    enc_p.inst(CNOT(data_q_index,ancilla_indices[0]))
    enc_p.inst(CNOT(data_q_index,ancilla_indices[1]))
    return enc_p
# #
# #
def decode_repetition_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with decoding circuit for repetition code.
    '''
    ancilla_indices = [q for q in code_indices if q != data_q_index]
    dec_p = p
    dec_p.inst(CNOT(data_q_index,ancilla_indices[1]))
    dec_p.inst(CNOT(data_q_index,ancilla_indices[0]))
    return dec_p
# #
# #
def repetition_logical_Z(p):
    '''
    '''
    new_p = p
    new_p.inst(Z(code_indices[0]))
    return new_p
# #
# #
def repetition_logical_X(p):
    '''
    '''
    new_p = p
    new_p.inst([X(q) for q in code_indices])
    return new_p
# #
# #
def encode_phase_correction_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with phase correction encoding circuit for qubits labelled
    with code_indices, and data qubit at data_q_index.
    '''
    enc_p = encode_repetition_code_qubit(code_indices,data_q_index,p)
    enc_p.inst([H(q) for q in code_indices])
    return enc_p
# #
# #
def decode_phase_correction_code_qubit(code_indices,data_q_index,p):
    '''
    Append p with decoding circuit for phase correction code.
    '''
    dec_p = p
    dec_p.inst([H(q) for q in code_indices])
    dec_p = decode_repetition_code_qubit(code_indices,data_q_index,enc_p)
    return dec_p
# #
# #
def phase_logical_Z(p):
    '''
    '''
    new_p = p
    new_p.inst([Z(q) for q in code_indices])
    return new_p
# #
# #
def phse_logical_X(p):
   '''
   '''
   new_p = p
   new_p.inst(X(code_indices[0]))
   return new_p







