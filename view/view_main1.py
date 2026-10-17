import tkinter as tk
from tkinter import ttk


class MainWindow:
    """رابط گرافیکی نمایشی مدیریت هزینه‌های شخصی؛ بدون اتصال به منطق برنامه."""

    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت هزینه‌های شخصی")
        self.root.geometry("1100x760")
        self.root.minsize(900, 650)
        self.root.configure(bg="#F4F7FB")

        self.colors = {
            "background": "#F4F7FB",
            "sidebar": "#172554",
            "sidebar_hover": "#263866",
            "primary": "#2563EB",
            "primary_light": "#DBEAFE",
            "text": "#172033",
            "muted": "#64748B",
            "white": "#FFFFFF",
            "border": "#E2E8F0",
            "green": "#059669",
            "green_light": "#D1FAE5",
            "red": "#DC2626",
            "red_light": "#FEE2E2",
            "orange": "#D97706",
            "orange_light": "#FEF3C7",
            "purple": "#7C3AED",
            "purple_light": "#EDE9FE",
        }

        self.current_page = "داشبورد"
        self.nav_buttons = {}
        self.page_area = None

        self._setup_style()
        self._build_layout()
        self.show_page("داشبورد")

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=self.colors["white"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["white"],
            rowheight=34,
            font=("Tahoma", 9),
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background="#EEF2F7",
            foreground=self.colors["text"],
            font=("Tahoma", 9, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", "#DBEAFE")])

    def _build_layout(self):
        # نوار کناری
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=225)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        brand.pack(fill="x", padx=18, pady=(24, 28))

        tk.Label(
            brand, text="◈", font=("Arial", 27, "bold"),
            bg=self.colors["sidebar"], fg="#93C5FD"
        ).pack(side="right", padx=(0, 9))
        brand_text = tk.Frame(brand, bg=self.colors["sidebar"])
        brand_text.pack(side="right")
        tk.Label(
            brand_text, text="مدیریت مالی",
            font=("Tahoma", 13, "bold"),
            bg=self.colors["sidebar"], fg="white"
        ).pack(anchor="e")
        tk.Label(
            brand_text, text="PERSONAL FINANCE",
            font=("Arial", 7, "bold"),
            bg=self.colors["sidebar"], fg="#A5B4D4"
        ).pack(anchor="e", pady=(3, 0))

        tk.Label(
            self.sidebar, text="منوی اصلی", font=("Tahoma", 9),
            bg=self.colors["sidebar"], fg="#A5B4D4", anchor="e"
        ).pack(fill="x", padx=20, pady=(0, 8))

        nav_items = [
            ("داشبورد", "⌂"),
            ("تراکنش‌ها", "↕"),
            ("ثبت تراکنش", "+"),
            ("دسته‌بندی‌ها", "▦"),
            ("یادآوری پرداخت‌ها", "◷"),
            ("گزارش‌های مالی", "▤"),
        ]
        for label, icon in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"{icon}    {label}",
                font=("Tahoma", 10),
                anchor="e",
                padx=18,
                pady=12,
                bd=0,
                relief="flat",
                cursor="hand2",
                bg=self.colors["sidebar"],
                fg="#E2E8F0",
                activebackground=self.colors["sidebar_hover"],
                activeforeground="white",
                command=lambda page=label: self.show_page(page),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[label] = btn

        spacer = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        spacer.pack(fill="both", expand=True)

        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill="x", padx=16, pady=12)
        tk.Button(
            self.sidebar,
            text="⚙    تنظیمات",
            font=("Tahoma", 10),
            anchor="e",
            padx=18,
            pady=11,
            bd=0,
            cursor="hand2",
            bg=self.colors["sidebar"],
            fg="#E2E8F0",
            activebackground=self.colors["sidebar_hover"],
            activeforeground="white",
            command=lambda: self.show_page("تنظیمات"),
        ).pack(fill="x", padx=10, pady=(0, 6))
        tk.Label(
            self.sidebar, text="نسخه نمایشی 1.0",
            font=("Tahoma", 8), bg=self.colors["sidebar"], fg="#94A3B8"
        ).pack(anchor="e", padx=20, pady=(0, 18))

        # بخش اصلی
        self.main_area = tk.Frame(self.root, bg=self.colors["background"])
        self.main_area.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.main_area, bg=self.colors["white"], height=70)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title_label = tk.Label(
            self.topbar, text="داشبورد",
            font=("Tahoma", 16, "bold"),
            bg=self.colors["white"], fg=self.colors["text"]
        )
        self.page_title_label.pack(side="right", padx=28, pady=20)

        user_area = tk.Frame(self.topbar, bg=self.colors["white"])
        user_area.pack(side="left", padx=25)
        tk.Label(
            user_area, text="کاربر مهمان",
            font=("Tahoma", 9, "bold"),
            bg=self.colors["white"], fg=self.colors["text"]
        ).pack(side="right", padx=8)
        tk.Label(
            user_area, text="●",
            font=("Arial", 16),
            bg=self.colors["white"], fg=self.colors["primary"]
        ).pack(side="right")

        self.page_area = tk.Frame(self.main_area, bg=self.colors["background"])
        self.page_area.pack(fill="both", expand=True, padx=26, pady=22)

    def _clear_page(self):
        for widget in self.page_area.winfo_children():
            widget.destroy()

    def _label(self, parent, text, size=10, color=None, bold=False, **kwargs):
        return tk.Label(
            parent, text=text,
            font=("Tahoma", size, "bold" if bold else "normal"),
            bg=kwargs.pop("bg", self.colors["background"]),
            fg=color or self.colors["text"],
            **kwargs
        )

    def _card(self, parent, padding=18, **kwargs):
        return tk.Frame(
            parent, bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1, padx=padding, pady=padding, **kwargs
        )

    def _action_button(self, parent, text, color=None, **kwargs):
        return tk.Button(
            parent, text=text,
            font=("Tahoma", 9, "bold"),
            bg=color or self.colors["primary"],
            fg="white", activebackground=color or self.colors["primary"],
            activeforeground="white", bd=0, relief="flat",
            padx=15, pady=9, cursor="hand2",
            **kwargs
        )

    def _section_heading(self, parent, title, subtitle=None):
        frame = tk.Frame(parent, bg=self.colors["background"])
        frame.pack(fill="x", pady=(0, 18))
        self._label(frame, title, size=15, bold=True).pack(anchor="e")
        if subtitle:
            self._label(frame, subtitle, size=9, color=self.colors["muted"]).pack(anchor="e", pady=(5, 0))
        return frame

    def show_page(self, page_name):
        self.current_page = page_name
        self.page_title_label.config(text=page_name)
        for name, button in self.nav_buttons.items():
            selected = name == page_name
            button.config(
                bg=self.colors["primary"] if selected else self.colors["sidebar"],
                fg="white" if selected else "#E2E8F0",
            )
        self._clear_page()

        pages = {
            "داشبورد": self._show_dashboard,
            "تراکنش‌ها": self._show_transactions,
            "ثبت تراکنش": self._show_add_transaction,
            "دسته‌بندی‌ها": self._show_categories,
            "یادآوری پرداخت‌ها": self._show_reminders,
            "گزارش‌های مالی": self._show_reports,
            "تنظیمات": self._show_settings,
        }
        pages.get(page_name, self._show_dashboard)()

    def _show_dashboard(self):
        self._section_heading(
            self.page_area, "سلام، خوش اومدی 👋",
            "نمای کلی وضعیت مالی شما در یک نگاه"
        )

        cards_row = tk.Frame(self.page_area, bg=self.colors["background"])
        cards_row.pack(fill="x", pady=(0, 18))
        summary = [
            ("موجودی فعلی", "۰ تومان", "مجموع درآمد منهای هزینه‌ها", self.colors["primary"], self.colors["primary_light"]),
            ("کل درآمد", "۰ تومان", "درآمدهای ثبت‌شده", self.colors["green"], self.colors["green_light"]),
            ("کل هزینه‌ها", "۰ تومان", "هزینه‌های ثبت‌شده", self.colors["red"], self.colors["red_light"]),
        ]
        for title, value, note, color, light in summary:
            card = self._card(cards_row, padding=16)
            card.pack(side="right", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text="●", font=("Arial", 16), bg=self.colors["white"], fg=color).pack(anchor="e")
            self._label(card, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(8, 5))
            self._label(card, value, size=17, color=color, bold=True, bg=self.colors["white"]).pack(anchor="e")
            self._label(card, note, size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(7, 0))

        lower = tk.Frame(self.page_area, bg=self.colors["background"])
        lower.pack(fill="both", expand=True)

        recent = self._card(lower, padding=16)
        recent.pack(side="right", fill="both", expand=True, padx=(0, 10))
        self._label(recent, "آخرین تراکنش‌ها", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 12))
        self._make_tree(
            recent,
            columns=("description", "category", "amount", "type"),
            headings=("شرح", "دسته‌بندی", "مبلغ", "نوع"),
            rows=[
                ("نمونه درآمد", "حقوق", "۰ تومان", "درآمد"),
                ("نمونه هزینه", "خرید مایحتاج", "۰ تومان", "هزینه"),
            ],
            height=5,
        )

        quick = self._card(lower, padding=16, width=220)
        quick.pack(side="left", fill="y")
        quick.pack_propagate(False)
        self._label(quick, "دسترسی سریع", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 12))
        self._action_button(quick, "＋  ثبت تراکنش", self.colors["primary"],
                            command=lambda: self.show_page("ثبت تراکنش")).pack(fill="x", pady=5)
        self._action_button(quick, "↕  مشاهده تراکنش‌ها", "#0F766E",
                            command=lambda: self.show_page("تراکنش‌ها")).pack(fill="x", pady=5)
        self._action_button(quick, "◷  یادآوری پرداخت‌ها", "#D97706",
                            command=lambda: self.show_page("یادآوری پرداخت‌ها")).pack(fill="x", pady=5)
        self._label(quick, "اطلاعات این صفحه نمونه است.", size=8, color=self.colors["muted"], bg=self.colors["white"], wraplength=180, justify="right").pack(anchor="e", pady=(18, 0))

    def _make_tree(self, parent, columns, headings, rows, height=8):
        wrap = tk.Frame(parent, bg=self.colors["white"])
        wrap.pack(fill="both", expand=True)
        tree = ttk.Treeview(wrap, columns=columns, show="headings", height=height)
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading, anchor="center")
            tree.column(col, anchor="center", width=120, stretch=True)
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True)
        return tree

    def _show_transactions(self):
        self._section_heading(self.page_area, "تراکنش‌ها", "فهرست نمایشی درآمدها و هزینه‌ها")
        filters = self._card(self.page_area, padding=14)
        filters.pack(fill="x", pady=(0, 14))
        self._label(filters, "جست‌وجو و فیلتر (نمایشی)", size=10, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 10))
        row = tk.Frame(filters, bg=self.colors["white"])
        row.pack(fill="x")
        self._entry_field(row, "جست‌وجو بر اساس شرح", "مثلاً خرید")
        self._combo_field(row, "نوع تراکنش", ["همه", "درآمد", "هزینه"])
        self._combo_field(row, "دسته‌بندی", ["همه", "حقوق", "خرید مایحتاج", "قبوض"])
        self._action_button(row, "فیلتر", "#64748B").pack(side="right", padx=5, pady=(17, 0))

        table_card = self._card(self.page_area, padding=14)
        table_card.pack(fill="both", expand=True)
        self._label(table_card, "همه تراکنش‌ها", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 10))
        self._make_tree(
            table_card,
            ("id", "description", "category", "date", "type", "amount"),
            ("شناسه", "شرح", "دسته‌بندی", "تاریخ", "نوع", "مبلغ"),
            [
                ("۱", "حقوق ماهانه", "حقوق", "۱۴۰۵/۰۷/۰۱", "درآمد", "۲۰۰٬۰۰۰ تومان"),
                ("۲", "خرید مایحتاج", "خرید مایحتاج", "۱۴۰۵/۰۷/۰۳", "هزینه", "۳۰٬۰۰۰ تومان"),
                ("۳", "پرداخت قبض", "قبوض", "۱۴۰۵/۰۷/۰۵", "هزینه", "۱۰٬۰۰۰ تومان"),
            ],
            height=9,
        )
        self._label(table_card, "ردیف‌های بالا فقط برای نمایش طراحی هستند.", size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(8, 0))

    def _entry_field(self, parent, title, placeholder=""):
        frame = tk.Frame(parent, bg=self.colors["white"])
        frame.pack(side="right", fill="x", expand=True, padx=5)
        self._label(frame, title, size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(0, 6))
        entry = tk.Entry(frame, font=("Tahoma", 9), justify="right", relief="solid", bd=1,
                         highlightthickness=0, bg="#FFFFFF", fg="#64748B")
        entry.pack(fill="x", ipady=7)
        if placeholder:
            entry.insert(0, placeholder)
        return entry

    def _combo_field(self, parent, title, values):
        frame = tk.Frame(parent, bg=self.colors["white"])
        frame.pack(side="right", fill="x", expand=True, padx=5)
        self._label(frame, title, size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(0, 6))
        combo = ttk.Combobox(frame, values=values, state="readonly", justify="right", font=("Tahoma", 9))
        combo.current(0)
        combo.pack(fill="x", ipady=3)
        return combo

    def _show_add_transaction(self):
        self._section_heading(self.page_area, "ثبت تراکنش جدید", "فرم ظاهری برای ثبت درآمد یا هزینه")
        card = self._card(self.page_area, padding=22)
        card.pack(fill="x", anchor="n")

        self._label(card, "اطلاعات تراکنش", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 16))
        grid = tk.Frame(card, bg=self.colors["white"])
        grid.pack(fill="x")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        self._form_entry(grid, "مبلغ (تومان)", "مثلاً ۲۰۰۰۰۰", 0, 1)
        self._form_combo(grid, "نوع تراکنش", ["درآمد", "هزینه"], 0, 0)
        self._form_combo(grid, "دسته‌بندی", ["حقوق", "خرید مایحتاج", "قبوض", "حمل‌ونقل", "سایر"], 1, 1)
        self._form_entry(grid, "تاریخ", "۱۴۰۵/۰۷/۲۵", 1, 0)
        self._form_entry(grid, "شرح تراکنش", "توضیح کوتاه درباره تراکنش", 2, 1, colspan=2)

        buttons = tk.Frame(card, bg=self.colors["white"])
        buttons.pack(fill="x", pady=(22, 0))
        self._action_button(buttons, "ثبت تراکنش", self.colors["primary"]).pack(side="right", padx=(0, 8))
        tk.Button(buttons, text="پاک کردن فرم", font=("Tahoma", 9), bg="#F1F5F9", fg=self.colors["text"],
                  activebackground="#E2E8F0", bd=0, padx=15, pady=9, cursor="hand2").pack(side="right")
        self._label(card, "این فرم فعلاً نمایشی است و اطلاعاتی ذخیره یا پردازش نمی‌شود.",
                    size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(18, 0))

    def _form_entry(self, parent, title, placeholder, row, col, colspan=1):
        frame = tk.Frame(parent, bg=self.colors["white"])
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=8, pady=8)
        self._label(frame, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(0, 6))
        entry = tk.Entry(frame, font=("Tahoma", 10), justify="right", relief="solid", bd=1)
        entry.pack(fill="x", ipady=8)
        entry.insert(0, placeholder)
        return entry

    def _form_combo(self, parent, title, values, row, col):
        frame = tk.Frame(parent, bg=self.colors["white"])
        frame.grid(row=row, column=col, sticky="ew", padx=8, pady=8)
        self._label(frame, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(0, 6))
        combo = ttk.Combobox(frame, values=values, state="readonly", justify="right", font=("Tahoma", 10))
        combo.current(0)
        combo.pack(fill="x", ipady=4)
        return combo

    def _show_categories(self):
        self._section_heading(self.page_area, "دسته‌بندی‌ها", "دسته‌بندی‌های نمونه برای مرتب‌سازی تراکنش‌ها")
        row = tk.Frame(self.page_area, bg=self.colors["background"])
        row.pack(fill="both", expand=True)
        list_card = self._card(row, padding=16)
        list_card.pack(side="right", fill="both", expand=True, padx=(0, 12))
        self._label(list_card, "فهرست دسته‌بندی‌ها", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 12))
        self._make_tree(
            list_card, ("id", "name", "type", "description"),
            ("شناسه", "نام دسته‌بندی", "نوع", "توضیحات"),
            [
                ("۱", "حقوق", "درآمد", "حقوق و دستمزد"),
                ("۲", "خرید مایحتاج", "هزینه", "خریدهای روزمره"),
                ("۳", "قبوض", "هزینه", "آب، برق، اینترنت و ..."),
                ("۴", "حمل‌ونقل", "هزینه", "رفت‌وآمد"),
                ("۵", "سایر", "عمومی", "موارد متفرقه"),
            ],
            height=10,
        )
        form = self._card(row, padding=16, width=245)
        form.pack(side="left", fill="y")
        form.pack_propagate(False)
        self._label(form, "دسته‌بندی جدید", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 15))
        self._entry_field_vertical(form, "نام دسته‌بندی", "نام را وارد کنید")
        self._combo_field_vertical(form, "نوع دسته‌بندی", ["درآمد", "هزینه", "عمومی"])
        self._action_button(form, "＋  افزودن دسته‌بندی").pack(fill="x", pady=(18, 0))
        self._label(form, "کنترل‌ها در این نسخه غیرفعال هستند.", size=8, color=self.colors["muted"], bg=self.colors["white"], wraplength=205, justify="right").pack(anchor="e", pady=(16, 0))

    def _entry_field_vertical(self, parent, title, placeholder):
        self._label(parent, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(0, 6))
        entry = tk.Entry(parent, font=("Tahoma", 9), justify="right", relief="solid", bd=1)
        entry.pack(fill="x", ipady=7)
        entry.insert(0, placeholder)
        return entry

    def _combo_field_vertical(self, parent, title, values):
        self._label(parent, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(15, 6))
        combo = ttk.Combobox(parent, values=values, state="readonly", justify="right", font=("Tahoma", 9))
        combo.current(0)
        combo.pack(fill="x", ipady=3)
        return combo

    def _show_reminders(self):
        self._section_heading(self.page_area, "یادآوری پرداخت‌ها", "نمایش نمونه‌ای پرداخت‌های آینده و سررسیدشده")
        summary = tk.Frame(self.page_area, bg=self.colors["background"])
        summary.pack(fill="x", pady=(0, 16))
        for title, value, color in [
            ("همه یادآوری‌ها", "۳", self.colors["primary"]),
            ("نزدیک به سررسید", "۱", self.colors["orange"]),
            ("پرداخت‌شده", "۱", self.colors["green"]),
        ]:
            card = self._card(summary, padding=14)
            card.pack(side="right", fill="both", expand=True, padx=(0, 10))
            self._label(card, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e")
            self._label(card, value, size=20, color=color, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(7, 0))

        table_card = self._card(self.page_area, padding=16)
        table_card.pack(fill="both", expand=True)
        self._label(table_card, "فهرست یادآوری‌ها", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 12))
        self._make_tree(
            table_card, ("title", "category", "amount", "date", "status"),
            ("عنوان", "دسته‌بندی", "مبلغ", "تاریخ سررسید", "وضعیت"),
            [
                ("پرداخت قبض اینترنت", "قبوض", "۵۰۰٬۰۰۰ تومان", "۱۴۰۵/۰۷/۲۸", "نزدیک به سررسید"),
                ("پرداخت اجاره", "مسکن", "۸٬۰۰۰٬۰۰۰ تومان", "۱۴۰۵/۰۸/۰۱", "پرداخت‌نشده"),
                ("شارژ ماهانه", "سایر", "۲۰۰٬۰۰۰ تومان", "۱۴۰۵/۰۷/۱۰", "پرداخت‌شده"),
            ],
            height=9,
        )
        controls = tk.Frame(table_card, bg=self.colors["white"])
        controls.pack(fill="x", pady=(12, 0))
        self._action_button(controls, "＋  یادآوری جدید", self.colors["orange"]).pack(side="right")
        self._label(table_card, "اطلاعات جدول صرفاً نمونه است.", size=8, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e", pady=(10, 0))

    def _show_reports(self):
        self._section_heading(self.page_area, "گزارش‌های مالی", "چیدمان نمایشی برای مرور وضعیت مالی")
        stats = tk.Frame(self.page_area, bg=self.colors["background"])
        stats.pack(fill="x", pady=(0, 16))
        for title, value, color in [
            ("درآمد این ماه", "۰ تومان", self.colors["green"]),
            ("هزینه این ماه", "۰ تومان", self.colors["red"]),
            ("پس‌انداز تقریبی", "۰ تومان", self.colors["primary"]),
        ]:
            card = self._card(stats, padding=18)
            card.pack(side="right", fill="both", expand=True, padx=(0, 10))
            self._label(card, title, size=9, color=self.colors["muted"], bg=self.colors["white"]).pack(anchor="e")
            self._label(card, value, size=17, color=color, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(8, 0))

        charts = tk.Frame(self.page_area, bg=self.colors["background"])
        charts.pack(fill="both", expand=True)
        expense_card = self._card(charts, padding=18)
        expense_card.pack(side="right", fill="both", expand=True, padx=(0, 10))
        self._label(expense_card, "هزینه‌ها بر اساس دسته‌بندی", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e")
        self._draw_mock_chart(expense_card)

        trend_card = self._card(charts, padding=18)
        trend_card.pack(side="left", fill="both", expand=True)
        self._label(trend_card, "نمای کلی درآمد و هزینه", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e")
        self._draw_mock_chart(trend_card, horizontal=True)
        self._label(self.page_area, "نمودارها و اعداد فعلاً نمونه هستند و از داده واقعی محاسبه نمی‌شوند.",
                    size=8, color=self.colors["muted"]).pack(anchor="e", pady=(12, 0))

    def _draw_mock_chart(self, parent, horizontal=False):
        chart = tk.Canvas(parent, bg=self.colors["white"], height=230, highlightthickness=0)
        chart.pack(fill="both", expand=True, pady=(12, 0))
        chart.update_idletasks()
        w = max(chart.winfo_width(), 250)
        h = 220
        if horizontal:
            labels = [("درآمد", "#059669", 0.72), ("هزینه", "#DC2626", 0.48), ("پس‌انداز", "#2563EB", 0.3)]
            y = 35
            for label, color, ratio in labels:
                chart.create_text(w - 12, y + 8, text=label, anchor="e", font=("Tahoma", 9), fill="#334155")
                chart.create_rectangle(12, y + 24, w - 12, y + 44, fill="#F1F5F9", outline="")
                chart.create_rectangle(12, y + 24, 12 + (w - 24) * ratio, y + 44, fill=color, outline="")
                y += 60
        else:
            labels = [("حقوق", "#2563EB", 120), ("خرید", "#0F766E", 75), ("قبوض", "#D97706", 45), ("سایر", "#7C3AED", 60)]
            n = len(labels)
            gap = 18
            bar_w = max(24, (w - 50 - gap * (n - 1)) // n)
            base_y = 190
            x = 25
            for label, color, bar_h in labels:
                chart.create_rectangle(x, base_y - bar_h, x + bar_w, base_y, fill=color, outline="")
                chart.create_text(x + bar_w / 2, base_y + 17, text=label, font=("Tahoma", 8), fill="#475569")
                x += bar_w + gap
            chart.create_line(12, base_y, w - 12, base_y, fill="#CBD5E1")

    def _show_settings(self):
        self._section_heading(self.page_area, "تنظیمات", "گزینه‌های ظاهری و عمومی برنامه")
        card = self._card(self.page_area, padding=22)
        card.pack(fill="x", anchor="n")
        self._label(card, "تنظیمات عمومی", size=11, bold=True, bg=self.colors["white"]).pack(anchor="e", pady=(0, 18))

        options = [
            ("واحد پول", ["تومان", "ریال"]),
            ("زبان رابط کاربری", ["فارسی", "English"]),
            ("نمایش اعداد", ["فارسی", "انگلیسی"]),
        ]
        for title, values in options:
            row = tk.Frame(card, bg=self.colors["white"])
            row.pack(fill="x", pady=8)
            self._label(row, title, size=9, bg=self.colors["white"]).pack(side="right")
            combo = ttk.Combobox(row, values=values, state="readonly", justify="right", width=20, font=("Tahoma", 9))
            combo.current(0)
            combo.pack(side="left", padx=10)
        tk.Frame(card, bg=self.colors["border"], height=1).pack(fill="x", pady=18)
        self._label(card, "درباره برنامه", size=10, bold=True, bg=self.colors["white"]).pack(anchor="e")
        self._label(
            card,
            "مدیریت هزینه‌های شخصی یک پروژه آموزشی با Python، برنامه‌نویسی شی‌گرا و رابط گرافیکی Tkinter است.",
            size=9, color=self.colors["muted"], bg=self.colors["white"], wraplength=650, justify="right"
        ).pack(anchor="e", pady=(8, 0))
        self._action_button(card, "ذخیره تنظیمات", "#64748B").pack(anchor="e", pady=(18, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
