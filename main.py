import sqlite3
from fastmcp import FastMCP
import os

mcp = FastMCP(name="expense tracker server")


sql_path = os.path.join(
    r"C:\Users\HP\OneDrive\Desktop\Expense Tracker MCP Server",
    "expense.db"
)


def init_db():
    with sqlite3.connect(sql_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                spent REAL,
                date TEXT,
                note TEXT
            )
            """
        )


init_db()


@mcp.tool
def add_expense(item, category, subcategory, spent, date, note):
    """Add a new expense"""
    with sqlite3.connect(sql_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO Expenses (item, category, subcategory, spent, date, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (item, category, subcategory, spent, date, note)
        )
        return {"status": "success", "id": cur.lastrowid}


@mcp.tool
def search_expense(item, category=None, subcategory=None, date=None):
    """Search expense ID based on filters"""

    query = "SELECT id FROM Expenses WHERE item = ?"
    params = [item]

    if category:
        query += " AND category = ?"
        params.append(category)

    if subcategory:
        query += " AND subcategory = ?"
        params.append(subcategory)

    if date:
        query += " AND date = ?"
        params.append(date)

    with sqlite3.connect(sql_path) as conn:
        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool
def update_expense(id, new_item=None, new_spent=None):
    """Update expense item or amount"""

    updates = []
    params = []

    if new_item:
        updates.append("item = ?")
        params.append(new_item)

    if new_spent:
        updates.append("spent = ?")
        params.append(new_spent)

    if not updates:
        return {"status": "nothing to update"}

    query = f"UPDATE Expenses SET {', '.join(updates)} WHERE id = ?"
    params.append(id)

    with sqlite3.connect(sql_path) as conn:
        conn.execute(query, params)
        return {"status": "success", "id": id}


@mcp.tool
def delete_expense(id):
    """Delete expense by ID"""

    with sqlite3.connect(sql_path) as conn:
        conn.execute("DELETE FROM Expenses WHERE id = ?", (id,))
        return {"status": "success", "id": id}


@mcp.tool()
def summarize(start_date, end_date, category=None):
    """Summarize expenses by category"""

    query = """
        SELECT category, SUM(spent) AS total_amount
        FROM Expenses
        WHERE date BETWEEN ? AND ?
    """
    params = [start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " GROUP BY category ORDER BY category ASC"

    with sqlite3.connect(sql_path) as conn:
        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


if __name__ == "__main__":
    mcp.run()