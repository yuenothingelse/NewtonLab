import tkinter as tk
from tkinter import ttk

import sympy as sp


x = sp.symbols("x")


def parse_function(function_text):
    """
    Mengubah input fungsi dari pengguna
    menjadi ekspresi matematika SymPy.
    """

    function_text = function_text.strip()

    if not function_text:
        raise ValueError(
            "Fungsi f(x) tidak boleh kosong."
        )

    function_text = function_text.replace(
        "^",
        "**"
    )

    allowed_functions = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "exp": sp.exp,
        "log": sp.log,
        "sqrt": sp.sqrt,
        "abs": sp.Abs
    }

    local_dict = {
        "x": x,
        "pi": sp.pi,
        "E": sp.E,
        **allowed_functions
    }

    try:
        expression = sp.sympify(
            function_text,
            locals=local_dict
        )
    except Exception as error:
        raise ValueError(
            "Format fungsi tidak valid."
        ) from error

    return expression


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
        title.pack(pady=(25, 5))

        subtitle = ttk.Label(
            self.root,
            text="Kalkulator Metode Newton-Raphson"
        )
        subtitle.pack()

        ttk.Label(
            self.root,
            text="Praktikum Komputasi Numerik C"
        ).pack(pady=5)

        main_frame = ttk.Frame(
            self.root,
            padding=30
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        input_frame = ttk.LabelFrame(
            main_frame,
            text="Parameter Newton-Raphson",
            padding=20
        )
        input_frame.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        ttk.Label(
            input_frame,
            text="Fungsi f(x):"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.function_entry = ttk.Entry(
            input_frame,
            width=30
        )
        self.function_entry.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        self.function_entry.insert(
            0,
            "x^2 - 4"
        )

        ttk.Label(
            input_frame,
            text="Tebakan awal (x₀):"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.x0_entry = ttk.Entry(
            input_frame,
            width=30
        )
        self.x0_entry.grid(
            row=3,
            column=0,
            pady=(0, 15)
        )

        self.x0_entry.insert(
            0,
            "3"
        )

        ttk.Label(
            input_frame,
            text="Toleransi error:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.tolerance_entry = ttk.Entry(
            input_frame,
            width=30
        )
        self.tolerance_entry.grid(
            row=5,
            column=0,
            pady=(0, 15)
        )

        self.tolerance_entry.insert(
            0,
            "0.000001"
        )

        ttk.Label(
            input_frame,
            text="Maksimum iterasi:"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=5
        )

        self.max_iteration_entry = ttk.Entry(
            input_frame,
            width=30
        )
        self.max_iteration_entry.grid(
            row=7,
            column=0,
            pady=(0, 20)
        )

        self.max_iteration_entry.insert(
            0,
            "50"
        )

        self.calculate_button = ttk.Button(
            input_frame,
            text="Hitung Akar",
            command=self.test_function
        )
        self.calculate_button.grid(
            row=8,
            column=0,
            sticky="ew"
        )

        result_frame = ttk.LabelFrame(
            main_frame,
            text="Hasil",
            padding=20
        )
        result_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        ttk.Label(
            result_frame,
            text="Hasil perhitungan akan ditampilkan di sini."
        ).pack(
            pady=30
        )

    def test_function(self):
        try:
            function = parse_function(
                self.function_entry.get()
            )

            print(
                "Fungsi:",
                function
            )

        except ValueError as error:
            print(
                "Error:",
                error
            )


def main():
    root = tk.Tk()

    app = NewtonRaphsonApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
