# 🔑 API Setup Guide

## Google Gemini API

### Getting Your Free API Key

1. **Visit Google AI Studio**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Select "Create API key in new project" (recommended)
   - Copy the key (starts with `AIzaSy...`)

3. **Add to config.json**
```bash
   nano config.json
```
```json
   {
       "gemini_api_key": "AIzaSyC_YOUR_ACTUAL_KEY_HERE"
   }
```

### Free Tier Limits
```
Rate Limits:
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per month

Model: gemini-2.0-flash
- Fast inference
- Vision capabilities
- Multimodal support
```

### Checking Your Usage

1. Visit: https://ai.google.dev/
2. Go to "API keys"
3. Click your project
4. View usage dashboard

---

## Testing API Connection

### Test 1: Basic AI Response
```bash
python tests/test_gemini.py
```

Expected output:
```
Testing Google Gemini AI...
✅ Gemini initialized!

--- Question 1 ---
Q: What is 5 + 7?
A: 5 + 7 equals 12.

✅ Gemini test complete!
```

### Test 2: Vision API
```bash
python tests/test_gemini_vision.py
```

Expected: AI describes what's in front of camera

---

## Alternative: Using Environment Variables

For better security, use environment variables instead of config.json:

### Setup
```bash
# Add to ~/.bashrc
echo 'export GEMINI_API_KEY="AIzaSy..."' >> ~/.bashrc
source ~/.bashrc
```

### Update Code
In `robot_advanced_fixed.py`:
```python
import os

# Replace:
with open('config.json', 'r') as f:
    api_key = json.load(f)['gemini_api_key']

# With:
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not set!")
    exit()
```

---

## API Error Codes

### Common Errors

#### 400 Bad Request
- **Cause:** Invalid API request format
- **Fix:** Check model name, ensure proper JSON format

#### 401 Unauthorized
- **Cause:** Invalid or missing API key
- **Fix:** Verify API key in config.json

#### 403 Forbidden
- **Cause:** API key doesn't have required permissions
- **Fix:** Regenerate API key with correct project

#### 404 Not Found
- **Cause:** Model name incorrect
- **Fix:** Use `check_models.py` to find valid model names

#### 429 Too Many Requests
- **Cause:** Rate limit exceeded (15/min)
- **Fix:** Wait 60 seconds, reduce request frequency

#### 500 Internal Server Error
- **Cause:** Google API temporary issue
- **Fix:** Retry after few minutes

---

## API Best Practices

### 1. Rate Limiting
```python
import time

# Add delay between requests
time.sleep(4)  # 4 seconds = max 15 requests/minute
```

### 2. Error Handling
```python
try:
    response = self.model.generate_content(prompt)
except Exception as e:
    if "429" in str(e):
        print("Rate limit hit, waiting...")
        time.sleep(60)
        response = self.model.generate_content(prompt)
    else:
        raise
```

### 3. Token Optimization
```python
# Limit response length to save tokens
response = self.model.generate_content(
    prompt,
    generation_config={
        "max_output_tokens": 150,
        "temperature": 0.7
    }
)
```

### 4. Caching Common Responses
```python
response_cache = {}

def ask_ai(self, question):
    if question in response_cache:
        return response_cache[question]
    
    response = self.model.generate_content(question)
    response_cache[question] = response.text
    return response.text
```

---

## Security Best Practices

### ⚠️ NEVER:
- ❌ Commit API keys to GitHub
- ❌ Share API keys publicly
- ❌ Hardcode keys in source code
- ❌ Include keys in screenshots

### ✅ ALWAYS:
- ✅ Use config.json (add to .gitignore)
- ✅ Use environment variables
- ✅ Regenerate if accidentally exposed
- ✅ Monitor usage dashboard

---

## Upgrading to Paid Tier

If you need more than free tier:

1. Visit: https://ai.google.dev/pricing
2. Current pricing (as of 2025):
   - Pay-as-you-go model
   - $0.50 per million tokens (input)
   - $1.50 per million tokens (output)

3. Enable billing in Google Cloud Console
4. Same API key continues to work

---

## Checking Available Models
```bash
python tests/check_models.py
```

Current models (as of March 2025):
```
✅ models/gemini-2.0-flash      # Recommended
✅ models/gemini-2.5-flash
✅ models/gemini-2.5-pro
```

---

## API Monitoring

### Simple Usage Tracker
```python
# Add to robot code
api_calls = 0

def ask_ai(self, question):
    global api_calls
    api_calls += 1
    print(f"API Calls: {api_calls}")
    
    if api_calls > 10:
        print("Warning: Approaching rate limit")
    
    response = self.model.generate_content(question)
    return response.text
```

---

## Troubleshooting API Issues

### Problem: API key not working
```bash
# Test API key manually
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_KEY')
model = genai.GenerativeModel('models/gemini-2.0-flash')
response = model.generate_content('test')
print(response.text)
"
```

### Problem: Slow responses

- **Check internet speed:**
```bash
speedtest-cli
```

- **Try different model:**
```python
# Faster but less capable
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
```

### Problem: Vision not working
```bash
# Verify model supports vision
python tests/check_models.py

# Use vision-specific model
model = genai.GenerativeModel('models/gemini-2.5-flash-image')
```

---

## Support

- **Official Docs:** https://ai.google.dev/docs
- **Community:** https://discuss.ai.google.dev/
- **Status:** https://status.cloud.google.com/

---

For general troubleshooting, see [troubleshooting.md](troubleshooting.md)
