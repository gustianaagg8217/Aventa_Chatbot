# 🤖 PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN

Selamat datang di Project Robot! Ini adalah chatbot berbasis AI yang dapat diajarkan untuk berbincang secara offline. Robot ini akan belajar dari setiap interaksi dan dapat disesuaikan dengan kebutuhan Anda.

## ✨ Fitur Utama

- 🤖 **Chatbot Conversational** - Berbincang santai seperti teman
- 🧠 **Machine Learning Sederhana** - Belajar dari pola percakapan
- 💾 **Persistent Memory** - Mengingat percakapan Anda
- 🎓 **Teachable** - Mudah diajari dengan intent dan response baru
- 📱 **Dual Interface** - Mode CLI dan GUI
- ⚡ **100% Offline** - Tidak perlu koneksi internet (dengan local cache)
- 🌐 **Online Vocabulary** - Akses vocabulary online dengan cache lokal otomatis
- 📚 **Wikipedia Integration** - Cari pengetahuan langsung dari Wikipedia dengan intelligent Q&A
- 🚀 **Extensible** - Mudah dikembangkan lebih lanjut

## 🚀 Cara Memulai

### 1. Instalasi Python
Pastikan Python 3.7 atau lebih tinggi sudah terinstall. Download dari [python.org](https://python.org)

### 2. Install Dependencies (Opsional)
```bash
# Untuk fitur online vocabulary dan Wikipedia
pip install -r requirements.txt
```

### 3. Jalankan Robot
```bash
# Mode Grafis dengan Vocabulary + Wikipedia (Recommended)
python robot_with_vocabulary.py

# Mode Terminal (Original)
python robot_core.py

# Atau gunakan launcher
launch.bat
```

## 📖 Panduan Penggunaan

### Mode CLI (Terminal)

Saat running, Anda bisa menggunakan perintah khusus:

**Perintah Dasar:**
```
- 'ajar'              → Ajarkan saya percakapan baru
- 'lihat pattern'     → Lihat semua yang sudah saya pelajari
- 'stats'             → Lihat statistik saya
- 'history'           → Lihat riwayat percakapan
- 'clear'             → Hapus memory
- 'exit'              → Keluar dari program
```

**Perintah Vocabulary (New):**
```
- 'cari arti [kata]'  → Cari arti kata dari vocabulary online
- 'sinkron vocab'     → Update vocabulary dari online
- 'vocab cache'       → Lihat cache vocabulary
```

**Perintah Wikipedia (New):**
```
- 'apa itu [topik]'   → Cari informasi di Wikipedia
- 'siapa itu [nama]'  → Cari biografi di Wikipedia
- 'cache wikipedia'   → Lihat cache Wikipedia
```

#### Contoh Mengajar Robot

```
🧑 Anda: ajar
📝 AJARKAN SAYA PERCAKAPAN BARU
Intent (nama kategori): makanan
Keywords (pisahkan dengan koma): makanan, makan, lapar, kuliner, resep
Responses (pisahkan dengan |): Aku suka makanan! Apa makanan favorit kamu? | Makanan adalah kebutuhan penting! Apa yang kamu makan hari ini? | Lapar ya? Makanan apa yang kamu inginkan?

✓ Berhasil mengajari saya intent 'makanan' dengan 5 keywords dan 3 responses!
```

Sekarang jika Anda mengatakan "Aku suka makan", robot akan merespons dengan salah satu response yang Anda ajarkan!

### Mode GUI (Grafis)

Interface yang lebih user-friendly:

1. **Chat Area** - Lihat percakapan Anda dengan robot
2. **Input Field** - Ketik pesan ke robot (Ctrl+Enter untuk kirim)
3. **Statistics Panel** - Lihat statistik real-time
4. **Control Buttons** - Berbagai fitur kontrol:
   - 📚 Lihat Pattern
   - 🎓 Ajarkan Baru
   - 📜 History
   - 🔄 Refresh Stats
   - 🗑️ Clear Memory

## 📁 Struktur Folder

```
Aventa_Chatbot/
├── robot_core.py                    # Core logic chatbot (original)
├── robot_gui.py                     # Graphical User Interface (original)
├── robot_with_vocabulary.py         # Enhanced robot dengan Vocabulary + Wikipedia
├── online_vocabulary.py             # Online Vocabulary Manager
├── wikipedia_integration.py         # Wikipedia Integration Module
├── launch.bat                       # Launcher script (Windows)
├── README.md                        # Dokumentasi ini
├── requirements.txt                 # Dependencies
├── data/
│   ├── patterns.json                # Penyimpanan pattern yang dipelajari
│   ├── conversation_memory.json     # Riwayat percakapan
│   ├── vocabulary_cache/            # Cache untuk vocabulary
│   │   ├── vocabulary_cache.json
│   │   └── metadata.json
│   └── wikipedia_cache/             # Cache untuk Wikipedia
│       ├── wikipedia_cache.json
│       └── search_history.json
└── docs/
    ├── VOCABULARY_QUICKSTART.md
    ├── ONLINE_VOCABULARY_GUIDE.md
    ├── WIKIPEDIA_QUICKSTART.md
    ├── WIKIPEDIA_INTEGRATION_GUIDE.md
    ├── COMPLETE_SYSTEM_OVERVIEW.md
    └── ...
```

## 🧠 Cara Kerja

Robot menggunakan sistem pengetahuan 3-layer untuk memberikan respon yang lebih cerdas:

### 1. **Pattern Matching Layer**
Robot menganalisis input user dan mencari pattern yang cocok dengan keywords yang telah dipelajari.

### 2. **Online Vocabulary Layer** (New)
Jika pattern tidak ditemukan, sistem mencari definisi kata dari online vocabulary dengan cache lokal.

### 3. **Wikipedia Knowledge Layer** (New)
Jika masih belum ditemukan, sistem mencari informasi di Wikipedia untuk memberikan jawaban yang lebih komprehensif.

### 4. **Intent Recognition**
Sistem menentukan intent (kategori) dari input untuk memberikan response yang sesuai.

### 5. **Response Generation**
Robot memilih response secara random dari daftar response untuk intent tersebut.

### 6. **Learning & Memory**
Setiap percakapan disimpan dalam memory, dan robot dapat diajari pattern baru kapan saja.

**Keuntungan Sistem 3-Layer:**
- ✅ Lebih cerdas dalam menjawab pertanyaan
- ✅ Akses pengetahuan luas dari Wikipedia
- ✅ Tetap 100% offline dengan local caching
- ✅ Response cepat (< 10ms untuk cache hit)
- ✅ Fallback otomatis jika koneksi internet gagal

## 📖 Fitur Vocabulary & Wikipedia (NEW!)

### 📚 Online Vocabulary
Sistem vocabulary online memungkinkan robot mencari arti kata dari sumber online dengan cache lokal:

```bash
# Cari arti kata
🧑 Anda: cari arti blockchain
📖 Robot akan cari di vocabulary online dan tampilkan definisi

# Update vocabulary dari online
🧑 Anda: sinkron vocab
✓ Vocabulary berhasil diupdate

# Lihat cache
🧑 Anda: vocab cache
📊 Total kata: 5000+ | Cache size: 2.3MB | Last sync: 2 jam lalu
```

**Fitur Vocabulary:**
- 5000+ kata dari online source
- Auto-cache untuk offline access
- Metadata tracking (tanggal update, status)
- Export ke berbagai format (JSON, CSV, TXT)
- Multi-language support

### 🌐 Wikipedia Integration
Robot dapat mencari informasi langsung dari Wikipedia dengan intelligent Q&A:

```bash
# Tanya tentang topik
🧑 Anda: apa itu blockchain?
🔍 Robot: Blockchain adalah teknologi ledger terdistribusi...
[Informasi lengkap dari Wikipedia]

# Tanya tentang orang
🧑 Anda: siapa itu Albert Einstein?
🔍 Robot: Albert Einstein adalah fisikawan terkenal...

# Lihat cache Wikipedia
🧑 Anda: cache wikipedia
📊 Total cache: 234 artikel | Cache size: 5.6MB
```

**Fitur Wikipedia:**
- Pencarian real-time dari Wikipedia API
- Intelligent question understanding
- Intelligent Q&A engine
- Auto-cache untuk fast retrieval
- Support 300+ Wikipedia language editions
- Fallback ke cache jika internet down
- Performance: < 10ms untuk cache hit, 2-5 detik untuk new search

## 📖 Contoh Penggunaan Lengkap

### Skenario 1: Teachable Mode
```
🧑 Anda: ajar
📝 AJARKAN SAYA PERCAKAPAN BARU
Intent: makanan
Keywords: makanan, makan, lapar, kuliner, resep
Responses: Aku suka makanan! Apa favorit kamu? | Lapar ya? Apa yang kamu makan?
✓ Berhasil!
```

### Skenario 2: Vocabulary Search
```
🧑 Anda: cari arti algorithm
📖 Robot: Algorithm adalah prosedur step-by-step untuk menyelesaikan masalah...
```

### Skenario 3: Wikipedia Search
```
🧑 Anda: apa itu machine learning?
🔍 Robot: Machine Learning adalah cabang artificial intelligence...
[Detailed Wikipedia content]
```

### Skenario 4: Combined Knowledge
```
🧑 Anda: apa itu Python programming?
1️⃣ Check pattern → tidak ditemukan
2️⃣ Check vocabulary → find "programming"
3️⃣ Check Wikipedia → find comprehensive article
✓ Gabungan jawaban dari semua layer
```

## 💾 Data Storage

Semua data disimpan secara lokal dalam format JSON:

- **patterns.json** - Berisi semua intent dan pattern yang dipelajari
- **conversation_memory.json** - Menyimpan riwayat percakapan (max 50 percakapan terakhir)

Data tersimpan di folder `data/` dan tidak ada yang dikirim ke internet.

## 🔧 Cara Mengembangkan Lebih Lanjut

### Menambah Fitur NLP
```python
# Di robot_core.py, modify PatternMatcher class
def advanced_nlp_matching(self, text):
    # Tambahkan tokenization, stemming, dll
    pass
```

### Menambah Database External
```python
# Integrate dengan SQLite atau database lainnya
import sqlite3

def save_to_db(self, conversation):
    # Simpan ke database
    pass
```

### Menambah Voice Integration
```python
# Gunakan library seperti pyttsx3 untuk text-to-speech
import pyttsx3

def speak(self, text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
```

## 📊 Statistik & Monitoring

Robot menyediakan statistik real-time:
- Total percakapan
- Total intent yang dipelajari
- Total keywords
- Total responses

Gunakan tombol `🔄 Refresh Stats` di GUI atau perintah `stats` di CLI.

## ⚙️ Requirements

**Minimum:**
- Python 3.7+
- tkinter (biasanya sudah built-in dengan Python)
- Standard library: json, pathlib, datetime, random, re

**Untuk Online Vocabulary & Wikipedia Features:**
```
requests==2.31.0     # HTTP library untuk API calls
```

Install dengan:
```bash
pip install -r requirements.txt
```

Atau manual:
```bash
pip install requests
```

## 🐛 Troubleshooting

### Robot tidak merespons dengan baik
→ Ajari robot lebih banyak pattern dengan perintah 'ajar'

### Memory terlalu besar
→ Gunakan 'clear' untuk menghapus memory yang sudah lama

### GUI tidak muncul
→ Pastikan tkinter terinstall: `pip install tk`

### Vocabulary tidak bekerja
→ Install requests: `pip install requests`
→ Periksa koneksi internet (untuk pertama kali sync)

### Wikipedia tidak merespons
→ Periksa koneksi internet
→ Wikipedia akan menggunakan cache jika offline
→ Tunggu beberapa detik untuk Wikipedia search pertama kali

### Error ModuleNotFoundError
→ Pastikan menjalankan dari folder yang benar
→ Install requirements: `pip install -r requirements.txt`

### Cache terlalu besar
→ Hapus file `data/wikipedia_cache/wikipedia_cache.json`
→ Atau `data/vocabulary_cache/vocabulary_cache.json`

## 🎯 Roadmap Pengembangan

### ✅ Completed (v1.0 - v1.1)
- [x] Chatbot conversational dasar
- [x] Pattern matching & learning
- [x] CLI interface
- [x] GUI interface
- [x] Persistent memory
- [x] **Online Vocabulary System** (v1.1)
- [x] **Wikipedia Integration** (v1.1)
- [x] **Intelligent Q&A Engine** (v1.1)

### 🔄 In Progress / Planned
- [ ] Advanced NLP integration (NLTK, spaCy)
- [ ] Sentiment analysis
- [ ] Named Entity Recognition (NER)
- [ ] Multi-language support (Indonesian, English, etc)
- [ ] Web interface
- [ ] Advanced conversation flow & context management
- [ ] Voice recognition & text-to-speech
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] API endpoint for external integration
- [ ] Real-time Wikipedia article streaming
- [ ] Custom knowledge base import/export
- [ ] Performance optimization & caching improvements

