import mido
from .Tracker import MidiNoteLengthTracker, ASPNoteTracker
import os
from .note import Note
from .Handler.midi_event_handler import (
    note_on_handler,
    note_off_handler,
    prog_change_handler,
    time_sig_handler,
    key_sig_handler,
    set_tempo_handler,
)
import time


def MIDI_to_ASP(
    input,
    tracks=None,
    handlers={},
    snap_points=None,
    skip_non_music_tracks=False,
    quiet=False,
) -> str:
    """
    This function converts a MIDI file into an ASP encoding. This is done using the mido package.
    Parameters
    ----------
    input : string or mido.MidiFile
            The filename of the MIDI file to convert
    tracks : list, int, optional
            The track(s) of the MIDI file to process.
    handlers : dict
            Adds handler for MIDI massages. The keys are the mido.Message.type strings and the values are functions.
            The functions should all follow the following signature:
                func(mido.Message: event, ASPI.MidiNoteTracker: tracker) -> str or none
                The return string is the ASP atom of the message
            The following mesages are naturally supported:
                note_on, note_off, program_change, time_signature, key_signature
    snap_points : list
            A list containing percentage values between and including 0 and 1. The standard snap distance is a 16th note e.g. [0, 0.25, 0.5, 0.75, 1].
            The length of the note will always have one of the specified decimal places.
    skip_non_music_tracks : bool
            If True all tracks without musical information (note_on and note_off messages) will be ignored.
    quiet : bool
            If true all command line output is shut down.
    Returns
    -------
    encoding : str
        The MIDI file as ASP facts.
    """

    snaps = snap_points
    if snap_points == None:
        # currently not implemented to be changed (snapping is working tho (to 16th notes))
        snaps = [0, 0.25, 0.5, 0.75, 1]

    MAP = {
        **{
            "note_on": note_on_handler,
            "note_off": note_off_handler,
            "program_change": prog_change_handler,
            "time_signature": time_sig_handler,
            "key_signature": key_sig_handler,
            "set_tempo": set_tempo_handler,
        },
        **handlers,
    }

    file = input
    if not isinstance(input, mido.MidiFile):
        if not quiet:
            print("Reading the input")
        file = mido.MidiFile(input)

    ASP_FACTS = []

    if isinstance(tracks, int):
        tracks = [tracks]
    elif tracks is None:
        tracks = [i for i in range(len(file.tracks))]

    if not quiet:
        print("Beginning to convert:")
    time_start = time.perf_counter()
    for i, track in enumerate(file.tracks):
        if i not in tracks:
            continue

        tracker = MidiNoteLengthTracker(i, file.ticks_per_beat, snaps)
        music_inf_present = False
        tmp_fact_stor = []
        for event in track:
            if event.type == "note_on" or event.type == "note_off":
                music_inf_present = True

            if event.type in MAP:
                value = MAP[event.type](event, tracker)
                if value != None:
                    tmp_fact_stor.append(value)

        if music_inf_present or not skip_non_music_tracks:
            ASP_FACTS.append(f"track({i}).")
            ASP_FACTS += tmp_fact_stor
        if not quiet:
            print(f"Finished parsing track {i}")

    if not quiet:
        print(f"Finished in {time.perf_counter() - time_start:.2f}")
    return "\n".join(ASP_FACTS)


def ASP_to_MIDI(input, ticks_per_beat=480, handlers={}, quiet=False) -> mido.MidiFile:
    """
    This method converts a ASP MIDI encoding into an actual MIDI file.
    Parameters
    ----------
    input : str or path
            The ASP encoding to convert into a MIDI file. This encoding needs to follow the way the
            MIDI_to_ASP function converts MIDI to ASP.
    ticks_per_beat : int
            The ticks per beat the MIDI file should use.
    handlers : dict
            A dict containing handler functions as values and atoms as keys. The functions will be called when evaluating the
            atoms. The functions need to have the following signature:
                func(string: atom, ASPNoteTracker: tracker) -> None
            Each return value will be ignored. The given atom is alredy prepered: only the comma seperated
            data is given as string.
    quiet : bool
            If True all command line output is shut down.
    Returns
    -------
    midifile_obj : mido.MidiFile
        This is the MIDI described in the encoding.
    """

    data = input
    try:
        if os.path.exists(input):
            with open(input, "r") as file:
                if not quiet:
                    print("Reading the input.")
                data = file.read()
    except ValueError:  # this happens if the string is to long to be a path; if this is the case assume the input is an encoding
        pass

    facts = data.replace("\n", "").split(".")

    facts = list(filter(lambda x: not x.isspace() and x, facts))

    tracker = ASPNoteTracker(facts, ticks_per_beat, handlers=handlers)
    file = mido.MidiFile(ticks_per_beat=ticks_per_beat)

    tracks = list(tracker.position_per_track.keys())

    if not quiet:
        print("Beginning to parse the input")
    time_start = time.perf_counter()
    for track in tracks:
        tracker.select_track(track)
        mido_track = mido.MidiTrack()
        file.tracks.append(mido_track)
        for dt, note_on, note_off, new_meta in tracker.do_timesteps():
            if note_off:
                mido_track.append(
                    note_off.pop(0).to_mido(
                        "note_off", distance=int(round(dt * ticks_per_beat))
                    )
                )
            elif note_on:
                mido_track.append(note_on.pop(0).to_mido("note_on"))
            elif new_meta:
                new_meta[0].time = int(round(dt * ticks_per_beat))
                mido_track.append(new_meta.pop(0))

            mido_track += list(map(lambda x: Note.to_mido(x, "note_off", 0), note_off))
            mido_track += list(map(lambda x: Note.to_mido(x, "note_on", 0), note_on))
            mido_track += new_meta

        mido_track.append(mido.MetaMessage("end_of_track"))
        if not quiet:
            print(tracker.counter)
            print(f"Finished track number {track}")

    if not quiet:
        print(f"Finished in {time.perf_counter() - time_start:.2f}")
    return file
