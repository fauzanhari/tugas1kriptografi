# 🔐 Implementasi Algoritma Kriptografi Klasik dengan Python

Repository ini berisi implementasi dan analisis tiga algoritma kriptografi klasik menggunakan **Python**, yaitu:

1. **Caesar Cipher**
2. **Vigenère Cipher**
3. **Enigma Machine**

Project ini dibuat untuk mempelajari cara kerja algoritma kriptografi klasik, mulai dari teknik substitusi sederhana pada Caesar Cipher, penggunaan kunci berulang pada Vigenère Cipher, hingga sistem rotor mekanis yang digunakan pada Enigma Machine.

---

## 📂 Struktur Project

```text
.
├── caesarcipher.py
├── vignere.py
├── enigma.py
└── README.md
```

Setiap file berisi implementasi algoritma yang berbeda.

---

# 1. 🔑 Caesar Cipher

**Caesar Cipher** merupakan salah satu algoritma kriptografi substitusi paling sederhana. Setiap huruf pada plaintext digeser sejumlah posisi tertentu dalam alfabet.

Misalnya dengan key:

```text
Key = 3
```

maka:

```text
A → D
B → E
C → F
...
```

Untuk proses dekripsi, pergeseran dilakukan ke arah sebaliknya.

Secara matematis, proses dekripsi dapat dituliskan sebagai:

```text
P = (C - K) mod 26
```

Keterangan:

- `P` = nilai plaintext
- `C` = nilai ciphertext
- `K` = key atau jumlah pergeseran
- `26` = jumlah huruf alfabet

### Implementasi

Program menerima ciphertext:

```text
RFMFXNXBF BFONG RJRFMFRN IFXFW PWNUYTLWFKN PQFXNP XJGJQZR RTIJWS
```

Setiap karakter alfabet dikonversi menjadi nilai **0–25**.

```text
A = 0
B = 1
C = 2
...
Z = 25
```

Kemudian program melakukan pergeseran ke kiri menggunakan:

```python
angka_baru = (angka - key) % 26
```

Program mencoba beberapa kemungkinan key dari:

```text
2 sampai 8
```

Setiap hasil dekripsi ditampilkan sehingga pengguna dapat melihat key yang menghasilkan plaintext paling masuk akal.

### Alur Caesar Cipher

```text
Ciphertext
    ↓
Konversi huruf → angka
    ↓
Kurangi dengan key
    ↓
Modulo 26
    ↓
Konversi angka → huruf
    ↓
Plaintext
```

---

# 2. 🔐 Vigenère Cipher

**Vigenère Cipher** merupakan pengembangan dari Caesar Cipher.

Jika Caesar Cipher menggunakan satu nilai pergeseran untuk seluruh karakter, Vigenère Cipher menggunakan **serangkaian pergeseran berdasarkan sebuah keyword**.

Contoh:

```text
Plaintext : KRIPTOGRAFI
Key       : ANGKAANGKAA
```

Setiap huruf pada key menentukan jumlah pergeseran untuk karakter plaintext yang bersesuaian.

Secara matematis, dekripsi Vigenère dapat dituliskan:

```text
Pᵢ = (Cᵢ - Kᵢ) mod 26
```

Keterangan:

- `Pᵢ` = karakter plaintext ke-i
- `Cᵢ` = karakter ciphertext ke-i
- `Kᵢ` = karakter key ke-i

Berbeda dari implementasi Caesar Cipher pada repository ini, program Vigenère tidak hanya melakukan dekripsi menggunakan key yang sudah diketahui. Program juga melakukan **cryptanalysis untuk mencoba menemukan karakteristik key dari ciphertext**.

## Tahapan Cryptanalysis

### 1. Text Cleaning

Ciphertext terlebih dahulu dibersihkan.

Program:

- mengubah karakter menjadi uppercase,
- menghapus spasi,
- menghapus angka,
- menghapus tanda baca,
- mempertahankan karakter `A-Z`.

---

### 2. Kasiski Examination

**Kasiski Examination** digunakan untuk mencari pola karakter yang muncul berulang pada ciphertext.

Program mencari sequence dengan panjang:

```text
3 sampai 5 karakter
```

