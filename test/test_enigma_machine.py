import pytest

import enigma_machine
from enigma_machine import M3, REFLECTORS, WHEELS, Reflector, Rotor
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


@pytest.mark.parametrize(
    "type,position,first,last",
    [
        ("I", "A", "E", "J"),
        ("I", "X", "R", "B"),
        ("II", "R", "G", "Q"),
        ("VII", "F", "R", "G"),
    ],
)
def test_rotor_initialisation(type, position, first, last) -> None:
    rotor = Rotor(type, position)
    assert rotor.type == type
    assert rotor.turnovers == list(enigma_machine.WHEELS[type][1])
    assert rotor.wiring[0] == first
    assert rotor.wiring[-1] == last


@pytest.mark.parametrize("type", WHEELS.keys())
def test_rotor_forward(type) -> None:
    rotor = Rotor(type, "A")
    alphabet, _ = WHEELS.get(type, ("", ""))
    assert rotor.forward("A") == alphabet[0]
    assert rotor.forward("Z") == alphabet[25]


@pytest.mark.parametrize("type", WHEELS.keys())
def test_rotor_reverse(type) -> None:
    rotor = Rotor(type, "A")
    alphabet = WHEELS.get(type, "")
    assert rotor.reverse("A") == chr(alphabet[0].index("A") + 65)


@pytest.mark.parametrize("type", ["B", "C"])
def test_reflector_initialisation(type) -> None:
    reflector = Reflector(type)
    assert reflector.type == type
    assert reflector.wiring == list(enigma_machine.REFLECTORS[type])


@pytest.mark.parametrize("type", REFLECTORS.keys())
def test_reflector_reflect(type) -> None:
    reflector = Reflector(type)
    alphabet = REFLECTORS.get(type, "")
    assert reflector.reflect("A") == alphabet[0]
    assert reflector.reflect("Z") == alphabet[25]


def test_m3_transform_string_locked() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B", locked=True)
    assert m3.transform_string("hello") == "EHPPK"


def test_m3_transform_string_basic() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert m3.transform_string("hello") == "MFNCZ"


def test_m3_transform_string_basic2() -> None:
    m3 = M3(rotors=(("I", "H"), ("II", "A"), ("III", "A")), reflector="B")
    assert m3.transform_string("E") == "K"
