% health.pl
symptom(fever).
symptom(cough).
symptom(headache).

disease(flu) :- has(fever), has(cough).
disease(cold) :- has(cough).
disease(migraine) :- has(headache).
