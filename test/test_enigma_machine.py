from enigma_machine import M3
from enigma_machine.enigma_machine import fib


def test_fib() -> None:
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(10) == 55


def test_m3_initialisation() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert len(m3.rotors) == 3
    assert m3.rotors[0].type == "I"
    assert m3.rotors[1].type == "II"
    assert m3.rotors[2].type == "III"
    assert m3.reflector.type == "B"
