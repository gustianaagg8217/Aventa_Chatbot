# Cara Test ChatGPT Fallback

## Quick Start

### Opsi 1: Auto Demo Test (Recommended)
```bash
python demo_chatgpt_test.py
```
Script ini akan:
1. ✅ Tampilkan ChatGPT status
2. ✅ Run 4 test queries otomatis
3. ✅ Identifikasi mana dari ChatGPT vs local
4. ✅ Show hasil summary

**Waktu:** ~30 detik

---

### Opsi 2: Interactive Test (Full Control)
```bash
python test_interactive_chatgpt.py
```
Script ini akan:
1. ✅ Explained 3 kategorisasi (Local/Vocab/ChatGPT)
2. ✅ Run automated test untuk tiap kategori
3. ✅ Offer interactive mode untuk test manual
4. ✅ Track conversation history

**Waktu:** ~5 menit (with interactive)

---

## Cara Identifikasi ChatGPT Response

### Indikator Respon ChatGPT ✅

1. **Response Panjang** - Minimum 80+ karakter
   ```
   ❌ "Halo Agus!" → Local Pattern
   ✅ "Artificial Intelligence adalah... [panjang]" → ChatGPT
   ```

2. **Detail & Natural Language**
   ```
   ❌ "Aku belum pernah belajar tentang itu" → Local Fallback
   ✅ "Machine learning adalah cabang dari AI yang..." → ChatGPT
   ```

3. **Conversation History Saved**
   ```
   // Check sebelum response
   History: 0 messages
   
   // After ChatGPT response
   History: 2 messages (user + assistant)
   ```

4. **Response Time**
   ```
   Local: < 100ms
   ChatGPT: 1-3 detik (API latency)
   ```

---

## Manual Testing (No Script)

Kalau ingin test manual tanpa script:

### Setup
```python
from robot_with_vocabulary import EnhancedRobotBrain

robot = EnhancedRobotBrain(
    enable_online_vocab=True,
    enable_wikipedia=False,  # DISABLE untuk clear test
    sync_on_startup=False
)
```

### Test Queries

#### Category 1: Local Pattern (NO API)
```
Input: "Halo"
Expected: "Halo Agus!" (short)
API Call: ❌ NO
```

#### Category 2: Vocabulary Search (NO API)
```
Input: "cari arti algoritma"
Expected: "📚 Hasil pencarian..." (from local cache)
API Call: ❌ NO
```

#### Category 3: ChatGPT Fallback (YES API) ⭐
```
Input: "Apa itu machine learning?"
Expected: "Machine learning adalah..." (long, detailed)
API Call: ✅ YES
History: Increase from 0 → 2 messages
```

---

## Step-by-Step Test Guide

### Step 1: Check Status
```python
stats = robot.chatgpt_fallback.get_stats()
print(stats)
# Output:
# {'enabled': True, 'api_key_set': True, 'history_length': 0, ...}
```

### Step 2: Test Local Pattern (Instant)
```python
response = robot.process_input("Halo")
print(response)
# Output: "Halo Agus!" (instant, no API)
```

### Step 3: Test Vocabulary (Local Cache)
```python
response = robot.process_input("cari arti algoritma")
print(response)
# Output: "📚 Hasil pencarian..." (local, no API)
```

### Step 4: Trigger ChatGPT (THIS USES API)
```python
response = robot.process_input("Bagaimana cara belajar programming?")
print(response)
# Output: "Untuk belajar programming... [detailed response]"

# Check history increased
stats_after = robot.chatgpt_fallback.get_stats()
print(stats_after['history_length'])  # Should be 2 (increased from 0)
```

---

## Expected Test Results

### Successful ChatGPT Integration ✅

```
✅ ChatGPT Status: Enabled
✅ API Key: Set  
✅ Test Local Pattern: "Halo Agus!" (no API)
✅ Test Vocabulary: "📚 Algoritma..." (no API)
✅ Test ChatGPT: Long, detailed response (API used)
✅ Conversation History: 2 messages after ChatGPT query
```

### Signs ChatGPT Not Working ❌

|  | Issue | Solution |
|---|-------|----------|
| ❌ | API Key not found | Check `.env` file |
| ❌ | ChatGPT status: Disabled | Re-import chatgpt_integration |
| ❌ | All responses short | Wikipedia enabled, disable it |
| ❌ | Timeout (>10s) | Check internet connection |
| ❌ | "API Error" message | Check OpenAI API account balance |

---

## Test Results Explanation

### What Each Test Shows

#### Test 1: "Halo" → "Halo Agus!"
```
✓ Learned patterns working
✓ User name remembered
✗ Does NOT prove ChatGPT working (local pattern)
```

#### Test 2: "cari arti algoritma" → "📚 Hasil pencarian..."
```
✓ Vocabulary search working
✓ Cache system working  
✗ Does NOT prove ChatGPT working (vocabulary match)
```

#### Test 3: "Apa itu machine learning?" → Long response
```
✓ ChatGPT fallback TRIGGERED
✓ API connection working
✓ Model responding (gpt-3.5-turbo)
✓ PROVES ChatGPT integration working! ✅
```

---

## Cost Tracking During Test

Setiap ChatGPT call estimate:
- Input tokens: ~20-50 (your question)
- Output tokens: ~50-150 (response)
- Cost: ~$0.0005-0.002 per query

**4 queries di demo_chatgpt_test.py:**
- Est. cost: ~$0.002-0.008
- But only 2 queries trigger ChatGPT (test 3 & 4)
- Actual cost: ~$0.001-0.004

---

## Advanced Testing

### Monitor API Calls
```python
# Check history
print(robot.chatgpt_fallback.conversation_history)
# Output: [
#   {'role': 'user', 'content': 'Apa itu AI?'},
#   {'role': 'assistant', 'content': 'AI adalah...'}
# ]
```

### Test Different Models
```python
# Change model (in .env or code)
robot.chatgpt_fallback.model = "gpt-4"
response = robot.process_input("Complex question...")
```

### Measure Response Time
```python
import time

start = time.time()
response = robot.process_input("Apa itu machine learning?")
elapsed = time.time() - start

if elapsed > 0.5:
    print(f"✓ API call detected (~{elapsed:.1f}s)")
else:
    print(f"✓ Local response (~{elapsed*1000:.0f}ms)")
```

---

## Troubleshooting

### Q: Response dari ChatGPT tapi singkat
**A:** Model mungkin OOM. Coba reset conversation history:
```python
robot.chatgpt_fallback.clear_history()
response = robot.process_input("Apa itu AI?")
```

### Q: API Error "rate limit"
**A:** Too many requests. Wait 1-2 menit atau check OpenAI dashboard

### Q: API Error "invalid API key"
**A:** Check `.env` file, API key mungkin invalid atau expired

### Q: Response dari Wikipedia, bukan ChatGPT
**A:** Disable Wikipedia untuk test murni ChatGPT:
```python
robot = EnhancedRobotBrain(
    enable_wikipedia=False  # ← Disable
)
```

---

## Summary

✅ **Easiest Way to Test:**
```bash
python demo_chatgpt_test.py
```

✅ **Signs ChatGPT Working:**
- Long, detailed response (80+ chars)
- Conversation history increases
- Response time 1-3 detik (API latency)

✅ **What NOT to Count:**
- "Halo Agus!" → Local greeting
- "Hasil pencarian..." → Vocabulary cache
- "Saya akan cari Wikipedia" → Wikipedia pattern

✅ **What IS ChatGPT:**
- "Machine learning adalah teknologi yang..." → CHATGPT ✅
- Natural conversation-like response
- Context-aware dari conversation history
