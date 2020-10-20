
rare(IL) :- IL=1..L, patlen(L), #count{ S : occ(S,IL,LS), seqlen(S,LS) } < maxsup.
rare(L) :- rare(L-1), L <= PL, patlen(PL).
:- not rare(L), patlen(L).
:- not support(S) : seq(S,_,_).