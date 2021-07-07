suppat(U) :- U=1..L, patlen(L), L>1.

spocc(S,1,2,P)     :- seq(S,P,I), pat(2,I), not support(S).
spocc(S,U,U,P)     :- suppat(U), occ(S,U-1,P), not support(S).
spocc(S,U,L,P+1)   :- spocc(S,U,L,P), seq(S,P+1,_).
spocc(S,U,L+1,P+1) :- spocc(S,U,L,P), seq(S,P+1,I), pat(L+1,I).

sprare(U,U-1) :- suppat(U), rare(U-1).
sprare(U,L)   :- sprare(U,L-1), L<=LP, patlen(LP).
sprare(U,IL)  :- suppat(U), IL=U+1..L, patlen(L), 
                #count{ S : spocc(S,U,IL,LS), seqlen(S,LS);
                        S : support(S) } < maxsup.
:- sprare(U,L), patlen(L).
