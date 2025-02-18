import requests
import telebot

from redmine_bot.middleware import UserAuthorizationMiddleware
from redmine_bot.env import REDMINE_URL, REDMINE_API_TOKEN
from redmine_bot.utils import try_to_state


HELP_MSG = "🤖 欢迎使用 Redmine 机器人！可用命令：\n" \
    "/issues - 列出你的工单\n" \
    "/create [项目ID] [标题] [描述] - 创建工单\n" \
    "/comment [工单ID] [评论] - 添加评论\n" \
    "/state [工单ID] [状态] - 修改工单状态\n" \
    "/issue [工单ID] - 查看工单状态" \
    "/resolve [工单ID] - 完成工单" \
    "/close [工单ID] - 关闭工单"


class RedmineBot:
    def __init__(self, token: str, auth_middleware: UserAuthorizationMiddleware):
        self.bot = telebot.TeleBot(token)
        self.auth_middleware = auth_middleware
        self.setup_handlers()
        self.status_id_mapping = self.get_issue_statuses()

    def check_authorization(self, message):
        """
        检查用户是否有权限使用 Bot
        """
        user_id = message.from_user.id
        if not self.auth_middleware.is_authorized(user_id):
            self.bot.reply_to(message, "❌ 抱歉，你没有使用此 Bot 的权限")
            return False
        return True

    # pylint-ignore: R0915
    def setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            # 首先检查授权
            if not self.check_authorization(message):
                return

            self.bot.reply_to(message, HELP_MSG)

        @self.bot.message_handler(commands=['issues'])
        def list_issues(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            try:
                # 获取当前用户的工单
                response = requests.get(
                    f"{REDMINE_URL}/issues.json",
                    params={"assigned_to_id": "me"},
                    headers={"X-Redmine-API-Key": REDMINE_API_TOKEN},
                    timeout=10
                )

                if response.status_code == 200:
                    issues = response.json().get('issues', [])
                    if not issues:
                        self.bot.reply_to(message, "📭 没有找到工单")
                        return

                    # 格式化工单列表
                    issue_list = []
                    for issue in issues:
                        issue_list.append(
                            f"🔢 ID: {issue['id']}, "
                            f"📁 项目: {issue['project']['name']}, "
                            f"📝 标题: {issue['subject']}, "
                            f"🚩 状态: {issue['status']['name']}"
                        )

                    self.bot.reply_to(message, "\n".join(issue_list))
                else:
                    self.bot.reply_to(message, f"❌ 获取工单失败：{response.text}")

            except Exception as e:
                self.bot.reply_to(message, f"❌ 发生错误：{str(e)}")

        @self.bot.message_handler(commands=['create'])
        def create_issue(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            try:
                # 解析命令参数
                parts = message.text.split(' ', 3)
                if len(parts) < 4:
                    self.bot.reply_to(message, "使用方法：/create [项目ID] [标题] [描述]")
                    return

                _, project_id, title, description = parts

                # 创建工单的 API 请求
                issue_data = {
                    'issue': {
                        'project_id': project_id,
                        'subject': title,
                        'description': description
                    }
                }

                response = requests.post(
                    f"{REDMINE_URL}/issues.json",
                    json=issue_data,
                    headers={
                        "Content-Type": "application/json",
                        "X-Redmine-API-Key": REDMINE_API_TOKEN
                    },
                    timeout=10
                )

                if response.status_code == 201:
                    issue_id = response.json()['issue']['id']
                    self.bot.reply_to(message, f"🎉 工单创建成功！工单 ID：{issue_id}")
                else:
                    self.bot.reply_to(message, f"❌ 创建工单失败：{response.text}")

            except Exception as e:
                self.bot.reply_to(message, f"❌ 发生错误：{str(e)}")

        @self.bot.message_handler(commands=['comment'])
        def add_comment(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            try:
                # 解析命令参数
                parts = message.text.split(' ', 2)
                if len(parts) < 3:
                    self.bot.reply_to(message, "使用方法：/comment [工单ID] [评论内容]")
                    return

                _, issue_id, comment = parts

                # 添加评论的 API 请求
                comment_data = {
                    'issue': {
                        'notes': comment
                    }
                }

                response = requests.put(
                    f"{REDMINE_URL}/issues/{issue_id}.json",
                    json=comment_data,
                    headers={
                        "Content-Type": "application/json",
                        "X-Redmine-API-Key": REDMINE_API_TOKEN
                    },
                    timeout=10
                )

                if response.status_code == 204:
                    self.bot.reply_to(message, "💬 评论添加成功！")
                else:
                    self.bot.reply_to(message, f"❌ 添加评论失败：{response.text}")

            except Exception as e:
                self.bot.reply_to(message, f"❌ 发生错误：{str(e)}")

        @self.bot.message_handler(commands=['state'])
        def update_issue_state(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            try:
                # 解析命令参数
                parts = message.text.split(' ', 2)
                if len(parts) < 3:
                    self.bot.reply_to(message, "使用方法：/state [工单ID] [状态ID]")
                    return

                _, issue_id, status_id = parts

                status_id = try_to_state(status_id, self.status_id_mapping)

                # 更新工单状态的 API 请求
                update_data = {
                    'issue': {
                        'status_id': status_id
                    }
                }

                response = requests.put(
                    f"{REDMINE_URL}/issues/{issue_id}.json",
                    json=update_data,
                    headers={
                        "Content-Type": "application/json",
                        "X-Redmine-API-Key": REDMINE_API_TOKEN
                    },
                    timeout=10
                )

                if response.status_code == 204:
                    self.bot.reply_to(message, "🔄 工单状态更新成功！")
                else:
                    self.bot.reply_to(message, f"❌ 更新工单状态失败：{response.text}")

            except ValueError:
                self.bot.reply_to(
                    message, f"❌ 无效的状态。支持的状态： {", ".join(self.status_id_mapping.values())}")
            except Exception as e:
                self.bot.reply_to(message, f"❌ 发生错误：{str(e)}")

        @self.bot.message_handler(commands=['issue'])
        def get_issue_details(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            try:
                # 解析命令参数
                parts = message.text.split(' ')
                if len(parts) < 2:
                    self.bot.reply_to(message, "使用方法：/issue [工单ID]")
                    return

                issue_id = parts[1]

                # 获取工单详细信息
                response = requests.get(
                    f"{REDMINE_URL}/issues/{issue_id}.json",
                    params={"include": ",".join(["journals", "attachments"])},
                    headers={"X-Redmine-API-Key": REDMINE_API_TOKEN},
                    timeout=10
                )

                if response.status_code == 200:
                    issue_data = response.json().get('issue', {})

                    # 构建详细信息消息
                    details_message = f"🔢 工单 ID: {issue_data['id']}\n"
                    details_message += f"📁 项目: {issue_data['project']['name']}\n"
                    details_message += f"📝 标题: {issue_data['subject']}\n"
                    details_message += f"🚩 状态: {issue_data['status']['name']}\n"

                    # 添加描述（如果有）
                    if issue_data.get('description'):
                        details_message += f"\n📄 描述:\n{issue_data['description']}\n"

                    # 添加优先级信息
                    if 'priority' in issue_data:
                        details_message += f"🏷️ 优先级: {issue_data['priority']['name']}\n"

                    # 添加处理人信息
                    if 'assigned_to' in issue_data:
                        details_message += f"👤 分配给: {issue_data['assigned_to']['name']}\n"

                    # 处理评论
                    journals = issue_data.get('journals', [])
                    if journals:
                        details_message += "\n💬 评论历史:\n"
                        # 只显示最近的5条评论
                        for journal in journals[-5:]:
                            if journal.get('notes'):
                                user_name = journal.get(
                                    'user', {}).get('name', '未知用户')
                                created_on = journal.get('created_on', '未知时间')
                                details_message += f"- {user_name} ({created_on}):\n{journal['notes']}\n\n"

                    # 发送详细信息
                    self.bot.reply_to(message, details_message)

                else:
                    self.bot.reply_to(message, f"❌ 获取工单详情失败：{response.text}")

            except requests.RequestException as e:
                self.bot.reply_to(message, f"❌ 网络请求错误：{str(e)}")

            except KeyError as e:
                self.bot.reply_to(message, f"❌ 解析工单信息时出错：{str(e)}")

            except Exception as e:
                self.bot.reply_to(message, f"❌ 发生未知错误：{str(e)}")

        @self.bot.message_handler(commands=['resolve'])
        def resolve(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            parts = message.text.split(' ')
            if len(parts) < 2:
                self.bot.reply_to(message, "使用方法：/resolve [工单ID]")
                return

            issue_id = parts[1]
            message.text = f"/state {issue_id} resolved"
            update_issue_state(message)

        @self.bot.message_handler(commands=['close'])
        def close(message):
            # 检查授权
            if not self.check_authorization(message):
                return

            parts = message.text.split(' ')
            if len(parts) < 2:
                self.bot.reply_to(message, "使用方法：/close [工单ID]")
                return

            issue_id = parts[1]
            message.text = f"/state {issue_id} closed"
            update_issue_state(message)

    def start(self):
        print("🚀 Redmine Bot 已启动")
        self.bot.polling(none_stop=True)

    def get_issue_statuses(self):
        response = requests.get(
            f"{REDMINE_URL}/issue_statuses.json",
            headers={"X-Redmine-API-Key": REDMINE_API_TOKEN},
            timeout=10
        )
        issue_statuses = response.json().get("issue_statuses", [])

        result = {}
        for status in issue_statuses:
            result[status["id"]] = status["name"]

        return result
