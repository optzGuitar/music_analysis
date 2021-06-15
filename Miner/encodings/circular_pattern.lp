% input: pat(Index, InnerIndex, Item).
% output: circular pattern


1{c(A) : pat(A,_,_)}.
p(A,L,I) :- pat(A,L,I), c(A).

patlen(P, L) :- pat(P,L,_), not pat(P,L+1,_).

association(P1, P2, L1, L2, a) :- p(P1,L1,I), p(P2,L2,I), P1!=P2, L1>=L2.
association(P1, P2, L1, L2, b) :- p(P1,L1,I), p(P2,L2,I), P1!=P2, L1<L2.

:- association(P1, P2, L1, L2, a), association(P1, P2, L3, L4, a), L1-L2 != L3-L4.
:- association(P1, P2, L1, L2, b), association(P1, P2, L3, L4, b), patlen(P1,L), (L1+L)-L2 != (L3+L)-L4.
:- p(P1,L,_), not association(P1,_,L,_,_).

#show pat(A,L,I) : p(A,L,I).
#show association/5.

pat(2, 1, a). pat(2, 2, b). pat(2, 3, c). pat(2, 4, d).
pat(1, 1, c). pat(1, 2, d). pat(1, 3, a). pat(1, 4, b).
pat(3, 1, c). pat(3, 2, d). pat(3, 3, a). pat(3, 4, f).
