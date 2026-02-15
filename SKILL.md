# Auto Video Publisher - 统一技能

全自动视频生成发布系统 - 支持多账号多平台

## 架构

```
auto-video-publisher/
├── publish.py              # 主调度脚本
├── setup.sh                # 一键安装脚本
├── SKILL.md                # 本文档
├── README.md               # 英文说明
├── requirements.txt        # Python依赖
├── accounts/               # 账号配置
│   └── shiftshen_douyin.json
├── cookies/                # Cookie存储
│   ├── douyin/
│   │   └── shiftshen.json
│   └── tiktok/
├── platforms/              # 平台上传（独立）
└── themes/                 # 主题配置
    └── themes.yaml
```

## 快速开始

### 1. 安装

```bash
git clone https://github.com/你的仓库/auto-video-publisher.git
cd auto-video-publisher
chmod +x setup.sh
./setup.sh
```

### 2. 配置账号

复制账号配置模板：

```bash
cp accounts/shiftshen_douyin.json accounts/新账号_douyin.json
```

编辑配置文件：

```json
{
  "account_id": "新账号_douyin",
  "platform": "douyin",
  "name": "账号名称",
  "language": "中文",
  "theme": "解压",
  "style": "舒服解压",
  "tags": ["解压", "ASMR", "强迫症", "治愈"],
  "title_patterns": ["🎉 {关键词}也太爽了"],
  "cookie_file": "cookies/douyin/新账号.json",
  "enabled": true,
  "schedule_hours": 3
}
```

### 3. 配置Cookie

登录对应平台，导出Cookie保存到：
- 抖音: `cookies/douyin/账号名.json`
- TikTok: `cookies/tiktok/账号名.json`

### 4. 使用方法

```bash
# 发布到指定账号
python3 publish.py shiftshen_douyin

# 发布到所有启用账号
python3 publish.py all
```

## 添加新账号

### 步骤1: 创建账号配置

在 `accounts/` 目录创建JSON文件：

```json
{
  "account_id": "my_douyin",
  "platform": "douyin",
  "name": "myaccount",
  "display_name": "我的账号",
  "language": "中文",
  "theme": "解压",
  "style": "舒服解压",
  "tags": ["解压", "ASMR", "强迫症", "治愈"],
  "title_patterns": ["🎉 {关键词}也太爽了"],
  "cookie_file": "cookies/douyin/myaccount.json",
  "enabled": true,
  "schedule_hours": 3
}
```

### 步骤2: 添加Cookie

在对应平台的cookies目录添加cookie文件

### 步骤3: 测试

```bash
python3 publish.py my_douyin
```

## 支持的主题

| 主题 | 说明 |
|------|------|
| 解压 | ASMR、收纳、切割 |
| 迷你厨房 | 烹饪、美食 |
| 滴胶 | 手工、DIY |
| 小人国 | 迷你世界、精致 |
| 自然风景 | 延时、唯美 |
| 宠物 | 动物、可爱 |
| 化妆 | 美妆、收纳 |
| 肥皂切割 | ASMR |
| 史莱姆 | 拉伸、解压 |

## 定时任务

在OpenClaw中设置：

```bash
# 每3小时发布一次
cron add --schedule "every 3h" --task "publish"
```

## 账号配置说明

| 字段 | 说明 | 示例 |
|------|------|------|
| account_id | 唯一ID | shiftshen_douyin |
| platform | 平台 | douyin/tiktok |
| name | 账号名 | shiftshen |
| display_name | 显示名称 | shiftshen |
| language | 语言 | 中文/英文/泰文 |
| theme | 主题 | 解压/迷你厨房/... |
| style | 风格描述 | 舒服解压 |
| tags | 默认标签 | ["解压","ASMR",...] |
| title_patterns | 标题模板 | ["🎉 {关键词}..."] |
| cookie_file | Cookie路径 | cookies/douyin/xxx.json |
| enabled | 是否启用 | true/false |
| schedule_hours | 发布间隔(小时) | 3 |

## 平台独立

- 抖音上传在 `platforms/douyin/`
- TikTok上传在 `platforms/tiktok/`
- 哪个平台出问题只需修改对应目录，不影响其他平台

## License

MIT
