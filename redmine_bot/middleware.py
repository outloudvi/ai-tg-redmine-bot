from typing import List


class UserAuthorizationMiddleware:
    def __init__(self, allowed_users: List[int]):
        self.allowed_users = allowed_users

    def is_authorized(self, user_id: int) -> bool:
        return user_id in self.allowed_users
