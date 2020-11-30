import sys

from enigma_machine.enigma_machine import fib

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
