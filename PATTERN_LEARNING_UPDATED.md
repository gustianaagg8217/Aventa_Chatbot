# Fitur Pembelajaran Pola Percakapan - UPDATED

## Overview
Robot dapat belajar pola percakapan baru dari user. Ketika user mengajarkan pola dengan format khusus menggunakan quoted strings, robot akan menyimpannya dan menggunakannya untuk respons di masa depan.

## Format Pembelajaran (QUOTED FORMAT)

Gunakan format kalimat berikut untuk mengajarkan pola (dengan tanda kutip untuk trigger dan response):
```
Kalau ada yang bilang "[TRIGGER]", jawab nya "[RESPONSE]"
Kalau ada yang nanya "[TRIGGER]" jawab nya "[RESPONSE]"
```

**PENTING**: Isikan trigger dan response dalam tanda kutip (`"..."`). Teks dalam kutip adalah yang akan dipelajari.

## Contoh Penggunaan

### Contoh 1: Kalimat Sambutan Islami
```
🧑 Anda: Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'assalamualaikum'
Response: 'waalaikumsalam'

🧑 Anda: Assalamualaikum

🤖 Robot: Waalaikumsalam
```

### Contoh 2: Pertanyaan Geografis
```
🧑 Anda: Kalau ada yang nanya "Ibu Kota Jawa Barat?" jawab nya "Bandung"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'ibu kota jawa barat?'
Response: 'bandung'

🧑 Anda: Ibu Kota Jawa Barat?

🤖 Robot: Bandung
```

### Contoh 3: Ungkapan Terima Kasih
```
🧑 Anda: Kalau ada yang bilang "Terima kasih", jawab nya "Sama-sama"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'terima kasih'
Response: 'sama-sama'

🧑 Anda: Terima kasih

🤖 Robot: Sama-sama
```

## Cara Kerja

1. **Deteksi Pola Pembelajaran**
   - Robot mendeteksi kalimat dengan format yang berisi quoted strings
   - Menggunakan regex untuk mengekstrak trigger dan response dari dalam kutip

2. **Penyimpanan**
   - Trigger phrase (text dalam kutip pertama) disimpan sebagai keyword
   - Response phrase (text dalam kutip kedua) disimpan sebagai respons
   - Pattern disimpan di `data/patterns.json` dengan prefix `learned_`
   - Juga disimpan di knowledge base (jika tersedia)

3. **Prioritas Respons**
   - Learned patterns dicek SEBELUM greeting default
   - Jika input cocok dengan learned pattern, gunakan response dari pattern
   - Jika tidak cocok, gunakan pattern lain atau response default

4. **Penyimpanan Permanen**
   - Patterns disimpan otomatis ke file
   - Tetap ada meskipun robot dimatikan/dihidupkan kembali

## Persyaratan Format

### ✓ Format Benar
```
Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"
Kalau ada yang nanya "Ibu Kota Jawa Barat?" jawab nya "Bandung"
Kalau ada yang bilang "Pagi", jawab nya "Pagi juga!"
```

### ✗ Format Salah
```
Kalau ada yang bilang Assalamualaikum, jawab nya Waalaikumsalam  (TIDAK ADA KUTIP)
Kalau ada yang bilang "Assalamualaikum jawab nya "Waalaikumsalam" (KUTIP TIDAK BENAR)
```

## Catatan Penting

- **Case Insensitive**: Trigger tidak peka huruf besar/kecil
  ```
  "Assalamualaikum" akan cocok dengan "assalamualaikum" atau "ASSALAMUALAIKUM"
  ```

- **Exact Match**: Input harus cocok persis dengan trigger
  ```
  ✓ "Assalamualaikum" -> "Waalaikumsalam"
  ✗ "Assalamualaikum apa kabar" -> tidak cocok
  ```

- **Tanda Kutip Required**: HARUS menggunakan tanda kutip untuk pembelajaran
  ```
  ✓ Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"
  ✗ Kalau ada yang bilang Assalamualaikum, jawab nya Waalaikumsalam
  ```

## Skenario Penggunaan Lengkap

```
🧑 Anda: Nama saya Agus

🤖 Robot: Hai Agus, saya adalah Mentis, senang bertemu denganmu.

🧑 Anda: Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'assalamualaikum'
Response: 'waalaikumsalam'

🧑 Anda: Halo

🤖 Robot: Halo Agus!

🧑 Anda: Kalau ada yang nanya "Ibu Kota Jawa Barat?" jawab nya "Bandung"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'ibu kota jawa barat?'
Response: 'bandung'

🧑 Anda: Assalamualaikum

🤖 Robot: Waalaikumsalam

🧑 Anda: Ibu Kota Jawa Barat?

🤖 Robot: Bandung
```

## Technical Details

### Pattern Storage
Patterns disimpan dalam struktur:
```json
{
  "learned_assalamualaikum": {
    "keywords": ["assalamualaikum"],
    "responses": ["waalaikumsalam"]
  },
  "learned_ibu_kota_jawa_barat": {
    "keywords": ["ibu kota jawa barat?"],
    "responses": ["bandung"]
  }
}
```

### Regex Pattern
```regex
kalau ada yang (?:bilang|nanya)\s+"(.+?)"\s*,?\s+jawab(?:\s+nya)?\s+"(.+?)"
```
- Group 1: Trigger phrase (text dalam kutip pertama)
- Group 2: Response phrase (text dalam kutip kedua)

### Key Methods
- `_learn_response_pattern()`: Deteksi dan proses pembelajaran dengan quoted strings
- `_check_learned_patterns()`: Check apakah input cocok dengan learned pattern
- `pattern_matcher.add_pattern()`: Menyimpan pattern ke file