Kemudian menghitung jarak antara kemunculan sequence tersebut.

Contoh konsep:

```text
ABC.........ABC
 ↑           ↑
 posisi 1    posisi 2
```

Jarak antar-sequence kemudian difaktorkan.

Faktor-faktor yang sering muncul dapat memberikan indikasi mengenai kemungkinan panjang key Vigenère.

---

### 3. Index of Coincidence

Program juga menggunakan **Index of Coincidence (IC)** untuk membantu menganalisis panjang key.

Rumus dasarnya:

```text
IC = Σ fᵢ(fᵢ - 1) / N(N - 1)
```

dengan:

- `fᵢ` = frekuensi suatu huruf,
- `N` = jumlah seluruh karakter.

Program menghitung Average IC untuk beberapa kemungkinan panjang key:

```text
1 sampai 10
```

Pada implementasi ini panjang key yang digunakan untuk analisis selanjutnya adalah:

```text
Key Length = 5
```

---

### 4. Membagi Ciphertext Menjadi Kolom

Setelah panjang key ditentukan, ciphertext dibagi menjadi beberapa kolom.

Jika panjang key:

```text
5
```

maka:

```text
Kolom 1 → karakter 1, 6, 11, 16, ...
Kolom 2 → karakter 2, 7, 12, 17, ...
Kolom 3 → karakter 3, 8, 13, 18, ...
Kolom 4 → karakter 4, 9, 14, 19, ...
Kolom 5 → karakter 5, 10, 15, 20, ...
```

Setiap kolom pada dasarnya dapat dianalisis seperti **Caesar Cipher**.

---

### 5. Analisis Frekuensi Bahasa Indonesia

Program memiliki tabel frekuensi huruf Bahasa Indonesia.

Contohnya:

```text
A = 20.39%
E = 8.28%
I = 7.98%
N = 9.33%
T = 5.58%
...
```

Distribusi tersebut digunakan sebagai referensi untuk menentukan kemungkinan pergeseran pada setiap kolom ciphertext.

---

### 6. Chi-Square Analysis

Untuk setiap kolom, program mencoba seluruh kemungkinan:

```text
26 Caesar Shift
```

Kemudian hasilnya dibandingkan dengan distribusi frekuensi Bahasa Indonesia menggunakan metode **Chi-Square**.

Secara sederhana:

```text
χ² = Σ ((Observed - Expected)² / Expected)
```

Semakin kecil nilai Chi-Square, semakin dekat distribusi hasil dekripsi dengan distribusi huruf Bahasa Indonesia yang digunakan program.

Program kemudian mengambil beberapa kandidat shift terbaik dari setiap kolom.

---

### 7. Generate Candidate Key

Kandidat huruf dari setiap kolom kemudian dikombinasikan untuk menghasilkan berbagai kemungkinan key.

Contohnya:

```text
Kolom 1 → A, B, C
Kolom 2 → N, M, O
Kolom 3 → G, H, F
...
```

Program membentuk berbagai kombinasi key dari kandidat tersebut.

---

### 8. Word Scoring

Setiap hasil dekripsi diperiksa terhadap beberapa kata umum Bahasa Indonesia seperti:

```text
DAN
YANG
INI
UNTUK
DENGAN
DALAM
TIDAK
DARI
ADALAH
KARENA
...
```

Jika hasil dekripsi mengandung kata-kata tersebut, nilai atau **score** akan bertambah.

Hasil dengan score tertinggi menjadi kandidat plaintext dan key yang lebih menarik untuk diperiksa.

Pada tahap verifikasi implementasi ini digunakan key:

```text
ANGKA
```

yang menghasilkan kalimat:

```text
VIGENERE CIPHER MENGGUNAKAN KATA KUNCI UNTUK MENGGESER TIAP HURUF SECARA BERBEDA
```

### Alur Cryptanalysis Vigenère

```text
Ciphertext
    ↓
Text Cleaning
    ↓
Kasiski Examination
    ↓
Index of Coincidence
    ↓
Estimasi Panjang Key
    ↓
Pisahkan Ciphertext Menjadi Kolom
    ↓
Analisis Frekuensi
    ↓
Chi-Square
    ↓
Kandidat Huruf Key
    ↓
Kombinasi Key
    ↓
Dekripsi Vigenère
    ↓
Word Scoring
    ↓
Kandidat Plaintext
```

