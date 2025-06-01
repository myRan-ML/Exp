class User:
    """用户模型"""
    def __init__(self, uid, username, password_hash, role='customer'):
        self.UID = uid
        self.USERNAME = username
        self.PASSWORD_HASH = password_hash
        self.ROLE = role