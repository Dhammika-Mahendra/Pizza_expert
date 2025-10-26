% family.pl
parent(john, mary).
parent(mary, susan).
parent(john, bob).

male(john).
female(mary).
female(susan).
male(bob).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
