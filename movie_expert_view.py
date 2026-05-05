import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MovieExpertView:

    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller

        self.root.title("Кино-Эксперт")
        self.root.geometry("1100x760")
        self.root.minsize(980, 680)
        self.root.configure(bg="#F5F6FA")

        self.var_q1 = tk.BooleanVar(value=True)
        self.var_q2 = tk.BooleanVar(value=True)
        self.var_q3 = tk.BooleanVar(value=True)
        self.genre_var = tk.StringVar(value="")

        self.profile_var = tk.StringVar(value="—")
        self.depth_var = tk.StringVar(value="—")
        self.tempo_var = tk.StringVar(value="—")
        self.movie_var = tk.StringVar(value="—")
        self.movie_subtitle_var = tk.StringVar(value="")
        self.movie_desc_var = tk.StringVar(
            value="Ответьте на вопросы и нажмите «Подобрать фильм»."
        )
        self.status_var = tk.StringVar(value="Рекомендация не найдена")

        self._yesno_buttons = {}
        self._genre_buttons = {}

        self._setup_styles()
        self._build_ui()
        self._refresh_yes_no_styles()
        self._refresh_genre_styles()

    def set_controller(self, controller):
        self.controller = controller

    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        self.COL_BG = "#F5F6FA"
        self.COL_CARD = "#FFFFFF"
        self.COL_TEXT = "#111827"
        self.COL_MUTED = "#6B7280"
        self.COL_BORDER = "#D9DDEA"
        self.COL_ACCENT = "#5B4BDB"
        self.COL_ACCENT_DARK = "#4A3CC9"
        self.COL_ACCENT_SOFT = "#EAE7FF"
        self.COL_SUCCESS = "#198754"
        self.COL_WARN = "#B07A00"

        style.configure("App.TFrame", background=self.COL_BG)
        style.configure("Card.TFrame", background=self.COL_CARD)
        style.configure("Section.TFrame", background=self.COL_CARD)

        style.configure(
            "Title.TLabel",
            background=self.COL_BG,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.COL_BG,
            foreground=self.COL_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "SectionTitle.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "ResultKey.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "ResultValue.TLabel",
            background=self.COL_CARD,
            foreground=self.COL_ACCENT,
            font=("Segoe UI", 10, "bold"),
        )

    def _build_ui(self):
        self.main = ttk.Frame(self.root, style="App.TFrame", padding=18)
        self.main.pack(fill="both", expand=True)

        self._build_header()
        self._build_content()

    def _build_header(self):
        header = ttk.Frame(self.main, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))

        left = ttk.Frame(header, style="App.TFrame")
        left.pack(side="left", anchor="w")

        ttk.Label(left, text="Подбор фильма", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            left,
            text="Ответьте на 3 вопроса, и система предложит фильм",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        right = ttk.Frame(header, style="App.TFrame")
        right.pack(side="right")

        self.btn_submit = self._make_button(
            right,
            text="Подобрать фильм",
            command=self._on_submit,
            width=18,
            primary=True,
        )
        self.btn_submit.pack(side="right", padx=(10, 0))

        self.btn_reset = self._make_button(
            right,
            text="Сбросить",
            command=self._on_reset,
            width=12,
            primary=False,
        )
        self.btn_reset.pack(side="right")

    def _build_content(self):
        content = ttk.Frame(self.main, style="App.TFrame")
        content.pack(fill="both", expand=True)

        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self.left_card = self._make_card(content)
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        self.right_card = self._make_card(content)
        self.right_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self._build_left_panel(self.left_card)
        self._build_right_panel(self.right_card)

    def _build_left_panel(self, parent):
        parent.columnconfigure(0, weight=1)

        ttk.Label(parent, text="1. Ответьте на вопросы", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 14)
        )

        q_frame = ttk.Frame(parent, style="Card.TFrame")
        q_frame.grid(row=1, column=0, sticky="ew")
        q_frame.columnconfigure(0, weight=1)

        self._create_yes_no_row(
            q_frame,
            row=0,
            title="Любит сложные сюжеты?",
            var=self.var_q1,
            key="q1",
        )
        self._create_yes_no_row(
            q_frame,
            row=1,
            title="Готов пересматривать?",
            var=self.var_q2,
            key="q2",
        )
        self._create_yes_no_row(
            q_frame,
            row=2,
            title="Смотрит авторское кино?",
            var=self.var_q3,
            key="q3",
        )

        sep = ttk.Separator(parent, orient="horizontal")
        sep.grid(row=2, column=0, sticky="ew", pady=18)

        ttk.Label(
            parent, text="2. Выберите предпочтительный жанр", style="CardTitle.TLabel"
        ).grid(row=3, column=0, sticky="w", pady=(0, 12))

        genres = ttk.Frame(parent, style="Card.TFrame")
        genres.grid(row=4, column=0, sticky="ew")
        genres.columnconfigure((0, 1), weight=1)
        genres.columnconfigure((2, 3), weight=1)

        self._create_genre_button(genres, 0, 0, "Драма")
        self._create_genre_button(genres, 0, 1, "Фантастика")
        self._create_genre_button(genres, 1, 0, "Боевик")
        self._create_genre_button(genres, 1, 1, "Романтическая комедия")

        bottom = ttk.Frame(parent, style="Card.TFrame")
        bottom.grid(row=5, column=0, sticky="ew", pady=(18, 0))
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)

        note = ttk.Label(
            parent,
            text="Система подберёт фильм на основе ваших ответов по правилам экспертной системы.",
            style="Muted.TLabel",
            wraplength=460,
            justify="left",
        )
        note.grid(row=6, column=0, sticky="w", pady=(18, 0))

    def _build_right_panel(self, parent):
        parent.columnconfigure(0, weight=1)

        ttk.Label(parent, text="Результат", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        status = ttk.Label(
            parent,
            textvariable=self.status_var,
            style="ResultValue.TLabel",
        )
        status.grid(row=1, column=0, sticky="w", pady=(0, 18))

        info = ttk.Frame(parent, style="Card.TFrame")
        info.grid(row=2, column=0, sticky="ew")
        info.columnconfigure(1, weight=1)

        self._create_result_row(info, 0, "Профиль зрителя", self.profile_var)
        self._create_result_row(info, 1, "Рекомендуемая глубина", self.depth_var)
        self._create_result_row(info, 2, "Рекомендуемый темп", self.tempo_var)

        sep = ttk.Separator(parent, orient="horizontal")
        sep.grid(row=3, column=0, sticky="ew", pady=16)

        ttk.Label(parent, text="Рекомендуемый фильм", style="CardTitle.TLabel").grid(
            row=4, column=0, sticky="w", pady=(0, 10)
        )

        film_card = ttk.Frame(parent, style="Card.TFrame")
        film_card.grid(row=5, column=0, sticky="ew")
        film_card.columnconfigure(0, weight=1)

        ttk.Label(
            film_card,
            textvariable=self.movie_var,
            font=("Segoe UI", 18, "bold"),
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            film_card,
            textvariable=self.movie_subtitle_var,
            font=("Segoe UI", 10),
            background=self.COL_CARD,
            foreground=self.COL_MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        ttk.Label(
            film_card,
            textvariable=self.movie_desc_var,
            wraplength=360,
            justify="left",
            background=self.COL_CARD,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 10),
        ).grid(row=2, column=0, sticky="w", pady=(12, 0))

        tip = ttk.Frame(parent, style="Card.TFrame")
        tip.grid(row=6, column=0, sticky="ew", pady=(18, 0))

    def _make_card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.configure()
        return card

    def _make_button(self, parent, text, command, width=14, primary=False):
        if primary:
            bg = self.COL_ACCENT
            fg = "white"
            active_bg = self.COL_ACCENT_DARK
        else:
            bg = "#FFFFFF"
            fg = self.COL_TEXT
            active_bg = "#EEF1F7"

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bd=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            cursor="hand2",
            padx=14,
            pady=10,
        )
        return btn

    def _create_yes_no_row(self, parent, row, title, var, key):
        row_frame = ttk.Frame(parent, style="Card.TFrame")
        row_frame.grid(row=row, column=0, sticky="ew", pady=8)
        row_frame.columnconfigure(1, weight=1)

        ttk.Label(row_frame, text=title, style="Body.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 18)
        )

        btns = ttk.Frame(row_frame, style="Card.TFrame")
        btns.grid(row=0, column=1, sticky="e")

        yes_btn = tk.Button(
            btns,
            text="Да",
            command=lambda: self._set_bool(var, True),
            bd=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            width=9,
            padx=10,
            pady=8,
            cursor="hand2",
        )
        yes_btn.pack(side="left", padx=(0, 8))

        no_btn = tk.Button(
            btns,
            text="Нет",
            command=lambda: self._set_bool(var, False),
            bd=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            width=9,
            padx=10,
            pady=8,
            cursor="hand2",
        )
        no_btn.pack(side="left")

        self._yesno_buttons[key] = {"yes": yes_btn, "no": no_btn}

    def _create_genre_button(self, parent, r, c, genre):
        btn = tk.Button(
            parent,
            text=genre,
            command=lambda g=genre: self._set_genre(g),
            bd=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            width=16,
            padx=12,
            pady=12,
            cursor="hand2",
            wraplength=130,
        )
        btn.grid(row=r, column=c, sticky="ew", padx=6, pady=6)
        self._genre_buttons[genre] = btn

    def _create_result_row(self, parent, row, label, variable):
        row_frame = ttk.Frame(parent, style="Card.TFrame")
        row_frame.grid(row=row, column=0, sticky="ew", pady=10)
        row_frame.columnconfigure(1, weight=1)

        ttk.Label(row_frame, text=label, style="ResultKey.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(row_frame, textvariable=variable, style="ResultValue.TLabel").grid(
            row=0, column=1, sticky="e"
        )

    def _set_bool(self, var, value):
        var.set(value)
        self._refresh_yes_no_styles()

    def _set_genre(self, genre):
        self.genre_var.set(genre)
        self._refresh_genre_styles()

    def _refresh_yes_no_styles(self):
        selected_bg = self.COL_ACCENT
        selected_fg = "white"
        unselected_bg = "#FFFFFF"
        unselected_fg = self.COL_TEXT
        border = self.COL_BORDER

        mapping = [
            ("q1", self.var_q1.get()),
            ("q2", self.var_q2.get()),
            ("q3", self.var_q3.get()),
        ]

        for key, value in mapping:
            yes_btn = self._yesno_buttons[key]["yes"]
            no_btn = self._yesno_buttons[key]["no"]

            if value is True:
                yes_btn.configure(bg=selected_bg, fg=selected_fg, activebackground=self.COL_ACCENT_DARK)
                no_btn.configure(bg=unselected_bg, fg=unselected_fg, activebackground="#EEF1F7")
            else:
                yes_btn.configure(bg=unselected_bg, fg=unselected_fg, activebackground="#EEF1F7")
                no_btn.configure(bg=selected_bg, fg=selected_fg, activebackground=self.COL_ACCENT_DARK)

            yes_btn.configure(highlightthickness=1, highlightbackground=border, highlightcolor=border)
            no_btn.configure(highlightthickness=1, highlightbackground=border, highlightcolor=border)

    def _refresh_genre_styles(self):
        for genre, btn in self._genre_buttons.items():
            active = (self.genre_var.get() == genre)
            if active:
                btn.configure(
                    bg=self.COL_ACCENT,
                    fg="white",
                    activebackground=self.COL_ACCENT_DARK,
                    activeforeground="white",
                    highlightthickness=0,
                )
            else:
                btn.configure(
                    bg="#FFFFFF",
                    fg=self.COL_TEXT,
                    activebackground="#EEF1F7",
                    activeforeground=self.COL_TEXT,
                    highlightthickness=1,
                    highlightbackground=self.COL_BORDER,
                    highlightcolor=self.COL_BORDER,
                )

    def get_data(self):
        return {
            "complex_plots": self.var_q1.get(),
            "rewatchable": self.var_q2.get(),
            "arthouse": self.var_q3.get(),
            "genre": self.genre_var.get(),
        }

    def _on_submit(self):
        if not self.genre_var.get():
            messagebox.showwarning(
                "Жанр не выбран",
                "Пожалуйста, выберите предпочтительный жанр перед подбором фильма."
            )
            return

        data = self.get_data()
        if self.controller and hasattr(self.controller, "handle_submit"):
            self.controller.handle_submit(data)

    def _on_reset(self):
        self.var_q1.set(True)
        self.var_q2.set(True)
        self.var_q3.set(True)
        self.genre_var.set("")

        self.clear_result()
        self._refresh_yes_no_styles()
        self._refresh_genre_styles()

        if self.controller and hasattr(self.controller, "handle_reset"):
            self.controller.handle_reset()

    def show_result(self, result: dict):
        """
        Ожидаемые ключи словаря:
            profile, depth, tempo, movie_title, movie_subtitle, movie_desc, status
        """
        self.profile_var.set(result.get("profile", "—"))
        self.depth_var.set(result.get("depth", "—"))
        self.tempo_var.set(result.get("tempo", "—"))
        self.movie_var.set(result.get("movie_title", "—"))
        self.movie_subtitle_var.set(result.get("movie_subtitle", ""))
        self.movie_desc_var.set(result.get("movie_desc", ""))
        self.status_var.set(result.get("status", "Рекомендация найдена"))

    def clear_result(self):
        self.profile_var.set("—")
        self.depth_var.set("—")
        self.tempo_var.set("—")
        self.movie_var.set("—")
        self.movie_subtitle_var.set("")
        self.movie_desc_var.set("Ответьте на вопросы и нажмите «Подобрать фильм».")
        self.status_var.set("Рекомендация не найдена")