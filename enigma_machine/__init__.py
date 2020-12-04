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

    def forward(self, char):
        return self.wiring[ord(char) - 65]

    def reverse(self, char):
        """"""
        value = ord(char) + self.count
        if value > 90:
            value = value - 26
        return chr(self.wiring.index(chr(value)) + 65)

    def step(self) -> bool:

        self.wiring = self.wiring[1:] + [self.wiring[0]]
        self.count = self.count + 1

        print("Stepping rotor: " + self.type + " - " + str(self.count))

        if self.count > 26:
            self.count = 1

        # import string
        # alphabet = list(string.ascii_uppercase)
        # print(alphabet[self.count:] + alphabet[:self.count-1])

        # print(chr(65 + self.count -1 ))
        # print(self.wiring)

        if chr(65 + self.count - 1) in self.turnovers:
            return True
        else:
            return False


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

        print("----------- " + c + " ---------------")

        r1 = self.rotors[0]
        r2 = self.rotors[1]
        r3 = self.rotors[2]

        # perform rotor stepping
        if not self.locked:
            if r1.step():
                if r2.step():
                    r3.step()

        # print(r1.count)
        # print(r2.count)
        # print(r3.count)

        print("r1 in: " + c)
        c = r1.forward(c)
        print("r1 out: " + c)

        p = ord(c) - r1.count
        print("p: " + str(p))
        if p < 65:
            p = p + 26
        c = chr(p)

        print("r2 in: " + c)
        c = r2.forward(c)
        print("r2 out: " + c)

        p = ord(c) - r2.count
        if p < 65:
            p = p + 26
        c = chr(p)

        c = r3.forward(c)
        print("r3 out: " + c)

        p = ord(c) - r3.count
        if p < 65:
            p = p + 26
        c = chr(p)
        print("reflector in: " + c)
        c = self.reflector.reflect(c)
        print("reflector out: " + c)

        print("> r3 in: " + c)
        c = r3.reverse(c)
        print("> r3 out: " + c)

        print("> r2 in: " + c)
        c = r2.reverse(c)
        print("> r2 out: " + c)

        print("> r1 in: " + c)
        c = r1.reverse(c)
        print("> r1 out: " + c)

        return c
