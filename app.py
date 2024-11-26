from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'hw12.db'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Fetch all students
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()

    # Fetch all quizzes
    cur.execute('SELECT * FROM quizzes')
    quizzes = cur.fetchall()

    conn.close()

    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form.get('subject')
        num_questions = request.form.get('num_questions')
        quiz_date = request.form.get('quiz_date')

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                    (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_quiz.html')

@app.route('/student/<int:id>')
def view_results(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''
        SELECT quizzes.subject, results.score
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    ''', (id,))
    results = cur.fetchall()

    cur.execute('SELECT first_name, last_name FROM students WHERE id = ?', (id,))
    student = cur.fetchone()

    conn.close()

    if not results:
        return f"No results found for {student[0]} {student[1]}."

    return render_template('view_results.html', student=student, results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        quiz_id = request.form.get('quiz_id')
        score = request.form.get('score')

        cur.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                    (student_id, quiz_id, score))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    cur.execute('SELECT * FROM students')
    students = cur.fetchall()

    cur.execute('SELECT * FROM quizzes')
    quizzes = cur.fetchall()

    conn.close()

    return render_template('add_result.html', students=students, quizzes=quizzes)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
