# S. Patomaki, April 2018 Quantum Hackathon for rigetti
import matplotlib.pyplot as plt
import numpy as np
def basic_plot(x,fig_name='x.pdf'):
    '''
    '''
    plt.figure()
    plt.plot(x)
    plt.savefig(fig_name)

# #
# #
def matrix_plot(x,fig_name='matrix_x.pdf'):
    '''
    '''
    dx = int(np.sqrt(len(x)))
    number_matrix = np.array(x).reshape((dx,dx))
    plt.figure()
    plt.matshow(number_matrix)
    plt.savefig(fig_name)
