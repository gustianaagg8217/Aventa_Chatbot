# 📖 WIKIPEDIA INTEGRATION GUIDE

## 🎯 Overview

Chatbot sekarang terhubung ke **Wikipedia Indonesia** untuk memberikan informasi yang luas dan akurat ketika ditanya tentang berbagai topik!

### Fitur Utama
✅ **Real-time Wikipedia Search** - Cari informasi langsung dari Wikipedia
✅ **Intelligent Caching** - Cache hasil pencarian untuk akses cepat
✅ **Multi-language Support** - Support berbagai bahasa Wikipedia
✅ **Smart Question Answering** - Pahami pertanyaan dan cari jawaban
✅ **Offline Fallback** - Gunakan cache saat tidak ada internet

---

## 🚀 Cara Menggunakan

### Contoh 1: Tanya Tentang Topik
```
🧑 Anda: Apa itu artificial intelligence?

🤖 Project Robot: 📖 Pertanyaan: Apa itu artificial intelligence?
═════════════════════════════════════

Artificial Intelligence (AI) atau Kecerdasan Buatan adalah 
simulasi proses intelijen manusia oleh mesin, khususnya sistem 
komputer. Proses-proses ini mencakup pembelajaran (learning), 
penalaran (reasoning), dan perbaikan diri (self-correction)...

📖 Dari: Wikipedia - Artificial Intelligence
🔗 Baca lebih lanjut: https://id.wikipedia.org/wiki/Artificial_Intelligence
```

### Contoh 2: Tanya Tentang Orang
```
🧑 Anda: Siapa itu Albert Einstein?

🤖 Project Robot: 📖 Pertanyaan: Siapa itu Albert Einstein?
═════════════════════════════════════

Albert Einstein adalah seorang fisikawan Jerman yang lahir pada 
tahun 1879. Ia terkenal dengan teori relativitasnya yang merevolusi 
pemahaman tentang ruang, waktu, dan gravitasi...

📖 Dari: Wikipedia - Albert Einstein
🔗 Baca lebih lanjut: https://id.wikipedia.org/wiki/Albert_Einstein
```

### Contoh 3: Tanya Cara Melakukan Sesuatu
```
🧑 Anda: Bagaimana cara membuat website?

🤖 Project Robot: 📖 Pertanyaan: Bagaimana cara membuat website?
═════════════════════════════════════

Website adalah kumpulan halaman web yang saling terhubung dan 
umumnya mempunyai nama domain atau URL yang sama. Untuk membuat 
website, Anda perlu belajar tentang HTML, CSS, dan JavaScript...

📖 Dari: Wikipedia - Website
🔗 Baca lebih lanjut: https://id.wikipedia.org/wiki/Website
```

---

## 📊 Fitur Lengkap

### 1. Wikipedia Search
```
Perintah yang dikenali:
  • "Apa itu [topik]"
  • "Siapa itu [orang]"
  • "Bagaimana cara [sesuatu]"
  • "Wikipedia [topik]"
```

### 2. Cache Management
```
Perintah:
  • "cache wikipedia" - Lihat cache statistics
  
Fitur:
  • Automatic caching dari hasil pencarian
  • Cache persisten di disk
  • Smart invalidation strategy
```

### 3. Knowledge Integration
```
Sistem pengetahuan bertingkat:
1. Robot Pattern Matching (lokal)
2. Vocabulary Search (5000+ words)
3. Wikipedia Search (unlimited)

Jika tidak ditemukan di level 1, coba level 2, dst.
```

---

## 🔧 Konfigurasi

### Language Settings
```python
# Indonesian Wikipedia
wiki = WikipediaSearcher(language="id")

# English Wikipedia
wiki = WikipediaSearcher(language="en")

# Available languages:
# id (Indonesia), en (English), ja (Japanese), 
# zh (Chinese), fr (French), de (German), etc.
```

### Cache Configuration
```python
# Default: data/wikipedia_cache/

# Custom cache directory
wiki = WikipediaSearcher(cache_dir="/custom/path")
```

### Search Timeout
```python
# Default: 10 seconds
result = wiki.search_wikipedia("algoritma", timeout=10)

# Custom timeout
result = wiki.search_wikipedia("algoritma", timeout=5)
```

---

## 📊 Cache Structure

### Cache Location
```
data/wikipedia_cache/
└── wiki_search_cache.json
```

### Cache Format
```json
{
  "query_lowercase": {
    "title": "Page Title",
    "summary": "First 500 characters of content...",
    "full_content": "Complete article content...",
    "url": "https://id.wikipedia.org/wiki/...",
    "cached_at": "2026-02-06T14:30:00",
    "source": "wikipedia"
  }
}
```

---

