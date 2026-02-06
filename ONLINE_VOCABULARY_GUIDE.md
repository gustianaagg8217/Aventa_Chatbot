# 📚 ONLINE VOCABULARY SYSTEM
## Chatbot dengan Vocabulary Online + Local Cache

### 🎯 Fitur Utama

✅ **Fetch Vocabulary dari Online**
- Sinkronisasi otomatis dengan sumber vocabulary online
- Support GitHub repository, API, dan file JSON

✅ **Local Caching**
- Simpan vocabulary secara lokal untuk penggunaan offline
- Cache metadata untuk tracking update

✅ **Search & Lookup**
- Pencarian exact match dan partial match
- Multiple format support (JSON, CSV, TXT)

✅ **Local Vocabulary**
- Tambah vocabulary custom yang disimpan lokal
- Terintegrasi dengan robot_core pattern matching

---

## 🚀 Instalasi Cepat

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Program

**Opsi A: Dengan Online Vocabulary (Recommended)**
```bash
python robot_with_vocabulary.py
```

**Opsi B: Original Robot (Tanpa Online)**
```bash
python robot_core.py
```

---

## 📖 Cara Penggunaan

### A. Command-Line Interface

#### 1. Cari Vocabulary
```
🧑 Anda: cari arti algoritma

🤖 Project Robot: 📚 Hasil pencarian untuk 'algoritma':
   Definition: Prosedur langkah demi langkah untuk menyelesaikan masalah
   Examples:
      • Algoritma sorting digunakan untuk mengurutkan data
      • Tim kami mengembangkan algoritma machine learning
```

#### 2. Sinkronisasi dengan Online
```
🧑 Anda: sinkron vocab

🤖 Project Robot: 📡 Mencari fetch vocabulary dari online...
   ✓ Total: 5000+ kata
```

#### 3. Lihat Statistik Vocabulary
```
🧑 Anda: statistik vocab

🤖 Project Robot: 📊 VOCABULARY STATISTICS
   • Total Vocabulary: 5234
   • Online Vocabulary: 5000
   • Local Vocabulary: 234
```

#### 4. Export Vocabulary
```
🧑 Anda: export vocab
Format? (json/csv/txt) [default: json]: csv

🤖 Project Robot: ✓ Vocabulary di-export ke: data/vocabulary_cache/vocabulary_export_20260206_120000.csv
```

---

### B. Integrasi Python

```python
from robot_with_vocabulary import EnhancedRobotBrain

# Inisialisasi dengan vocabulary online
robot = EnhancedRobotBrain(
    enable_online_vocab=True,
    sync_on_startup=True
)

# Cari vocabulary
results = robot.vocab_manager.search_vocabulary("algoritma")

# Tambah vocabulary lokal
robot.add_local_vocabulary(
    word="chatbot",
    definition="Program yang mensimulasikan percakapan",
    examples=["Ini adalah chatbot AI", "Chatbot membantu customer service"],
    part_of_speech="noun"
)

# Export
filepath = robot.export_vocabulary("json")

# Chat normal
response = robot.process_input("Halo, apa arti algoritma?")
print(response)
```

---

## 🏗️ Struktur File

```
Aventa_Chatbot/
├── robot_core.py                    # Robot original (tanpa online vocab)
├── online_vocabulary.py             # Manager untuk online vocabulary
├── robot_with_vocabulary.py         # Robot dengan online vocabulary (REKOMENDASI)
├── data/
│   ├── patterns.json               # Pattern pembelajaran robot
│   ├── conversation_memory.json    # Memory percakapan
│   └── vocabulary_cache/           # Cache vocabulary online
│       ├── vocabulary_cache.json   # Vocabulary data
│       └── cache_metadata.json     # Metadata cache
└── requirements.txt                # Dependencies

```

---

## 🔧 Konfigurasi

### Online Sources

File `online_vocabulary.py` mendukport sumber-sumber:
1. **GitHub Repository** (recommended)
2. **Raw Content GitHub**
3. **Custom API endpoints**

Modifikasi method `_get_default_sources()`:

```python
def _get_default_sources(self) -> List[str]:
    return [
        "https://api.example.com/vocabulary/data.json",
        "https://raw.githubusercontent.com/username/repo/main/vocab.json"
    ]
```

### Cache Configuration

