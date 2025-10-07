from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "learning_platform"    
        )


@app.route('/users', methods = ["POST"])
def create_user():
    data = request.json
    conn= get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
               (data["name"],data["email"],data["password"]))
    conn.commit()
    conn.close()
    return jsonify ({"message":"User cretaed succesdully"}),201

@app.route("/courses",methods  = ["POST"])
def create_course():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (titles,description) VALUES(%s,%s,%s)",
               (data["titles"],data["description"]))
    conn.commit()
    conn.close()
    return jsonify ({"message": "course created"}),201

@app.route("/enroll",methods  = ["POST"])
def enroll_courses():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO enrollment (user_id,course_id) VALUES(%s,%s,%s)",
               (data["user_id"],data["course_id"]))
    conn.commit()
    conn.close()
    return jsonify ({"message": "enrolled succesfully"}),201

@app.route("/progress",methods  = ["POST"])
def update_progress():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO progress (USER_id,course_id,progress_precent) VALUES(%s,%s,%s)",
               "ON DUPLICATE KEY UPDATE progress_percent=%s",
               (data["title"],data["description"]))
    conn.commit()
    conn.close()
    return jsonify ({"message": "course created"})

@app.route("/quizzes",methods  = ["POST"])
def add_quiz():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO quizzes (course_id,question,answer) VALUES(%s,%s,%s)",
               (data["course_id"],data["question"],data["answer"]))
    conn.commit()
    conn.close()
    return jsonify ({"message": "quiz added"}),201

@app.route('/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    conn.close()
    return jsonify(courses)

@app.route('/progress/<int:user_id>', methods=['GET'])
def get_user_progress(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM progress WHERE user_id = %s", (user_id,))
    progress = cur.fetchall()
    conn.close()
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True)