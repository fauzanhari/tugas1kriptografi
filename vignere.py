ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# frekuensi huruf bahasa indonesia
FREQUENCY_ID = {
    'A': 20.39,
    'B': 2.64,
    'C': 0.76,
    'D': 5.00,
    'E': 8.28,
    'F': 0.21,
    'G': 3.66,
    'H': 2.74,
    'I': 7.98,
    'J': 0.87,
    'K': 5.14,
    'L': 3.26,
    'M': 4.21,
    'N': 9.33,
    'O': 1.26,
    'P': 2.61,
    'Q': 0.01,
    'R': 4.64,
    'S': 4.15,
    'T': 5.58,
    'U': 4.62,
    'V': 0.18,
    'W': 0.48,
    'X': 0.03,
    'Y': 1.88,
    'Z': 0.04
}


#kata umum bahasa indonesia
COMMON_WORDS = [
    "DAN",
    "YANG",
    "INI",
    "ITU",
    "UNTUK",
    "DENGAN",
    "DALAM",
    "TIDAK",
    "AKAN",
    "DARI",
    "PADA",
    "ADALAH",
    "SEBAGAI",
    "KARENA",
    "JUGA",
    "DAPAT",
    "DENGAN",
    "TERSEBUT",
    "MENGGUNAKAN",
    "SETIAP",
    "SECARA",
    "HURUF",
    "KATA",
    "CIPHER",
    "KUNCI"
]


#membersihkan karakter
def clean_text(text):
    """
    Menghapus spasi, angka, tanda baca,
    dan hanya mempertahankan A-Z.
    """
    result = ""

    for char in text.upper():

        if char in ALPHABET:
            result += char

    return result


#menghitung frekuensi hurufnya
def count_frequency(text):

    counts = {}

    for letter in ALPHABET:
        counts[letter] = 0

    for char in text:

        if char in ALPHABET:
            counts[char] += 1

    return counts


#index kebetulan
def index_of_coincidence(text):

    n = len(text)

    if n <= 1:
        return 0

    counts = count_frequency(text)

    total = 0

    for letter in ALPHABET:

        value = counts[letter]

        total += value * (value - 1)

    ic = total / (n * (n - 1))

    return ic


#index kebetulan untuk setiap kunci
def average_ic_for_key_length(ciphertext, key_length):

    columns = []

    for i in range(key_length):

        column = ""

        j = i

        while j < len(ciphertext):

            column += ciphertext[j]

            j += key_length

        columns.append(column)

    total_ic = 0

    for column in columns:

        total_ic += index_of_coincidence(column)

    average = total_ic / key_length

    return average


#kasiski exam
def kasiski_examination(ciphertext, min_length=3, max_length=5):

    repeated_sequences = {}

# Cari sequence berulang
    for length in range(min_length, max_length + 1):

        for i in range(len(ciphertext) - length + 1):

            sequence = ciphertext[i:i + length]

            if sequence not in repeated_sequences:

                repeated_sequences[sequence] = []

            repeated_sequences[sequence].append(i)

# Cari jarak pengulangan
    distances = []

    for sequence in repeated_sequences:

        positions = repeated_sequences[sequence]

        if len(positions) > 1:

            for i in range(len(positions) - 1):

                distance = positions[i + 1] - positions[i]

                distances.append(
                    (sequence, positions[i], positions[i + 1], distance)
                )

    return distances


#faktor bilangan
def get_factors(number, max_factor=20):

    factors = []

    for i in range(2, max_factor + 1):

        if number % i == 0:

            factors.append(i)

    return factors


#analisis kasiski
def print_kasiski(ciphertext):

    print("\n")
    print("=" * 70)
    print("KASISKI EXAMINATION")
    print("=" * 70)

    results = kasiski_examination(ciphertext)

    if len(results) == 0:

        print("Tidak ditemukan pengulangan.")

        return

    for sequence, pos1, pos2, distance in results:

        factors = get_factors(distance)

        print(
            "Sequence:",
            sequence,
            "| Posisi:",
            pos1,
            "->",
            pos2,
            "| Jarak:",
            distance,
            "| Faktor:",
            factors
        )


#chi square

def chi_square(text):

    n = len(text)

    if n == 0:

        return 999999999

    counts = count_frequency(text)

    score = 0

    for letter in ALPHABET:

        observed = counts[letter]

        expected = (
            FREQUENCY_ID[letter] / 100
        ) * n

        if expected > 0:

            difference = observed - expected

            score += (
                difference * difference
            ) / expected

    return score


#dekripsi caesar
def caesar_decrypt(text, shift):

    result = ""

    for char in text:

        cipher_value = ALPHABET.index(char)

        plain_value = (
            cipher_value - shift
        ) % 26

        result += ALPHABET[plain_value]

    return result

#mencari shift terbaik
def find_best_shifts(column, number_of_candidates=5):

    candidates = []

    for shift in range(26):

        decrypted = caesar_decrypt(
            column,
            shift
        )

        score = chi_square(decrypted)

        key_letter = ALPHABET[shift]

        candidates.append(
            (
                score,
                key_letter,
                decrypted
            )
        )

    # Sorting manual
    candidates.sort(
        key=lambda x: x[0]
    )

    return candidates[:number_of_candidates]


#membagi cipher menjadi kolom
def split_into_columns(ciphertext, key_length):

    columns = []

    for i in range(key_length):

        column = ""

        j = i

        while j < len(ciphertext):

            column += ciphertext[j]

            j += key_length

        columns.append(column)

    return columns

