# Fitur Pembelajaran Pola Percakapan

## Overview
Robot dapat belajar pola percakapan baru dari user. Ketika user mengajarkan pola dengan format khusus, robot akan menyimpannya dan menggunakannya untuk respons di masa depan.

## Format Pembelajaran

Gunakan format kalimat berikut untuk mengajarkan pola:
```
Kalau ada yang bilang [TRIGGER], jawab [RESPONSE]
Kalau ada yang bilang [TRIGGER], jawab nya [RESPONSE]
```

## Contoh - Kalimat Sambutan

### Belajar
```
🧑 Anda: Kalau ada yang bilang Assalamualaikum, jawab nya Waalaikumsalam

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'assalamualaikum'
Response: 'waalaikumsalam'
```

### Penggunaan
```
🧑 Anda: Assalamualaikum

🤖 Robot: Waalaikumsalam
```

## Contoh Lainnya

### Ungkapan Terima Kasih
```
🧑 Anda: Kalau ada yang bilang Terima kasih, jawab nya Sama-sama

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'terima kasih'
Response: 'sama-sama'
```

### Pertanyaan & Jawaban
```
🧑 Anda: Kalau ada yang bilang Apa kabar kamu?, jawab nya Saya baik-baik saja, terima kasih!

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'apa kabar kamu?'
Response: 'saya baik-baik saja, terima kasih!'
```

## Cara Kerja

1. **Deteksi Pola Pembelajaran**
   - Robot mendeteksi kalimat dengan format "Kalau ada yang bilang..., jawab..."
   - Menggunakan regex untuk mengekstrak trigger dan response

2. **Penyimpanan**
   - Trigger phrase disimpan sebagai keyword dalam pola
   - Response phrase disimpan sebagai respons pola
   - Pattern disimpan di `data/patterns.json` dengan prefix `learned_`
   - Juga disimpan di knowledge base (jika tersedia) untuk referensi

3. **Prioritas Respons**
   - Learned patterns diprioritaskan SEBELUM greeting default
   - Jika input cocok dengan learned pattern, gunakan response dari pattern tersebut
   - Jika tidak cocok, gunakan pattern lain atau response default

4. **Penyimpanan Permanen**
   - Patterns disimpan otomatis ke `data/patterns.json`
   - Akan tetap ada meskipun robot dimatikan dan dihidupkan kembali

## Catatan Penting

- **Case Insensitive**: Trigger phrases tidak peka huruf besar/kecil
  ```
  Trigger "Assalamualaikum" akan cocok dengan input "assalamualaikum" atau "ASSALAMUALAIKUM"
  ```

- **Exact Match**: Input harus cocok persis dengan trigger phrase (tidak partial)
  ```
  ✓ "Assalamualaikum" -> "Waalaikumsalam"
  ✗ "Assalamualaikum apa kabar" -> tidak cocok (input lebih panjang)
  ```

- **Conflict dengan Patterns Default**: Jika trigger phrase cocok dengan pattern default (seperti greeting), pattern default akan diabaikan asalkan learned pattern sudah tersimpan lebih dahulu

## Contoh Penggunaan Lengkap

```
🧑 Anda: nama saya Agus

🤖 Robot: Hai Agus, saya adalah Mentis, senang bertemu denganmu.

🧑 Anda: Kalau ada yang bilang Assalamualaikum, jawab nya Waalaikumsalam

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'assalamualaikum'
Response: 'waalaikumsalam'

🧑 Anda: Kalau ada yang bilang Terima kasih, jawab nya Sama-sama

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'terima kasih'
Response: 'sama-sama'

🧑 Anda: Assalamualaikum

🤖 Robot: Waalaikumsalam

🧑 Anda: Terima kasih

🤖 Robot: Sama-sama
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
  "learned_terima_kasih": {
    "keywords": ["terima kasih"],
    "responses": ["sama-sama"]
  }
}
```

### Regex Pattern
Format pembelajaran dikenali dengan regex:
```regex
kalau ada yang bilang\s+(.+?),?\s+(?:jawab(?:\s+nya)?)\s+(.+?)$
```
- Group 1: Trigger phrase (apa yang user ajarkan sebagai input)
- Group 2: Response phrase (apa yang robot respond)

### Methods
- `_learn_response_pattern(user_input)`: Deteksi dan process pembelajaran
- `_check_learned_patterns(user_input)`: Check apakah input cocok dengan learned pattern
- `pattern_matcher.add_pattern(intent, keywords, responses)`: Menyimpan pattern ke file
