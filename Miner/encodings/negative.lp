#include "interface.lp".

% I use 
% - E for elements (called items before),
% - S for sequences names,
% - I,J,K,L for indices
% I rename to have more room for index names

% this fixes the number of positive/negative items in a pattern

% setup
index(1..patlenmax).
element(E) :- seq(_,_,E).
seqlen(S,I) :- seq(S,I,_), not seq(S,I+1,_).

% generate positive pattern
{ pat(I,E) : element(E) }1 :- index(I).
% generate negative part (like this to avoid symmetric patterns)
minneg { neg(I,E) : element(E), index(I), index(I+1) } maxneg.
:- #count {I, 1 : pat(I,_); I, 2 : neg(I,_)} = C, 1{C < patlenmin; C > patlenmax}.
:- not pat(1, _).
:- pat(I, _), not pat(I-1,_), I > 1.
:- neg(I,_), not pat(I,_).

poslen(I) :- pat(I,_), not pat(I+1,_).

% ensure the pattern is optimized
:- pat(I,E), neg((I;I-1),E).

% the pattern must support the sequence
% - we use chaining of the supports here to keep the encoding compact
% - like this a partern supports a chain if the last pattern index is supported
support(S,1,J)   :- seq(S,J,E), pat(1,E).
support(S,I,J+1) :- support(S,I,J), seq(S,J+1,E), not neg(I,E).
support(S,I,J)   :- support(S,I-1,J-1), seq(S,J,E), pat(I,E).

support(S) :- support(S,L,J), seqlen(S,J), poslen(L).

:- not minsup {support(S)} maxsup.

#show neg/2.
