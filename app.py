# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import ExpenseDB

# Matplotlib for charts inside Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ExpenseTracker")
        self.geometry("900x600")
        self.db = ExpenseDB()
        self._create_widgets()
        self.refresh_expense_table()
        self.draw_charts()

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._create_add_tab()
        self._create_view_tab()
        self._create_charts_tab()

    def _create_add_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Add Expense")

        pad = {'padx': 6, 'pady': 6}

        ttk.Label(add_frame, text="Amount (e.g., 12.50):").grid(row=0, column=0, sticky="w", **pad)
        self.amount_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.amount_var).grid(row=0, column=1, **pad)

        ttk.Label(add_frame, text="Category:").grid(row=1, column=0, sticky="w", **pad)
        self.category_var = tk.StringVar()
        categories = ["Food", "Transport", "Shopping", "Bills", "Study", "Other"]
        ttk.Combobox(add_frame, textvariable=self.category_var, values=categories).grid(row=1, column=1, **pad)
        self.category_var.set(categories[0])

        ttk.Label(add_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", **pad)
        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        ttk.Entry(add_frame, textvariable=self.date_var).grid(row=2, column=1, **pad)

        ttk.Label(add_frame, text="Description:").grid(row=3, column=0, sticky="nw", **pad)
        self.desc_text = tk.Text(add_frame, width=40, height=4)
        self.desc_text.grid(row=3, column=1, **pad)

        add_btn = ttk.Button(add_frame, text="Add Expense", command=self.add_expense)
        add_btn.grid(row=4, column=1, sticky="e", pady=(10, 0), padx=6)

        self.add_status = ttk.Label(add_frame, text="")
        self.add_status.grid(row=5, column=0, columnspan=2, sticky="w", **pad)

    def _create_view_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Expenses")

        top_frame = ttk.Frame(view_frame)
        top_frame.pack(fill="x", padx=6, pady=6)

        refresh_btn = ttk.Button(top_frame, text="Refresh", command=self.refresh_expense_table)
        refresh_btn.pack(side="left", padx=(0, 8))

        delete_btn = ttk.Button(top_frame, text="Delete Selected", command=self.delete_selected)
        delete_btn.pack(side="left")

        cols = ("id", "date", "category", "amount", "description")
        self.tree = ttk.Treeview(view_frame, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

    def _create_charts_tab(self):
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="Charts")

        # Left: pie chart by category (last 30 days)
        left = ttk.Frame(chart_frame)
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        self.fig1 = Figure(figsize=(4,4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=left)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Right: bar chart of daily totals (last 30 days)
        right = ttk.Frame(chart_frame)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        self.fig2 = Figure(figsize=(6,4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

        refresh_charts_btn = ttk.Button(chart_frame, text="Refresh Charts", command=self.draw_charts)
        refresh_charts_btn.pack(side="bottom", pady=(0,8))

    def add_expense(self):
        amount = self.amount_var.get().strip()
        category = self.category_var.get().strip()
        date = self.date_var.get().strip()
        description = self.desc_text.get("1.0", "end").strip()

        # validate amount
        try:
            amt = float(amount)
            if amt <= 0:
                raise ValueError("Amount must be > 0")
        except Exception:
            self.add_status.config(text="❌ Invalid amount. Enter a number > 0.")
            return

        # validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            self.add_status.config(text="❌ Date must be YYYY-MM-DD")
            return

        self.db.add_expense(amt, category, date, description)
        self.add_status.config(text="✅ Expense added.")
        self.amount_var.set("")
        self.desc_text.delete("1.0", "end")
        self.refresh_expense_table()
        self.draw_charts()

    def refresh_expense_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.db.get_expenses(limit=1000)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["date"], r["category"], f"{r['amount']:.2f}", r["description"]))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select a row to delete.")
            return
        confirm = messagebox.askyesno("Confirm", "Delete selected expense(s)?")
        if not confirm:
            return
        for item in sel:
            vals = self.tree.item(item, "values")
            expense_id = vals[0]
            self.db.delete_expense(expense_id)
        self.refresh_expense_table()
        self.draw_charts()

    def draw_charts(self):
        # Pie chart
        data = self.db.get_sum_by_category()
        self.ax1.clear()
        if data:
            cats = list(data.keys())
            vals = list(data.values())
            self.ax1.pie(vals, labels=cats, autopct="%1.1f%%", startangle=140)
            self.ax1.set_title("Spending by Category (last 30 days)")
        else:
            self.ax1.text(0.5, 0.5, "No data yet", ha='center')
        self.canvas1.draw()

        # Bar chart
        daily = self.db.get_daily_totals(days=30)
        self.ax2.clear()
        if daily:
            s = pd.Series(daily)
            s.index = pd.to_datetime(s.index)
            s = s.sort_index()
            s.plot(kind='bar', ax=self.ax2)
            self.ax2.set_title("Daily Totals (last 30 days)")
            self.ax2.set_ylabel("Amount")
            self.ax2.tick_params(axis='x', rotation=45)
        else:
            self.ax2.text(0.5, 0.5, "No daily data", ha='center')
        self.canvas2.draw()

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
