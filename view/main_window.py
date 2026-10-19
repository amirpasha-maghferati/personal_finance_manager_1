import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

from model import Category, Income, Expense, Reminder
from controller import TransactionController, CategoryController, ReminderController


class MainWindow:
    """Tkinter UI connected to in-memory controllers; no file persistence yet."""

    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت هزینه‌های شخصی")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)

        self.transaction_controller = TransactionController()
        self.category_controller = CategoryController()
        self.reminder_controller = ReminderController()
        self._seed_categories()

        self._build_layout()
        self.show_dashboard()

    def _seed_categories(self):
        self.category_controller.add_category(Category(1, "حقوق", "income"))
        self.category_controller.add_category(Category(2, "خرید مایحتاج", "expense"))
        self.category_controller.add_category(Category(3, "حمل‌ونقل", "expense"))
        self.category_controller.add_category(Category(4, "سایر درآمدها", "income"))

    def _build_layout(self):
        self.root.configure(bg="#f3f5f9")
        self.sidebar = tk.Frame(self.root, bg="#172238", width=205)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="مدیریت مالی", bg="#172238", fg="white",
                 font=("Tahoma", 17, "bold")).pack(pady=(24, 28))
        nav_items = [
            ("داشبورد", self.show_dashboard),
            ("تراکنش‌ها", self.show_transactions),
            ("ثبت تراکنش", self.show_add_transaction),
            ("دسته‌بندی‌ها", self.show_categories),
            ("یادآورها", self.show_reminders),
            ("گزارش‌های مالی", self.show_reports),
        ]
        for label, command in nav_items:
            tk.Button(self.sidebar, text=label, command=command, anchor="e",
                      bg="#263650", fg="white", activebackground="#365078",
                      activeforeground="white", relief="flat", padx=18, pady=11,
                      font=("Tahoma", 10)).pack(fill="x", padx=12, pady=5)

        self.content = tk.Frame(self.root, bg="#f3f5f9")
        self.content.pack(side="left", fill="both", expand=True)
        self._build_statusbar()

    def _build_statusbar(self):
        self.status = tk.Label(self.root, text="اطلاعات فقط تا زمان بسته بودن برنامه در حافظه نگهداری می‌شود.",
                               bg="#e5eaf2", fg="#43516a", anchor="w", padx=10,
                               font=("Tahoma", 8))
        self.status.place(relx=0, rely=1, relwidth=1, anchor="sw", height=24)

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _page_header(self, title, subtitle=""):
        self._clear_content()
        tk.Label(self.content, text=title, bg="#f3f5f9", fg="#172238",
                 font=("Tahoma", 19, "bold"), anchor="e").pack(fill="x", padx=28, pady=(24, 4))
        if subtitle:
            tk.Label(self.content, text=subtitle, bg="#f3f5f9", fg="#65718a",
                     font=("Tahoma", 9), anchor="e").pack(fill="x", padx=30, pady=(0, 16))

    def _card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        tk.Label(card, text=title, bg="white", fg="#65718a", font=("Tahoma", 10)).pack(anchor="e", padx=14, pady=(14, 6))
        tk.Label(card, text=value, bg="white", fg=color, font=("Tahoma", 15, "bold")).pack(anchor="e", padx=14, pady=(0, 14))
        return card

    def show_dashboard(self):
        self._page_header("داشبورد", "خلاصه وضعیت مالی شما")
        cards = tk.Frame(self.content, bg="#f3f5f9")
        cards.pack(fill="x", padx=24, pady=8)
        values = [
            ("موجودی فعلی", f"{self.transaction_controller.get_balance():,.0f}", "#1b8b69"),
            ("مجموع درآمد", f"{self.transaction_controller.get_total_income():,.0f}", "#2878d0"),
            ("مجموع هزینه", f"{self.transaction_controller.get_total_expenses():,.0f}", "#d45c5c"),
        ]
        for i, (title, value, color) in enumerate(values):
            card = self._card(cards, title, value, color)
            card.grid(row=0, column=i, sticky="nsew", padx=7)
            cards.grid_columnconfigure(i, weight=1)
        tk.Label(self.content, text="آخرین تراکنش‌ها", bg="#f3f5f9", fg="#172238",
                 font=("Tahoma", 13, "bold")).pack(anchor="e", padx=30, pady=(22, 8))
        self._transaction_table(self.content, limit=5)
        tk.Button(self.content, text="ثبت تراکنش جدید", command=self.show_add_transaction,
                  bg="#2463eb", fg="white", relief="flat", padx=18, pady=9,
                  font=("Tahoma", 10, "bold")).pack(anchor="e", padx=30, pady=18)

    def _transaction_table(self, parent, limit=None):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=28, pady=5)
        columns = ("id", "date", "description", "category", "type", "amount")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=9)
        headers = {"id": "شناسه", "date": "تاریخ", "description": "شرح",
                   "category": "دسته‌بندی", "type": "نوع", "amount": "مبلغ"}
        widths = {"id": 55, "date": 130, "description": 210, "category": 150, "type": 90, "amount": 130}
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor="center")
        for item in self.transaction_controller.get_all_transactions()[-limit if limit else 0:]:
            category = self.category_controller.find_category(item.get_category_id())
            category_name = category.get_name() if category else str(item.get_category_id())
            type_name = "درآمد" if item.get_transaction_type() == "income" else "هزینه"
            tree.insert("", "end", values=(item.get_transaction_id(),
                item.get_created_at().strftime("%Y-%m-%d %H:%M"),
                item.get_description(), category_name, type_name, f"{item.get_amount():,.0f}"))
        tree.pack(fill="both", expand=True, padx=8, pady=8)
        return tree

    def show_transactions(self):
        self._page_header("تراکنش‌ها", "فهرست تراکنش‌های ثبت‌شده در همین اجرا")
        self._transaction_table(self.content)

    def show_add_transaction(self):
        self._page_header("ثبت تراکنش", "مبلغ باید مثبت باشد؛ نوع تراکنش موجودی را تغییر می‌دهد.")
        form = tk.Frame(self.content, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        form.pack(fill="x", padx=32, pady=8)
        self.amount_var = tk.StringVar()
        self.type_var = tk.StringVar(value="expense")
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()

        def add_field(label, widget, row):
            tk.Label(form, text=label, bg="white", fg="#263650", font=("Tahoma", 10)).grid(
                row=row, column=1, sticky="e", padx=14, pady=10)
            widget.grid(row=row, column=0, sticky="ew", padx=14, pady=10)

        amount_entry = ttk.Entry(form, textvariable=self.amount_var, justify="right")
        add_field("مبلغ", amount_entry, 0)
        type_box = ttk.Combobox(form, textvariable=self.type_var, values=("income", "expense"),
                                state="readonly", justify="right")
        add_field("نوع تراکنش", type_box, 1)

        self.category_box = ttk.Combobox(form, textvariable=self.category_var, state="readonly", justify="right")
        self._refresh_category_choices()
        add_field("دسته‌بندی", self.category_box, 2)
        add_field("شرح", ttk.Entry(form, textvariable=self.description_var, justify="right"), 3)
        form.grid_columnconfigure(0, weight=1)

        tk.Button(form, text="ثبت", command=self._submit_transaction, bg="#2463eb", fg="white",
                  relief="flat", padx=24, pady=9, font=("Tahoma", 10, "bold")).grid(
                      row=4, column=0, sticky="e", padx=14, pady=(12, 18))
        type_box.bind("<<ComboboxSelected>>", lambda event: self._refresh_category_choices())

    def _refresh_category_choices(self):
        if not hasattr(self, "category_box"):
            return
        current_type = self.type_var.get()
        choices = []
        for category in self.category_controller.get_all_categories():
            if category.get_category_type() in (current_type, "both"):
                choices.append(f"{category.get_category_id()} | {category.get_name()}")
        self.category_box["values"] = choices
        if choices:
            self.category_var.set(choices[0])
        else:
            self.category_var.set("")

    def _submit_transaction(self):
        try:
            amount = float(self.amount_var.get().replace(",", "").strip())
            if amount <= 0:
                raise ValueError("مبلغ باید بیشتر از صفر باشد.")
            selected = self.category_var.get()
            if not selected:
                raise ValueError("ابتدا یک دسته‌بندی مناسب انتخاب کن.")
            category_id = int(selected.split("|", 1)[0].strip())
            description = self.description_var.get().strip()
            next_id = max([int(x.get_transaction_id()) for x in self.transaction_controller.get_all_transactions()] or [0]) + 1
            if self.type_var.get() == "income":
                transaction = Income(next_id, amount, category_id, description)
            else:
                transaction = Expense(next_id, amount, category_id, description)
            self.transaction_controller.add_transaction(transaction)
        except (ValueError, TypeError) as error:
            messagebox.showerror("خطا در ثبت", str(error), parent=self.root)
            return
        messagebox.showinfo("موفق", "تراکنش با موفقیت ثبت شد.", parent=self.root)
        self.show_dashboard()

    def show_categories(self):
        self._page_header("دسته‌بندی‌ها", "ایجاد، ویرایش و حذف دسته‌بندی‌ها")
        toolbar = tk.Frame(self.content, bg="#f3f5f9")
        toolbar.pack(fill="x", padx=28, pady=(0, 8))
        tk.Button(toolbar, text="دسته‌بندی جدید", command=self._category_form,
                  bg="#2463eb", fg="white", relief="flat", padx=14, pady=8,
                  font=("Tahoma", 10, "bold")).pack(side="right", padx=4)
        tk.Button(toolbar, text="ویرایش انتخاب‌شده", command=lambda: self._category_form(tree),
                  relief="flat", padx=12, pady=8, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Button(toolbar, text="حذف انتخاب‌شده", command=lambda: self._delete_category(tree),
                  bg="#b93838", fg="white", relief="flat", padx=12, pady=8,
                  font=("Tahoma", 9)).pack(side="right", padx=4)
        panel = tk.Frame(self.content, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=28, pady=8)
        columns = ("id", "name", "type")
        tree = ttk.Treeview(panel, columns=columns, show="headings", selectmode="browse")
        for col, label in (("id", "شناسه"), ("name", "نام دسته‌بندی"), ("type", "نوع")):
            tree.heading(col, text=label)
            tree.column(col, anchor="center", width=180)
        for item in self.category_controller.get_all_categories():
            type_name = {"income": "درآمد", "expense": "هزینه", "both": "هر دو"}.get(item.get_category_type(), item.get_category_type())
            tree.insert("", "end", values=(item.get_category_id(), item.get_name(), type_name))
        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _category_form(self, tree=None):
        selected_id = None
        existing = None
        if tree is not None:
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("انتخاب لازم است", "ابتدا یک دسته‌بندی انتخاب کن.", parent=self.root)
                return
            selected_id = tree.item(selected[0], "values")[0]
            existing = self.category_controller.find_category(selected_id)
            if existing is None:
                try: existing = self.category_controller.find_category(int(selected_id))
                except (ValueError, TypeError): pass
        dialog = tk.Toplevel(self.root)
        dialog.title("ویرایش دسته‌بندی" if existing else "دسته‌بندی جدید")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        panel = tk.Frame(dialog, padx=18, pady=16)
        panel.pack(fill="both", expand=True)
        name_var = tk.StringVar(value=existing.get_name() if existing else "")
        type_map = {"income": "درآمد", "expense": "هزینه", "both": "هر دو"}
        reverse_type = {value: key for key, value in type_map.items()}
        type_var = tk.StringVar(value=type_map.get(existing.get_category_type(), "هزینه") if existing else "هزینه")
        tk.Label(panel, text="نام دسته‌بندی", font=("Tahoma", 10)).grid(row=0, column=1, padx=8, pady=8, sticky="e")
        ttk.Entry(panel, textvariable=name_var, justify="right", width=28).grid(row=0, column=0, padx=8, pady=8)
        tk.Label(panel, text="نوع", font=("Tahoma", 10)).grid(row=1, column=1, padx=8, pady=8, sticky="e")
        ttk.Combobox(panel, textvariable=type_var, values=tuple(type_map.values()), state="readonly", justify="right", width=25).grid(row=1, column=0, padx=8, pady=8)

        def save():
            try:
                name = name_var.get().strip()
                if not name:
                    raise ValueError("نام دسته‌بندی را وارد کن.")
                category_type = reverse_type[type_var.get()]
                if existing:
                    ok = self.category_controller.update_category(existing.get_category_id(), name=name, category_type=category_type)
                    if not ok: raise ValueError("دسته‌بندی پیدا نشد.")
                else:
                    ids = []
                    for item in self.category_controller.get_all_categories():
                        try: ids.append(int(item.get_category_id()))
                        except (ValueError, TypeError): pass
                    self.category_controller.add_category(Category(max(ids or [0]) + 1, name, category_type))
            except (ValueError, TypeError, KeyError) as error:
                messagebox.showerror("خطا", str(error), parent=dialog)
                return
            dialog.destroy()
            self.show_categories()
            self._refresh_category_choices()
        tk.Button(panel, text="ذخیره", command=save, bg="#2463eb", fg="white", relief="flat", padx=16, pady=7).grid(row=2, column=0, sticky="e", padx=8, pady=(12, 0))

    def _delete_category(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("انتخاب لازم است", "ابتدا یک دسته‌بندی انتخاب کن.", parent=self.root)
            return
        raw_id = tree.item(selected[0], "values")[0]
        category = self.category_controller.find_category(raw_id)
        if category is None:
            try: category = self.category_controller.find_category(int(raw_id))
            except (ValueError, TypeError): pass
        if category is None:
            messagebox.showerror("خطا", "دسته‌بندی پیدا نشد.", parent=self.root)
            return
        used_by_transaction = any(str(x.get_category_id()) == str(category.get_category_id()) for x in self.transaction_controller.get_all_transactions())
        used_by_reminder = any(str(x.get_category_id()) == str(category.get_category_id()) for x in self.reminder_controller.get_all_reminders())
        if used_by_transaction or used_by_reminder:
            messagebox.showwarning("امکان حذف نیست", "این دسته‌بندی در تراکنش یا یادآور استفاده شده است.", parent=self.root)
            return
        if messagebox.askyesno("تأیید حذف", f"دسته‌بندی «{category.get_name()}» حذف شود؟", parent=self.root):
            self.category_controller.delete_category(category.get_category_id())
            self.show_categories()
            self._refresh_category_choices()


    def show_reports(self):
        self._page_header("گزارش‌های مالی", "گزارش درآمد و هزینه در بازه زمانی دلخواه")

        controls = tk.Frame(self.content, bg="#f3f5f9")
        controls.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(controls, text="از تاریخ (YYYY-MM-DD)", bg="#f3f5f9", font=("Tahoma", 9)).grid(row=0, column=0, padx=5, pady=5)
        start_var = tk.StringVar()
        start_entry = ttk.Entry(controls, textvariable=start_var, width=16, justify="center")
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(controls, text="تا تاریخ (YYYY-MM-DD)", bg="#f3f5f9", font=("Tahoma", 9)).grid(row=0, column=2, padx=5, pady=5)
        end_var = tk.StringVar()
        end_entry = ttk.Entry(controls, textvariable=end_var, width=16, justify="center")
        end_entry.grid(row=0, column=3, padx=5, pady=5)

        summary = tk.Frame(self.content, bg="#f3f5f9")
        summary.pack(fill="x", padx=22, pady=5)
        details = tk.Frame(self.content, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        details.pack(fill="both", expand=True, padx=28, pady=12)
        tk.Label(details, text="هزینه‌ها به تفکیک دسته‌بندی", bg="white", fg="#172238",
                 font=("Tahoma", 12, "bold")).pack(anchor="e", padx=12, pady=10)
        columns = ("category", "count", "amount")
        tree = ttk.Treeview(details, columns=columns, show="headings", height=10)
        tree.heading("category", text="دسته‌بندی")
        tree.heading("count", text="تعداد تراکنش")
        tree.heading("amount", text="مجموع هزینه")
        tree.column("category", width=240, anchor="center")
        tree.column("count", width=130, anchor="center")
        tree.column("amount", width=180, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        def generate():
            try:
                start_text = start_var.get().strip()
                end_text = end_var.get().strip()
                start_date = datetime.strptime(start_text, "%Y-%m-%d").date() if start_text else None
                end_date = datetime.strptime(end_text, "%Y-%m-%d").date() if end_text else None
                if start_date and end_date and start_date > end_date:
                    raise ValueError("تاریخ شروع نباید بعد از تاریخ پایان باشد.")
            except ValueError as exc:
                messagebox.showerror("تاریخ نامعتبر", str(exc) or "تاریخ را با قالب YYYY-MM-DD وارد کنید.")
                return

            transactions = self.transaction_controller.get_all_transactions()
            if start_date:
                transactions = [x for x in transactions if x.get_created_at().date() >= start_date]
            if end_date:
                transactions = [x for x in transactions if x.get_created_at().date() <= end_date]

            income = sum(x.get_amount() for x in transactions if x.get_transaction_type() == "income")
            expenses = sum(x.get_amount() for x in transactions if x.get_transaction_type() == "expense")
            for child in summary.winfo_children():
                child.destroy()
            summary_values = [
                ("مجموع درآمد در بازه", f"{income:,.0f}", "#2878d0"),
                ("مجموع هزینه در بازه", f"{expenses:,.0f}", "#d45c5c"),
                ("خالص بازه", f"{income - expenses:,.0f}", "#1b8b69"),
            ]
            for i, (title, value, color) in enumerate(summary_values):
                card = self._card(summary, title, value, color)
                card.grid(row=0, column=i, sticky="nsew", padx=6)
                summary.grid_columnconfigure(i, weight=1)

            for item in tree.get_children():
                tree.delete(item)
            grouped = {}
            for item in transactions:
                if item.get_transaction_type() != "expense":
                    continue
                category = self.category_controller.find_category(item.get_category_id())
                name = category.get_name() if category else str(item.get_category_id())
                if name not in grouped:
                    grouped[name] = {"count": 0, "amount": 0.0}
                grouped[name]["count"] += 1
                grouped[name]["amount"] += item.get_amount()
            for name, data in sorted(grouped.items(), key=lambda pair: pair[1]["amount"], reverse=True):
                tree.insert("", "end", values=(name, data["count"], f"{data['amount']:,.0f}"))
            if not grouped:
                tree.insert("", "end", values=("هزینه‌ای در این بازه ثبت نشده است", 0, "0"))

        tk.Button(controls, text="ساخت گزارش", command=generate, bg="#2463eb", fg="white",
                  relief="flat", padx=16, pady=7, font=("Tahoma", 9, "bold")).grid(row=0, column=4, padx=10)
        tk.Label(self.content, text="برای گزارش کل اطلاعات، تاریخ شروع و پایان را خالی بگذار.",
                 bg="#f3f5f9", fg="#65718a", font=("Tahoma", 9)).pack(anchor="e", padx=30, pady=(0, 5))
        generate()

    def show_reminders(self):
        self._page_header("یادآورها", "ثبت یادآور برای یک دسته‌بندی و تاریخ آینده؛ اطلاعات فقط در حافظه است")
        form = tk.Frame(self.content, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        form.pack(fill="x", padx=28, pady=(0, 12))
        title_var = tk.StringVar()
        date_var = tk.StringVar(value=date.today().isoformat())
        category_var = tk.StringVar()
        notes_var = tk.StringVar()
        tk.Label(form, text="عنوان", bg="white", font=("Tahoma", 9)).grid(row=0, column=1, padx=8, pady=8, sticky="e")
        ttk.Entry(form, textvariable=title_var, justify="right", width=25).grid(row=0, column=0, padx=8, pady=8)
        tk.Label(form, text="تاریخ (YYYY-MM-DD)", bg="white", font=("Tahoma", 9)).grid(row=1, column=1, padx=8, pady=8, sticky="e")
        ttk.Entry(form, textvariable=date_var, justify="right", width=25).grid(row=1, column=0, padx=8, pady=8)
        tk.Label(form, text="دسته‌بندی", bg="white", font=("Tahoma", 9)).grid(row=2, column=1, padx=8, pady=8, sticky="e")
        choices = [f"{x.get_category_id()} | {x.get_name()}" for x in self.category_controller.get_all_categories()]
        category_box = ttk.Combobox(form, textvariable=category_var, values=choices, state="readonly", justify="right", width=22)
        category_box.grid(row=2, column=0, padx=8, pady=8)
        if choices: category_var.set(choices[0])
        tk.Label(form, text="توضیحات", bg="white", font=("Tahoma", 9)).grid(row=3, column=1, padx=8, pady=8, sticky="e")
        ttk.Entry(form, textvariable=notes_var, justify="right", width=25).grid(row=3, column=0, padx=8, pady=8)
        tree_frame = tk.Frame(self.content, bg="white", highlightbackground="#dce2ec", highlightthickness=1)
        tree_frame.pack(fill="both", expand=True, padx=28, pady=4)
        columns = ("id", "title", "date", "category", "status", "notes")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        headings = {"id": "شناسه", "title": "عنوان", "date": "موعد", "category": "دسته‌بندی", "status": "وضعیت", "notes": "توضیحات"}
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, anchor="center", width=130)
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        def refresh():
            for row in tree.get_children(): tree.delete(row)
            for item in self.reminder_controller.get_all_reminders():
                category = self.category_controller.find_category(item.get_category_id())
                category_name = category.get_name() if category else str(item.get_category_id())
                status = "انجام‌شده" if item.is_completed() else ("سررسید گذشته" if item.is_due() else "در انتظار")
                tree.insert("", "end", values=(item.get_reminder_id(), item.get_title(), item.get_due_date().isoformat(), category_name, status, item.get_notes()))

        def add_reminder():
            try:
                if not category_var.get(): raise ValueError("یک دسته‌بندی انتخاب کن.")
                due_date = date.fromisoformat(date_var.get().strip())
                category_id = category_var.get().split("|", 1)[0].strip()
                category = self.category_controller.find_category(category_id)
                if category is None:
                    try: category = self.category_controller.find_category(int(category_id))
                    except (ValueError, TypeError): pass
                if category is None: raise ValueError("دسته‌بندی انتخاب‌شده معتبر نیست.")
                ids = []
                for item in self.reminder_controller.get_all_reminders():
                    try: ids.append(int(item.get_reminder_id()))
                    except (ValueError, TypeError): pass
                self.reminder_controller.add_reminder(Reminder(max(ids or [0]) + 1, title_var.get(), due_date, category.get_category_id(), notes_var.get()))
            except (ValueError, TypeError) as error:
                messagebox.showerror("خطا در ثبت یادآور", str(error), parent=self.root)
                return
            title_var.set(""); notes_var.set("")
            refresh()
            messagebox.showinfo("موفق", "یادآور ثبت شد.", parent=self.root)

        def complete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("انتخاب لازم است", "ابتدا یک یادآور انتخاب کن.", parent=self.root); return
            item_id = tree.item(selected[0], "values")[0]
            item = next((x for x in self.reminder_controller.get_all_reminders() if str(x.get_reminder_id()) == str(item_id)), None)
            if item is None: return
            self.reminder_controller.mark_as_completed(item.get_reminder_id())
            refresh()

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("انتخاب لازم است", "ابتدا یک یادآور انتخاب کن.", parent=self.root); return
            item_id = tree.item(selected[0], "values")[0]
            item = next((x for x in self.reminder_controller.get_all_reminders() if str(x.get_reminder_id()) == str(item_id)), None)
            if item and messagebox.askyesno("تأیید حذف", "این یادآور حذف شود؟", parent=self.root):
                self.reminder_controller.delete_reminder(item.get_reminder_id())
                refresh()

        tk.Button(form, text="ثبت یادآور", command=add_reminder, bg="#2463eb", fg="white", relief="flat", padx=12, pady=7).grid(row=4, column=0, padx=8, pady=10, sticky="e")
        actions = tk.Frame(self.content, bg="#f3f5f9")
        actions.pack(fill="x", padx=28, pady=6)
        tk.Button(actions, text="علامت‌گذاری به‌عنوان انجام‌شده", command=complete_selected, relief="flat", padx=10, pady=7).pack(side="right", padx=4)
        tk.Button(actions, text="حذف یادآور", command=delete_selected, bg="#b93838", fg="white", relief="flat", padx=10, pady=7).pack(side="right", padx=4)
        refresh()
