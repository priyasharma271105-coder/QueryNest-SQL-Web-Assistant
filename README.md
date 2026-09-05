# QueryNest v17 — All Bugs Fixed

## ✅ Fixes in this version

| # | Bug | Fix |
|---|-----|-----|
| 1 | IDE "Cannot read null style" crash | `renderResults()` null crash fixed |
| 2 | IDE theme not dark purple | Full deep purple theme applied |
| 3 | Saved programs panel showing to users | Panel permanently hidden |
| 4 | Missing JS functions (`checkKeyBanner`, `getKey`) | Stub functions added |
| 5 | AI giving ugly template message | Smart, friendly fallback responses |
| 6 | Non-programming queries (meggi recipe) show bad response | Friendly rejection: "Main programming AI hoon! 😄" |
| 7 | AI system prompt too strict | ChatGPT-style friendly prompts |
| 8 | Wrong Claude model name | Fixed to `claude-haiku-4-5-20251001` |

---

## 🚀 How AI Works (3 layers)

```
User query
    │
    ▼
[Layer 1] Real AI API (if key set)
    │  ✅ Real-time answer like ChatGPT
    │
    ▼ (if no key / API fails)
[Layer 2] Built-in Smart Answers (OFFLINE — 50+ topics)
    │  ✅ Pre-built working code for: fibonacci, factorial,
    │     bubble sort, armstrong, patterns, OOP, SQL tables, etc.
    │
    ▼ (if topic not in built-in)
[Layer 3] Helpful suggestion message
    │  ✅ Lists what topics ARE available
    │     + how to enable real AI
    │
    ▼ (if non-programming query like "recipe of meggi")
[Friendly rejection]
    ✅ "Main programming AI hoon, Maggi nahi jaanta! 😄"
```

---

## ⚙️ Setup

### Run karo:
```bash
pip install -r requirements.txt
python app.py
```

### Real AI enable karo (optional but recommended):

Open `config.py` and add your API key:

```python
# FREE option — Google Gemini
GEMINI_API_KEY = 'AIzaSy-YOUR-FREE-KEY'
# Get key: https://aistudio.google.com/app/apikey

# Paid option — Anthropic Claude (better quality)
ANTHROPIC_API_KEY = 'sk-ant-api03-YOUR-KEY'
# Get key: https://console.anthropic.com/settings/keys
```

**App tries:** Gemini → Claude → Built-in answers (all automatic)

---

## 📁 Changed Files

- `templates/ide.html` — null crash fix + purple theme
- `templates/home_premium.html` — saved panel hidden + JS fixes + better AI prompt  
- `routes/ai.py` — friendly rejection + smart fallback + better system prompt
- `utils/ai_client.py` — correct Claude model name
- `static/js/ai-chat.js` — better system prompt
