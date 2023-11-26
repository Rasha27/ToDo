from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

# Database initialization
def create_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed BOOLEAN)''')
    conn.commit()
    conn.close()

create_table()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM tasks''')
    tasks = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    task_data = request.get_json()
    task = task_data.get('task')
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (task, completed) VALUES (?, ?)''', (task, False))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
