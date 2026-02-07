# ChatGPT Integration - Option A (Fallback)

## Deskripsi
ChatGPT diintegrasikan sebagai **fallback mechanism** - digunakan hanya jika pertanyaan user tidak cocok dengan:
- Learned patterns ✗
- Local vocabulary ✗  
- Wikipedia (jika enabled) ✗
- Default pattern matcher ✗

## Setup

### 1. API Key (Sudah dikonfigurasi)
File: `.env`
```
OPENAI_API_KEY=sk-proj-...
CHATGPT_MODEL=gpt-3.5-turbo
CHATGPT_FALLBACK_ENABLED=true
```

### 2. Dependencies (Sudah installed)
```bash
pip install openai python-dotenv
```

### 3. Module
File: `chatgpt_integration.py` - ChatGPTFallback class
- Manage OpenAI API calls
- Handle conversation history
- Graceful fallback jika API error

## Flow Diagram

```
User Input
    ↓
[1] Check Learned Patterns
    ↓ (Match → Respond)
    ↓ (No Match → Continue)
[2] Check Vocabulary Search
    ↓ (Match → Respond)
    ↓ (No Match → Continue)
[3] Check Wikipedia Questions
    ↓ (Match → Search & Respond)
    ↓ (No Match → Continue)
[4] Default Pattern Matcher
    ↓ (Match → Respond)
    ↓ (Default Response → Continue)
[5] ChatGPT Fallback
    ↓
ChatGPT API Call → Response
    ↓
Return Response
```

## Contoh Penggunaan

### Scenario 1: Learned Pattern (Instant, No API Call)
```
🧑 Anda: Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"

🤖 Robot: ✓ Pola pembelajaran berhasil ditambahkan!
Trigger: 'assalamualaikum'
Response: 'waalaikumsalam'
```

### Scenario 2: Vocabulary Search (Local, No API Call)
```
🧑 Anda: cari arti algoritma

🤖 Robot: 📚 Hasil pencarian untuk 'algoritma':
...
```

### Scenario 3: Wikipedia (Optional API, Cached)
```
🧑 Anda: apa itu machine learning?

🔍 Searching Wikipedia for 'machine learning'...

🤖 Robot: 📚 Machine Learning
...
```

### Scenario 4: ChatGPT Fallback (API Required)
```
🧑 Anda: Bagaimana cara membuat startup yang sukses?

🤖 Robot: Membangun startup yang sukses memerlukan beberapa hal penting...
[Response dari ChatGPT]
```

## Command-Command ChatGPT

### Lihat Status ChatGPT
```
🧑 Anda: statistik chatgpt

🤖 Robot: 🤖 CHATGPT FALLBACK STATISTICS
═════════════════════════════════════
• Status: ✓ Enabled
• Model: gpt-3.5-turbo
• API Key: ✓ Set
• Conversation History: 5 messages
• History File: data\chatgpt_history.json
═════════════════════════════════════
```

## Features

### ✓ Conversation History
- Simpan hingga 10 messages terakhir untuk context
- Stored di `data/chatgpt_history.json`
- Load otomatis saat startup

### ✓ Error Handling
- Graceful fallback jika API error
- Fallback ke local response jika timeout
- Long-running queries supported (timeout 10s)

### ✓ Personalization  
- Gunakan user name untuk personalisasi responses
- System prompt yang friendly dan helpful

### ✓ Cost Optimization
- Hanya call ChatGPT saat benar-benar diperlukan
- Caching untuk local queries
- No API calls untuk pertanyaan yang cocok dengan learned patterns/vocab

## Cost Estimation

### gpt-3.5-turbo (Model Saat Ini)
- **Input**: $0.50 per 1M tokens
- **Output**: $1.50 per 1M tokens
- Typical per-request: $0.001-0.005

### Estimate Usage
- **Low**: 100 fallback queries/hari = ~$0.10-0.50/hari
- **Medium**: 500 fallback queries/hari = ~$0.50-2.50/hari
- **High**: 1000 fallback queries/hari = ~$1-5/hari

## Configuration

### .env File
```
# ChatGPT settings
OPENAI_API_KEY=sk-proj-...            # OpenAI API key
CHATGPT_MODEL=gpt-3.5-turbo           # Model (gpt-3.5-turbo atau gpt-4)
CHATGPT_FALLBACK_ENABLED=true         # Enable/disable fallback
```

### Model Options
- `gpt-3.5-turbo` (default) - Fast & Cheap
- `gpt-4` - More intelligent, More expensive

## Technical Notes

### System Prompt
Robot diberi system prompt untuk:
- Respond dalam Bahasa Indonesia
- Remain helpful dan friendly
- Avoid harmful content
- Keep responses concise (max 3 paragraphs)

### Conversation History
- Max 10 messages untuk mencegah token overflow
- Saved dengan timestamp
- Cleared otomatis per session

### Fallback Logic
```python
# In process_input():
response = super().process_input(user_input)

# Check if response adalah default/fallback
is_default = "Saya belum memahami" in response or "tidak mengerti" in response

if is_default and chatgpt_fallback.enable:
    chatgpt_response = chatgpt_fallback.get_response(user_input, user_name)
    if chatgpt_response:
        return chatgpt_response
```

## Test Results

```
✓ ChatGPT Status: Enabled
✓ API Key: Set
✓ Fallback Working: Yes
✓ Conversation History: Saved
```

### Test Case
```
Input: "Apa pendapatmu tentang teknologi AI?"
Source: ChatGPT Fallback (tidak cocok pattern lokal)
Response: "Saya sangat tertarik dengan teknologi AI..."
```

## Troubleshooting

### ChatGPT Response Slow
- Model gpt-3.5-turbo normal ~1-2 detik
- Jika > 5 detik, check internet connection
- Timeout: 10 detik

### API Key Error
Check `.env` file:
```bash
cat .env | grep OPENAI_API_KEY
```

### No Conversation History
Check file exists: `data/chatgpt_history.json`

## Future Enhancements

1. **Function Calling**: ChatGPT control local commands
2. **Streaming**: Real-time response streaming
3. **Long Context**: Store multiple conversation sessions
4. **Rate Limiting**: Prevent excessive API calls
5. **Caching**: Cache frequently asked questions

## Summary

✅ ChatGPT integration complete sebagai **fallback mechanism**
✅ Smart fallback: hanya digunakan saat diperlukan
✅ Cost-effective: minimize API calls
✅ Context-aware: maintains conversation history
✅ Robust: error handling dan graceful degradation
