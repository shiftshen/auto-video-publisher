# Auto Video Publisher

Unified skill for automated video generation and publishing to Douyin (抖音).

## Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt
playwright install chromium firefox

# Setup cookies
# 1. Login to Douyin creator studio
# 2. Export cookies to config/cookies/douyin_uploader/cookie.json

# Publish a video
python3 publish.py "解压"
python3 publish.py "迷你厨房"
python3 publish.py "小人国"
```

## Supported Themes

- 解压/ASMR
- 迷你厨房
- 滴胶
- 小人国
- 自然风景
- 宠物
- 化妆
- 肥皂切割
- 史莱ム

## Requirements

- Python 3.8+
- Playwright
- Chrome/Firefox browser
- Douyin creator account with valid cookies

## File Structure

```
auto-video-publisher/
├── publish.py              # Main script
├── setup.sh               # One-click setup
├── SKILL.md               # Chinese documentation
├── README.md              # This file
├── config/
│   └── cookies/          # Cookie storage
└── requirements.txt      # Python dependencies
```

## Deployment

### New Computer

```bash
git clone https://github.com/your-repo/auto-video-publisher.git
cd auto-video-publisher
chmod +x setup.sh
./setup.sh
# Add your Douyin cookies
# Done!
```

### OpenClaw Integration

```bash
# Add cron job
cron add --schedule "every 3h" --task "auto-publish"
```

## License

MIT
