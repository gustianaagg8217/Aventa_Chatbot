# ⚡ PROJECT ROBOT - QUICK START GUIDE

Panduan cepat untuk mulai menggunakan Project Robot dalam 5 menit!

## 🚀 Langkah 1: Jalankan Robot (30 detik)

### Opsi A: Mode Grafis (Recommended)
```bash
python robot_gui.py
```

### Opsi B: Mode Terminal
```bash
python robot_core.py
```

### Opsi C: Gunakan Launcher (Windows)
```bash
launch.bat
```

---

## 💬 Langkah 2: Coba Percakapan Sederhana (1 menit)

Setelah robot jalan, coba ini:

```
Anda: Halo!
🤖 Project Robot: Halo! Apa kabar? Nama saya Project Robot 🤖

Anda: Siapa nama kamu?
🤖 Project Robot: Nama saya Project Robot, senang berkenalan dengan Anda!

Anda: Bagaimana kabarmu?
🤖 Project Robot: Kabar saya baik! Terima kasih sudah bertanya 😊

Anda: Kamu bisa apa?
🤖 Project Robot: Saya bisa diajari percakapan baru! Gunakan perintah 'ajar' untuk melatih saya.
```

---

## 🎓 Langkah 3: Ajari Robot Hal Baru (2 menit)

### Menggunakan CLI Mode

```
Anda: ajar

📝 AJARKAN SAYA PERCAKAPAN BARU
────────────────────────────────

Intent (nama kategori): musik

Keywords (pisahkan dengan koma): musik, lagu, menyanyi, instrumen, melodi

Responses (pisahkan dengan |): Aku suka musik! Musik apa favoritmu? | Genre musik favorit apa? | Musik bisa menenangkan jiwa!

✓ Berhasil mengajari saya intent 'musik' dengan 5 keywords dan 3 responses!
```

### Menggunakan GUI Mode

1. Klik tombol 🎓 **Ajarkan Baru**
2. Isi form:
   - Intent: `musik`
   - Keywords: `musik, lagu, menyanyi, instrumen, melodi`
   - Responses: `Aku suka musik! Musik apa favoritmu? | Genre musik favorit apa? | Musik bisa menenangkan jiwa!`
3. Klik 💾 **Simpan & Ajarkan**

### Test Hasil

```
Anda: Aku suka menyanyi
🤖 Project Robot: Genre musik favorit apa?

Anda: Musik apa yang kamu suka?
🤖 Project Robot: Aku suka musik! Musik apa favoritmu?
```

---

## 📚 Langkah 4: Lihat Apa yang Robot Sudah Pelajari (30 detik)

### CLI Mode
```
Anda: lihat pattern
```

### GUI Mode
Klik 📚 **Lihat Pattern**

Akan muncul daftar lengkap semua intent dan keyword!

---

## 📊 Langkah 5: Lihat Statistik (30 detik)

### CLI Mode
```
Anda: stats
```

### GUI Mode
Lihat **📊 Statistik** di panel kanan (update real-time)

---

## 🎯 Contoh Pengajaran Lengkap (Siap Copy-Paste)

### Intent 1: Makanan

```
Intent: makanan

Keywords: 
makanan, makan, lapar, kuliner, resep, restoran, jajan, makanan ringan

Responses: 
Aku suka makanan! Apa makanan favorit kamu? | 
Makanan apa yang kamu makan hari ini? | 
Lapar ya? Ada makanan favorit? |
Kuliner Indonesia itu lezat-lezat! 😋
```

### Intent 2: Olahraga

```
Intent: olahraga

Keywords:
olahraga, main bola, sepak bola, badminton, fitness, gym, lari, renang, sehat

Responses:
Olahraga itu menyehatkan! Olahraga favorit kamu apa? |
Aku suka lihat orang berolahraga! Kamu atlet? |
Olahraga penting untuk kesehatan! 💪 |
Apa olahraga yang kamu sukai?
```

### Intent 3: Teknologi

```
Intent: teknologi

Keywords:
teknologi, coding, programming, python, javascript, aplikasi, software, gadget

Responses:
Teknologi itu exciting! Bahasa pemrograman apa yang kamu pelajari? |
Programming bisa membuat kita ciptakan hal-hal amazing! |
Tech skills sangat dicari di era digital ini! |
Apa proyek tekno yang sedang kamu kerjakan?
```

### Intent 4: Cuaca

```
Intent: cuaca

Keywords:
cuaca, hujan, panas, dingin, cerah, awan, musim, mendung, badai

Responses:
Cuaca hari ini gimana menurut kamu? |
Cuaca bisa mempengaruhi mood kita! ☀️ |
Hujan atau cerah, tetap semangat! |
Cuaca ekstrem akhir-akhir ini ya?
```

### Intent 5: Hobi

```
Intent: hobi

Keywords:
hobi, main game, nonton film, baca, menulis, gaming, aktivitas favorit

Responses:
Hobi itu membuat kita bahagia! Hobi kamu apa? |
Aku suka dengar cerita tentang hobi orang! |
Punya hobi yang menyenangkan itu bagus! 😊 |
Apa yang biasanya kamu lakukan di waktu luang?
```

---

## 💡 Pro Tips

### Tip 1: Variasikan Keywords
```
❌ KURANG: ["halo"]
✅ BAIK: ["halo", "hai", "hello", "pagi", "siang", "malam"]
```

### Tip 2: Buat Multiple Responses
Semakin banyak response, semakin natural robot terdengar

### Tip 3: Test Lebih Banyak
Ajari robot berbagai varian dari setiap intent

### Tip 4: Kelompokkan Topik
Pisahkan percakapan ke intent yang berbeda

---

## 🔥 Fitur Rahasia yang Jarang Diketahui

### CLI Mode
```
history    → Lihat riwayat percakapan
clear      → Hapus semua memory
```

### GUI Mode
- Klik 📜 **History** untuk lihat percakapan terakhir
- Real-time stats di panel kanan
- Semua data tersimpan otomatis

---

## ❓ FAQ Cepat

**Q: Bagaimana jika robot tidak paham?**
A: Ajari dengan keyword yang lebih variatif! Robot belajar dari apa yang kamu ajarkan.

**Q: Bisa hapus intent yang sudah diajarkan?**
A: Edit file `data/patterns.json` langsung atau gunakan `clear` untuk reset semua.

**Q: Data saya tersimpan dimana?**
A: Di folder `data/`:
- `patterns.json` - Pattern yang dipelajari
- `conversation_memory.json` - Riwayat percakapan

**Q: Bisa pakai offline?**
A: Ya! 100% offline, tidak perlu internet sama sekali!

**Q: Bisa export pattern?**
A: Buka file `data/patterns.json` dengan text editor, copy isi-nya!

---

## 🎮 Challenge untuk Pemula

Coba complete challenge ini dalam 10 menit:

1. ✅ Jalankan robot
2. ✅ Ajari 5 intent baru
3. ✅ Test setiap intent
4. ✅ Lihat statistik
5. ✅ Check history

**Selesai!** Kamu sekarang master dalam menggunakan Project Robot! 🎉

---

## 📖 Mau Pelajari Lebih Lanjut?

- Baca [README.md](README.md) untuk dokumentasi lengkap
- Lihat [ADVANCED_GUIDE.md](ADVANCED_GUIDE.md) untuk tips advanced
- Eksperimen dengan berbagai intent dan response!

---

## 🚀 Happy Learning! 🤖

Sekarang mulai ajarkan robot Anda dan lihat bagaimana ia belajar dari setiap interaksi!

Semoga menyenangkan! 😊
