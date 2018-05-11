import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


def straight_line(x, m, c):

    return m*x + c


def fit_data(populations):

    logged_populations = np.log(populations)
    times = 50e-9 * np.arange(1, 250, 25)  # An identity gate takes 50ns
    popt, pcov = curve_fit(straight_line, times, logged_populations)
    m, c = popt
    T1 = -1/m

    plt.semilogy(times, populations, label = "Data")
    plt.semilogy(times, np.exp(m*logged_populations + c), label = "Fit: T1 = {}".format(T1))
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("Excited population")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()
    plt.savefig("T1_times.pdf")


if __name__ == "__main__":

    populations = np.loadtxt("excited_populations_1_250_25")
    fit_data(populations)
