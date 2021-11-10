

and(X,Y) :- X,Y.
or(X,Y) :- X; Y.
impl(X,Y) :- X -> Y.
equ(X,Y) :- X==Y.
evaluate(E, true) :- E, !.
evaluate(_, false).
bool(true).
bool(false).

table(X,Y,Z,Expression) :-
	bool(X),
  	bool(Y),
  	bool(Z),
	write(X),
  	write(' \t '),
  	write(Y),
  	write(' \t '),
  	write(Z),
  	write(' \t '),
  	evaluate(Expression, Result),
  	write(Result), nl, fail.
	
