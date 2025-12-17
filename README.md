# 🤖 TikTok Bot - Enhanced Version

Enhanced TikTok automation bot with modern Selenium practices, better error handling, and professional logging.

## ⚠️ IMPORTANT DISCLAIMER

**THIS PROJECT IS FOR EDUCATIONAL PURPOSES ONLY**

Using automation bots to manipulate TikTok metrics (views, likes, followers) **VIOLATES TikTok's Terms of Service** and may result in:
- ⛔ Permanent account suspension
- 🚫 IP bans
- ⚖️ Legal consequences
- 📉 Damaged reputation

**USE AT YOUR OWN RISK. The authors are NOT responsible for any consequences.**

---

## ✨ Features

- 🔄 **Modern Selenium 4** - Updated with current best practices
- 📊 **Professional Logging** - Detailed logs with timestamps
- ⚙️ **JSON Configuration** - Easy setup without code modification
- 🛡️ **Better Error Handling** - Retry logic and graceful failures
- 📈 **Statistics Tracking** - Monitor bot performance
- 🎯 **Multiple Modes** - Views, Hearts, or Followers automation
- 🔍 **Headless Support** - Run in background (optional)

---

## 🚀 Installation

### Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver

### Step 1: Clone Repository

```bash
git clone https://github.com/Pausiar/tiktok_boost.git
cd tiktok_boost
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download ChromeDriver

**Option A: Automatic (Recommended)**
```bash
pip install webdriver-manager
```

Then modify `tiktok_bot.py` to use WebDriver Manager:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=chrome_options)
```

**Option B: Manual**
1. Check your Chrome version: `chrome://version`
2. Download matching ChromeDriver: https://chromedriver.chromium.org/downloads
3. Extract and place in project folder
4. Update `chromedriver_path` in `config.json`

---

## ⚙️ Configuration

Edit `config.json`:

```json
{
    "video_url": "https://www.tiktok.com/@username/video/123456789",
    "bot_mode": 1,
    "chromedriver_path": "chromedriver",
    "headless": false,
    "max_retries": 3,
    "base_wait_time": 10,
    "target_site": "https://vipto.de/"
}
```

### Configuration Options

| Parameter | Description | Values |
|-----------|-------------|--------|
| `video_url` | Your TikTok video URL | Full TikTok video link |
| `bot_mode` | Automation type | 1=Views, 2=Hearts, 4=Followers |
| `chromedriver_path` | Path to ChromeDriver | `chromedriver` or full path |
| `headless` | Run browser hidden | `true` or `false` |
| `max_retries` | Retry attempts on error | Integer (3 recommended) |
| `base_wait_time` | Wait time in seconds | Integer (10+ recommended) |

---

## 🎮 Usage

### Basic Usage

```bash
python tiktok_bot.py
```

### Mode Selection

**Mode 1: Auto Views** (Default)
```json
"bot_mode": 1
```
Delivers ~1000 views per cycle

**Mode 2: Auto Hearts/Likes**
```json
"bot_mode": 2
```
Delivers hearts to your video

**Mode 4: Auto Followers**
```json
"bot_mode": 4
```
Delivers followers to your account

### Important Notes

1. **Captcha Solving Required**
   - Bot will pause and wait for you to solve captchas manually
   - Keep browser window visible for first-time captcha solving

2. **Long Running Times**
   - Followers mode: ~11 minutes per cycle
   - Hearts mode: ~6 minutes per cycle
   - Views mode: ~1 minute per cycle

3. **Browser Control**
   - Don't close the browser window manually
   - Let the bot control everything
   - Use `Ctrl+C` to stop gracefully

---

## 📊 Output & Logs

### Console Output
```
╔══════════════════════════════════════════════╗
║     TikTok Bot - Enhanced Version            ║
║     Educational Purposes Only                ║
║     ⚠️  Use at your own risk!                ║
╚══════════════════════════════════════════════╝

2025-12-16 10:30:00 - INFO - Bot started
2025-12-16 10:30:00 - INFO - Mode: Views
2025-12-16 10:30:00 - INFO - Video URL: https://tiktok.com/@user/video/123
2025-12-16 10:30:45 - INFO - ✅ Views delivered! Total: 1000 views
```

### Log Files

Logs are saved with timestamps: `tiktok_bot_20251216_103000.log`

---

## 🛠️ Troubleshooting

### Common Issues

**1. ChromeDriver version mismatch**
```
Solution: Update ChromeDriver to match your Chrome version
```

**2. Element not found errors**
```
Solution: The target website may have changed. XPaths need updating.
```

**3. Captcha loop**
```
Solution: Solve the captcha within 60 seconds when prompted
```

**4. "Automation controlled" detection**
```
Solution: Use headless=false and solve captchas manually
```

**5. No views/hearts delivered**
```
Solution: 
- Check if vipto.de is working
- Verify your video URL is correct and public
- Check logs for specific errors
```

---

## 🔧 Advanced Usage

### Using WebDriver Manager (Recommended)

Install:
```bash
pip install webdriver-manager
```

Update code in `setup_driver()`:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=chrome_options)
```

### Running Headless

Set in `config.json`:
```json
"headless": true
```

⚠️ **Warning**: Headless mode makes captcha solving impossible

### Custom Wait Times

For slower connections:
```json
"base_wait_time": 20
```

---

## 📝 Code Structure

```
tiktok_boost/
├── tiktok_bot.py          # Main bot logic
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── *.log                 # Generated log files
```

### Main Classes

- `TikTokBot`: Main bot controller
  - `setup_driver()`: Initialize Selenium WebDriver
  - `views_loop()`: Views automation
  - `hearts_loop()`: Hearts automation
  - `followers_loop()`: Followers automation
  - `safe_click()`: Protected element clicking
  - `wait_for_element()`: Smart element waiting

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

This project is provided "as-is" for educational purposes only.

---

## 🙏 Credits

- **Original Author**: [NoNameoN-A](https://github.com/NoNameoN-A)
- **Enhanced By**: GitHub Copilot AI Assistant
- **Repository**: [bymork/TikTok-Follow-Heart-Views-Bot](https://github.com/bymork/TikTok-Follow-Heart-Views-Bot)

---

## ⚖️ Legal Notice

This software is provided for **educational and research purposes only**.

The authors and contributors:
- Do NOT endorse violating any terms of service
- Are NOT responsible for misuse of this software
- Do NOT guarantee functionality or safety
- Recommend against using automation on social media platforms

**By using this software, you accept full responsibility for any consequences.**

---

## 🔗 Related Links

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

---

**Remember: Authentic engagement beats fake metrics every time. Focus on creating great content! 🎥✨**