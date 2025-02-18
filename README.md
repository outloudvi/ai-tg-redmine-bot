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

---

（以下文字作者为人类。）

## 关于 AI 作品

（注：首个 commit (`cbb5616`) 基本完全由 Claude 3.5 Haiku 完成；其余 commit 作者为人类。）

主要 prompt：

> 写一个 Telegram bot，可以通过和 bot 互动在 Redmine 创建 issue。它需要满足以下功能：
> * Redmine 实例端点和 API token 通过环境变量传递。
> * 命令 /issues 可以列出当前用户的所有 issue。
> * 命令 /create [ProjectId] [TItle] [Description] 可以创建一个 issue。
> * 命令 /comment [IssueId] [Comment] 可以给一个 issue 添加评论。
> * 命令 /state [IssueId] [Status] 可以修改一个 issue 的状态。

由于此 repo 首个 commit 的知识产权归属不明，此项目未有指定开源协议。使用时请多加注意。