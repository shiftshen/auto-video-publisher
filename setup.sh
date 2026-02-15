#!/bin/bash
# Auto Video Publisher - 一键安装脚本

set -e

echo "=========================================="
echo "🚀 Auto Video Publisher 安装脚本"
echo "=========================================="

# 检查Python
echo "📌 检查Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi
echo "✅ Python3 已安装: $(python3 --version)"

# 检查pip
echo "📌 检查pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3"
    exit 1
fi
echo "✅ pip3 已安装"

# 创建目录
echo "📌 创建目录..."
mkdir -p ~/Videos/line_videos
mkdir -p cookies/douyin
mkdir -p cookies/tiktok
echo "✅ 目录创建完成"

# 安装依赖
echo "📌 安装Python依赖..."
pip3 install -r requirements.txt --quiet
echo "✅ 依赖安装完成"

# 安装浏览器
echo "📌 安装Playwright浏览器..."
playwright install chromium firefox --with-deps --quiet 2>/dev/null || true
echo "✅ 浏览器安装完成"

echo ""
echo "=========================================="
echo "✅ 安装完成!"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 复制账号配置模板创建新账号"
echo "   cp accounts/shiftshen_douyin.json accounts/你的账号_douyin.json"
echo ""
echo "2. 登录平台获取Cookie"
echo "   抖音: https://creator.douyin.com/creator-micro/content/upload"
echo "   TikTok: https://www.tiktok.com/upload"
echo ""
echo "3. 保存Cookie到对应文件"
echo "   抖音: cookies/douyin/你的账号.json"
echo "   TikTok: cookies/tiktok/你的账号.json"
echo ""
echo "4. 测试发布"
echo "   python3 publish.py shiftshen_douyin"
echo ""
echo "5. 添加定时任务（可选）"
echo "   在OpenClaw中添加cron任务"
echo ""
