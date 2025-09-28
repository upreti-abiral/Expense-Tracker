# db.py
import sqlite3
from datetime import datetime

class ExpenseDB:
    def __init__(self, path="expenses.db"):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            );
        ''')
        self.conn.commit()

    def add_expense(self, amount, category, date=None, description=""):
        if date is None or date.strip() == "":
            date = datetime.today().strftime("%Y-%m-%d")
        c = self.conn.cursor()
        c.execute('INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
                  (date, category, float(amount), description))
        self.conn.commit()
        return c.lastrowid

    def delete_expense(self, expense_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.conn.commit()

    def get_expenses(self, start_date=None, end_date=None, limit=1000):
        c = self.conn.cursor()
        query = 'SELECT * FROM expenses'
        params = []
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        elif start_date:
            query += ' WHERE date >= ?'
            params.append(start_date)
        elif end_date:
            query += ' WHERE date <= ?'
            params.append(end_date)
        query += ' ORDER BY date DESC LIMIT ?'
        params.append(limit)
        c.execute(query, params)
        return [dict(row) for row in c.fetchall()]

    def get_sum_by_category(self, start_date=None, end_date=None):
        c = self.conn.cursor()
        query = 'SELECT category, SUM(amount) as total FROM expenses'
        params = []
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        query += ' GROUP BY category ORDER BY total DESC'
        c.execute(query, params)
        return {row['category']: row['total'] for row in c.fetchall()}

    def get_daily_totals(self, days=30):
        c = self.conn.cursor()
        # SQLite: date("now", "-N days")
        c.execute('''
            SELECT date, SUM(amount) as total FROM expenses
            WHERE date >= date("now", ?)
            GROUP BY date ORDER BY date ASC
        ''', (f"-{days} days",))
        return {row['date']: row['total'] for row in c.fetchall()}

    def close(self):
        self.conn.close()