```python
vocab_manager = OnlineVocabularyManager(
    cache_dir="/path/to/cache",      # Custom cache directory
    online_sources=["https://..."]    # Custom sources
)

# Sinkronisasi dengan custom timeout
vocab_manager.sync_with_online(
    force=False,        # Jangan force jika sudah cache
    cache_hours=24      # Cache berlaku 24 jam
)
```

---

## 💾 Local Cache Structure

### vocabulary_cache.json
```json
{
  "algoritma": {
    "definition": "Prosedur langkah demi langkah untuk menyelesaikan masalah",
    "examples": ["...", "..."],
    "part_of_speech": "noun",
    "added_date": "2026-02-06T12:00:00",
    "source": "online"
  },
  "chatbot": {
    "definition": "Program yang mensimulasikan percakapan",
    "examples": ["...", "..."],
    "part_of_speech": "noun",
    "added_date": "2026-02-06T13:00:00",
    "source": "local"
  }
}
```

### cache_metadata.json
```json
{
  "last_updated": "2026-02-06T14:30:00",
  "vocab_count": 5234,
  "cache_version": "1.0"
}
```

---

## 🔄 Auto-Sync Strategy

Program menggunakan intelligent caching:

```
Startup → Check cache age
         ↓
    Cache fresh? (< 24 jam)
         ├─ YES → Use cache lokal (cepat)
         └─ NO  → Fetch online (update)
                  ↓
              Online available?
              ├─ YES → Merge & save cache
              └─ NO  → Use cache lama
```

---

## 📊 Performa

### Caching Performance
| Operation | Speed |
|-----------|-------|
| Load cache lokal | < 100ms |
| Search vocabulary | < 50ms |
| Fetch online (first time) | 2-5 detik |
| Fetch online (cached) | < 100ms |

### Memory Usage
- 5000 vocabulary: ~2-3 MB
- Cache file: ~1-2 MB
- RAM usage: ~10-15 MB

---

## 🐛 Troubleshooting

### 1. "Koneksi gagal (cache lokal masih digunakan)"
**Solusi:**
- Check internet connection
- Verify online sources are accessible
- Cache lokal masih akan digunakan

### 2. "Tidak ada hasil pencarian"
**Solusi:**
```python
# Tambah vocabulary secara manual
robot.add_local_vocabulary(
    word="kata_baru",
    definition="Definisi Anda",
    examples=["Contoh 1", "Contoh 2"]
)
```

### 3. Cache Corrupted
**Solusi:**
```python
# Hapus cache dan force re-sync
import shutil
shutil.rmtree("data/vocabulary_cache")

# Re-run program atau:
vocab_manager.sync_with_online(force=True)
```

---

## 🎓 Advanced Usage

### Custom Vocabulary Source

```python
# Implementasi custom fetch
class CustomVocabManager(OnlineVocabularyManager):
    def fetch_online(self, timeout=10):
        # Custom logic untuk fetch dari sumber Anda
        response = requests.get("https://custom-api.com/vocab")
        self.vocabulary.update(response.json())
        self.save_cache()
        return True
```

### Batch Operations

```python
# Import banyak vocabulary
import json

with open("vocab_batch.json") as f:
    vocab_batch = json.load(f)

robot.vocab_manager.merge_vocabulary(vocab_batch)

# Export untuk sharing
robot.export_vocabulary("csv", "shared_vocab.csv")
```

### Integration dengan Pattern Matching

```python
# Otomatis generate keywords dari vocabulary
for word in robot.vocab_manager.vocabulary.keys():
    robot.pattern_matcher.add_pattern(
        "definition_request",
        [f"apa itu {word}", f"arti {word}"],
        [f"{word} adalah: {robot.vocab_manager.vocabulary[word]['definition']}"]
    )
```

---

## 📝 Changelog

### v1.0 (Current)
- ✅ Online vocabulary fetching
- ✅ Local caching system
- ✅ Search functionality
- ✅ Export to JSON/CSV/TXT
- ✅ Integration dengan robot_core
- ✅ Auto-sync strategy

---

## 🤝 Support & Kontribusi

Untuk menambah sumber vocabulary online:

1. Fork repository
2. Tambahkan sumber di `_get_default_sources()`
3. Test dengan `python online_vocabulary.py`
4. Submit PR

---

## 📄 License

Same as Project Robot - Free untuk personal & educational use

---

**🎉 Enjoy your enhanced chatbot dengan extensive vocabulary!**
