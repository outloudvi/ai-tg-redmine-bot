import os

from dotenv import load_dotenv

load_dotenv()

# 从环境变量获取配置
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
REDMINE_URL = os.environ.get('REDMINE_URL')
REDMINE_API_TOKEN = os.environ.get('REDMINE_API_TOKEN')

# 允许使用 Bot 的用户 ID 列表（从环境变量读取）
ALLOWED_USER_IDS = os.environ.get('ALLOWED_USER_IDS', '').split(',')
ALLOWED_USER_IDS = [int(uid.strip())
                    for uid in ALLOWED_USER_IDS if uid.strip()]
