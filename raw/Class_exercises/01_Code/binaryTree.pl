member2(K, node(K, S, T)).
member2(K, node(N, S, T)) :- K < N, member2(K, S).
member2(K, node(N, S, T)) :- K > N, member2(K, T).

insert(N, empty, node(N, empty, empty)).
insert(N, node(K, empty, R), T) :- N < K, insert(N, empty, M), T = node(K, M, R).
insert(N, node(K, empty, R), T) :- N > K, insert(N, R, M), T = node(K, empty, M).
insert(N, node(K, L, empty), T) :- N < K, insert(N, L, M), T = node(K, M, empty).
insert(N, node(K, L, empty), T) :- N > K, insert(N, empty, M), T = node(K, L, M).
insert(N, node(K, L, R), T) :- N < K, insert(N, L, M), T = node(K, M, R).
insert(N, node(K, L, R), T) :- N > K, insert(N, R, M), T = node(K, L, M).

delete2(N, node(N, empty, empty), empty).
delete2(N, node(N, L, empty), L).
delete2(N, node(N, empty, R), R).
delete2(N, node(N, L, R), M) :- inOrderSuccesor(R, X), delete2(X, R, R2), M = node(X, L, R2).
delete2(N, node(K, L, R), T) :- N < K, delete2(N, L, M), T = node(K, M, R).
delete2(N, node(K, L, R), T) :- N > K, delete2(N, R, M), T = node(K, R, M).

inOrderSuccesor(node(K, empty, empty), K).
inOrderSuccesor(node(K, empty, R), K).
inOrderSuccesor(node(K, L, empty), X) :- inOrderSuccesor(L, X).
inOrderSuccesor(node(K, L, R), X) :- inOrderSuccesor(L, X).