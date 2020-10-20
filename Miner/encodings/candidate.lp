#include "interface.lp".

item(I) :- seq(_,_,I).
seqlen(S,L) :- seq(S,L,_), not seq(S,L+1,_).

patpos(1).
{ patpos(X+1) } :- patpos(X), X < patlenmax.
patlen(L)  :- patpos(L), not patpos(L+1).
1{ pat(X,I) : item(I) }1 :- patpos(X).

occ(S,1,P) :- pat(1,I), seq(S,P,I).
occ(S,L,P) :- occ(S,L,P-1), seq(S,P,_).
occ(S,L,P) :- occ(S,L-1,P-1), seq(S,P,C), pat(L,C).

support(S) :- occ(S,L,LS), patlen(L), seqlen(S,LS).

:- #count{X,I : pat(X,I)} < patlenmin.
