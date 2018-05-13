from shors_code import *
from pyquil.quil import Program
from pyquil.api import QVMConnection

def main():
    code_indices    = [0,1,2,4,5,6,7,8,9]
    ancilla_indices = [10,11,12,13,14,15,16,17]
    p = Program()
    qvm = QVMConnection()
    p = encode_shors_code_quiltxt(code_indices,p)
    p = logical_X_quiltxt(code_indices,p)
    for q in range(1,9):
        p = stabilizer_quiltxt(q,code_indices,p)
    p = decode_shors_code_quiltxt(code_indices,p)
    #stabilizer_index = 1
    #p = append_stabilizer_quiltxt(stabilizer_index,code_indices,p)
    print(p)
    ket_results = qvm.wavefunction(p)
    print(ket_results)

if __name__ == '__main__':
    main()
