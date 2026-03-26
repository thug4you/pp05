from storage.db_conn import get_connection


class User:
    def __init__(self, user_id, username, role, is_blocked, failed_attempts):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.is_blocked = is_blocked
        self.failed_attempts = failed_attempts

    @staticmethod
    def get_by_username(username):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, password, role, is_blocked, failed_attempts "
                    "FROM users WHERE username = %s",
                    (username,),
                )
                return cur.fetchone()

    @staticmethod
    def increment_failures(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET failed_attempts = failed_attempts + 1, "
                    "is_blocked = CASE WHEN failed_attempts + 1 >= 3 THEN true ELSE is_blocked END "
                    "WHERE user_id = %s",
                    (user_id,),
                )
                conn.commit()

    @staticmethod
    def reset_failures(user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET failed_attempts = 0 WHERE user_id = %s", (user_id,)
                )
                conn.commit()

    @staticmethod
    def get_all():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, role, is_blocked, failed_attempts "
                    "FROM users ORDER BY user_id"
                )
                return cur.fetchall()

    @staticmethod
    def get_roles():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT role_name FROM user_roles ORDER BY role_name")
                return [row[0] for row in cur.fetchall()]

    @staticmethod
    def exists(username):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                return cur.fetchone() is not None

    @staticmethod
    def create(username, password, role, is_blocked):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password, role, is_blocked, failed_attempts) "
                    "VALUES (%s, %s, %s, %s, 0)",
                    (username, password, role, is_blocked),
                )
                conn.commit()

    @staticmethod
    def update(user_id, username, password, role, is_blocked):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET username=%s, password=%s, role=%s, "
                    "is_blocked=%s, failed_attempts=0 WHERE user_id=%s",
                    (username, password, role, is_blocked, user_id),
                )
                conn.commit()
