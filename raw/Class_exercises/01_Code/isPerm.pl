isPerm(X, Y) :- isInc(X, Y), isInc(Y, X).

isInc([], Y).
isInc([X|XS],Y) :- isMember(X, Y), isInc(XS, Y).

isMember(X, [X|XS]).
isMember(X, [Y|XS]) :- isMember(X, XS).