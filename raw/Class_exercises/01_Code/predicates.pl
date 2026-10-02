isEven([], 'true').
isEven([X|XS], Y) :- isOdd(XS, Y).

isOdd([],'false').
isOdd([Y|YS], Z) :- isEven(YS, Z).

isPerm(X, Y) :- isInc(X, Y), isInc(Y, X).

isInc([], Y).
isInc([X|XS],Y) :- isMember(X, Y), isInc(XS, Y).

isMember(X, [X|XS]).
isMember(X, [Y|XS]) :- isMember(X, XS).

isMerged([], [], []).
isMerged(L1, [], L3) :- isTail(L1, L3).
isMerged(L1, L2, []) :- isTail(L1, L2).
isMerged([X1|[X2|L1]],[X|L2], [Y|L3]) :- X=X1, Y=X2, isMerged(L1, L2, L3).

isTail([],[]).
isTail([X|XS], [Y|YS]) :- X=Y, isTail(XS, YS).