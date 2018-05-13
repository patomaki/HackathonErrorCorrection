import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from matplotlib import rc

rc('font', **{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def straight_line(x, m, c):

    return m*x + c


def my_exp(x, a, b, c):

    return a * np.exp(-b*x) + c


def fit_data(populations):

    logged_populations = np.log(populations)
    times = 50e-3 * np.arange(1, 250, 25)  # An identity gate takes 50ns. Use units of microsecs.
#    popt, pcov = curve_fit(straight_line, times, logged_populations)
    popt, pcov = curve_fit(my_exp, times, populations)
#    m, c = popt
#    T1 = -1/m
    a, b, c = popt
    T1 = 1/b

    plt.plot(times, populations, 'bo', label = "Data")
#    plt.plot(times, np.exp(m*logged_populations + c), label = r"Fit: T1 = {:.2f} $\mu\mathrm{{s}}$".format(T1))
    plt.plot(times, my_exp(times, *popt), color = 'tab:orange', label = r"Fit: T1 = {:.2f} $\mu\mathrm{{s}}$".format(T1))
    plt.xlabel(r"Time ($\mu\mathrm{s}$)")
    plt.ylabel(r"Excited population")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("T1_times.pdf")
    plt.show()


if __name__ == "__main__":

    populations = np.loadtxt("excited_populations_1_250_25")
    fit_data(populations)
