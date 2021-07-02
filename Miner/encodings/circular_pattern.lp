% input: pat(Index, InnerIndex, Item).
% output: circular patterns

% choose at least two of the input sequences
2 { c(A) : pat(A,_,_) }.
p(A,L,I) :- pat(A,L,I), c(A).

% chosen pattern length must be equal
patlen(P, L) :- pat(P,L,_), not pat(P,L+1,_).
:- p(P1,_,_), patlen(P1,L1), p(P2,_,_), patlen(P2,L2), L1!=L2.

% mapping from one pattern to another
association(P1, P2, L1, L2) :- p(P1,L1,I), p(P2,L2,I), L1>=L2, P1!=P2.

%mapping distance must be constant
:- association(P1, P2, L1, L2), association(P1, P2, L3, L4), L1-L2 != L3-L4.

% there must be a mapping from all chosen patterns to all chosen patterns
hasAss(P1,P2,L1,L2) :- association(P1,P2,L1,L2).
hasAss(P1,P2,L1,L2) :- association(P2,P1,L2,L1).
:- not hasAss(P1,P2,L1,L2), p(P1,L1,_), p(P2,L2,_), L1<L2, P1!=P2.

#show pat(A,L,I) : p(A,L,I).
#show.
