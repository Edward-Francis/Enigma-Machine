from string import ascii_uppercase

import pytest

import enigma_machine
from enigma_machine import (
    M3,
    M4,
    REFLECTORS,
    InputException,
    Plugboard,
    Reflector,
    Rotor,
)


@pytest.mark.parametrize(
    "type,position,ring,first,last",
    [
        ("I", "A", 1, "E", "J"),
        ("I", "X", 1, "R", "B"),
        ("II", "R", 1, "G", "Q"),
        ("VII", "F", 1, "R", "G"),
        ("I", "A", 3, "E", "T"),
        ("I", "A", 2, "K", "D"),
        ("I", "O", 15, "S", "X"),
        ("I", "Z", 26, "D", "I"),
    ],
)
def test_rotor_initialisation(type, position, ring, first, last) -> None:
    rotor = Rotor(type, position, ring)
    assert rotor.type == type
    assert rotor.ring == ring - 1
    assert rotor.turnovers == list(enigma_machine.WHEELS[type][1])
    assert rotor.wiring[0] == first
    assert rotor.wiring[-1] == last
    assert rotor.alphabet[0] == ascii_uppercase[ord(position) - 65]


def test_rotor_stepping() -> None:
    rotor = Rotor("I", "A")
    alphabet = list(ascii_uppercase)
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
        alphabet = ascii_uppercase
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


def test_m3_initialisation() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert len(m3.rotors) == 3
    assert m3.rotors[0].type == "I"
    assert m3.rotors[1].type == "II"
    assert m3.rotors[2].type == "III"
    assert m3.reflector.type == "B"
    assert m3.plugboard.map == {}


@pytest.mark.parametrize(
    "settings,input,output",
    [
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A")),
                "reflector": "B",
                "locked": True,
            },
            "HELLO",
            "EHPPK",
        ),
        (
            {"rotors": (("I", "A"), ("II", "A"), ("III", "A")), "reflector": "B"},
            "HELLO",
            "MFNCZ",
        ),
        (
            {"rotors": (("IV", "J"), ("V", "Y"), ("VIII", "Q")), "reflector": "C"},
            "HELLO",
            "ATXGN",
        ),
        (
            {"rotors": (("III", "U"), ("II", "D"), ("I", "A")), "reflector": "B"},
            "HELLO",
            "IBXXX",
        ),
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A")),
                "reflector": "B",
                "locked": True,
                "plugboard": {"H": "I", "E": "F", "L": "M", "O": "P"},
            },
            "HELLO",
            "RBWWM",
        ),
        (
            {
                "rotors": (("III", "U"), ("II", "D"), ("I", "A")),
                "reflector": "B",
                "plugboard": {"H": "I", "E": "F", "L": "M", "O": "P"},
            },
            "HELLO",
            "ITYJZ",
        ),
        (
            {
                "rotors": (("II", "W"), ("VII", "E"), ("VI", "H")),
                "reflector": "C",
                "plugboard": {
                    "A": "B",
                    "C": "D",
                    "E": "F",
                    "G": "H",
                    "I": "K",
                    "L": "P",
                    "Z": "V",
                },
            },
            "LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELIT",
            "REMHWEVCZSZQBFELFWCDUYTXXGIXFNEWONKSLECFVRVXOED",
        ),
        (
            {
                "rotors": (("I", "A", 3), ("II", "A", 15), ("III", "A", 26)),
                "reflector": "B",
            },
            "HELLO",
            "IGTGM",
        ),
        (
            {
                "rotors": (("VII", "J", 11), ("V", "H", 16), ("II", "G", 3)),
                "reflector": "C",
            },
            "HELLO",
            "PUAUB",
        ),
    ],
)
def test_m3_transform_string(settings, input, output) -> None:
    assert M3(**settings).transform_string(input) == output
    assert M3(**settings).transform_string(output) == input


def test_m3_transform_invalid_character() -> None:
    with pytest.raises(InputException, match=r"Input must be between A-Z"):
        m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
        m3.transform_character("[")


def test_m3_transform_spaces_ignored() -> None:
    m3 = M3(rotors=(("I", "A"), ("II", "A"), ("III", "A")), reflector="B")
    assert m3.transform_string("Hello World") == "MFNCZBBFZM"


@pytest.mark.parametrize(
    "settings,input,output",
    [
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A"), ("Beta", "A")),
                "reflector": "B-Thin",
                "locked": True,
            },
            "HELLO",
            "EHPPK",
        ),
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A"), ("Beta", "A")),
                "reflector": "B-Thin",
            },
            "HELLO",
            "MFNCZ",
        ),
        (
            {
                "rotors": (("IV", "J"), ("V", "Y"), ("VIII", "Q"), ("Beta", "X")),
                "reflector": "C-Thin",
            },
            "HELLO",
            "IDWBT",
        ),
        (
            {
                "rotors": (("III", "U"), ("II", "D"), ("I", "A"), ("Gamma", "F")),
                "reflector": "C-Thin",
            },
            "HELLO",
            "DHTBB",
        ),
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A"), ("Gamma", "L")),
                "reflector": "B-Thin",
                "locked": True,
                "plugboard": {"H": "I", "E": "F", "L": "M", "O": "P"},
            },
            "HELLO",
            "PQZZW",
        ),
        (
            {
                "rotors": (("I", "A"), ("II", "A"), ("III", "A"), ("Gamma", "L")),
                "reflector": "B-Thin",
                "plugboard": {"H": "I", "E": "F", "L": "M", "O": "P"},
            },
            "HELLO",
            "LCHMB",
        ),
        (
            {
                "rotors": (("II", "W"), ("VII", "E"), ("VI", "H"), ("Beta", "E")),
                "reflector": "B-Thin",
                "plugboard": {
                    "A": "B",
                    "C": "D",
                    "E": "F",
                    "G": "H",
                    "I": "K",
                    "L": "P",
                    "Z": "V",
                },
            },
            "LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELIT",
            "YGNFBLNYRSUBOZNTFLNZNDDUVIQGWNOEDPKEUNOWEMJRTQV",
        ),
        (
            {
                "rotors": (
                    ("I", "A", 3),
                    ("II", "A", 15),
                    ("III", "A", 26),
                    ("Beta", "E", 8),
                ),
                "reflector": "B-Thin",
            },
            "HELLO",
            "LOHRZ",
        ),
        (
            {
                "rotors": (
                    ("VII", "J", 11),
                    ("V", "H", 16),
                    ("II", "G", 3),
                    ("Gamma", "T", 16),
                ),
                "reflector": "C-Thin",
            },
            "HELLO",
            "BNCJC",
        ),
    ],
)
def test_m4_transform_string(settings, input, output) -> None:
    assert M4(**settings).transform_string(input) == output
    assert M4(**settings).transform_string(output) == input
