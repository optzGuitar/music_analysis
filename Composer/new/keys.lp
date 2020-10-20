type(major, ionian).
type(hmajor, ionian).
type(mmajor, ionian).
type(minor, aeolian).
type(hminor, aeolian).
type(mminor, aeolian).

base(major, 0).
base(minor, 9).
base(hmajor, 0).
base(hminor, 9).
base(mmajor, 0).
base(mminor, 9).

mode(ionian, 0).
mode(dorian, 2).
mode(phrygian, 4).
mode(lydian, 5).
mode(mixolydian, 7).
mode(aeolian, 9).
mode(lokrien, 11).

keysteps(K, 12) :- keysteps(K,_).

keysteps((major, ionian), 0).
keysteps((major, ionian), 2).
keysteps((major, ionian), 4).
keysteps((major, ionian), 5).
keysteps((major, ionian), 7).
keysteps((major, ionian), 9).
keysteps((major, ionian), 11).

keysteps((mmajor, ionian), 0).
keysteps((mmajor, ionian), 2).
keysteps((mmajor, ionian), 4).
keysteps((mmajor, ionian), 5).
keysteps((mmajor, ionian), 7).
keysteps((mmajor, ionian), 8).
keysteps((mmajor, ionian), 10).

keysteps((hmajor, ionian), 0).
keysteps((hmajor, ionian), 2).
keysteps((hmajor, ionian), 4).
keysteps((hmajor, ionian), 5).
keysteps((hmajor, ionian), 7).
keysteps((hmajor, ionian), 8).
keysteps((hmajor, ionian), 11).

keysteps((minor, aeolian), 0).
keysteps((minor, aeolian), 2).
keysteps((minor, aeolian), 3).
keysteps((minor, aeolian), 5).
keysteps((minor, aeolian), 7).
keysteps((minor, aeolian), 8).
keysteps((minor, aeolian), 10).

keysteps((mminor, aeolian), 0).
keysteps((mminor, aeolian), 2).
keysteps((mminor, aeolian), 3).
keysteps((mminor, aeolian), 5).
keysteps((mminor, aeolian), 7).
keysteps((mminor, aeolian), 9).
keysteps((mminor, aeolian), 11).

keysteps((hminor, aeolian), 0).
keysteps((hminor, aeolian), 2).
keysteps((hminor, aeolian), 3).
keysteps((hminor, aeolian), 5).
keysteps((hminor, aeolian), 7).
keysteps((hminor, aeolian), 8).
keysteps((hminor, aeolian), 11).

% generates all remainding keysteps for all existing keys;
% the 24 is there to avoid S-MO-BO to be negative
% because otherwise the modulo result is negative
keysteps((B, M), (S-MO-BO+24)\12) :- base(B, BO),
    mode(M, MO), type(B, TM), keysteps((B, TM), S).

% selects the notes which are in key K
inkey(12-S, (R, K)) :- range(12-S),
    keys(_,_,_,(R, K)), keysteps(K, S), 12-S < R, S != 12.
inkey(N, (R, K)) :- range(N),
    keys(_,_,_,(R, K)), keysteps(K, ((N-(R\12))\12)).