## ⚡ Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Cache hit | < 10ms | ⚡ Instant |
| First search | 2-5 sec | 📡 Network dependent |
| Cached search | < 10ms | 🚀 Very fast |
| Cache file size | 1-5 MB | Depends on queries |

---

## 🛡️ Error Handling

Program handle berbagai kondisi:

### Network Timeout
```
⚠ Wikipedia timeout - coba offline atau check internet
```
→ Program akan gunakan cache jika tersedia

### Connection Error
```
⚠ Wikipedia tidak terhubung - gunakan cache atau offline mode
```
→ Fallback ke cached results otomatis

### No Results Found
```
⚠ Tidak ada hasil untuk '[query]' di Wikipedia
```
→ Coba pertanyaan lain atau gunakan vocabulary search

---

## 💻 API Reference

### WikipediaSearcher Class

#### Methods

**search_wikipedia(query, timeout=10, use_cache=True)**
- Cari informasi di Wikipedia
- Returns: Dict dengan title, summary, url, atau None

**get_summary(query)**
- Dapatkan ringkasan singkat
- Returns: Formatted string dengan informasi

**search_multiple(queries: List[str])**
- Cari multiple queries sekaligus
- Returns: Dict {query: result, ...}

**get_cache_stats()**
- Dapatkan statistik cache
- Returns: Dict dengan cache info

**clear_cache()**
- Hapus semua cache Wikipedia
- Useful untuk reset atau cleanup

**export_cache(output_path)**
- Export cache ke file
- Useful untuk backup

---

### QuestionAnswerer Class

#### Methods

**answer_question(question)**
- Jawab pertanyaan dengan info Wikipedia
- Smart topic extraction dari pertanyaan
- Returns: Formatted answer string

**get_question_history(limit=10)**
- Dapatkan history pertanyaan
- Returns: List of questions

**clear_history()**
- Hapus history pertanyaan

---

### KnowledgeBase Class

#### Methods

**search_all(query)**
- Cari di semua sources (vocab + wiki)
- Returns: Combined results

**get_comprehensive_answer(question)**
- Jawab dengan kombinasi vocab + wiki
- Multi-source fallback strategy
- Returns: Comprehensive answer

---

## 🎯 Usage Examples

### Example 1: Direct Usage

```python
from wikipedia_integration import WikipediaSearcher

# Create searcher
wiki = WikipediaSearcher(language="id")

# Search
result = wiki.search_wikipedia("algoritma")
print(result['title'])
print(result['summary'])

# Get summary
summary = wiki.get_summary("machine learning")
print(summary)
```

### Example 2: Question Answering

```python
from wikipedia_integration import QuestionAnswerer, WikipediaSearcher

wiki = WikipediaSearcher()
answerer = QuestionAnswerer(wiki)

# Answer question
answer = answerer.answer_question("Apa itu Python?")
print(answer)

# Check history
history = answerer.get_question_history()
```

### Example 3: Combined Knowledge

```python
from robot_with_vocabulary import EnhancedRobotBrain

# Create robot dengan semua fitur
robot = EnhancedRobotBrain(
    enable_online_vocab=True,
    enable_wikipedia=True,
    sync_on_startup=True
)

# Process question
response = robot.process_input("Apa itu cloud computing?")
print(response)
```

---

## 🔍 Smart Search Strategy

Program menggunakan intelligent search:

```
User Question: "Apa itu blockchain?"
    ↓
Extract Topics: ["blockchain"]
    ↓
Search in:
  1. Local Pattern Matching
  2. Vocabulary Database (5000+ words)
  3. Wikipedia (millions of articles)
    ↓
Return First Match Found
    ↓
Cache Result untuk Fast Access
```

---

## 🌐 Multiple Language Support

### Tersedia:
- 🇮🇩 Indonesian (id)
- 🇺🇸 English (en)
- 🇯🇵 Japanese (ja)
- 🇨🇳 Chinese (zh)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- Dan banyak lagi!

### Cara Menggunakan:
```python
# Indonesian Wikipedia
robot_id = EnhancedRobotBrain()

# English Wikipedia
from wikipedia_integration import WikipediaSearcher
wiki_en = WikipediaSearcher(language="en")

# Combine dalam robot
# (Requires custom setup)
```

---

## 💾 Cache Management

### Automatic Caching
```python
# Hasil pencarian otomatis di-cache
result1 = wiki.search_wikipedia("algoritma")  # Dari online
result2 = wiki.search_wikipedia("algoritma")  # Dari cache (< 10ms!)
```

### Manual Cache Control
```python
# View stats
stats = wiki.get_cache_stats()
print(f"Cached pages: {stats['total_cached_pages']}")

# Export cache
wiki.export_cache("my_wiki_cache.json")

# Clear cache
wiki.clear_cache()
```

