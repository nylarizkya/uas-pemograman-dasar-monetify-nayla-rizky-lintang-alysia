import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


class FinanceTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Finance Tracker — Monetify")
        self.master.configure(bg="#ffeef7")

        self.transactions = []

        # ------------------- HEADER -------------------
        title = tk.Label(
            master,
            text="💰Monetify — Finance Tracker",
            font=("Poppins", 26, "bold"),
            bg="#ffeef7",
            fg="#6d5dfc"
        )
        title.pack(pady=5)

        subtitle = tk.Label(
            master,
            text="by Nayla Rizky Amalia & Lintang Alysia Gantari",
            font=("Arial", 16),
            bg="#ffeef7",
            fg="#6d5dfc"
        )
        subtitle.pack(pady=3)

        # ------------------- MAIN CONTAINER -------------------
        main_layout = tk.Frame(master, bg="#ffeef7")
        main_layout.pack(fill="both", expand=True)

        left_side = tk.Frame(main_layout, bg="#ffeef7")
        left_side.pack(side="left", fill="both", expand=True)

        right_side = tk.Frame(main_layout, bg="#ffeef7")
        right_side.pack(side="right", fill="y")

        # ------------------- INPUT FRAME -------------------
        input_frame = tk.LabelFrame(
            left_side,
            text="Tambah Transaksi",
            padx=10,
            pady=10,
            bg="#f7e9ff",
            font=("Poppins", 16, "bold")
        )
        input_frame.pack(padx=10, pady=5, fill="x")

        self.type_var = tk.StringVar(value="Pemasukan")
        ttk.Combobox(
            input_frame,
            textvariable=self.type_var,
            values=["Pemasukan", "Pengeluaran"],
            width=15, state="readonly"
        ).grid(row=0, column=0, padx=5, pady=5)

        # ---- Deskripsi Entry ----
        self.desc_entry = tk.Entry(input_frame, width=25, font=("Poppins", 12), fg="grey")
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)
        self.desc_entry.insert(0, "Deskripsi")
        self.desc_entry.bind("<FocusIn>", self.clear_placeholder_desc)
        self.desc_entry.bind("<FocusOut>", self.add_placeholder_desc)

        # ---- Jumlah Entry ----
        self.amount_entry = tk.Entry(input_frame, width=15, font=("Poppins", 12), fg="grey")
        self.amount_entry.grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry.insert(0, "Jumlah (Rp)")
        self.amount_entry.bind("<FocusIn>", self.clear_placeholder_amount)
        self.amount_entry.bind("<FocusOut>", self.add_placeholder_amount)

        self.category_var = tk.StringVar(value="Lainnya")
        ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=["Jajan", "Transport", "Tagihan", "Hiburan", "Gaji", "Uang Saku", "Hadiah", "Lainnya"],
            width=15, state="readonly"
        ).grid(row=0, column=3, padx=5, pady=5)

        tk.Button(
            input_frame,
            text="Simpan",
            command=self.add_transaction,
            bg="#fcbad3",
            fg="black",
            width=12,
            font=("Poppins", 12)
        ).grid(row=0, column=4, padx=5, pady=5)

        tk.Button(
            input_frame,
            text="Bersihkan",
            command=self.clear_all,
            bg="#bde0fe",
            fg="black",
            width=12,
            font=("Poppins", 12)
        ).grid(row=0, column=5, padx=5, pady=5)

        # ------------------- BALANCE FRAME -------------------
        balance_frame = tk.Frame(left_side, bg="#ffbed3")
        balance_frame.pack(pady=10)

        self.income_label = tk.Label(
            balance_frame,
            text="Pemasukan: Rp 0",
            font=("Poppins", 15),
            bg="#ffbed3"
        )
        self.income_label.grid(row=0, column=0, padx=25)

        self.expense_label = tk.Label(
            balance_frame,
            text="Pengeluaran: Rp 0",
            font=("Poppins", 15),
            bg="#ffbed3"
        )
        self.expense_label.grid(row=0, column=1, padx=25)

        self.balance_label = tk.Label(
            balance_frame,
            text="Sisa Tabungan: Rp 0",
            font=("Poppins", 15, "bold"),
            bg="#ffbed3",
            fg="#444"
        )
        self.balance_label.grid(row=0, column=2, padx=25)

        # ------------------- LIST FRAME -------------------
        list_frame = tk.LabelFrame(
            left_side,
            text="Daftar Transaksi",
            bg="#ffbed3",
            font=("Poppins", 16, "bold")
        )
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Tipe", "Deskripsi", "Jumlah", "Kategori"),
            show="headings"
        )
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins", 12, "bold"))
        style.configure("Treeview", font=("Poppins", 14), rowheight=35)

        for col in ("Tipe", "Deskripsi", "Jumlah", "Kategori"):
            self.tree.heading(col, text=col)

        self.tree.column("Tipe", anchor="center", width=130)
        self.tree.column("Deskripsi", anchor="center", width=300)
        self.tree.column("Jumlah", anchor="center", width=200)
        self.tree.column("Kategori", anchor="center", width=170)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # ------------------- BUTTONS -------------------
        export_frame = tk.Frame(left_side, bg="#ffeef7")
        export_frame.pack(pady=5)

        tk.Button(
            export_frame,
            text="Hapus Transaksi Terpilih",
            command=self.delete_selected,
            bg="#ffb4c6",
            fg="black",
            width=20,
            font=("Poppins", 12, "bold")
        ).pack(side="left", padx=6)

        tk.Button(
            export_frame,
            text="Export ke PDF",
            command=self.export_pdf,
            bg="#fcbad3",
            fg="black",
            width=12,
            font=("Poppins", 12, "bold")
        ).pack(side="left", padx=6)

        # ------------------- CHART FRAME -------------------
        charts_container = tk.Frame(right_side, bg="#ffeef7")
        charts_container.pack(fill="both", expand=True, padx=10)

        top_chart = tk.LabelFrame(
            charts_container,
            text="Diagram Pemasukan (%)",
            bg="#f7e9ff",
            font=("Poppins", 16, "bold")
        )
        top_chart.pack(fill="both", expand=True, padx=5, pady=8)

        self.fig_income, self.ax_income = plt.subplots(figsize=(5.8, 4.5), dpi=100)
        self.canvas_income = FigureCanvasTkAgg(self.fig_income, master=top_chart)
        self.canvas_income.get_tk_widget().pack(fill="both", expand=True)

        bottom_chart = tk.LabelFrame(
            charts_container,
            text="Diagram Pengeluaran (%)",
            bg="#f7e9ff",
            font=("Poppins", 16, "bold")
        )
        bottom_chart.pack(fill="both", expand=True, padx=5, pady=8)

        self.fig_expense, self.ax_expense = plt.subplots(figsize=(5.8, 4.5), dpi=100)
        self.canvas_expense = FigureCanvasTkAgg(self.fig_expense, master=bottom_chart)
        self.canvas_expense.get_tk_widget().pack(fill="both", expand=True)

        self.draw_empty_charts()

    # -------- PLACEHOLDER --------
    def clear_placeholder_desc(self, event):
        if self.desc_entry.get() == "Deskripsi":
            self.desc_entry.delete(0, "end")
            self.desc_entry.config(fg="black")

    def clear_placeholder_amount(self, event):
        if self.amount_entry.get() == "Jumlah (Rp)":
            self.amount_entry.delete(0, "end")
            self.amount_entry.config(fg="black")

    def add_placeholder_desc(self, event):
        if self.desc_entry.get().strip() == "":
            self.desc_entry.insert(0, "Deskripsi")
            self.desc_entry.config(fg="grey")

    def add_placeholder_amount(self, event):
        if self.amount_entry.get().strip() == "":
            self.amount_entry.insert(0, "Jumlah (Rp)")
            self.amount_entry.config(fg="grey")

    def draw_empty_charts(self):
        self.ax_income.clear()
        self.ax_expense.clear()
        self.ax_income.pie([1], labels=["Belum ada data"])
        self.ax_expense.pie([1], labels=["Belum ada data"])
        self.canvas_income.draw()
        self.canvas_expense.draw()

    def add_transaction(self):
        tipe = self.type_var.get()
        desc = self.desc_entry.get().strip()
        kategori = self.category_var.get().strip()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return

        if desc == "Deskripsi" or not desc or amount <= 0:
            messagebox.showwarning("Peringatan", "Isi deskripsi dan jumlah dengan benar!")
            return

        self.transactions.append({"type": tipe, "desc": desc, "amount": amount, "cat": kategori})
        self.tree.insert("", "end", values=(tipe, desc, f"Rp {amount:,.0f}", kategori))

        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, "Deskripsi")
        self.desc_entry.config(fg="grey")

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, "Jumlah (Rp)")
        self.amount_entry.config(fg="grey")

        self.update_summary()
        self.plot_charts()

    def update_summary(self):
        income = sum(t["amount"] for t in self.transactions if t["type"] == "Pemasukan")
        expense = sum(t["amount"] for t in self.transactions if t["type"] == "Pengeluaran")
        balance = income - expense
        self.income_label.config(text=f"Pemasukan: Rp {income:,.0f}")
        self.expense_label.config(text=f"Pengeluaran: Rp {expense:,.0f}")
        self.balance_label.config(text=f"Sisa Tabungan: Rp {balance:,.0f}")

    def plot_charts(self):
        self.ax_income.clear()
        pemasukan = {}
        for t in self.transactions:
            if t["type"] == "Pemasukan":
                pemasukan[t["cat"]] = pemasukan.get(t["cat"], 0) + t["amount"]

        if pemasukan:
            self.ax_income.pie(pemasukan.values(), labels=pemasukan.keys(), autopct="%1.1f%%")
        else:
            self.ax_income.pie([1], labels=["Belum ada pemasukan"])
        self.canvas_income.draw()

        self.ax_expense.clear()
        pengeluaran = {}
        for t in self.transactions:
            if t["type"] == "Pengeluaran":
                pengeluaran[t["cat"]] = pengeluaran.get(t["cat"], 0) + t["amount"]

        if pengeluaran:
            self.ax_expense.pie(pengeluaran.values(), labels=pengeluaran.keys(), autopct="%1.1f%%")
        else:
            self.ax_expense.pie([1], labels=["Belum ada pengeluaran"])
        self.canvas_expense.draw()

    def clear_all(self):
        if messagebox.askyesno("Konfirmasi", "Hapus semua data transaksi?"):
            self.transactions.clear()
            for i in self.tree.get_children():
                self.tree.delete(i)
            self.update_summary()
            self.draw_empty_charts()

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang mau dihapus!")
            return

        if not messagebox.askyesno("Konfirmasi", "Hapus transaksi yang dipilih?"):
            return

        item = self.tree.item(selected_item)["values"]
        tipe, desc, jumlahStr, kategori = item
        jumlah = float(jumlahStr.replace("Rp ", "").replace(",", ""))

        for i, t in enumerate(self.transactions):
            if t["type"] == tipe and t["desc"] == desc and t["amount"] == jumlah and t["cat"] == kategori:
                del self.transactions[i]
                break

        self.tree.delete(selected_item)
        self.update_summary()
        self.plot_charts()

    def export_pdf(self):
        if not self.transactions:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diexport!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Simpan Laporan PDF"
        )

        if not file_path:
            return

        c = pdf_canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Laporan Keuangan - Monetify")

        y = height - 100
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Tipe")
        c.drawString(150, y, "Deskripsi")
        c.drawString(310, y, "Jumlah")
        c.drawString(400, y, "Kategori")

        c.setFont("Helvetica", 11)
        y -= 20

        for t in self.transactions:
            if y < 60:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 60
            c.drawString(50, y, t["type"])
            c.drawString(150, y, t["desc"][:25])
            c.drawString(310, y, f"Rp {t['amount']:,.0f}")
            c.drawString(400, y, t["cat"])
            y -= 18

        income = sum(t["amount"] for t in self.transactions if t["type"] == "Pemasukan")
        expense = sum(t["amount"] for t in self.transactions if t["type"] == "Pengeluaran")
        balance = income - expense

        y -= 20
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Total Pemasukan  : Rp {income:,.0f}")
        y -= 15
        c.drawString(50, y, f"Total Pengeluaran: Rp {expense:,.0f}")
        y -= 15
        c.drawString(50, y, f"Sisa Tabungan    : Rp {balance:,.0f}")

        c.save()
        messagebox.showinfo("Berhasil", "File PDF berhasil disimpan!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()
