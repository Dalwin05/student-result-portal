from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Sample student result data
STUDENTS = [
    {"roll": "CS001", "name": "Arun Kumar",     "tamil": 88, "english": 76, "maths": 92, "science": 85, "social": 79},
    {"roll": "CS002", "name": "Priya Rajan",    "tamil": 91, "english": 83, "maths": 78, "science": 90, "social": 88},
    {"roll": "CS003", "name": "Karthik S",      "tamil": 72, "english": 69, "maths": 95, "science": 88, "social": 74},
    {"roll": "CS004", "name": "Meena Devi",     "tamil": 85, "english": 90, "maths": 67, "science": 74, "social": 82},
    {"roll": "CS005", "name": "Ravi Shankar",   "tamil": 60, "english": 55, "maths": 72, "science": 65, "social": 70},
    {"roll": "CS006", "name": "Lakshmi N",      "tamil": 95, "english": 88, "maths": 91, "science": 94, "social": 89},
    {"roll": "CS007", "name": "Suresh P",       "tamil": 78, "english": 74, "maths": 80, "science": 77, "social": 83},
    {"roll": "CS008", "name": "Divya M",        "tamil": 82, "english": 87, "maths": 74, "science": 80, "social": 76},
]

def calculate(student):
    subjects = ["tamil", "english", "maths", "science", "social"]
    total = sum(student[s] for s in subjects)
    avg = total / len(subjects)
    grade = "O" if avg >= 90 else "A+" if avg >= 80 else "A" if avg >= 70 else "B+" if avg >= 60 else "B" if avg >= 50 else "F"
    result = "PASS" if all(student[s] >= 35 for s in subjects) else "FAIL"
    return {**student, "total": total, "average": round(avg, 2), "grade": grade, "result": result}

@app.route("/")
def index():
    students = [calculate(s) for s in STUDENTS]
    return render_template("index.html", students=students)

@app.route("/student/<roll>")
def student_detail(roll):
    student = next((s for s in STUDENTS if s["roll"] == roll), None)
    if not student:
        return "Student not found", 404
    return render_template("detail.html", student=calculate(student))

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    students = [calculate(s) for s in STUDENTS if query in s["name"].lower() or query in s["roll"].lower()]
    return render_template("index.html", students=students, query=query)

@app.route("/health")
def health():
    return {"status": "ok", "service": "student-result-portal"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