---

## ⚠️ Limitations & Considerations

### Data Freshness
- Cache berlaku sampai di-clear secara manual
- Wikipedia di-update terus, cache bisa outdate
- Solusi: Clear cache berkala atau force refresh

### Offline Limitation
- Tanpa cache, Wikipedia search tidak bisa berjalan offline
- Solusi: Gunakan cache yang sudah ada atau pre-populate

### Rate Limiting
- Wikipedia API punya rate limit
- Solusi: Jangan search terlalu banyak dalam waktu singkat

### Language Availability
- Tidak semua topik tersedia di semua bahasa
- Indonesian Wikipedia lebih kecil dari English
- Solusi: Try fallback ke English jika tidak ada

---

## 🎯 Best Practices

✅ **Do's:**
- Cache hasil pencarian untuk reuse
- Gunakan specific queries (bukan terlalu general)
- Clear cache berkala untuk data freshness
- Combine dengan vocabulary untuk better results

❌ **Don'ts:**
- Jangan search terlalu sering (rate limit)
- Jangan expect 100% accuracy dari Wikipedia
- Jangan rely hanya pada Wikipedia (combine dengan vocab)
- Jangan clear cache saat offline

---

## 🚀 Advanced Features

### Custom Search Strategy
```python
class CustomWikiSearcher(WikipediaSearcher):
    def search_wikipedia(self, query, **kwargs):
        # Custom search logic
        # E.g., filter results, multi-language search, etc.
        return super().search_wikipedia(query, **kwargs)
```

### Integration dengan NLP
```python
from wikipedia_integration import QuestionAnswerer
import nlp_library  # Your NLP library

# Enhanced question processing
# Extract entities, intents, etc.
# Better topic extraction
```

### Batch Processing
```python
queries = ["Python", "Machine Learning", "Cloud Computing"]
results = wiki.search_multiple(queries)

# Process results
for query, result in results.items():
    if result:
        print(f"{query}: {result['title']}")
```

---

## 📈 Monitoring & Logging

### Cache Growth
```python
stats = wiki.get_cache_stats()
print(f"Cache size: {stats['cache_file_size_kb']} KB")
print(f"Pages cached: {stats['total_cached_pages']}")

# Monitor growth over time
# Clean up jika terlalu besar
```

### Query Tracking
```python
# Via QuestionAnswerer
answerer.get_question_history()

# Shows:
# - What questions were asked
# - When they were asked
# - Pattern analysis
```

---

## 🎓 Learning Resources

### Understanding Wikipedia API
- Official: https://en.wikipedia.org/w/api.php
- Documentation: https://www.mediawiki.org/wiki/API:Main_page

### Python Requests Library
- Documentation: https://docs.python-requests.org/

### JSON Processing in Python
- Built-in json module: https://docs.python.org/3/library/json.html

---

## 🐛 Troubleshooting

### "Wikipedia tidak terhubung"
**Cause:** Network error atau Wikipedia API down
**Solution:** 
- Check internet connection
- Check Wikipedia status
- Use cached results

### "No results found"
**Cause:** Query terlalu spesifik atau topik tidak ada
**Solution:**
- Try simpler query
- Try English Wikipedia
- Use vocabulary search

### "Cache file size too large"
**Cause:** Terlalu banyak queries disimpan
**Solution:**
```python
wiki.clear_cache()  # Clear all
# atau selective delete di file
```

### "Timeout atau slow"
**Cause:** Network slow atau Wikipedia API slow
**Solution:**
- Increase timeout: `timeout=15`
- Use cached results
- Try again later

---

## 📞 Support & FAQ

**Q: Apakah Wikipedia search perlu internet?**
A: Ya untuk first time, tapi setelah itu bisa gunakan cache offline.

**Q: Berapa lama cache berlaku?**
A: Sampai Anda clear secara manual. Tidak ada auto-expiry.

**Q: Bisa gunakan Wikipedia English?**
A: Ya! `WikipediaSearcher(language="en")`

**Q: Bagaimana kalau Wikipedia offline?**
A: Program akan fallback ke cache atau vocabulary.

**Q: Apakah ada rate limiting?**
A: Ya, Wikipedia API punya rate limit. Jangan spam requests.

---

## 🎊 Conclusion

Wikipedia integration membuat chatbot Anda:
✅ **Lebih informatif** - Akses jutaan artikel
✅ **Lebih intelligent** - Understand complex questions
✅ **Lebih responsive** - Smart caching untuk fast access
✅ **Lebih capable** - Multi-source knowledge base

Sekarang chatbot Anda adalah pengetahuan yang hidup! 📖🤖

---

**Version:** 1.0
**Status:** Production Ready ✅
**Last Updated:** 2026-02-06
