import string
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
}

REFLECTORS = {"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT", "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}


class InputException(Exception):
    pass


class Rotor:
    def __init__(self, __type, position):
        self.type = __type
        self.position = position
        wiring, turnovers = WHEELS[self.type]
        self.alphabet = list(string.ascii_uppercase)
        self.wiring = list(wiring)
        self.turnovers = list(turnovers)
        offset = ord(position) - 65
        self.count = offset
        self.alphabet = self.alphabet[offset:] + self.alphabet[:offset]
        self.wiring = self.wiring[offset:] + self.wiring[:offset]

    def step(self, offset=1) -> None:
        """Moves rotors to new position."""
        self.alphabet = self.alphabet[offset:] + [self.alphabet[0]]
        self.wiring = self.wiring[offset:] + [self.wiring[0]]
        self.count = self.count + offset
        if self.count > 25:
            self.count = 0

    def rotor_position(self) -> str:
        """Returns the rotor's current position."""
        return chr(self.count + 65)

    def forward(self, char, offset) -> Tuple[str, int]:
        """Calculates and returns the transposed character moving forwards."""
        return (self.wiring[ord(char) - 65 - offset], self.count)

    def reverse(self, char, offset) -> Tuple[str, int]:
        """Calculates and returns the transposed character moving backwards."""
        position = self.alphabet[ord(char) - 65 - offset]
        char = self.alphabet[self.wiring.index(position)]
        return char, self.count


class Reflector(Rotor):
    def __init__(self, __type):
        self.type = __type
        self.wiring = list(REFLECTORS[self.type])
        self.count = 0


class M3:
    def __init__(self, *args, **kwargs) -> None:
        self.reflector = Reflector(kwargs["reflector"])
        self.rotors = [Rotor(*r) for r in kwargs["rotors"]]
        self.locked = kwargs.get("locked")

    def transform_string(self, msg: str) -> str:
        """Returns the enigma encoded string."""
        return "".join([self.transform_character(c) for c in msg])

    def rotor_positions(self) -> List[str]:
        """Return the rotors current positions."""
        return [r.rotor_position() for r in self.rotors]

    def transform_character(self, char: str) -> str:
        """Returns the enigma encoded character."""

        if char not in string.ascii_uppercase:
            raise InputException("Input must be between A-Z")

        if not self.locked:
            r1, r2, r3 = self.rotors
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

        return chr((ord(char) - 65 - offset) % 26 + 65)
