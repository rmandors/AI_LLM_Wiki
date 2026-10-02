% family.pl -- the knowledge base used in the Prolog lecture
% (slides "Anatomy of a Prolog Program" and "Querying the Knowledge Base")
%
%   ?- consult('family.pl').        % or just:  ?- [family].

% AI helped with this 2 following lines: 
:- use_module(library(plunit)).         % to be able to run the tests.
:- set_test_options([format(log)]).     % to see the full run_tests listing.


% ---- facts ------------------------------------------------------------

male(hector).   male(pedro).    male(luis).     male(juan).
male(andres).   male(carlos).   male(diego).    male(mateo).

female(carmen). female(ana).    female(maria).  female(rosa).
female(sofia).  female(elena).  female(lucia).  female(valentina).

spouse(hector, carmen).  spouse(carmen, hector).
spouse(ana, pedro).      spouse(pedro, ana).
spouse(luis, maria).     spouse(maria, luis).
spouse(rosa, juan).      spouse(juan, rosa).
spouse(sofia, andres).   spouse(andres, sofia).
spouse(carlos, elena).   spouse(elena, carlos).

% Gen 1 -> Gen 2  
parent(hector, ana).     parent(carmen, ana).
parent(hector, luis).    parent(carmen, luis).
parent(hector, rosa).    parent(carmen, rosa).

% Gen 2 -> Gen 3
parent(ana,    sofia).   parent(pedro,  sofia).
parent(ana,    carlos).  parent(pedro,  carlos).
parent(luis,   diego).   parent(maria,  diego).

% Gen 3 -> Gen 4
parent(sofia,  lucia).   parent(andres, lucia).
parent(sofia,  mateo).   parent(andres, mateo).
parent(carlos, valentina). parent(elena, valentina).


% ---- rules ------------------------------------------------------------

mother(X, Y) :- parent(X, Y), female(X).

father(X, Y) :- parent(X, Y), male(X).

sibling(X, Y) :-
    father(F, X), father(F, Y),
    mother(M, X), mother(M, Y),
    X \= Y.

sister(X, Y) :- sibling(X, Y), female(X).

brother(X, Y) :- sibling(X, Y), male(X).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).

grandmother(X, Z) :- grandparent(X, Z), female(X).

uncle(X, Y) :-
    parent(P, Y),
    brother(X, P).
uncle(X, Y) :-
    parent(P, Y),
    sister(S, P),
    spouse(X, S),
    male(X).

aunt(X, Y) :-
    parent(P, Y),
    sister(X, P).
aunt(X, Y) :-
    parent(P, Y),
    brother(B, P),
    spouse(X, B),
    female(X).

cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY).

father_in_law(X, Y) :-
    spouse(Y, S),
    father(X, S).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% Recursive, D is a descendant of A.
descendant(D, A) :- parent(A, D).
descendant(D, A) :- parent(A, Z), descendant(D, Z).

person(P) :- male(P).
person(P) :- female(P).

related(X, Y) :-
    person(X),
    reachable(X, Y, [X]).

reachable(X, X, _).
reachable(X, Y, Visited) :-
    family_link(X, Z),
    \+ memberchk(Z, Visited),
    reachable(Z, Y, [Z|Visited]).

family_link(X, Y) :- parent(X, Y).
family_link(X, Y) :- parent(Y, X).
family_link(X, Y) :- spouse(X, Y).


% ---- tests ------------------------------------------------------------

:- begin_tests(family).

test(mother_carmen_ana) :-
    mother(carmen, ana).

test(sister_ana_of_luis) :-
    once(sister(ana, luis)).

test(grandmother_carmen_sofia) :-
    once(grandmother(carmen, sofia)).

test(uncle_luis_of_sofia) :-
    once(uncle(luis, sofia)).

test(cousin_sofia_diego) :-
    once(cousin(sofia, diego)).

test(father_in_law_hector_pedro) :-
    father_in_law(hector, pedro).

test(descendant_recursive_four_generations) :-
    once(descendant(lucia, hector)).

test(aunt_rosa_of_sofia) :-
    once(aunt(rosa, sofia)).

test(father_hector_ana) :-
    father(hector, ana).

test(sibling_ana_luis) :-
    once(sibling(ana, luis)).

test(ancestor_hector_lucia) :-
    once(ancestor(hector, lucia)).

test(nobody_is_own_sibling, [fail]) :-
    sibling(X, X).

test(rosa_has_no_children, [fail]) :-
    parent(rosa, _).

test(diego_has_no_children, [fail]) :-
    parent(diego, _).

test(hector_is_not_mother, [fail]) :-
    mother(hector, ana).

test(luis_is_not_sister_of_ana, [fail]) :-
    sister(luis, ana).

test(siblings_are_not_cousins, [fail]) :-
    cousin(sofia, carlos).

test(related_parent_child_terminates) :-
    once(related(ana, hector)).

test(related_by_marriage_across_tree) :-
    once(related(juan, valentina)).

test(not_related_to_stranger, [fail]) :-
    related(hector, stranger).

:- end_tests(family).


% ---- try these --------------------------------------------------------
%   ?- parent(hector, Who).
%   ?- grandmother(G, sofia).
%   ?- uncle(U, lucia).
%   ?- cousin(lucia, C).
%   ?- descendant(D, hector).
%   ?- related(ana, hector).
%   ?- related(juan, valentina).
%   ?- run_tests.