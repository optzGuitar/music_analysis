#include "interface.lp".

slot(1..patlenmax).
item(E) :- seq(T,P,E).
{ pat(X,E) : item(E) } 1 :- slot(X).

pos(X) :- pat(X,E).
:- not pos(1).
:- pos(X), X > 1, not pos(X-1).

occ(S,1,P) :- pat(1,I), seq(S,P,I).
occ(S,L,P) :- occ(S,L,P-1), seq(S,P,_).
occ(S,L,P) :- occ(S,L-1,P-1), seq(S,P,C), pat(L,C).

patlen(X) :- pat(X,_), not pat(X+1,_).
seqlen(S,L) :- seq(S,L,_), not seq(S,L+1,_).
support(S) :- occ(S,L,LS), patlen(L), seqlen(S,LS).
:- not minsup { support(T) }.
:- #count {X,E : pat(X,E)} < patlenmin.
