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


class Reflector:
    def __init__(self, __type):
        self.type = __type
        self.wiring = list(REFLECTORS[self.type])


class M3:
    def __init__(self, *args, **kwargs) -> None:
        self.reflector = Reflector(kwargs["reflector"])
        self.rotors = [Rotor(*r) for r in kwargs["rotors"]]
