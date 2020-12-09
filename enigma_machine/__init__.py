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


class Rotor:
    def __init__(self, __type, position):
        self.type = __type
        self.position = position
        wiring, turnovers = WHEELS[self.type]
        self.wiring = list(wiring)
        self.turnovers = list(turnovers)
        self.count = ord(position) - 65

        # reset rotor wiring to reflect starting position
        offset = ord(position) - 65
        self.wiring = self.wiring[offset:] + self.wiring[:offset]

    def step(self) -> None:
        """"""
        self.wiring = self.wiring[1:] + [self.wiring[0]]
        self.count = self.count + 1
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
        alphabet = list(string.ascii_uppercase)
        r_alphabet = alphabet[self.count :] + alphabet[: self.count]
        foo = r_alphabet[ord(char) - 65 - offset]
        char = r_alphabet[self.wiring.index(foo)]
        return char, self.count


class Reflector:
    def __init__(self, __type):
        self.type = __type
        self.wiring = list(REFLECTORS[self.type])

    def reflect(self, char: str, offset: int) -> str:
        """Calculates and returns the inverted input character."""
        return self.wiring[ord(char) - 65 - offset]


class M3:
    def __init__(self, *args, **kwargs) -> None:
        self.reflector = Reflector(kwargs["reflector"])
        self.rotors = [Rotor(*r) for r in kwargs["rotors"]]
        self.locked = kwargs.get("locked")

    def transform_string(self, msg: str) -> str:
        return "".join([self.transform_character(c) for c in msg.upper()])

    def rotor_positions(self) -> List[str]:
        """Return the rotors current positions."""
        return [r.rotor_position() for r in self.rotors]

    def transform_character(self, char: str) -> str:
        """"""

        r1 = self.rotors[0]
        r2 = self.rotors[1]
        r3 = self.rotors[2]

        if not self.locked:
            r1.step()
            if chr(r1.count + 64) in r1.turnovers:
                r2.step()
            elif r2.rotor_position() in r2.turnovers:
                r2.step()
                r3.step()

        offset = 0

        for r in self.rotors:
            char, offset = r.forward(char, offset)

        # fixme reflector can possibly become a custom rotor object
        char = self.reflector.reflect(char, offset)
        offset = 0

        for r in reversed(self.rotors):
            char, offset = r.reverse(char, offset)

        return chr((ord(char) - 65 - offset) % 26 + 65)
