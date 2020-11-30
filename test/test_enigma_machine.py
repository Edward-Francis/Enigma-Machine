import pytest

import enigma_machine
from enigma_machine import M3, Reflector, Rotor
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


@pytest.mark.parametrize("type", ["I", "II", "III"])
def test_rotor_initialisation(type) -> None:
    rotor = Rotor(type, "A")
    assert rotor.type == type
    assert rotor.wiring == list(enigma_machine.WHEELS[type][0])
    assert rotor.turnovers == list(enigma_machine.WHEELS[type][1])


@pytest.mark.parametrize("type", ["B", "C"])
def test_reflector_initialisation(type) -> None:
    reflector = Reflector(type)
    assert reflector.type == type
    assert reflector.wiring == list(enigma_machine.REFLECTORS[type])
