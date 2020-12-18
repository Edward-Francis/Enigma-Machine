def ringstellung(position, ring):
    r1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
    # move rotor position
    ring_setting = ord(ring) - 65
    offset = ord(position) - 65
    r1 = r1[offset:] + r1[:offset]

    dot = r1.index(position)
    for i in range(ring_setting):
        dot = dot + 1
        for index, c in enumerate(r1):
            r1[index] = chr(((ord(c) - 64) % 26) + 65)

    offset = ring_setting * -1
    return "".join(r1[offset:] + r1[:offset])


def test_foo():
    assert ringstellung("A", "C") == "ELGMOHNIFSXBPVQYAJZWURCKDT"
    assert ringstellung("A", "B") == "KFLNGMHERWAOUPXZIYVTQBJCSD"
    assert ringstellung("A", "O") == "CKMVLIGDOWPFQXSYATZUREJNBH"
    assert ringstellung("O", "O") == "SYATZUREJNBHCKMVLIGDOWPFQX"
    assert ringstellung("Z", "Z") == "DJLEKFCPUYMSNVXGWTROZHAQBI"
