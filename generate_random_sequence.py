import numpy as np

def generate_random_sequence(n):

    return np.random.randint(low=0, high=2, size=n)
            

def write_to_file(sequence, filename):

    np.savetxt(filename, sequence, fmt='%d')


def main():

    n = 10000
    sequence = generate_random_sequence(n)
    write_to_file(sequence, "python_random_sequence_10000.txt")


if __name__ == "__main__":

    main()
