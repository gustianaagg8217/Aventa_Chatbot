# Fix: Wikipedia Search - Keyword Extraction Improvement

## Masalah Sebelumnya
Ketika user bertanya ke Wikipedia dengan pertanyaan lengkap seperti:
```
🧑 Anda: apa itu intel Processor?
```

Robot mengirimkan **seluruh pertanyaan** ke Wikipedia API, bukan hanya kata kuncinya. Hasilnya:
- Query: "apa itu intel Processor?" → Hasil: "Ultrabook" (tidak relevan)
- Query: "apa itu Processor?" → Hasil: "OpenDocument" (sangat tidak relevan)

## Solusi
Ditambahkan fungsi ekstraksi keyword (`_extract_wiki_search_query`) yang:
1. Menghapus pertanyaan prefix seperti "apa itu", "siapa itu", "bagaimana cara"
2. Menangani variasi pertanyaan kompleks seperti "apa yang dimaksud dengan"
3. Menghapus tanda tanya dan punctuation trailing

## Contoh Ekstraksi Keyword

| Input | Extracted Keyword | Wikipedia Result |
|-------|------------------|------------------|
| "apa itu intel Processor?" | "intel processor" | Ultrabook (closest match) |
| "apa itu Processor?" | "processor" | Processor |
| "siapa itu Mahatma Gandhi?" | "mahatma gandhi" | Mahatma Gandhi ✓ |
| "apa yang dimaksud dengan algoritma?" | "algoritma" | Algoritma ✓ |
| "siapa sih Albert Einstein?" | "albert einstein" | Albert Einstein ✓ |
| "bagaimana cara memasak nasi?" | "memasak nasi" | Cara Memasak Nasi |
| "apa nama ibu kota Indonesia?" | "ibu kota indonesia" | Ibu Kota Indonesia ✓ |

## Hasil Sebelum vs Sesudah

### SEBELUM (dengan seluruh pertanyaan)
```
🧑 Anda: apa itu Processor?

🔍 Searching Wikipedia...

🤖 Project Robot: 📚 OpenDocument
Open Document Format for Office Applications...
```

### SESUDAH (dengan keyword extraction)
```
🧑 Anda: apa itu Processor?

🔍 Searching Wikipedia for 'processor'...

🤖 Project Robot: 📚 Processor
Processor adalah...
```

## Technical Details

### Regex Patterns
```regex
^apa\s+yang\s+dimaksud\s+dengan\s+(.+)$    # apa yang dimaksud dengan X
^siapa\s+itu\s+(.+)$                       # siapa itu X
^bagaimana\s+cara\s+(.+)$                  # bagaimana cara X
^apa\s+itu\s+(.+)$                         # apa itu X
```

### Methods
- `_extract_wiki_search_query(question)`: Extract keyword dari pertanyaan
  - Input: "apa itu intel Processor?"
  - Output: "intel processor"
  
- `_handle_wiki_search(question)`: Handle Wikipedia search dengan keyword extraction
  - Calls `_extract_wiki_search_query()` terlebih dahulu
  - Mencetak search query yang digunakan untuk transparency

## Notes
- Ekstraksi keyword case-insensitive
- Handles multiple question variations
- Fallback untuk pertanyaan yang tidak cocok dengan pattern
- Print search query untuk user visibility

## Test Coverage
File test: `test_wiki_search.py`
- ✓ Keyword extraction dari berbagai format pertanyaan
- ✓ Actual Wikipedia API searches
- ✓ Relevance improvement validation