---

# 3. ⚙️ Enigma Machine

**Enigma Machine** merupakan mesin kriptografi elektro-mekanis yang terkenal karena penggunaannya pada Perang Dunia II.

Berbeda dengan Caesar dan Vigenère Cipher, Enigma menggunakan beberapa komponen yang membuat substitusi huruf terus berubah setiap kali sebuah karakter diproses.

Implementasi pada repository ini menggunakan:

```text
Rotor I
Rotor II
Rotor III
Reflector B
Plugboard
Ring Setting
Rotor Position
Rotor Stepping
Double Stepping
```

## Konfigurasi Rotor

Wiring rotor yang digunakan:

```text
Rotor I   = EKMFLGDQVZNTOWYHXUSPAIBRCJ
Rotor II  = AJDKSIRUXBLHWTMCQGZNPYFVOE
Rotor III = BDFHJLCPRTXVZNYEIWGAKMUSQO
```

Sedangkan reflector yang digunakan adalah:

```text
Reflector B = YRUHQSLDPXNGOKMIEBFZCWVJAT
```

Urutan rotor dari kanan ke kiri:

```text
II → III → I
```

Dalam program disimpan dari kiri ke kanan sebagai:

```text
I → III → II
```

---

## Ring Setting

Ring setting yang diberikan dari kanan ke kiri adalah:

```text
L T U
```

Sehingga ketika disimpan dari kiri ke kanan menjadi:

```text
U T L
```

Huruf tersebut dikonversi menjadi angka:

```text
A = 0
B = 1
...
Z = 25
```

---

## Initial Rotor Position

Posisi awal rotor dari kanan ke kiri:

```text
S Y V
```

Kemudian disimpan oleh program dari kiri ke kanan:

```text
V Y S
```

---

## Plugboard

Sebelum sinyal memasuki rotor, Enigma memiliki **plugboard** yang dapat menukar pasangan huruf.

Pada implementasi ini terdapat pasangan:

```text
Y ↔ U
J ↔ A
```

Artinya ketika huruf `Y` masuk, sinyal akan berubah menjadi `U`, dan sebaliknya.

Hal yang sama berlaku untuk pasangan `J` dan `A`.

---

## Rotor Stepping

Salah satu karakteristik penting Enigma adalah rotor bergerak setiap kali sebuah karakter diproses.

Rotor kanan bergerak setiap satu karakter:

```text
Rotor kanan → +1
```

Rotor memiliki posisi **notch**:

```text
Rotor I   → Q
Rotor II  → E
Rotor III → V
```

Ketika rotor mencapai posisi tertentu, rotor di sebelahnya ikut bergerak.

Implementasi ini juga memperhitungkan mekanisme:

```text
Double Stepping
```

yang merupakan karakteristik penting dari mekanisme Enigma.

---

## Jalur Sinyal Enigma

Saat sebuah karakter masuk, aliran sinyal secara umum adalah:

```text
Input
  ↓
Rotor Stepping
  ↓
Plugboard
  ↓
Rotor II
  ↓
Rotor III
  ↓
Rotor I
  ↓
Reflector B
  ↓
Rotor I
  ↓
Rotor III
  ↓
Rotor II
  ↓
Plugboard
  ↓
Output
```

Sinyal pertama bergerak melalui rotor dari **kanan ke kiri**:

```text
II → III → I
```

Kemudian masuk ke:

```text
Reflector B
```

Reflector mengembalikan sinyal sehingga melewati rotor secara terbalik:

```text
I → III → II
```

Setelah itu sinyal kembali melewati plugboard dan menghasilkan karakter output.

---

## Enkripsi dan Dekripsi Enigma

Salah satu karakteristik menarik Enigma adalah proses enkripsi dan dekripsi menggunakan mekanisme yang sama.

Jika konfigurasi berikut identik:

```text
Rotor Order
Ring Setting
Initial Position
Plugboard
Reflector
```

maka ciphertext dapat dimasukkan kembali ke mesin untuk memperoleh plaintext.

