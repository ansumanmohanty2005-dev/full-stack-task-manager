from flask import Flask, jsonify, request, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("tasks.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/tasks")
def get_tasks():
    status = request.args.get("status", "All")
    conn = get_db()
    if status in {"Pending", "Completed"}:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status=? ORDER BY id DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    priority = data.get("priority", "Medium")
    if not title:
        return jsonify({"error": "Title is required."}), 400
    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
        (title, description, priority)
    )
    conn.commit()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return jsonify(dict(task)), 201

@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM tasks WHERE id=?", (task_id,)
    ).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Task not found."}), 404

    title = str(data.get("title", existing["title"])).strip()
    description = str(data.get("description", existing["description"])).strip()
    priority = data.get("priority", existing["priority"])
    status = data.get("status", existing["status"])

    if not title:
        conn.close()
        return jsonify({"error": "Title is required."}), 400
    if priority not in {"Low", "Medium", "High"}:
        priority = existing["priority"]
    if status not in {"Pending", "Completed"}:
        status = existing["status"]

    conn.execute(
        "UPDATE tasks SET title=?, description=?, priority=?, status=? WHERE id=?",
        (title, description, priority, status, task_id)
    )
    conn.commit()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?", (task_id,)
    ).fetchone()
    conn.close()
    return jsonify(dict(task))

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "Task not found."}), 404
    return jsonify({"message": "Task deleted."})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
