import string

import pytest

import enigma_machine
from enigma_machine import M3, REFLECTORS, InputException, Plugboard, Reflector, Rotor


def test_m3_initialisation() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert len(m3.rotors) == 3
    assert m3.rotors[0].type == "I"
    assert m3.rotors[1].type == "II"
    assert m3.rotors[2].type == "III"
    assert m3.reflector.type == "B"
    assert m3.plugboard.map == {}


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
    assert rotor.alphabet[0] == string.ascii_uppercase[ord(position) - 65]


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


def test_rotor_reverse() -> None:
    assert Rotor("I", "A").reverse("A", 0) == ("U", 0)
    assert Rotor("I", "A").reverse("B", 0) == ("W", 0)
    assert Rotor("I", "A").reverse("Z", 0) == ("J", 0)
    assert Rotor("I", "B").reverse("A", 0) == ("W", 1)
    assert Rotor("I", "B").reverse("Z", 0) == ("U", 1)
    assert Rotor("I", "G").reverse("R", 3) == ("R", 6)
    assert Rotor("I", "G").reverse("O", 3) == ("X", 6)
    assert Rotor("I", "Z").reverse("A", 25) == ("U", 25)
    assert Rotor("I", "Z").reverse("Z", 25) == ("J", 25)


@pytest.mark.parametrize("type", REFLECTORS.keys())
def test_reflector_initialisation(type) -> None:
    reflector = Reflector(type)
    assert reflector.type == type
    assert reflector.wiring == list(enigma_machine.REFLECTORS[type])
    assert reflector.count == 0


@pytest.mark.parametrize("type", REFLECTORS.keys())
def test_reflector_reflect(type) -> None:
    reflector = Reflector(type)
    alphabet = REFLECTORS[type]
    for i in range(26):
        assert reflector.forward("A", i) == (alphabet[(26 - i) % 26], 0)
        assert reflector.forward("Z", i) == (alphabet[25 - i], 0)


def test_plugboard_initialisation() -> None:
    pb = Plugboard({"A": "B", "C": "D"})
    assert pb.map["A"] == "B"
    assert pb.map["C"] == "D"
    assert pb.map["B"] == "A"
    assert pb.map["D"] == "C"


def test_plugboard_map_character() -> None:
    pb = Plugboard({"A": "B"})
    assert pb.map_character("A") == "B"
    assert pb.map_character("B") == "A"


def test_plugboard_maximum_connections() -> None:
    with pytest.raises(
        InputException, match=r"Exceeds 13 maximum plugboard connections."
    ):
        alphabet = string.ascii_uppercase
        Plugboard(list(zip(alphabet, reversed(alphabet))))


def test_plugboard_invalid_characters() -> None:
    with pytest.raises(
        InputException, match=r"Plugboard connections must be between A-Z."
    ):
        Plugboard({"A": "]"})


def test_plugboard_repeated_characters() -> None:
    with pytest.raises(InputException, match=r"Plugboard connections repeated."):
        Plugboard({"A": "B", "B": "C"})


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


def test_m3_transform_string_locked() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B", locked=True)
    assert m3.transform_string("HELLO") == "EHPPK"


def test_m3_transform_string_basic() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert m3.transform_string("HELLO") == "MFNCZ"


def test_m3_transform_string_stepping_double() -> None:
    m3 = M3(rotors=(("III", "U"), ("II", "D"), ("I", "A")), reflector="B")
    assert m3.transform_string("HELLO") == "IBXXX"


def test_m3_transform_string_long() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    input = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    output = "ftzmgisxipjwgdnjjcoqtyrigdmxfiesrwzgtoiuiekkdcshtpyoepvxnhvrwwesfruxdgwozdmnkizwnczducobltuyhdzgovbuypkojwbowseemtzfwygkodtbzdqrczcifdidxcqzookviiomllegmsojxhnfhbofdzctzqpowvomqnwqquozufmsdxmjxiyzkozdewgedjxsmyhkjkriqxwbitwlyusthzqmgtxxwihdobtkcgzuvekyekyrewlywfmhlqjqjwcvtksnhzegwzkvexktdzxlchryjqqdzhyypzorygfkkkgufdcutkrjqgzwjdlmtyyigdoxoigqdwqgouyupewdwcingpdobrkxtjlkqjsrbimxvgzmebfzklowxuktdfnfnyyyowzyjworigokhhlngbpuyxfdcqlpxschhsljlsyfslcmmbknglvkwvqvdjgoiquuhqxokdpicpeycmhkokedzdtjvsyekpowmcrzgrvfwgfekewtpmztvbxmkiihhhmyxjnjvjillvqbxeqyhomtnzrfdbstekfirqhyoizdmbtsverbnhjpijoufljtnulrzzcbwswexnrhfgkjludpxzjiqtlnzfkylrugebhruksygqkprclkyqbpbhdvlosrzfbrungqydwsleymypsnrwmhyrglvruptfupucneomqhbecbnjxvzfsqmzbusefxwfcpliprqlkpmumkhvkboxbkunixhbhdvqgdpjgjcsc".upper()
    assert m3.transform_string(input) == output
    assert 1 == 1


def test_m3_transform_invalid_character() -> None:
    with pytest.raises(InputException, match=r"Input must be between A-Z"):
        m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
        m3.transform_character("[")


def test_m3_transform_string_locked_plugboard() -> None:
    m3 = M3(
        rotors=(("I", "A"), ("II", "A"), ("III", "A")),
        reflector="B",
        locked=True,
        plugboard={"H": "I", "E": "F", "L": "M", "O": "P"},
    )
    assert m3.transform_string("HELLOB") == "RBWWME"
