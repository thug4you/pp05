
import sys
import os
import tkinter as tk
from tkinter import messagebox

# путь для импорта
sys.path.insert(0, os.path.dirname(__file__))

from storage.db_conn import init_db
from screens.user import AuthView

def start_application():
    main_window = tk.Tk()
    
    # скрываем окно до проверки бд
    main_window.withdraw()
    
    try:
        # инициализация бд
        init_db()
    except Exception as connection_error:
        messagebox.showerror(
            title="Ошибка инициализации",
            message=f"Не удалось подключиться к базе данных приложения.\n"
                    f"Проверьте настройки подключения.\n\nКод ошибки:\n{connection_error}"
        )
        main_window.destroy()
        return

    # показываем главное окно
    main_window.deiconify()
    
    # форма авторизации
    auth_form = AuthView(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    start_application()
