from ..note import Note, LETTER_TO_KEYNUMBER
import mido

def note_handler(atom, tracker):
    """handles the note atoms in the ASPNoteTracker class"""
    data = atom.split(",")
    if len(data) != 9:
        return
    # 0 : track, 1 : position, 2 : channel, 3 : note, 4 : velocity, 5 : length_nom, 6 : length_denom, 7 : dist_num, 8 : dist_denom
    track = int(data[0].strip())
    pos = int(data[1].strip())
    channel = int(data[2].strip())
    note = int(data[3].strip())
    length = float(data[5].strip()[1:]) * 4 / float(data[6].strip()[:-1])
    veloc = int(data[4].strip())
    dist = float(data[7].strip()[1:]) * 4 / float(data[8].strip()[:-1])
    tracker.remaining_notes[track].add(
        Note(note, veloc, pos, dist, length=length, track=track, channel=channel)
    )


def prog_change_handler(atom, tracker):
    """handles the prochange atoms in the ASPNoteTracker class"""
    data = atom.split(",")
    message = mido.Message("program_change", program=int(data[2].strip()), time=0)
    tracker.remaining_meta[int(data[0].strip())].append((message, int(data[1].strip())))


def signature_change_handler(atom, tracker):
    """handles the sig atoms in the ASPNoteTracker class"""
    data = atom.split(",")
    message = mido.MetaMessage(
        "time_signature",
        numerator=int(data[2].strip()),
        denominator=int(data[3].strip()),
        time=0,
    )
    tracker.remaining_meta[int(data[0].strip())].append((message, int(data[1].strip())))


def key_change_handler(atom, tracker):
    """handles the key atoms in the ASPNoteTracker class"""
    data = atom.split(",")
    root = data[2].strip().strip('"')
    mode = data[3].strip()
    if mode in ["ionian", "lydian", "mixolydian"]:
        mode = ""
    else:
        mode = "m"
    KEYNUMBER_TO_LETTER = {}
    for key, value in LETTER_TO_KEYNUMBER.items():
        if value not in KEYNUMBER_TO_LETTER:
            KEYNUMBER_TO_LETTER[value] = key

    message = mido.MetaMessage(
        "key_signature", key=f"{KEYNUMBER_TO_LETTER[int(root)]}{mode}", time=0
    )
    tracker.remaining_meta[int(data[0].strip())].append((message, int(data[1].strip())))


def pause_handler(atom, tracker):
    """handles the pause atoms in the ASPNoteTracker class"""
    # data = atom.split(",")
    # tracker.remaining_notes[int(data[0].strip())] = Pause(int(data[1].strip()), int(
    #    data[3].strip()), int(data[2].strip()), int(data[0].strip()))
    pass


def tempo_handler(atom, tracker):
    """handles tempo change atoms"""
    data = atom.split(",")
    message = mido.MetaMessage("set_tempo", tempo=int(data[2].strip()), time=0)
    track = int(data[0].strip())
    tracker.remaining_meta[track].append((message, int(data[1].strip())))


def control_handler(atom, tracker):
    """handles control change atoms"""
    data = atom.split(",")
    message = mido.Message("control_change", change=int(data[2].strip()), time=0)
    track = int(data[0].strip())
    tracker.remaining_meta[track].append((message, int(data[1].strip())))


def midi_port_handler(atom, tracker):
    """handles port change atoms"""
    data = atom.split(",")
    message = mido.MetaMessage("midi_port", port=int(data[2].strip()), time=0)
    track = int(data[0].strip())
    tracker.remaining_meta[track].append((message, int(data[1].strip())))