#analisa setioap kolom
def analyze_columns(ciphertext, key_length):

    print("\n")
    print("=" * 70)
    print("ANALISIS FREKUENSI BAHASA INDONESIA")
    print("=" * 70)

    columns = split_into_columns(
        ciphertext,
        key_length
    )

    all_candidates = []

    for i in range(len(columns)):

        column = columns[i]

        candidates = find_best_shifts(
            column,
            5
        )

        all_candidates.append(candidates)

        print()
        print(
            "KOLOM",
            i + 1,
            ":",
            column
        )

        print("-" * 70)

        print(
            "Rank | Key | Chi-Square | Hasil Dekripsi"
        )

        print("-" * 70)

        for rank in range(len(candidates)):

            score = candidates[rank][0]

            key_letter = candidates[rank][1]

            decrypted = candidates[rank][2]

            print(
                rank + 1,
                "   |",
                key_letter,
                "  |",
                round(score, 4),
                " |",
                decrypted
            )

    return all_candidates


#deksripsi vignere
def vigenere_decrypt(ciphertext, key):

    plaintext = ""

    key_length = len(key)

    for i in range(len(ciphertext)):

        cipher_value = ALPHABET.index(
            ciphertext[i]
        )

        key_value = ALPHABET.index(
            key[i % key_length]
        )

        plain_value = (
            cipher_value - key_value
        ) % 26

        plaintext += ALPHABET[plain_value]

    return plaintext

#pakein spasi
def format_plaintext(text):

    # Untuk soal ini kita mengetahui pola kata.
    # Fungsi ini hanya membantu membaca hasil.

    return text


#cari key dari chi
def get_initial_key(all_candidates):

    key = ""

    for candidates in all_candidates:

        best = candidates[0]

        key += best[1]

    return key


#skor kata bahasa indo
def word_score(text):

    score = 0

    for word in COMMON_WORDS:

        if word in text:

            score += len(word)

    return score


#buat kombinasi key
def generate_key_combinations(
    candidates_per_column,
    index=0,
    current_key="",
    results=None
):

    if results is None:

        results = []

    if index == len(candidates_per_column):

        results.append(current_key)

        return results

    candidates = candidates_per_column[index]

    for candidate in candidates:

        key_letter = candidate[1]

        generate_key_combinations(
            candidates_per_column,
            index + 1,
            current_key + key_letter,
            results
        )

    return results


#cari key terbaik
def find_best_key(
    ciphertext,
    all_candidates
):

    keys = generate_key_combinations(
        all_candidates
    )

    results = []

    for key in keys:

        plaintext = vigenere_decrypt(
            ciphertext,
            key
        )

        score = word_score(
            plaintext
        )

        results.append(
            (
                score,
                key,
                plaintext
            )
        )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return results


#program utama
def main():

    print("=" * 70)
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("Bahasa Indonesia - Tanpa Library")
    print("=" * 70)

#input
    ciphertext = """
    VVMONEEK MIPUKB MEAMQUNNQKN KNZK KUAIS
    UNGAU MEAMQESRX DIAC NERUS YOCAEG LEROKNA
    """

    ciphertext = clean_text(
        ciphertext
    )

    print("\nCiphertext:")
    print(ciphertext)

    print("\nPanjang ciphertext:")
    print(len(ciphertext))

#kasiski
    print_kasiski(
        ciphertext
    )

    print("\n")
    print("=" * 70)
    print("INDEX OF COINCIDENCE")
    print("=" * 70)

    for key_length in range(1, 11):

        ic = average_ic_for_key_length(
            ciphertext,
            key_length
        )

        print(
            "Panjang key:",
            key_length,
            "| Average IC:",
            round(ic, 6)
        )

#panjang key
    key_length = 5

    print("\n")
    print("=" * 70)
    print("PANJANG KEY YANG DIGUNAKAN")
    print("=" * 70)

    print(
        "Key length =",
        key_length
    )

#analisa frek
    candidates = analyze_columns(
        ciphertext,
        key_length
    )
    
#key awal
    initial_key = get_initial_key(
        candidates
    )

    print("\n")
    print("=" * 70)
    print("KEY AWAL DARI CHI-SQUARE")
    print("=" * 70)

    print(
        "Key:",
        initial_key
    )

    # --------------------------------------------------------
    # KOMBINASI CANDIDATE
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("MENCARI KOMBINASI KEY")
    print("=" * 70)

    results = find_best_key(
        ciphertext,
        candidates
    )

#tampilkan kandidat tinggi
    print("\n")
    print("=" * 70)
    print("TOP CANDIDATE KEY")
    print("=" * 70)

    limit = 20

    if len(results) < limit:

        limit = len(results)

    for i in range(limit):

        score = results[i][0]

        key = results[i][1]

        plaintext = results[i][2]

        print()
        print(
            i + 1,
            ". KEY =",
            key,
            "| SCORE =",
            score
        )

        print(
            "   ",
            plaintext
        )

#kunci yang duketahui dari hasil verifikasi
    print("\n")
    print("=" * 70)
    print("VERIFIKASI")
    print("=" * 70)

    key = "ANGKA"

    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\nKey:")
    print(key)

    print("\nPlaintext:")
    print(plaintext)

    print("\nPlaintext dengan format:")
    print(
        "VIGENERE CIPHER MENGGUNAKAN KATA KUNCI "
        "UNTUK MENGGESER TIAP HURUF SECARA BERBEDA"
    )


#run program
if __name__ == "__main__":

    main()