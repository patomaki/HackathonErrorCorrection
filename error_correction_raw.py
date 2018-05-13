def enc1(prog,q1,i,j): #takes single qubit, specify which ancillas to use
    enc1 = prog
    return enc1.inst(CNOT(q1,i)).inst(CNOT(q1,j))

def meas1(prog): #measures first 3 qubits
    results = qvm.run_and_measure(prog, qubits=range(3), trials=10)
    return results

def qpumeas1(prog): #measures first 3 qubits
    results = qpu.run_and_measure(prog, qubits=range(3), trials=10)
    return results

def meas2(prog): #measures first 9
    results = qvm.run_and_measure(prog, qubits=range(9), trials=10)
    return results

def enc2(prog): #takes 3 bit rep
    enc2 = prog
    return enc2.inst(CNOT(0,1)).inst(CNOT(0,2)).inst(CNOT(3,4)).inst(CNOT(3,5)).inst(CNOT(6,7)).inst(CNOT(6,8))

def enc(prog): #concatenated repetition code for qubit 1
    encoded = enc1(prog,3,6)
    conc = enc2(encoded)
    return conc

def decode1(enc,q1,q2,q3): #decode 3bitflip 
    dec = enc
    return dec.inst(CNOT(q1,q2)).inst(CNOT(q1,q3))

def zpar(prog, i, j, k):
    return  prog.inst(CNOT(i,k),CNOT(j,k))

def xpar(prog, i, j, k):
    return  prog.inst(H(i),H(j),CNOT(i,k),CNOT(j,k),H(i),H(j))
    
def correctphas(prog,q1,q2,q3,a1,a2):
    xpar(prog,q1,q2,a1)
    xpar(prog,q2,q3,a2)
    return prog.inst(H(q2),CCNOT(a1,a2,q2),H(q2),H(q1),X(a2)
                     ,CCNOT(a1,a2,q1),X(a2),H(q1),H(q3),X(a1),CCNOT(a1,a2,q3),H(q3),X(a1),MEASURE(a1,a1),MEASURE(a2,a2))

def correctbit(prog,q1,q2,q3,a1,a2):
    zpar(prog,q1,q2,a1)
    zpar(prog,q2,q3,a2)
    return prog.inst(CCNOT(a1,a2,q2),X(a2),CCNOT(a1,a2,q1),X(a2),X(a1),CCNOT(a1,a2,q3),X(a1),MEASURE(a1,a1),MEASURE(a2,a2))
        
def encphas(prog,q1,i,j): #takes single qubit, specify which ancillas to use
    enc1 = prog
    return enc1.inst(CNOT(q1,i)).inst(CNOT(q1,j)).inst(H(q1)).inst(H(i)).inst(H(j)) 

def decodephas1(enc,q1,q2,q3): #decode 3phaseflip 
    dec = enc
    return dec.inst(H(q1)).inst(H(q2)).inst(H(q3)).inst(CNOT(q1,q2)).inst(CNOT(q1,q3))
