from ..Tracker.midi_note_length_tracker import MidiNoteLengthTracker
from ..note import LETTER_TO_KEYNUMBER


def note_on_handler(event, tracker: MidiNoteLengthTracker):
    if event.velocity == 0:
        return note_off_handler(event, tracker)
    tracker.do_timestep(event.time)
    tracker.note_on(event.note, event.velocity, event.channel)


def note_off_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    note = tracker.note_off(event.note)
    if note is None:
        return None
    return note.to_asp(tracker.ticks_per_beat, snap_points=tracker.snap_points)


def prog_change_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    return f"progchange({tracker.track},{tracker.position},{event.program})."


def time_sig_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    return f"sig({tracker.track},{tracker.position},{event.numerator},{event.denominator})."


def key_sig_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    key = event.key
    mode = "ionian"
    if "m" in key:
        key = key[:-1]
        mode = "aeolian"
    return f"key({tracker.track},{tracker.position},{LETTER_TO_KEYNUMBER[key]},(major,{mode}))."


def set_tempo_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    return f"tempo({tracker.track},{tracker.position},{event.tempo})."


def control_change_handler(event, tracker: MidiNoteLengthTracker):
    tracker.do_timestep(event.time)
    return f"control({tracker.track},{tracker.position},{event.control})."


def midi_port_handler(event, tracker):
    tracker.do_timestep(event.time)
    return f"port({tracker.track},{tracker.position},{event.port})."
