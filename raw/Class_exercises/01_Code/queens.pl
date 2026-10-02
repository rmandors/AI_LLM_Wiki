queens(N, Qs) :-
    range(1, N, Ns),
    queens(Ns, [], Qs).

queens([], Qs, Qs).
queens(UnplacedQs, SafeQs, Qs) :-
    select(Q, UnplacedQs, NewUnplaced),
    \+ threat(Q, SafeQs),
    queens(NewUnplaced, [Q|SafeQs], Qs).

threat(X, Xs) :- threat(X, 1, Xs).
threat(X, N, [Y|_Ys]) :-
    X is Y + N;
    X is Y - N.
threat(X, N, [_Y|Ys]) :-
    N1 is N + 1,
    threat(X, N1, Ys).

range(M, N, [M|Ns]) :-
    M < N,
    M1 is M + 1,
    range(M1, N, Ns).
range(N, N, [N]).