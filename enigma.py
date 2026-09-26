ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# WIRING ROTOR ENIGMA
ROTOR_I   = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II  = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
# Reflector B standar
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
# KONFIGURASI
# Urutan diberikan soal dari KANAN -> KIRI:
# II, III, I
# Program menyimpan rotor dari KIRI -> KANAN:
# I, III, II

rotor_names = ["I", "III", "II"]

rotor_wirings = {
    "I": ROTOR_I,
    "II": ROTOR_II,
    "III": ROTOR_III
}

# Ring setting dari kanan -> kiri:
# L, T, U
#
# Diubah ke kiri -> kanan:
# U, T, L
#
# A = 0, B = 1, ..., Z = 25

ring_settings = [
    ALPHABET.index("U"),
    ALPHABET.index("T"),
    ALPHABET.index("L")
]


# Posisi awal dari kanan -> kiri:
# S, Y, V
#
# Diubah ke kiri -> kanan:
# V, Y, S

positions = [
    ALPHABET.index("V"),
    ALPHABET.index("Y"),
    ALPHABET.index("S")
]

# PLUGBOARD
plugboard = {}

# Awalnya setiap huruf terhubung ke dirinya sendiri
for letter in ALPHABET:
    plugboard[letter] = letter

# Y-U
plugboard["Y"] = "U"
plugboard["U"] = "Y"

# J-A
plugboard["J"] = "A"
plugboard["A"] = "J"

# NOTCH ROTOR
  
#
# Rotor I  : Q
# Rotor II : E
# Rotor III: V
#
# Nilai:
# Q = 16
# E = 4
# V = 21

notches = {
    "I": 16,
    "II": 4,
    "III": 21
}
# FUNGSI STEPPING ROTOR
  

def step_rotors():

    global positions

    left = 0
    middle = 1
    right = 2

    # Apakah rotor tengah berada di notch?
    middle_at_notch = (
        positions[middle] ==
        notches[rotor_names[middle]]
    )

    # Apakah rotor kanan berada di notch?
    right_at_notch = (
        positions[right] ==
        notches[rotor_names[right]]
    )

    # DOUBLE STEPPING
    if middle_at_notch:

        # Rotor kiri bergerak
        positions[left] = (
            positions[left] + 1
        ) % 26

        # Rotor tengah bergerak
        positions[middle] = (
            positions[middle] + 1
        ) % 26

    elif right_at_notch:

        # Rotor tengah bergerak
        positions[middle] = (
            positions[middle] + 1
        ) % 26

    # Rotor kanan selalu bergerak
    positions[right] = (
        positions[right] + 1
    ) % 26

# ROTOR MAJU
def rotor_forward(letter_index, wiring, ring, position):

    # Koreksi berdasarkan posisi rotor dan ring setting
    shifted = (
        letter_index
        + position
        - ring
    ) % 26

    # Masuk ke wiring rotor
    output = ALPHABET.index(
        wiring[shifted]
    )

    # Kembalikan ke posisi sebenarnya
    output = (
        output
        - position
        + ring
    ) % 26

    return output

# ROTOR BALIK
def rotor_backward(letter_index, wiring, ring, position):
    # Koreksi berdasarkan posisi rotor dan ring setting
    shifted = (
        letter_index
        + position
        - ring
    ) % 26

    # Cari posisi huruf pada wiring rotor
    output = wiring.index(
        ALPHABET[shifted]
    )

    # Kembalikan ke posisi sebenarnya
    output = (
        output
        - position
        + ring
    ) % 26

    return output

# PROSES SATU HURUF
def process_letter(letter):

    # 1. Rotor bergerak SEBELUM huruf diproses
    step_rotors()

    # 2. Plugboard masuk
    letter = plugboard[letter]

    # Ubah huruf menjadi angka
    signal = ALPHABET.index(letter)
  
    # 3. MASUK ROTOR
    #
    # Dari kanan -> kiri
    #
    # II -> III -> I
    for i in [2, 1, 0]:

        rotor_name = rotor_names[i]

        signal = rotor_forward(
            signal,
            rotor_wirings[rotor_name],
            ring_settings[i],
            positions[i]
        )
  
    # 4. REFLECTOR B
    signal = ALPHABET.index(
        REFLECTOR_B[signal]
    )

    # 5. KEMBALI MELALUI ROTOR
    #
    # Dari kiri -> kanan
    #
    # I -> III -> II
    for i in [0, 1, 2]:

        rotor_name = rotor_names[i]

        signal = rotor_backward(
            signal,
            rotor_wirings[rotor_name],
            ring_settings[i],
            positions[i]
        )

    # 6. Plugboard keluar
    letter = ALPHABET[signal]

    letter = plugboard[letter]

    return letter


  
# ENKRIPSI / DEKRIPSI
def enigma(text):

    result = ""

    for character in text:

        # Abaikan karakter selain A-Z
        if character not in ALPHABET:
            continue

        result += process_letter(character)

    return result


  
# PROGRAM UTAMA
ciphertext = "LMYBYQBWFLTMATMBWQFTLGHZQWSPYGFWQCIJZNTLDYV"

plaintext = enigma(ciphertext)

print("==============================================")
print("          ENIGMA MACHINE DECRYPTOR")
print("==============================================")

print()
print("Ciphertext :")
print(ciphertext)

print()
print("Plaintext :")
print(plaintext)

print()
print("==============================================")