class HashRow:
    def __init__(self, index):
        self.index = index
        self.id = ""
        self.c = 0
        self.u = 0
        self.t = 1
        self.l = 0
        self.d = 0
        self.p0 = index
        self.pi = ""


def calculate_v(word):

    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    if len(word) < 2:
        word = word + "а"

    char1 = word[0].lower()
    char2 = word[1].lower()

    v1 = alphabet.find(char1) if char1 in alphabet else 0
    v2 = alphabet.find(char2) if char2 in alphabet else 0

    return v1 * 33 + v2
