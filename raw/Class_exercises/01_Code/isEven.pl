isEven([], 'true').
isEven([X|XS], Y) :- isOdd(XS, Y).

isOdd([],'false').
isOdd([Y|YS], Z) :- isEven(YS, Z).