## 📝 License

Project Robot adalah open-source dan bebas untuk dikembangkan lebih lanjut.

## 💬 Tips Mengajari Robot dengan Baik

1. **Gunakan keywords yang relevan** - Keywords harus mencerminkan intent
2. **Buat response yang natural** - Response harus terasa seperti percakapan manusia
3. **Varied responses** - Satu intent bisa punya banyak response untuk variasi
4. **Organize by intent** - Kelompokkan percakapan serupa dalam satu intent
5. **Consistent training** - Semakin banyak ajaran, semakin pintar robot
6. **Leverage Online Features** - Gunakan vocabulary & Wikipedia untuk memperluas pengetahuan robot
7. **Monitor Performance** - Gunakan 'stats' untuk melihat performa sistem
8. **Regular Sync** - Update vocabulary secara berkala dengan 'sinkron vocab'

## 🚀 Getting Started Now

### Langkah 1: Setup (Opsional)
```bash
pip install -r requirements.txt
```

### Langkah 2: Run Robot
```bash
python robot_with_vocabulary.py
```

### Langkah 3: Try Commands
```
Anda: apa itu machine learning?
Robot: [Jawaban dari Wikipedia]

Anda: cari arti algorithm
Robot: [Definisi dari Vocabulary]

Anda: ajar
Robot: [Ajarkan pattern baru]
```

