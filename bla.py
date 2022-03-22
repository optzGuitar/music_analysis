s = """track(0).key(0,0,0,(major,ionian)).key(0,1,0,(major,ionian)).key(0,2,0,(major,ionian)).key(0,3,0,(major,ionian)).key(0,4,0,(major,ionian)).key(0,5,0,(major,ionian)).key(0,6,0,(major,ionian)).key(0,7,0,(major,ionian)).key(0,8,0,(major,ionian)).key(0,9,0,(major,ionian)).key(0,10,0,(major,ionian)).key(0,11,0,(major,ionian)).key(0,12,0,(major,ionian)).key(0,13,0,(major,ionian)).key(0,14,0,(major,ionian)).key(0,15,0,(major,ionian)).key(0,16,0,(major,ionian)).key(0,17,0,(major,ionian)).key(0,18,0,(major,ionian)).key(0,19,0,(major,ionian)).key(0,20,0,(major,ionian)).note(0,0,0,83,100,(1,2),(1,4)).note(0,1,0,60,41,(1,2),(1,4)).note(0,2,0,83,100,(1,2),(1,4)).note(0,3,0,83,100,(1,4),(1,4)).note(0,4,0,83,100,(1,4),(1,4)).note(0,5,0,83,100,(1,2),(1,4)).note(0,6,0,59,61,(1,4),(1,4)).note(0,7,0,83,100,(1,2),(1,4)).note(0,8,0,83,100,(1,2),(1,4)).note(0,9,0,60,43,(1,2),(1,4)).note(0,10,0,83,100,(1,2),(1,4)).note(0,11,0,71,76,(1,2),(1,4)).note(0,12,0,83,100,(1,2),(1,4)).note(0,13,0,83,91,(1,4),(1,4)).note(0,14,0,69,96,(1,2),(1,4)).note(0,15,0,83,56,(1,2),(1,4)).note(0,16,0,83,69,(1,2),(1,4)).note(0,17,0,83,97,(1,2),(1,4)).note(0,18,0,59,92,(1,4),(1,4)).note(0,19,0,83,90,(1,2),(1,4)).note(0,20,0,83,100,(1,2),(1,4))."""

from ASPI import ASP_to_MIDI

m = ASP_to_MIDI(s)

m.save('example1.mid')

