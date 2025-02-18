from redmine_bot.env import TELEGRAM_BOT_TOKEN, REDMINE_URL, REDMINE_API_TOKEN, ALLOWED_USER_IDS
from redmine_bot.bot import RedmineBot
from redmine_bot.middleware import UserAuthorizationMiddleware


def main():
    # 验证必要的环境变量
    if not all([TELEGRAM_BOT_TOKEN, REDMINE_URL, REDMINE_API_TOKEN]):
        raise ValueError(
            "❌ 缺少必要的环境变量：TELEGRAM_BOT_TOKEN, REDMINE_URL, REDMINE_API_TOKEN")

    # 检查是否配置了允许的用户
    if not ALLOWED_USER_IDS:
        raise ValueError("❌ 未配置允许使用 Bot 的用户 ID")

    # 创建用户授权中间件
    auth_middleware = UserAuthorizationMiddleware(ALLOWED_USER_IDS)

    # 初始化并启动 Bot
    bot = RedmineBot(TELEGRAM_BOT_TOKEN, auth_middleware)
    bot.start()


if __name__ == '__main__':
    main()
