from tkinter import *
from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()
prolog.consult("health.pl")

# Symptoms we’ll ask about
questions = [
    ("Do you have a fever?", "fever"),
    ("Do you have a cough?", "cough"),
    ("Do you have a headache?", "headache"),
    ("Do you feel tired?", "tiredness")
]

answers = {}  # store yes/no answers

# --- Logic ---
def next_question():
    global current_question
    if current_question < len(questions):
        q_text, _ = questions[current_question]
        label_question.config(text=q_text)
    else:
        diagnose()

def record_answer(answer):
    global current_question
    # Get symptom name
    _, symptom = questions[current_question]
    answers[symptom] = answer

    # Assert facts if "yes"
    if answer == "yes":
        prolog.assertz(f"has({symptom})")

    current_question += 1
    next_question()

def diagnose():
    label_question.config(text="Analyzing your symptoms...")
    yes_button.pack_forget()
    no_button.pack_forget()

    diseases = list(prolog.query("disease(D)."))
    if diseases:
        result_text = "\n".join([f"✅ You might have {d['D']}." for d in diseases])
    else:
        result_text = "❌ No matching disease found."
    
    label_result.config(text=result_text)
    label_result.pack(pady=10)
    restart_button.pack(pady=10)

def restart():
    global current_question, answers
    answers = {}
    for fact in list(prolog.query("has(_)")):
        # Clean old facts
        prolog.retract(f"has({fact['_']})")
    current_question = 0
    label_result.pack_forget()
    yes_button.pack(pady=5)
    no_button.pack(pady=5)
    next_question()

# --- GUI Setup ---
root = Tk()
root.title("Simple Health Expert System")
root.geometry("400x300")

label_title = Label(root, text="Health Diagnosis Expert System", font=("Arial", 14, "bold"))
label_title.pack(pady=10)

label_question = Label(root, text="", font=("Arial", 12))
label_question.pack(pady=10)

yes_button = Button(root, text="YES", width=10, command=lambda: record_answer("yes"))
no_button = Button(root, text="NO", width=10, command=lambda: record_answer("no"))

yes_button.pack(pady=5)
no_button.pack(pady=5)

label_result = Label(root, text="", font=("Arial", 12), fg="blue")
restart_button = Button(root, text="Restart", width=10, command=restart)

current_question = 0
next_question()

root.mainloop()
