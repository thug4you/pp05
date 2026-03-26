import os
import random
import tkinter as tk
from PIL import Image, ImageTk

CAPTCHA_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


class CaptchaBlock(tk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Капча: расставьте фрагменты по порядку", **kwargs)
        self._tiles: list[ImageTk.PhotoImage] = []
        self._order: list[int] = []
        self._selected: int | None = None
        self._buttons: list[tk.Button] = []
        self._load()
        self._render()

    def _load(self):
        images = sorted(f for f in os.listdir(CAPTCHA_DIR) if f.endswith(".png"))
        self._tiles = [
            ImageTk.PhotoImage(Image.open(os.path.join(CAPTCHA_DIR, f)).resize((100, 100), Image.LANCZOS))
            for f in images[:4]
        ]
        self._order = list(range(4))
        while self._order == [0, 1, 2, 3]:
            random.shuffle(self._order)

    def _render(self):
        for btn in self._buttons:
            btn.destroy()
        self._buttons = []
        self._selected = None
        for i, tile_idx in enumerate(self._order):
            r, c = divmod(i, 2)
            photo = self._tiles[tile_idx]
            btn = tk.Button(
                self,
                image=photo,
                relief="raised",
                bd=2,
                command=lambda pos=i: self._on_click(pos),
            )
            btn.image = photo
            btn.grid(row=r, column=c, padx=1, pady=1)
            self._buttons.append(btn)

    def _on_click(self, pos: int):
        if self._selected is None:
            self._selected = pos
            self._buttons[pos].config(relief="sunken", bg="gray")
        else:
            if self._selected != pos:
                self._order[self._selected], self._order[pos] = (
                    self._order[pos],
                    self._order[self._selected],
                )
            self._render()

    def is_solved(self) -> bool:
        return self._order == [0, 1, 2, 3]

    def reset(self):
        self._load()
        self._render()
