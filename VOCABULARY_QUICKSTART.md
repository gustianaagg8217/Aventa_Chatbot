# 🚀 QUICK START - Online Vocabulary Chatbot v1.0

## 1️⃣ Instalasi (2 Menit)

### Windows
```bash
# Buka Command Prompt di folder Aventa_Chatbot
cd d:\Aventa_Chatbot

# Jalankan setup otomatis
python setup_vocabulary.py
```

### Linux/Mac
```bash
cd ~/Aventa_Chatbot
pip install -r requirements.txt
```

---

## 2️⃣ Jalankan Program

### Pilihan A: Launch Interactive (Recommended)
```bash
python launch_vocabulary.bat    # Windows
python robot_with_vocabulary.py  # Linux/Mac
```

### Pilihan B: Command Line
```bash
python robot_with_vocabulary.py
```

---

## 3️⃣ Gunakan Vocabulary Features

### 🔍 Cari Arti Kata
```
🧑 Anda: cari arti algoritma

🤖 Project Robot: 📚 Hasil pencarian untuk 'algoritma':
   🔤 ALGORITMA
   Definition: Prosedur langkah demi langkah untuk menyelesaikan masalah
   Part of Speech: noun
   Examples:
      • Algoritma sorting digunakan untuk mengurutkan data
      • Tim kami mengembangkan algoritma machine learning
```

### 🔄 Sinkronisasi Online
```
🧑 Anda: sinkron vocab

🤖 Project Robot: 📡 Mencoba fetch vocabulary dari online...
   → Mencoba: https://raw.githubusercontent.com/...
   ✓ Berhasil fetch dari: ...
   → Total vocabulary sekarang: 5000+
   ✓ Vocabulary berhasil diperbarui!
   📊 Total: 5000+ kata
      Online: 5000
      Local: 0
```

### 📊 Lihat Statistik
```
🧑 Anda: statistik vocab

🤖 Project Robot: 📊 VOCABULARY STATISTICS
   • Total Vocabulary: 5234
   • Online Vocabulary: 5000
   • Local Vocabulary: 234
   • Last Updated: 2026-02-06T14:30:00
   • Cache Size: 2.50 MB
```

### 💾 Export Vocabulary
```
🧑 Anda: export vocab
Format? (json/csv/txt) [default: json]: csv

🤖 Project Robot: ✓ Vocabulary di-export ke: 
   data/vocabulary_cache/vocabulary_export_20260206_143000.csv
```

---

## 4️⃣ Perintah Standar Robot

| Perintah | Fungsi |
|----------|--------|
| `cari arti [kata]` | 🔍 Cari vocabulary |
| `sinkron vocab` | 🔄 Update dari online |
| `statistik vocab` | 📊 Lihat stats vocabulary |
| `export vocab` | 💾 Export ke JSON/CSV/TXT |
| `ajar` | 📚 Ajar pattern percakapan |
| `lihat pattern` | 👀 Lihat semua pattern |
| `stats` | 📈 Statistik robot |
| `exit` | 🚪 Keluar program |

---

## 5️⃣ Struktur File Penting

```
Aventa_Chatbot/
├── robot_with_vocabulary.py      ⭐ JALANKAN INI
├── online_vocabulary.py          💡 Manager vocabulary
├── robot_core.py                 📖 Original chatbot
├── setup_vocabulary.py           ⚙️ Setup script
├── launch_vocabulary.bat          🚀 Launcher (Windows)
├── vocabulary_config.json        🔧 Konfigurasi
│
├── data/
│   ├── patterns.json             📝 Pattern pembelajaran
│   ├── conversation_memory.json  💭 Memory percakapan
│   └── vocabulary_cache/         📚 Cache vocabulary
│       ├── vocabulary_cache.json
│       └── cache_metadata.json
│
├── ONLINE_VOCABULARY_GUIDE.md    📖 Dokumentasi lengkap
├── QUICKSTART.md                 🚀 Original quick start
└── requirements.txt              📦 Dependencies
```

---

## 🎯 Workflow Typical

```
START
  ↓
[Program checks cache]
  ├─ Cache ada & fresh (< 24 jam) → Use cache lokal (fast! ⚡)
  └─ Cache expired or missing → Try fetch online → Use cache
  ↓
[User commands]
  ├─ Normal chat → Process with pattern matching
  ├─ cari arti → Search vocabulary
  ├─ sinkron vocab → Force update online
  ├─ export vocab → Save to file
  └─ exit → Exit program
  ↓
END
```

---

## ⚡ Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Load cache lokal | < 100ms | ⚡ Instant |
| Search vocabulary | < 50ms | Super fast |
| First sync online | 2-5 sec | 📡 Network dependent |
| Subsequent sync | < 100ms | Cached |
| Export vocabulary | < 500ms | Depends on size |

---

## 🔧 Troubleshooting

### ❌ Error: "No module named 'requests'"
```bash
pip install requests
```

### ❌ "Koneksi gagal (cache lokal masih digunakan)"
✅ **Normal!** Program akan otomatis gunakan cache lokal.
   - Check internet connection
   - Cache masih berfungsi sempurna

### ❌ "No results found"
✅ Sinkronisasi vocabulary dari online:
```
🧑 Anda: sinkron vocab
```

### ❌ "Permission denied"
```bash
# Linux/Mac
chmod +x robot_with_vocabulary.py setup_vocabulary.py

# Windows - Run as Administrator
```

---

## 🎁 Fitur Unggulan

✨ **Online + Offline**
- Fetch dari online sumber
- Fallback ke cache lokal
- Work tanpa internet

✨ **Smart Caching**
- 24 jam cache validity
- Metadata tracking
- Auto-sync strategy

✨ **Multiple Export**
- JSON (for backup)
- CSV (for spreadsheet)
- TXT (for reading)

✨ **Full Integration**
- Integrate dengan robot patterns
- Add custom vocabulary
- Merge multiple sources

---

## 💡 Tips & Tricks

### Auto-update Vocabulary
```python
# Program automatically syncs setiap startup
# Atau manual: "sinkron vocab"
```

### Offline Mode
```python
# Hanya use cache lokal:
vocab_manager = OnlineVocabularyManager()
# (Internet tidak diperlukan)
```

### Batch Add Vocabulary
```python
robot.vocab_manager.merge_vocabulary({
    "word1": {...},
    "word2": {...}
})
```

### Export untuk Sharing
```python
# User bisa share CSV file vocabulary
# Atau import JSON ke sistem lain
```

---

## 🚀 Next Steps

1. **Explore Features**
   ```bash
   python robot_with_vocabulary.py
   ```

2. **Read Full Guide**
   → ONLINE_VOCABULARY_GUIDE.md

3. **Customize Config**
   → Edit vocabulary_config.json

4. **Add Custom Vocabulary**
   ```
   🧑 Anda: cari arti [custom_word]
   → Tambah manual jika tidak ada
   ```

---

## 📞 Support

**Error/Issue?**
1. Check ONLINE_VOCABULARY_GUIDE.md
2. Review requirements.txt
3. Run setup_vocabulary.py again
4. Check internet connection

**Questions?**
→ Dokumentasi di ONLINE_VOCABULARY_GUIDE.md

---

**Happy Chatting! 🤖💬✨**

---

### Version Info
- **Version:** 1.0
- **Last Updated:** 2026-02-06
- **Status:** Production Ready ✅
- **Features:** Online Vocabulary + Local Caching + Full Integration
