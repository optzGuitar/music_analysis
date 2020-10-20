#include "interface.lp".

item(E) :- seq(_,_,E).
index(1..patlenmax).
seqlen(S, L) :- seq(S,L,_), not seq(S,L+1,_).

{pat(P, E) : item(E)} 1 :- index(P).
:- not pat(1,_).
:- pat(I,_), not pat(I-1,_), I>1.
:- not pat(patlenmin,_).

patlen(I) :- pat(I,_), not pat(I+1,_).

occd(S, 1, SP, maxdist)  :- seq(S,SP,E), pat(1,E).
occd(S, PP, SP, MD-1) :- occd(S,PP,SP-1, MD), seq(S,SP,_), MD>0.
occd(S, PP, SP, maxdist) :- occd(S,PP-1,SP-1,_), seq(S,SP,E), pat(PP,E).

occ(S,1,P) :- pat(1,I), seq(S,P,I).
occ(S,L,P) :- occ(S,L,P-1), seq(S,P,_).
occ(S,L,P) :- occ(S,L-1,P-1), seq(S,P,C), pat(L,C).

supportd(S) :- occd(S,L,_,MD), patlen(L), MD=0.
:- not supportd(_).
support(S)  :- supportd(S).
support(S)  :- occ(S,L,SP), seqlen(S,SP), patlen(L).

:- not minsup {support(S)} maxsup.

#show pat/2.