Karena itu fungsi utama pada program cukup menggunakan:

```python
enigma(text)
```

untuk menjalankan proses transformasi karakter berdasarkan konfigurasi mesin.

---

# 📊 Perbandingan Ketiga Algoritma

| Aspek                 | Caesar Cipher          | Vigenère Cipher                    | Enigma                        |
| --------------------- | ---------------------- | ---------------------------------- | ----------------------------- |
| Jenis                 | Substitution Cipher    | Polyalphabetic Cipher              | Rotor Cipher                  |
| Kunci                 | Angka pergeseran       | Keyword                            | Konfigurasi mesin             |
| Substitusi            | Tetap                  | Berubah mengikuti key              | Berubah setiap karakter       |
| Mekanisme             | Shift alfabet          | Multiple Caesar Shift              | Rotor + Reflector + Plugboard |
| Analisis pada program | Percobaan beberapa key | Kasiski, IC, Frequency, Chi-Square | Simulasi konfigurasi mesin    |
| Kompleksitas          | Rendah                 | Menengah                           | Tinggi                        |

---

# ▶️ Menjalankan Program

Pastikan Python sudah terinstal.

Cek menggunakan:

```bash
python --version
```

Kemudian clone repository:

```bash
git clone <URL-REPOSITORY>
cd <NAMA-REPOSITORY>
```

### Menjalankan Caesar Cipher

```bash
python caesarcipher.py
```

### Menjalankan Vigenère Cipher

```bash
python vignere.py
```

### Menjalankan Enigma Machine

```bash
python enigma.py
```

Program dibuat menggunakan fitur dasar Python sehingga tidak membutuhkan library eksternal tambahan.

---

# 🧠 Konsep yang Dipelajari

Melalui project ini beberapa konsep dasar kriptografi yang dapat dipelajari antara lain:

- Classical Cryptography
- Caesar Cipher
- Vigenère Cipher
- Polyalphabetic Substitution
- Cryptanalysis
- Frequency Analysis
- Kasiski Examination
- Index of Coincidence
- Chi-Square Analysis
- Rotor Cipher
- Plugboard
- Reflector
- Rotor Stepping
- Double Stepping
- Modular Arithmetic

---

# 🎯 Tujuan Project

Project ini bertujuan untuk memahami bagaimana perkembangan algoritma kriptografi klasik terjadi dari metode sederhana hingga sistem yang lebih kompleks.

```text
Caesar Cipher
      ↓
Single Alphabet Shift
      ↓
Vigenère Cipher
      ↓
Multiple Alphabet Shift
      ↓
Enigma Machine
      ↓
Dynamic Rotor Substitution
```

Ketiga implementasi menunjukkan bahwa peningkatan kompleksitas kunci dan mekanisme substitusi dapat membuat proses cryptanalysis menjadi semakin sulit.

---

## ⚠️ Catatan

Implementasi dalam repository ini dibuat untuk **tujuan pembelajaran dan eksperimen kriptografi klasik**.

Caesar Cipher, Vigenère Cipher, dan Enigma merupakan algoritma historis dan **tidak direkomendasikan untuk mengamankan data modern**.

Untuk sistem modern, algoritma kriptografi yang dirancang dan ditinjau untuk penggunaan keamanan kontemporer sebaiknya digunakan.

---

# 🛠️ Teknologi

```text
Language : Python
Type     : Classical Cryptography
Purpose  : Education / Cryptanalysis
```

---

## 📚 Algoritma

**Caesar Cipher**  
Teknik substitusi dengan menggeser setiap huruf berdasarkan sebuah nilai key.

**Vigenère Cipher**  
Teknik polyalphabetic substitution yang menggunakan keyword untuk menentukan pergeseran setiap karakter.

**Enigma Machine**  
Sistem rotor cipher yang menggunakan kombinasi rotor, reflector, plugboard, ring setting, dan mekanisme stepping untuk menghasilkan substitusi yang berubah pada setiap karakter.

---

## 📄 License

Project ini dibuat untuk kebutuhan pembelajaran dan dapat dikembangkan lebih lanjut untuk eksperimen mengenai algoritma kriptografi klasik.
