# db.py
import sqlite3

class ExpenseDB:
    def __init__(self, db_name="expenses.db"):
        # row_factory lets us fetch rows as dictionaries
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        # Create table if not exists
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL,
            description TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

        # ✅ Ensure category column exists (old DBs might not have it)
        try:
            self.conn.execute("SELECT category FROM expenses LIMIT 1;")
        except sqlite3.OperationalError:
            self.conn.execute("ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT 'Other';")
            self.conn.commit()

        # ✅ Ensure description column exists
        try:
            self.conn.execute("SELECT description FROM expenses LIMIT 1;")
        except sqlite3.OperationalError:
            self.conn.execute("ALTER TABLE expenses ADD COLUMN description TEXT DEFAULT '';")
            self.conn.commit()

    def add_expense(self, amount, category, date, description):
        query = "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?);"
        self.conn.execute(query, (amount, category, date, description))
        self.conn.commit()

    def view_expenses(self):
        query = "SELECT * FROM expenses;"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def get_expenses(self, limit=None):
        query = "SELECT * FROM expenses ORDER BY date DESC"
        if limit:
            query += f" LIMIT {limit}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_expense(self, expense_id):
        query = "DELETE FROM expenses WHERE id = ?;"
        self.conn.execute(query, (expense_id,))
        self.conn.commit()

    def get_sum_by_category(self, days=30):
        query = """
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE date >= date('now', ?)
        GROUP BY category;
        """
        cursor = self.conn.execute(query, (f"-{days} days",))
        return {row["category"]: row["total"] for row in cursor.fetchall()}

    def get_daily_totals(self, days=30):
        query = """
        SELECT date, SUM(amount) as total
        FROM expenses
        WHERE date >= date('now', ?)
        GROUP BY date
        ORDER BY date ASC;
        """
        cursor = self.conn.execute(query, (f"-{days} days",))
        return {row["date"]: row["total"] for row in cursor.fetchall()}

    def close(self):
        self.conn.close()
