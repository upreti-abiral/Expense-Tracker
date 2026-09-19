import sqlite3


class ExpenseDB:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
        """

        self.conn.execute(query)
        self.conn.commit()

    def add_expense(self, amount, category, date, description):
        query = """
        INSERT INTO expenses
        (amount, category, date, description)
        VALUES (?, ?, ?, ?)
        """

        self.conn.execute(
            query,
            (amount, category, date, description)
        )

        self.conn.commit()

    def get_expenses(self):
        query = """
        SELECT id, amount, category, date, description
        FROM expenses
        ORDER BY date DESC, id DESC
        """

        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_expense(self, expense_id):
        query = """
        DELETE FROM expenses
        WHERE id = ?
        """

        self.conn.execute(
            query,
            (expense_id,)
        )

        self.conn.commit()

    def get_sum_by_category(self, days=30):
        query = """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE date >= date('now', ?)
        GROUP BY category
        ORDER BY total DESC
        """

        cursor = self.conn.execute(
            query,
            (f"-{days} days",)
        )

        return {
            row["category"]: row["total"]
            for row in cursor.fetchall()
        }

    def get_daily_totals(self, days=30):
        query = """
        SELECT date, SUM(amount) AS total
        FROM expenses
        WHERE date >= date('now', ?)
        GROUP BY date
        ORDER BY date
        """

        cursor = self.conn.execute(
            query,
            (f"-{days} days",)
        )

        return {
            row["date"]: row["total"]
            for row in cursor.fetchall()
        }

    def close(self):
        self.conn.close()
