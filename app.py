import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from db import ExpenseDB

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("900x600")

        self.db = ExpenseDB()

        self.create_widgets()
        self.refresh_expense_table()
        self.draw_charts()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.create_add_tab()
        self.create_view_tab()
        self.create_charts_tab()

    def create_add_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Expense")

        padding = {"padx": 6, "pady": 6}

        ttk.Label(
            frame,
            text="Amount:"
        ).grid(row=0, column=0, sticky="w", **padding)

        self.amount_var = tk.StringVar()

        ttk.Entry(
            frame,
            textvariable=self.amount_var
        ).grid(row=0, column=1, **padding)

        ttk.Label(
            frame,
            text="Category:"
        ).grid(row=1, column=0, sticky="w", **padding)

        self.category_var = tk.StringVar()

        categories = [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Study",
            "Other"
        ]

        category_box = ttk.Combobox(
            frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly"
        )
        category_box.grid(row=1, column=1, **padding)
        self.category_var.set("Food")

        ttk.Label(
            frame,
            text="Date (YYYY-MM-DD):"
        ).grid(row=2, column=0, sticky="w", **padding)

        self.date_var = tk.StringVar(
            value=datetime.today().strftime("%Y-%m-%d")
        )

        ttk.Entry(
            frame,
            textvariable=self.date_var
        ).grid(row=2, column=1, **padding)

        ttk.Label(
            frame,
            text="Description:"
        ).grid(row=3, column=0, sticky="nw", **padding)

        self.desc_text = tk.Text(
            frame,
            width=40,
            height=4
        )
        self.desc_text.grid(row=3, column=1, **padding)

        ttk.Button(
            frame,
            text="Add Expense",
            command=self.add_expense
        ).grid(
            row=4,
            column=1,
            sticky="e",
            padx=6,
            pady=10
        )

        self.add_status = ttk.Label(frame, text="")
        self.add_status.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            **padding
        )

    def create_view_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="View Expenses")

        top_frame = ttk.Frame(frame)
        top_frame.pack(
            fill="x",
            padx=6,
            pady=6
        )

        ttk.Button(
            top_frame,
            text="Refresh",
            command=self.refresh_expense_table
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            top_frame,
            text="Delete Selected",
            command=self.delete_selected
        ).pack(side="left")

        columns = (
            "id",
            "date",
            "category",
            "amount",
            "description"
        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("description", width=350)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=6
        )

    def create_charts_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Charts")

        chart_frame = ttk.Frame(frame)
        chart_frame.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=6
        )

        left_frame = ttk.Frame(chart_frame)
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        self.figure1 = Figure(
            figsize=(4, 4),
            dpi=100
        )

        self.axis1 = self.figure1.add_subplot(111)

        self.canvas1 = FigureCanvasTkAgg(
            self.figure1,
            master=left_frame
        )

        self.canvas1.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        right_frame = ttk.Frame(chart_frame)
        right_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        self.figure2 = Figure(
            figsize=(6, 4),
            dpi=100
        )

        self.axis2 = self.figure2.add_subplot(111)

        self.canvas2 = FigureCanvasTkAgg(
            self.figure2,
            master=right_frame
        )

        self.canvas2.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            frame,
            text="Refresh Charts",
            command=self.draw_charts
        ).pack(pady=(0, 8))

    def add_expense(self):
        amount = self.amount_var.get().strip()
        category = self.category_var.get().strip()
        date = self.date_var.get().strip()
        description = self.desc_text.get("1.0", "end").strip()

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            self.add_status.config(
                text="Invalid amount. Enter a number greater than 0."
            )
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self.add_status.config(
                text="Invalid date. Use YYYY-MM-DD."
            )
            return

        self.db.add_expense(
            amount,
            category,
            date,
            description
        )

        self.add_status.config(
            text="Expense added."
        )

        self.amount_var.set("")
        self.desc_text.delete("1.0", "end")

        self.refresh_expense_table()
        self.draw_charts()

    def refresh_expense_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.db.get_expenses()

        for expense in expenses:
            self.tree.insert(
                "",
                "end",
                values=(
                    expense["id"],
                    expense["date"],
                    expense["category"],
                    f"{expense['amount']:.2f}",
                    expense["description"]
                )
            )

    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "No Selection",
                "Select an expense to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete the selected expense(s)?"
        )

        if not confirm:
            return

        for item in selected:
            expense_id = self.tree.item(
                item,
                "values"
            )[0]

            self.db.delete_expense(expense_id)

        self.refresh_expense_table()
        self.draw_charts()

    def draw_charts(self):
        category_data = self.db.get_sum_by_category()

        self.axis1.clear()

        if category_data:
            categories = list(category_data.keys())
            amounts = list(category_data.values())

            self.axis1.pie(
                amounts,
                labels=categories,
                autopct="%1.1f%%",
                startangle=140
            )

            self.axis1.set_title(
                "Spending by Category"
            )
        else:
            self.axis1.text(
                0.5,
                0.5,
                "No data yet",
                ha="center",
                va="center"
            )

        self.canvas1.draw()

        daily_data = self.db.get_daily_totals()

        self.axis2.clear()

        if daily_data:
            dates = list(daily_data.keys())
            amounts = list(daily_data.values())

            self.axis2.bar(
                dates,
                amounts
            )

            self.axis2.set_title(
                "Daily Spending"
            )

            self.axis2.set_ylabel(
                "Amount"
            )

            self.axis2.tick_params(
                axis="x",
                rotation=45
            )
        else:
            self.axis2.text(
                0.5,
                0.5,
                "No daily data",
                ha="center",
                va="center"
            )

        self.figure2.tight_layout()
        self.canvas2.draw()

    def close_app(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.protocol(
        "WM_DELETE_WINDOW",
        app.close_app
    )
    app.mainloop()
