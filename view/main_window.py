
import tkinter as tk


class MainWindow:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Personal Finance Manager")
        self.root.geometry("650x780")
        self.root.minsize(550, 650)
        self.root.configure(bg="#F3F6FB")

        # Colors
        self.dark_color = "#172554"
        self.primary_color = "#2563EB"
        self.background_color = "#F3F6FB"
        self.card_color = "#FFFFFF"
        self.text_color = "#1E293B"

        # Build the interface
        self.create_header()
        self.create_balance_card()
        self.create_menu()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg=self.dark_color,
            height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="مدیریت هزینه‌های شخصی",
            font=("Tahoma", 18, "bold"),
            bg=self.dark_color,
            fg="white"
        )
        title.pack(pady=(17, 4))

        subtitle = tk.Label(
            header,
            text="Personal Finance Manager",
            font=("Arial", 10),
            bg=self.dark_color,
            fg="#CBD5E1"
        )
        subtitle.pack()

    def create_balance_card(self):
        balance_frame = tk.Frame(
            self.root,
            bg=self.primary_color,
            padx=15,
            pady=12
        )
        balance_frame.pack(
            fill="x",
            padx=25,
            pady=(18, 12)
        )

        balance_title = tk.Label(
            balance_frame,
            text="موجودی فعلی",
            font=("Tahoma", 12),
            bg=self.primary_color,
            fg="white"
        )
        balance_title.pack()

        balance_amount = tk.Label(
            balance_frame,
            text="0 تومان",
            font=("Tahoma", 21, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        balance_amount.pack(pady=(5, 0))

    def create_menu(self):
        menu_frame = tk.Frame(
            self.root,
            bg=self.background_color
        )
        menu_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        menu_title = tk.Label(
            menu_frame,
            text="منوی اصلی",
            font=("Tahoma", 14, "bold"),
            bg=self.background_color,
            fg=self.text_color
        )
        menu_title.pack(
            anchor="e",
            pady=(0, 10)
        )

        buttons_frame = tk.Frame(
            menu_frame,
            bg=self.background_color
        )
        buttons_frame.pack(
            fill="both",
            expand=True
        )

        buttons = [
            ("➕ ثبت تراکنش", "#2563EB"),
            ("📋 مشاهده تراکنش‌ها", "#0F766E"),
            ("📂 مدیریت دسته‌بندی‌ها", "#7C3AED"),
            ("🔔 یادآوری پرداخت‌ها", "#D97706"),
            ("📊 گزارش‌های مالی", "#475569"),
            ("⚙ تنظیمات", "#64748B")
        ]

        for index, (text, color) in enumerate(buttons):
            row = index // 2
            column = index % 2

            button = tk.Button(
                buttons_frame,
                text=text,
                font=("Tahoma", 10, "bold"),
                bg=self.card_color,
                fg=color,
                activebackground="#E2E8F0",
                activeforeground=color,
                relief="flat",
                bd=0,
                cursor="hand2",
                height=3
            )

            button.grid(
                row=row,
                column=column,
                padx=7,
                pady=7,
                sticky="nsew"
            )

        # Make both columns and all rows resize proportionally
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        for row in range(3):
            buttons_frame.grid_rowconfigure(row, weight=1)

    def create_footer(self):
        footer = tk.Frame(
            self.root,
            bg=self.background_color
        )
        footer.pack(
            fill="x",
            pady=(5, 12)
        )

        footer_label = tk.Label(
            footer,
            text="نسخه اولیه | Personal Finance Manager",
            font=("Tahoma", 9),
            bg=self.background_color,
            fg="#64748B"
        )
        footer_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
