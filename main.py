from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Генерацыя прыкладу
def generate_problem(level):
    if level == "easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif level == "medium":
        a, b = random.randint(10, 100), random.randint(10, 100)
    else:
        a, b = random.randint(100, 1000), random.randint(100, 1000)
    operation = random.choice(["+", "-"])
    answer = eval(f"{a} {operation} {b}")
    return {"question": f"{a} {operation} {b} = ?", "answer": answer}

current_problem = generate_problem("easy")

@app.route("/")
def index():
    return render_template("index.html", question=current_problem["question"])

@app.route("/check", methods=["POST"])
def check():
    global current_problem
    user_answer = request.json.get("answer", "")
    level = request.json.get("level", "easy")

    if str(user_answer) == str(current_problem["answer"]):
        current_problem = generate_problem(level)
        return jsonify({"result": "correct", "new_question": current_problem["question"]})
    else:
        return jsonify({"result": "wrong"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
