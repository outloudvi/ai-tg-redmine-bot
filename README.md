# Redmine Telegram Bot

## 功能
- 列出当前用户的 Redmine 工单
- 创建新的工单
- 为工单添加评论
- 修改工单状态

## 环境要求
- Python 3.9+
- Poetry

## 安装步骤
1. 克隆仓库
2. 安装依赖：`poetry install`
3. 配置环境变量
4. 运行 Bot：`poetry run redmine-bot`

## 环境变量
- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token
- `REDMINE_URL`: Redmine 实例 URL
- `REDMINE_API_TOKEN`: Redmine API Token
- `ALLOWED_USER_IDS`: 允许使用 Bot 的用户 ID 列表

## 开发
- 代码检查：`poetry run black .`
- 运行测试：`poetry run pytest`
