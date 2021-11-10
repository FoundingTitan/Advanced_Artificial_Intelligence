


word(apastosaurus,a,p,a,t,o,s,a,u,r,u,s).
word(bones,b,o,n,e,s).
word(eggs,e,g,g,s).
word(extinct,e,x,t,i,n,c,t).
word(claws,c,l,a,w,s).
word(fossil,f,o,s,s,i,l).
word(raptor,r,a,p,t,o,r).
word(teeth,t,e,e,t,h).
word(triassic,t,r,i,a,s,s,i,c).
word(triceratops,t,r,i,c,e,r,a,t,o,p,s).

%% Crossword Solver
	
% Implementation of the Dinosaur crossword

% crossword is true if A,B,C,D,E,F,G,H,I,J
% 	are all words that fulfill the constrains
% 	of this crossword puzzle
crossword(A,B,C,D,E,F,G,H,I,J):-
	word(A, _, N1, _, _, N4, _, _, _, _, _, N10),
	word(B, _, _, _, N10),
	word(C, N1, _, _, _, _, _),
	word(D, N4, _, _, _, _, _, N0),
	word(E, N0, _, _, N3, _, _, _, N7),
	word(F, N3, _, _, F3, _, _, _, _, _, _, F10),
	word(G, N7, _, _, _, _),
	word(H, _, _, _, F3, _),
	word(I, _, I1, _, _, _),
	word(J, _, I1, _, F10, _, _).