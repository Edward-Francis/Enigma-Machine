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

        # reset rotor wiring to reflect starting position
        offset = ord(position) - 65
        self.wiring = self.wiring[offset:] + self.wiring[:offset]

    def forward(self, char):
        return self.wiring[ord(char) - 65]

    def reverse(self, char):
        return chr(self.wiring.index(char) + 65)


class Reflector:
    def __init__(self, __type):
        self.type = __type
        self.wiring = list(REFLECTORS[self.type])

    def reflect(self, char):
        return self.wiring[ord(char) - 65]


class M3:
    def __init__(self, *args, **kwargs) -> None:
        self.reflector = Reflector(kwargs["reflector"])
        self.rotors = [Rotor(*r) for r in kwargs["rotors"]]
        self.locked = kwargs.get("locked")

    def transform_string(self, msg: str) -> str:
        return "".join([self.transform_character(c) for c in msg.upper()])

    def transform_character(self, c: str) -> str:

        r1 = self.rotors[0]
        r2 = self.rotors[1]
        r3 = self.rotors[2]

        # perform rotor stepping
        if not self.locked:
            pass

        c = r1.forward(c)
        c = r2.forward(c)
        c = r3.forward(c)
        c = self.reflector.reflect(c)
        c = r3.reverse(c)
        c = r2.reverse(c)
        c = r1.reverse(c)

        return c
