import string

import pytest

import enigma_machine
from enigma_machine import M3, REFLECTORS, Reflector, Rotor
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


def test_rotor_stepping() -> None:
    rotor = Rotor("I", "A")
    alphabet = list(string.ascii_uppercase)
    for _ in range(3):
        for letter in alphabet:
            assert rotor.rotor_position() == letter
            rotor.step()


def test_rotor_forward() -> None:
    assert Rotor("I", "A").forward("A", 0) == ("E", 0)
    assert Rotor("I", "A").forward("B", 0) == ("K", 0)
    assert Rotor("I", "A").forward("Z", 0) == ("J", 0)
    assert Rotor("I", "B").forward("A", 0) == ("K", 1)
    assert Rotor("I", "B").forward("Z", 0) == ("E", 1)
    assert Rotor("I", "G").forward("R", 3) == ("A", 6)
    assert Rotor("I", "G").forward("O", 3) == ("U", 6)
    assert Rotor("I", "Z").forward("A", 25) == ("E", 25)
    assert Rotor("I", "Z").forward("Z", 25) == ("J", 25)


@pytest.mark.parametrize("type", REFLECTORS.keys())
def test_reflector_initialisation(type) -> None:
    reflector = Reflector(type)
    assert reflector.type == type
    assert reflector.wiring == list(enigma_machine.REFLECTORS[type])


@pytest.mark.parametrize("type", REFLECTORS.keys())
def test_reflector_reflect(type) -> None:
    reflector = Reflector(type)
    alphabet = REFLECTORS[type]
    for i in range(26):
        assert reflector.reflect("A", i) == alphabet[(26 - i) % 26]
        assert reflector.reflect("Z", i) == alphabet[25 - i]


def test_m3_stepping_locked() -> None:
    m3 = M3(rotors=(("III", "U"), ("II", "A"), ("I", "A")), reflector="B", locked=True)
    assert m3.rotor_positions() == ["U", "A", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["U", "A", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["U", "A", "A"]


def test_m3_stepping_normal() -> None:
    m3 = M3(rotors=(("III", "U"), ("II", "A"), ("I", "A")), reflector="B")
    assert m3.rotor_positions() == ["U", "A", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["V", "A", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["W", "B", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["X", "B", "A"]


def test_m3_stepping_double() -> None:
    m3 = M3(rotors=(("III", "U"), ("II", "D"), ("I", "A")), reflector="B")
    assert m3.rotor_positions() == ["U", "D", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["V", "D", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["W", "E", "A"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["X", "F", "B"]
    m3.transform_character("A")
    assert m3.rotor_positions() == ["Y", "F", "B"]


def test_m3_transform_string_basic() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert m3.transform_string("HELLO") == "MFNCZ"


def test_m3_transform_string_stepping_double() -> None:
    m3 = M3(rotors=(("III", "U"), ("II", "D"), ("I", "A")), reflector="B")
    assert m3.transform_string("HELLO") == "IBXXX"
