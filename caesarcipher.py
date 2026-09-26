ciphertext = "RFMFXNXBF BFONG RJRFMFRN IFXFW PWNUYTLWFKN PQFXNP XJGJQZR RTIJWS"


def caesar_decrypt(text, key):
    hasil = ""

    for karakter in text:
        if karakter.isalpha():
            # Ubah huruf menjadi angka 0-25
            angka = ord(karakter.upper()) - ord('A')

            # Geser ke kiri sebanyak key
            angka_baru = (angka - key) % 26

            # Ubah kembali angka menjadi huruf
            karakter_baru = chr(angka_baru + ord('A'))

            hasil += karakter_baru
        else:
            # Spasi tetap dipertahankan
            hasil += karakter
    return hasil

# Mencoba kunci dari 2 sampai 8
for key in range(2, 9):
    plaintext = caesar_decrypt(ciphertext, key)

    print("Kunci =", key)
    print(plaintext)
    print()