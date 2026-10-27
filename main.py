import re
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


BG = "#101522"
PANEL = "#192235"
PANEL_2 = "#202c43"
TEXT = "#f1f5f9"
MUTED = "#a8b4c8"
ACCENT = "#8b7cff"
GREEN = "#45d6a1"
RED = "#91303d"

x = sp.symbols("x")
ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "exp": sp.exp,
    "log": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
}
ALLOWED_NAMES = {"x", "pi", "E", *ALLOWED_FUNCTIONS.keys()}


def parse_function(raw_text):
    """Memvalidasi dan mengubah input fungsi menjadi ekspresi SymPy."""
    expression = raw_text.strip().replace("^", "**")
    if not expression:
        raise ValueError("Fungsi f(x) belum diisi.")

    if not re.fullmatch(r"[A-Za-z0-9_+\-*/().,\s]*", expression):
        raise ValueError("Gunakan hanya angka, x, operator matematika, kurung, dan fungsi yang didukung.")

    identifiers = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression)
    unknown_names = sorted(set(identifiers) - ALLOWED_NAMES)
    if unknown_names:
        raise ValueError(
            "Nama tidak dikenal: " + ", ".join(unknown_names) +
            ". Gunakan x, sin, cos, tan, exp, log, sqrt, abs, pi, atau E."
        )

    local_names = {"x": x, "pi": sp.pi, "E": sp.E, **ALLOWED_FUNCTIONS}
    try:
        result = sp.sympify(expression, locals=local_names, evaluate=True)
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as exc:
        raise ValueError("Format fungsi tidak valid. Contoh yang benar: x^2 - 4 atau cos(x) - x.") from exc

    if result.free_symbols - {x}:
        raise ValueError("Fungsi hanya boleh menggunakan variabel x.")
    if result.is_real is False:
        raise ValueError("Fungsi harus berupa ekspresi real untuk penggunaan ini.")
    return result


def as_real_number(value, description):
    """Konversi nilai numerik menjadi float dan menolak NaN/inf."""
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{description} bukan angka yang valid.") from exc
    if not np.isfinite(number):
        raise ValueError(f"{description} harus berupa angka hingga (bukan NaN atau tak hingga).")
    return number


class NewtonRaphsonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NewtonLab | Kalkulator Newton-Raphson")
        self.root.geometry("1220x800")
        self.root.minsize(980, 680)
        self.root.configure(bg=BG)

        self._configure_styles()
        self._build_ui()
        self._draw_empty_graph()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Helvetica Neue", 10))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=("Helvetica Neue", 9))
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=("Helvetica Neue", 10))
        style.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED, font=("Helvetica Neue", 9))
        style.configure("Heading.TLabel", background=BG, foreground=TEXT, font=("Helvetica Neue", 22, "bold"))
        style.configure("Subheading.TLabel", background=BG, foreground=MUTED, font=("Helvetica Neue", 10))
        style.configure("TEntry", fieldbackground="#0f1726", foreground=TEXT, insertcolor=TEXT,
                        bordercolor=PANEL_2, padding=9)
        style.configure("Accent.TButton", background=ACCENT, foreground="#ffffff",
                        font=("Helvetica Neue", 10, "bold"), padding=(14, 10), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#7667ec")])
        style.configure("Secondary.TButton", background=PANEL_2, foreground=TEXT,
                        font=("Helvetica Neue", 10), padding=(12, 10), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#2b3a55")])
        style.configure("Treeview", background="#111a2a", fieldbackground="#111a2a",
                        foreground=TEXT, rowheight=29, borderwidth=0, font=("Helvetica Neue", 9))
        style.configure("Treeview.Heading", background=PANEL_2, foreground=TEXT,
                        font=("Helvetica Neue", 9, "bold"), padding=8, borderwidth=0)
        style.map("Treeview", background=[("selected", "#443c83")])

    def _build_ui(self):
        header = ttk.Frame(self.root, padding=(24, 20, 24, 12))
        header.pack(fill="x")
        title_area = ttk.Frame(header)
        title_area.pack(side="left", fill="x", expand=True)
        ttk.Label(title_area, text="NewtonLab", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(title_area, text="Kalkulator metode Newton-Raphson · Komputasi Numerik",
                  style="Subheading.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(header, text="PYTHON  •  DESKTOP GUI", style="Subheading.TLabel").pack(side="right", anchor="center")

        body = ttk.Frame(self.root, padding=(24, 4, 24, 20))
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=0, minsize=285)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_input_panel(body)
        self._build_results_panel(body)

        footer = ttk.Frame(self.root, padding=(24, 0, 24, 12))
        footer.pack(fill="x")
        ttk.Label(footer, text="Catatan: hasil numerik bergantung pada tebakan awal dan sifat fungsi.",
                  style="Muted.TLabel").pack(anchor="w")

    def _build_input_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=18)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="PARAMETER INPUT", style="PanelMuted.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 14))
        ttk.Label(panel, text="Fungsi f(x)", style="Panel.TLabel").grid(row=1, column=0, sticky="w")
        self.function_var = tk.StringVar(value="x^2 - 4")
        ttk.Entry(panel, textvariable=self.function_var).grid(row=2, column=0, sticky="ew", pady=(6, 4))
        ttk.Label(panel, text="Contoh: x^3 - x - 2, cos(x) - x", style="PanelMuted.TLabel").grid(row=3, column=0, sticky="w", pady=(0, 14))

        ttk.Label(panel, text="Tebakan awal (x₀)", style="Panel.TLabel").grid(row=4, column=0, sticky="w")
        self.x0_var = tk.StringVar(value="3")
        ttk.Entry(panel, textvariable=self.x0_var).grid(row=5, column=0, sticky="ew", pady=(6, 14))

        ttk.Label(panel, text="Toleransi error", style="Panel.TLabel").grid(row=6, column=0, sticky="w")
        self.tol_var = tk.StringVar(value="0.000001")
        ttk.Entry(panel, textvariable=self.tol_var).grid(row=7, column=0, sticky="ew", pady=(6, 14))

        ttk.Label(panel, text="Maksimum iterasi", style="Panel.TLabel").grid(row=8, column=0, sticky="w")
        self.max_iter_var = tk.StringVar(value="50")
        ttk.Entry(panel, textvariable=self.max_iter_var).grid(row=9, column=0, sticky="ew", pady=(6, 18))

        ttk.Button(panel, text="Hitung akar  →", style="Accent.TButton", command=self.calculate).grid(row=10, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(panel, text="Reset", style="Secondary.TButton", command=self.reset).grid(row=11, column=0, sticky="ew")

        ttk.Separator(panel).grid(row=12, column=0, sticky="ew", pady=18)
        ttk.Label(panel, text="FUNGSI YANG DIDUKUNG", style="PanelMuted.TLabel").grid(row=13, column=0, sticky="w", pady=(0, 6))
        ttk.Label(panel, text="x, +, -, *, /, ^, ( )\nsin(x), cos(x), tan(x)\nexp(x), log(x), sqrt(x), abs(x)\npi, E",
                  style="Panel.TLabel", justify="left").grid(row=14, column=0, sticky="w")

    def _build_results_panel(self, parent):
        panel = ttk.Frame(parent)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=3)
        panel.rowconfigure(2, weight=2)

        cards = ttk.Frame(panel)
        cards.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        for col in range(3):
            cards.columnconfigure(col, weight=1)
        self.root_value = self._metric_card(cards, 0, "PERKIRAAN AKAR", "—")
        self.error_value = self._metric_card(cards, 1, "ERROR AKHIR", "—")
        self.iter_value = self._metric_card(cards, 2, "JUMLAH ITERASI", "—")

        graph_frame = ttk.Frame(panel, style="Panel.TFrame", padding=10)
        graph_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        graph_frame.rowconfigure(0, weight=1)
        graph_frame.columnconfigure(0, weight=1)
        self.figure = Figure(figsize=(7, 3.2), dpi=100, facecolor=PANEL)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        table_frame = ttk.Frame(panel, style="Panel.TFrame", padding=10)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)
        ttk.Label(table_frame, text="RIWAYAT ITERASI", style="Panel.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        columns = ("n", "xn", "fxn", "dfxn", "next", "error")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        headings = {"n": "n", "xn": "xₙ", "fxn": "f(xₙ)", "dfxn": "f′(xₙ)", "next": "xₙ₊₁", "error": "Error"}
        widths = {"n": 42, "xn": 115, "fxn": 115, "dfxn": 115, "next": 115, "error": 115}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], minwidth=40, anchor="center", stretch=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.status_var = tk.StringVar(value="Masukkan parameter lalu klik Hitung akar.")
        ttk.Label(table_frame, textvariable=self.status_var, style="PanelMuted.TLabel", wraplength=800).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def _metric_card(self, parent, column, label, value):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=(13, 12))
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 6, 0 if column == 2 else 6))
        ttk.Label(card, text=label, style="PanelMuted.TLabel").pack(anchor="w")
        value_label = ttk.Label(card, text=value, style="Panel.TLabel", font=("Helvetica Neue", 15, "bold"))
        value_label.pack(anchor="w", pady=(7, 0))
        return value_label

    def _style_axes(self):
        self.ax.set_facecolor("#111a2a")
        self.ax.tick_params(colors=MUTED, labelsize=8)
        self.ax.xaxis.label.set_color(MUTED)
        self.ax.yaxis.label.set_color(MUTED)
        self.ax.title.set_color(TEXT)
        for spine in self.ax.spines.values():
            spine.set_color("#39465d")
        self.ax.grid(True, color="#2a354b", linewidth=0.7, alpha=0.8)
        self.ax.axhline(0, color="#8290a8", linewidth=0.8)
        self.ax.axvline(0, color="#8290a8", linewidth=0.8)

    def _draw_empty_graph(self):
        self.ax.clear()
        self._style_axes()
        self.ax.set_title("Grafik fungsi akan muncul di sini", pad=10)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.figure.tight_layout()
        self.canvas.draw_idle()

    @staticmethod
    def _fmt(number):
        return f"{number:.8g}"

    def calculate(self):
        try:
            function = parse_function(self.function_var.get())
            derivative = sp.diff(function, x)
            x0 = as_real_number(self.x0_var.get(), "Tebakan awal x₀")
            tolerance = as_real_number(self.tol_var.get(), "Toleransi error")
            if tolerance <= 0:
                raise ValueError("Toleransi error harus lebih besar dari 0.")
            try:
                max_iterations = int(self.max_iter_var.get())
            except ValueError as exc:
                raise ValueError("Maksimum iterasi harus berupa bilangan bulat.") from exc
            if max_iterations < 1 or max_iterations > 10000:
                raise ValueError("Maksimum iterasi harus antara 1 dan 10000.")

            f = sp.lambdify(x, function, modules=["numpy"])
            df = sp.lambdify(x, derivative, modules=["numpy"])
            rows = []
            xn = x0
            converged = False
            final_error = None
            reason = "Maksimum iterasi tercapai sebelum toleransi terpenuhi."

            for n in range(1, max_iterations + 1):
                try:
                    fxn = as_real_number(f(xn), f"f(x) pada iterasi {n}")
                    dfxn = as_real_number(df(xn), f"f′(x) pada iterasi {n}")
                except (ValueError, ZeroDivisionError, OverflowError) as exc:
                    raise ValueError(f"Perhitungan gagal pada iterasi {n}: {exc}") from exc

                if abs(dfxn) < 1e-14:
                    raise ValueError(
                        f"Turunan f′(x) mendekati nol pada x = {self._fmt(xn)}. "
                        "Metode Newton-Raphson tidak dapat melanjutkan dari tebakan ini. Coba x₀ lain."
                    )

                x_next = xn - fxn / dfxn
                if not np.isfinite(x_next):
                    raise ValueError("Perhitungan menghasilkan nilai tak hingga. Coba tebakan awal lain.")
                error = abs(x_next - xn)
                rows.append((n, xn, fxn, dfxn, x_next, error))
                xn = x_next
                final_error = error

                if error <= tolerance:
                    converged = True
                    reason = f"Konvergen: error ≤ toleransi ({self._fmt(tolerance)})."
                    break

            self._show_results(rows, xn, final_error, converged, reason, function, f)
        except Exception as exc:
            messagebox.showerror("Input atau perhitungan tidak valid", str(exc), parent=self.root)
            self.status_var.set("Perhitungan belum berhasil. Periksa input dan coba lagi.")

    def _show_results(self, rows, root_value, final_error, converged, reason, function, f):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for n, xn, fxn, dfxn, x_next, error in rows:
            self.tree.insert("", "end", values=(
                n, self._fmt(xn), self._fmt(fxn), self._fmt(dfxn), self._fmt(x_next), self._fmt(error)
            ))

        self.root_value.configure(text=self._fmt(root_value))
        self.error_value.configure(text=self._fmt(final_error) if final_error is not None else "—")
        self.iter_value.configure(text=str(len(rows)))
        self.status_var.set(("BERHASIL  ·  " if converged else "BELUM KONVERGEN  ·  ") + reason)

        self.ax.clear()
        self._style_axes()
        # Rentang grafik mengikuti tebakan awal dan hasil akar, dengan batas aman.
        left = min(rows[0][1], root_value) - max(2.0, abs(root_value - rows[0][1]) * 0.35)
        right = max(rows[0][1], root_value) + max(2.0, abs(root_value - rows[0][1]) * 0.35)
        xs = np.linspace(left, right, 600)
        try:
            with np.errstate(all="ignore"):
                ys = np.asarray(f(xs), dtype=float)
            if ys.ndim == 0:
                ys = np.full_like(xs, float(ys))
            ys = np.where(np.isfinite(ys), ys, np.nan)
            self.ax.plot(xs, ys, color=ACCENT, linewidth=2.2, label="f(x)")
            self.ax.scatter([root_value], [0], color=GREEN, s=55, zorder=5, label=f"Akar ≈ {self._fmt(root_value)}")
            self.ax.axvline(root_value, color=GREEN, linewidth=1, linestyle="--", alpha=0.6)
            self.ax.legend(facecolor=PANEL, edgecolor="#39465d", labelcolor=TEXT, fontsize=8)
            self.ax.set_title(f"f(x) = {sp.sstr(function)}", pad=10)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.set_xlim(left, right)
            self.figure.tight_layout()
            self.canvas.draw_idle()
        except (ValueError, TypeError, OverflowError):
            self.ax.set_title("Grafik tidak dapat ditampilkan untuk rentang ini", pad=10)
            self.figure.tight_layout()
            self.canvas.draw_idle()

    def reset(self):
        self.function_var.set("x^2 - 4")
        self.x0_var.set("3")
        self.tol_var.set("0.000001")
        self.max_iter_var.set("50")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.root_value.configure(text="—")
        self.error_value.configure(text="—")
        self.iter_value.configure(text="—")
        self.status_var.set("Masukkan parameter lalu klik Hitung akar.")
        self._draw_empty_graph()


def main():
    root = tk.Tk()
    NewtonRaphsonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
