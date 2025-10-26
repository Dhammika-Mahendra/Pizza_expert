from pyswip import Prolog

# Initialize Prolog engine
prolog = Prolog()

# Load your knowledge base
prolog.consult("health.pl")

print("Welcome to the simple health expert system!")
print("---------------------------------------------")

# Ask user questions
fever = input("Do you have a fever? (yes/no): ").strip().lower()
cough = input("Do you have a cough? (yes/no): ").strip().lower()
headache = input("Do you have a headache? (yes/no): ").strip().lower()

# Assert facts based on user input
if fever == "yes":
    prolog.assertz("has(fever)")
if cough == "yes":
    prolog.assertz("has(cough)")
if headache == "yes":
    prolog.assertz("has(headache)")

# Query Prolog for possible disease
print("\nChecking possible diagnosis...\n")

for sol in prolog.query("disease(D)."):
    print(f"✅ You might have {sol['D']}.")

# If nothing matched
if not list(prolog.query("disease(_)")):
    print("❌ No matching disease found.")

print("\nThank you for using the expert system!")