## 🤝 Kontribusi

Anda bisa mengembangkan Project Robot lebih lanjut dengan:
- Menambah fitur baru
- Membuat pattern library yang lebih lengkap
- Mengintegrasikan dengan teknologi lainnya
- Sharing improvement dengan komunitas

## 📚 Dokumentasi Lengkap

Untuk penggunaan lebih detail, baca dokumentasi lengkap:

### Quick Start Guides
- [VOCABULARY_QUICKSTART.md](VOCABULARY_QUICKSTART.md) - 5-menit quick start untuk Online Vocabulary
- [WIKIPEDIA_QUICKSTART.md](WIKIPEDIA_QUICKSTART.md) - 5-menit quick start untuk Wikipedia

### Comprehensive Guides
- [ONLINE_VOCABULARY_GUIDE.md](ONLINE_VOCABULARY_GUIDE.md) - Panduan lengkap Vocabulary System (50+ pages)
- [WIKIPEDIA_INTEGRATION_GUIDE.md](WIKIPEDIA_INTEGRATION_GUIDE.md) - Panduan lengkap Wikipedia Integration (50+ pages)
- [COMPLETE_SYSTEM_OVERVIEW.md](COMPLETE_SYSTEM_OVERVIEW.md) - Overview lengkap sistem 3-layer

