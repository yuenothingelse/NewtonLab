import tkinter as tk
from tkinter import ttk


class NewtonRaphsonApp:
    def __init__(self, root):
        self.root = root

        self.root.title("NewtonLab | Newton-Raphson")
        self.root.geometry("1000x650")

        self.build_ui()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="NewtonLab",
            font=("Helvetica Neue", 24, "bold")
        )
        title.pack(pady=(30, 5))

        subtitle = ttk.Label(
            self.root,
            text="Kalkulator Metode Newton-Raphson"
        )
        subtitle.pack()

        ttk.Label(
            self.root,
            text="Praktikum Komputasi Numerik C"
        ).pack(pady=5)

        separator = ttk.Separator(
            self.root,
            orient="horizontal"
        )
        separator.pack(
            fill="x",
            padx=40,
            pady=20
        )

        ttk.Label(
            self.root,
            text="Aplikasi siap digunakan."
        ).pack(pady=50)


def main():
    root = tk.Tk()

    app = NewtonRaphsonApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
