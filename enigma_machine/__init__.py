from string import ascii_uppercase
from typing import List, Tuple

WHEELS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
    "VI": ("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
    "VII": ("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
    "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
    "Beta": ("LEYJVCNIXWPBQMDRTAKZGFUHOS", ""),
    "Gamma": ("FSOKANUERHMBTIYCWLQPZXVGJD", ""),
}

REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    "B-Thin": "ENKQAUYWJICOPBLMDXZVFTHRGS",
    "C-Thin": "RDOBJNTKVEHMLFCWZAXGYIPSUQ",
}


class InputException(Exception):
    """Exception representing Enigma configuration failure."""

    pass


class Rotor:
    """Module representing Enigma rotor mechanism."""

    def __init__(self, __type: str, position: str, ring: int = 1):
        self.type = __type
        self.position = position
        self.ring = ring - 1
        wiring, turnovers = WHEELS[self.type]
        self.alphabet = list(ascii_uppercase)
        self.wiring = list(wiring)
        self.turnovers = list(turnovers)
        offset = ord(position) - 65
        self.count = offset
        self.alphabet = self.alphabet[offset:] + self.alphabet[:offset]
        self.wiring = self.wiring[offset:] + self.wiring[:offset]

        dot = self.wiring.index(self.position)
        for i in range(self.ring):
            dot = dot + 1
            for index, c in enumerate(self.wiring):
                self.wiring[index] = chr(((ord(c) - 64) % 26) + 65)
        ring_offset = self.ring * -1
        self.wiring = self.wiring[ring_offset:] + self.wiring[:ring_offset]

    def step(self) -> None:
        """Rotates the rotor position forward by one."""
        self.alphabet = self.alphabet[1:] + [self.alphabet[0]]
        self.wiring = self.wiring[1:] + [self.wiring[0]]
        self.count = self.count + 1
        if self.count > 25:
            self.count = 0

    def rotor_position(self) -> str:
        """Function returns the character of the rotor current position."""
        return chr(self.count + 65)

    def forward(self, char: str, offset: int) -> Tuple[str, int]:
        """Function for rotor traversal in the forward direction."""
        return (self.wiring[ord(char) - 65 - offset], self.count)

    def reverse(self, char: str, offset: int) -> Tuple[str, int]:
        """Function for rotor traversal in the backwards direction."""
        position = self.alphabet[ord(char) - 65 - offset]
        char = self.alphabet[self.wiring.index(position)]
        return char, self.count


class Reflector(Rotor):
    """Module representing Enigma reflector mechanism."""

    def __init__(self, __type):
        self.type = __type
        self.wiring = list(REFLECTORS[self.type])
        self.count = 0


class Plugboard:
    """Module representing Enigma plugboard mechanism."""

    def __init__(self, _map={}) -> None:
        used_characters = []

        if len(_map) > 13:
            raise InputException("Exceeds 13 maximum plugboard connections.")

        for k, v in _map.items():
            if k not in ascii_uppercase or v not in ascii_uppercase:
                raise InputException("Plugboard connections must be between A-Z.")
            if k in used_characters or v in used_characters:
                raise InputException("Plugboard connections repeated.")
            else:
                used_characters.append(k)
                used_characters.append(v)

        inv_map = {v: k for k, v in _map.items()}
        self.map = {**inv_map, **_map}

    def map_character(self, char) -> str:
        """Calculates and returns the transposed character."""
        return self.map.get(char, char)


class M3:
    """Module representing Enigma Machine Type M3."""

    def __init__(self, *args, **kwargs) -> None:
        self.reflector = Reflector(kwargs["reflector"])
        self.rotors = [Rotor(*r) for r in kwargs["rotors"]]
        self.locked = kwargs.get("locked")
        self.plugboard = Plugboard(kwargs.get("plugboard", {}))

    def transform_string(self, msg: str) -> str:
        """Returns the enigma encoded string."""
        return "".join([self.transform_character(c) for c in msg])

    def rotor_positions(self) -> List[str]:
        """Return the rotors current positions."""
        return [r.rotor_position() for r in self.rotors]

    def transform_character(self, char: str) -> str:
        """Returns the enigma encoded character."""

        if char not in ascii_uppercase:
            raise InputException("Input must be between A-Z")

        char = self.plugboard.map_character(char)

        if not self.locked:
            r1, r2, r3, *_ = self.rotors
            r1.step()
            if chr(r1.count + 64) in r1.turnovers:
                r2.step()
            elif r2.rotor_position() in r2.turnovers:
                r2.step()
                r3.step()

        offset = 0

        for r in (*self.rotors, self.reflector):
            char, offset = r.forward(char, offset)
        for r in reversed(self.rotors):
            char, offset = r.reverse(char, offset)

        char = chr((ord(char) - 65 - offset) % 26 + 65)
        return self.plugboard.map_character(char)


class M4(M3):
    """Module representing Enigma Machine Type M4."""

    pass