### Implementation Status
- [WIKIPEDIA_IMPLEMENTATION_COMPLETE.txt](WIKIPEDIA_IMPLEMENTATION_COMPLETE.txt) - Status implementasi fitur Wikipedia

---

**Happy Training! 🤖📚**

Robot Anda sekarang memiliki akses ke pengetahuan luas dari Wikipedia dan vocabulary online, sambil tetap bisa belajar dari Anda. Mulai dengan mengajari beberapa pattern dasar dan eksplorasi fitur baru!

**Bergabunglah dengan komunitas!** Share improvement Anda dan bantu pengembangan Project Robot.
---
**Happy Training! 🤖📚**
Robot Anda sekarang memiliki akses ke pengetahuan luas dari Wikipedia dan vocabulary online, sambil tetap bisa belajar dari Anda. Mulai dengan mengajari beberapa pattern dasar dan eksplorasi fitur baru!
**Bergabunglah dengan komunitas!** Share improvement Anda dan bantu pengembangan Project Robot.

---

**Happy Training! 🤖📚**

Robot Anda sekarang memiliki akses ke pengetahuan luas dari Wikipedia dan vocabulary online, sambil tetap bisa belajar dari Anda. Mulai dengan mengajari beberapa pattern dasar dan eksplorasi fitur baru!

**Bergabunglah dengan komunitas!** Share improvement Anda dan bantu pengembangan Project Robot.
