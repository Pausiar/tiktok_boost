# 🚀 TikTok Bot Enhanced

> ⚠️ **DISCLAIMER**: This tool is for educational purposes only. Using automation bots violates TikTok's Terms of Service and may result in account suspension or permanent ban. Use at your own risk.

An improved and modernized TikTok automation bot with better error handling, logging, and code structure.

## ✨ Features

- 🔄 **Modern Selenium 4** - Updated to use current best practices
- 📊 **Professional Logging** - Track all actions with timestamped logs
- ⚙️ **JSON Configuration** - Easy setup via config file
- 🛡️ **Robust Error Handling** - Smart retry logic and graceful failures
- 📈 **Real-time Statistics** - Monitor bot performance
- 🎯 **Multiple Modes** - Views, Hearts, and Followers

## 📋 Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Pausiar/tiktok_boost.git
cd tiktok_boost
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download ChromeDriver
- Visit https://chromedriver.chromium.org/downloads
- Download version matching your Chrome browser
- Extract and place in project directory (or note the path)

### 4. Configure the bot
Edit `config.json` with your settings:
```json
{
    "video_url": "https://www.tiktok.com/@username/video/1234567890",
    "bot_mode": 1,
    "chromedriver_path": "chromedriver",
    "headless": false
}
```

## 🎮 Usage

```bash
python tiktok_bot.py
```

### Bot Modes

- **Mode 1**: Auto Views (1000 views per cycle)
- **Mode 2**: Auto Hearts/Likes
- **Mode 4**: Auto Followers

## 📁 Project Structure

```
tiktok_boost/
├── tiktok_bot.py      # Main bot script
├── config.json        # Configuration file
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── .gitignore        # Git ignore rules
└── logs/             # Log files (auto-generated)
```

## 🔍 Logging

All bot activities are logged to:
- Console output (real-time)
- `tiktok_bot.log` (persistent file)

## ⚠️ Important Notes

1. **Captcha Required**: You must manually solve captchas when they appear
2. **Rate Limiting**: The bot includes delays to avoid detection
3. **Account Risk**: Your TikTok account may be banned for using automation
4. **Third-party Service**: Relies on vipto.de (reliability not guaranteed)

## 🐛 Troubleshooting

### ChromeDriver version mismatch
```bash
# Check Chrome version
google-chrome --version

# Download matching ChromeDriver version
```

### Element not found errors
- Website structure may have changed
- Try increasing wait times in config.json
- Check if vipto.de is accessible

### Captcha issues
- Don't use headless mode for captcha solving
- Allow sufficient time to solve manually

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

This project is provided as-is for educational purposes only.

## ⚖️ Legal Warning

**Using this bot:**
- Violates TikTok's Terms of Service
- May result in permanent account suspension
- Could be considered fraudulent activity
- May violate laws in your jurisdiction

**The author is not responsible for any consequences of using this software.**

## 🌟 Acknowledgments

Based on the original work by [NoNameoN-A](https://github.com/NoNameoN-A)

Enhanced and modernized by the community.

---

**Remember**: Organic growth through quality content is always better than automation! 🎬✨