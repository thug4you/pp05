import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from storage.db_conn import get_connection

ROLES = ["Администратор", "Пользователь"]
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"


def seed():
    with get_connection() as conn:
        with conn.cursor() as cur:
            for role in ROLES:
                cur.execute(
                    "INSERT INTO user_roles (role_name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (role,),
                )

            cur.execute("SELECT 1 FROM users WHERE username = %s", (ADMIN_USERNAME,))
            if cur.fetchone():
                print(f"Пользователь '{ADMIN_USERNAME}' уже существует.")
            else:
                cur.execute(
                    "INSERT INTO users (username, password, role, is_blocked, failed_attempts) "
                    "VALUES (%s, %s, %s, false, 0)",
                    (ADMIN_USERNAME, ADMIN_PASSWORD, "Администратор"),
                )
                print(f"Создан администратор: логин='{ADMIN_USERNAME}', пароль='{ADMIN_PASSWORD}'")

        conn.commit()
    print("Seed выполнен успешно.")


if __name__ == "__main__":
    seed()
