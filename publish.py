#!/usr/bin/env python3
"""
Auto Video Publisher - 主调度脚本
根据账号配置自动生成视频并发布到对应平台
"""
import os
import sys
import json
import random
import glob

# 配置路径
SKILL_DIR = "/Users/shift/.openclaw/workspace/skills/auto-video-publisher"
ACCOUNTS_DIR = f"{SKILL_DIR}/accounts"
VIDEO_GENERATOR = "/Users/shift/.openclaw/workspace/skills/video-generator/bin/video-generator"
UPLOAD_DOUYIN = "/Users/shift/.openclaw/workspace/skills/video-uploader-skill/scripts/upload_video.py"


def load_accounts():
    """加载所有账号配置"""
    accounts = []
    for f in glob.glob(f"{ACCOUNTS_DIR}/*.json"):
        with open(f, 'r', encoding='utf-8') as fp:
            account = json.load(fp)
            if account.get('enabled', True):
                accounts.append(account)
    return accounts


def load_themes(language='中文'):
    """加载主题配置"""
    import yaml
    with open(f"{SKILL_DIR}/themes/themes.yaml", 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if language == '中文':
        return data.get('themes', {})
    elif language == '英文':
        return data.get('themes_en', {})
    elif language == '泰文':
        return data.get('themes_th', {})
    return data.get('themes', {})


def generate_title(theme_config, account_config):
    """生成标题"""
    patterns = theme_config.get('title_patterns', account_config.get('title_patterns', []))
    if not patterns:
        return f"新视频发布"
    
    pattern = random.choice(patterns)
    tags = theme_config.get('tags', account_config.get('tags', []))
    keyword = random.choice(tags) if tags else '视频'
    return pattern.format(关键词=keyword, keyword=keyword)


def generate_tags(theme_config):
    """生成标签"""
    tags = theme_config.get('tags', [])
    return ",".join(tags[:4])


def generate_video(prompt):
    """生成视频"""
    print(f"🎬 正在生成视频...")
    
    cmd = f'/opt/homebrew/bin/python3 {VIDEO_GENERATOR} generate "{prompt}" --duration "15秒" --resolution "竖屏" --text-only'
    result = os.popen(cmd).read()
    
    import re
    match = re.search(r"Saved: (.+\.mp4)", result)
    if match:
        video_path = match.group(1).strip()
        print(f"✅ 视频生成成功: {video_path}")
        return video_path
    
    print(f"❌ 视频生成失败: {result}")
    return None


def upload_douyin(video_path, title, tags, cookie_file):
    """上传到抖音"""
    print(f"📤 正在上传到抖音...")
    
    cmd = f'cd {SKILL_DIR} && PYTHONPATH=/Users/shift/.openclaw/workspace/skills/video-generator PYTHONPATH=. /opt/homebrew/bin/python3 {UPLOAD_DOUYIN} --platform douyin --title "{title}" --video "{video_path}" --tags "{tags}" --account "{cookie_file}"'
    
    result = os.popen(cmd).read()
    print(result)
    
    return "发布成功" in result or "Successfully uploaded" in result


def publish_to_account(account):
    """发布视频到指定账号"""
    print(f"\n{'='*50}")
    print(f"📱 账号: {account['name']} ({account['platform']})")
    print(f"{'='*50}")
    
    # 加载主题
    language = account.get('language', '中文')
    themes = load_themes(language)
    
    # 获取主题
    theme_name = account.get('theme', '解压')
    theme_config = themes.get(theme_name, themes.get('解压', {}))
    
    if not theme_config:
        print(f"❌ 找不到主题: {theme_name}")
        return False
    
    # 生成标题和标签
    title = generate_title(theme_config, account)
    tags = generate_tags(theme_config)
    
    print(f"📝 标题: {title}")
    print(f"🏷️ 标签: {tags}")
    
    # 生成视频
    video_path = generate_video(theme_config.get('prompt', ''))
    if not video_path:
        return False
    
    # 上传
    platform = account['platform']
    cookie_path = f"{SKILL_DIR}/{account['cookie_file']}"
    
    if platform == 'douyin':
        success = upload_douyin(video_path, title, tags, cookie_path)
    else:
        print(f"❌ 不支持的平台: {platform}")
        return False
    
    return success


def main():
    if len(sys.argv) < 2:
        # 发布到所有启用的账号
        accounts = load_accounts()
        if not accounts:
            print("❌ 没有找到启用的账号")
            sys.exit(1)
        
        print(f"📋 将发布到 {len(accounts)} 个账号")
        
        for account in accounts:
            try:
                publish_to_account(account)
            except Exception as e:
                print(f"❌ 发布失败: {e}")
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("""
Auto Video Publisher - 视频发布工具

使用方法:
  python3 publish.py                 # 发布到所有启用的账号
  python3 publish.py 账号ID          # 发布到指定账号

示例:
  python3 publish.py                 # 发布到所有账号
  python3 publish.py shiftshen_douyin  # 只发布到抖音账号

可用账号:
  - shiftshen_douyin (抖音)
  - shiftshen_tiktok (TikTok)

添加新账号:
  在 accounts/ 目录添加 JSON 配置文件
""")
    else:
        # 发布到指定账号
        account_id = sys.argv[1]
        account_file = f"{ACCOUNTS_DIR}/{account_id}.json"
        
        if not os.path.exists(account_file):
            print(f"❌ 找不到账号配置: {account_id}")
            sys.exit(1)
        
        with open(account_file, 'r', encoding='utf-8') as f:
            account = json.load(f)
        
        success = publish_to_account(account)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
