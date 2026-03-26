import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def get_connection():
    return psycopg2.connect(
        host=os.getenv("APP_DB_HOST", "localhost"),
        port=int(os.getenv("APP_DB_PORT", 5432)),
        dbname=os.getenv("APP_DB_NAME"),
        user=os.getenv("APP_DB_USER"),
        password=os.getenv("APP_DB_PASSWORD"),
    )

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    failed_attempts INT DEFAULT 0,
                    is_blocked BOOLEAN DEFAULT false
                );
            """)
            cur.execute("SELECT COUNT(*) FROM users;")
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO users (username, password, role) "
                    "VALUES ('admin', 'admin', 'Администратор'), ('user', 'user', 'Пользователь')"
                )
        conn.commit()
