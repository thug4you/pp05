import tkinter as tk
from tkinter import messagebox

from ui_modules.captcha import CaptchaBlock
from entities.user_model import User

APP_TITLE = "ИС ООО \"Ассоль\""


class AuthView:
    def __init__(self, root: tk.Tk):
        self._root = root
        root.title(f"Система управления | {APP_TITLE}")
        root.geometry("400x580")
        root.minsize(380, 550)
        
        # Настраиваем основной шрифт для всего приложения
        font_main = ("Arial", 11)
        font_title = ("Arial", 14, "bold")

        # Основной контейнер с отступами
        main_container = tk.Frame(root, padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Заголовок формы
        tk.Label(main_container, text="Вход в систему", font=font_title).pack(pady=(0, 15))

        # Блок для ввода учетных данных
        auth_frame = tk.LabelFrame(main_container, text="Авторизация", font=("Arial", 10, "italic"), padx=15, pady=10)
        auth_frame.pack(fill=tk.X, pady=5)

        tk.Label(auth_frame, text="Имя пользователя (Логин):", font=font_main).pack(anchor="w")
        self._username_var = tk.StringVar()
        tk.Entry(auth_frame, textvariable=self._username_var, font=font_main, relief="solid").pack(fill=tk.X, pady=(2, 10))

        tk.Label(auth_frame, text="Ваш пароль:", font=font_main).pack(anchor="w")
        self._password_var = tk.StringVar()
        tk.Entry(auth_frame, textvariable=self._password_var, show="•", font=font_main, relief="solid").pack(fill=tk.X, pady=(2, 5))

        # Блок капчи
        captcha_frame = tk.LabelFrame(main_container, text="Проверка безопасности (Соберите пазл)", font=("Arial", 10, "italic"), padx=10, pady=10)
        captcha_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self._captcha = CaptchaBlock(captcha_frame)
        self._captcha.pack(pady=5)

        # Панель кнопок для капчи
        tools_frame = tk.Frame(captcha_frame)
        tools_frame.pack(fill=tk.X, pady=5)
        tk.Button(tools_frame, text="Сменить картинку", command=self._captcha.reset, font=("Arial", 9)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(tools_frame, text="Проверить капчу", command=self._check_captcha, font=("Arial", 9)).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

        # Кнопка входа
        tk.Button(main_container, text="Войти в аккаунт", font=("Arial", 12, "bold"), bg="#e0e0e0", height=2, command=self._on_login).pack(fill=tk.X, pady=(15, 0))

        root.bind("<Return>", lambda _: self._on_login())

    def _check_captcha(self):
        if self._captcha.is_solved():
            messagebox.showinfo("Капча", "Капча пройдена успешно!")
        else:
            messagebox.showwarning("Капча", "Фрагменты расставлены неверно. Попробуйте ещё раз.")

    def _on_login(self):
        username = self._username_var.get().strip()
        password = self._password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Поля «Логин» и «Пароль» обязательны для заполнения.")
            return

        try:
            row = User.get_by_username(username)
        except Exception as exc:
            messagebox.showerror("Ошибка БД", f"Не удалось подключиться к базе данных:\n{exc}")
            return

        if row is None:
            messagebox.showerror(
                "Ошибка входа",
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные.",
            )
            return

        user_id, _, db_password, role, is_blocked, _ = row

        if is_blocked:
            messagebox.showerror(
                "Доступ запрещён",
                "Вы заблокированы. Обратитесь к администратору.",
            )
            return

        if not self._captcha.is_solved():
            self._handle_failure(user_id, "Капча собрана неверно. Повторите попытку.")
            return

        if password != db_password:
            self._handle_failure(
                user_id,
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные.",
            )
            return

        User.reset_failures(user_id)
        messagebox.showinfo("Успех", "Вы успешно авторизовались.")
        self._open_main(role)

    def _handle_failure(self, user_id: int, message: str):
        User.increment_failures(user_id)
        updated = User.get_by_username(self._username_var.get().strip())
        self._captcha.reset()
        if updated and updated[4]:  # is_blocked
            messagebox.showerror(
                "Доступ запрещён",
                "Вы заблокированы. Обратитесь к администратору.",
            )
        else:
            messagebox.showerror("Ошибка входа", message)

    def _open_main(self, role: str):
        from screens.admin import AdminView
        self._root.withdraw()
        top = tk.Toplevel()
        top.protocol("WM_DELETE_WINDOW", self._root.destroy)
        if role == "Администратор":
            AdminView(top)
        else:
            top.title(f"{APP_TITLE} — Рабочий стол")
            top.minsize(300, 150)
            tk.Label(top, text=f"Добро пожаловать, {self._username_var.get()}!", padx=20, pady=40).pack()
