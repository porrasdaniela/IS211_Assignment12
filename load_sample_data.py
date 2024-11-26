import sqlite3

def load_sample_data():
    with sqlite3.connect('hw12.db') as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (first_name, last_name) VALUES (?, ?)",
            ('John', 'Smith')
        )

        cursor.execute(
            "INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)",
            ('Python Basics', 5, '2015-02-05')
        )

        cursor.execute(
            "INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
            (1, 1, 85)
        )

        conn.commit()
        print("Sample data loaded successfully.")

if __name__ == '__main__':
    load_sample_data()