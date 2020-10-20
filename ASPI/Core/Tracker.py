import mido
from ..note import Note
from ..ASP_Note_Handler import (
    note_handler,
    signature_change_handler,
    prog_change_handler,
    key_change_handler,
    pause_handler,
    tempo_handler,
    control_handler,
    midi_port_handler,
)
from .TrackerCore import deactivationQueue
from .TrackerCore import noteList


class MidiNoteLengthTracker:
    """
    This class tracks the length of Midi notes.
    """

    def __init__(self, track, tpb, snap_points):
        # this list contains notes
        self.active_notes = []
        self._ticks_per_beat = tpb
        self.position = 0
        self._track = track
        self.distance = 0
        self._last_note_on = False
        self._acumulated_time = 0
        self._pos_feed = False
        self._snap_points = sorted(snap_points)
        self._min_time_division = int(
            round((self._snap_points[1] - self.snap_points[0]) * self.ticks_per_beat)
        )

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def track(self):
        return self._track

    @property
    def ticks_per_beat(self):
        return self._ticks_per_beat

    @property
    def snap_points(self):
        return self._snap_points

    def note_on(self, note, velocity, channel=0) -> None:
        """
        Adds a note to be tracked.
        Parameters
        ----------
        note : int
            The note to be tracked.
        velocity : int
            The velocity of the note.
        """

        self._last_note_on = True

        note_obj = Note(
            note,
            velocity,
            self._position,
            self.distance,
            track=self._track,
            channel=channel,
        )
        self.active_notes.append(note_obj)
        self._pos_feed = False

    def do_timestep(self, ticks) -> None:
        """
        Adds the deltatime to all currently active notes.
        Parameters
        ----------
        ticks : int
            The timedelta from the MIDI message.
        """
        if ticks == 0:
            return

        timeplus = float(ticks) / float(self.ticks_per_beat)
        if not self._pos_feed:
            self._acumulated_time += ticks
        if self._acumulated_time >= self._min_time_division and not self._pos_feed:
            self.position += 1
            self._acumulated_time = 0
            self._pos_feed = True

        if self._last_note_on:
            self.distance = timeplus
        else:
            self.distance += timeplus
        self._last_note_on = False

        for note in self.active_notes:
            note.length += timeplus

    def note_off(self, note) -> Note:
        """
        Removes the given note from the active list and returns the Note object.
        Parameters
        ----------
        note : int
            The note to be shut off.
        Returns
        -------
        note_obj : Note
            The Note object used to track the note length.
        """
        self._last_note_on = False
        pos = None
        for i in range(len(self.active_notes)):
            if note == self.active_notes[i].note:
                pos = i
                break

        # already added note could have wrong distance
        # all current notes need to be adjusted
        # maybe preprocess midi files?
        if pos == None:
            return None
        if self.active_notes[pos].length == 0:
            self.distance -= self.active_notes[pos].distance

        return self.active_notes.pop(pos)


class ASPNoteTracker:
    def __init__(self, atoms, tpb=480, handlers={}):
        self.active_meta = {}
        self._ticks_per_beat = tpb
        self.atoms = atoms
        self._remaining_notes = {}
        self._remaining_meta = {}
        # positions differ between tracks; so for each track there is a seperate position
        self.position = {}
        self.track = 0
        self.ATOM_HANDLER = {
            **{
                "note": note_handler,
                "progchange": prog_change_handler,
                "sig": signature_change_handler,
                "key": key_change_handler,
                "tempo": tempo_handler,
                "control": control_handler,
                "port": midi_port_handler,
            },
            **handlers,
        }
        self.deact_queue = {}

        self.__parse_atoms()
        self.counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    @property
    def positions(self) -> dict:
        """
        The current positions of the different tracks.
        """
        return self.position

    @property
    def remaining_notes(self):
        return self._remaining_notes

    @remaining_notes.setter
    def remaining_notes(self, value):
        self._remaining_notes = value

    @property
    def remaining_meta(self):
        return self._remaining_meta

    @remaining_meta.setter
    def remaining_meta(self, value):
        self.remaining_meta = value

    @property
    def ticks_per_beat(self):
        return self._ticks_per_beat

    def __parse_atoms(self):

        for atom in self.atoms:
            if atom.startswith("track"):
                tracknr = atom[6:-1]
                tracknr = int(tracknr)
                self.position[tracknr] = 0

        self.__init_dicts()

        for atom in self.atoms:
            if not "(" in atom:
                continue
            splited = atom.split("(")
            data = atom[len(splited[0]) + 1 : -1]
            if splited[0] in self.ATOM_HANDLER:
                self.ATOM_HANDLER[splited[0]](data, self)

    def __init_dicts(self):
        for trackid in self.position.keys():
            self.deact_queue[trackid] = deactivationQueue()
            self.remaining_notes[trackid] = noteList()
            self.remaining_meta[trackid] = []
            self.active_meta[trackid] = []

    def select_track(self, trackid) -> None:
        """
        Selects the track to perform the text timestep(s) on. It is possible to select a new track after each do_timestep call.
        Parameters
        ----------
        trackid : int
            The number of the track.
        Raises
        ------
        AttributeError
            Raised if trackid is not valid.
        """
        if trackid not in self.position:
            raise AttributeError("The trackid needs to be a valid track number")
        self.track = trackid

    def do_timestep(self):
        """
        This method goes throught all timesteps and returns note_on note_off timing and meta event information.
        This should be used mainly by the helper function do_timesteps (for ease of use).
        It is save to switch tracks whenever one desieres.

        Returns
        -------
        information : tuple
            A tuple of the following shape:
                (deltatime, note_on, note_off, meta_events)
            The delatatime is the deltatime as found in the ASP atoms. The note_on and note_off lists contain
            Note-objects which an be easily converted to mido.Message obejcts. The meta_events list alredy contains
            mido.Message objects which can be added to a mido.MidiTrack right away.
        """
        min_step_deac = self.deact_queue[self.track].get_next_timestep()
        min_step_note = self.remaining_notes[self.track].get_next_timestep()
        new_meta = self._track_meta()
        min_time = min_step_deac
        nons = []
        noffs = []

        if min_step_note == None and min_step_deac == None and not new_meta:
            return None
        elif min_step_note == None and min_step_deac == None and new_meta:
            self.position[self.track] += 1
            self.remaining_notes[self.track].position += 1
            return 0, [], [], new_meta

        if min_step_note == None:
            noffs = self._note_offs(min_step_deac)
            self.counter[1] += 1

        elif min_step_deac == None:
            nons = self._note_ons(min_step_note)
            min_time = min_step_note
            self.counter[2] += 1

        elif min_step_note < min_step_deac:
            nons = self._note_ons(min_step_note)
            min_time = min_step_note
            self.counter[3] += 1

        elif min_step_deac < min_step_note:
            noffs = self._note_offs(min_step_deac)
            self.counter[4] += 1

        else:
            noffs = self._note_offs(min_step_deac, False)
            nons = self._note_ons(min_step_note, False)
            self.counter[5] += 1

        return min_time, nons, noffs, new_meta

    def _track_meta(self):
        new_meta = []
        for meta in self.remaining_meta[self.track]:
            if meta[1] == self.position[self.track]:
                new_meta.append(meta[0])

        rem_list = []
        for meta in new_meta:
            for act_meta in self.active_meta[self.track]:
                if meta.type == act_meta.type:
                    rem_list.append(act_meta)

        self.active_meta[self.track] = list(
            filter(lambda x: x not in rem_list, self.active_meta[self.track])
        )
        self.remaining_meta[self.track] = list(
            filter(lambda x: x[0] not in new_meta, self.remaining_meta[self.track])
        )
        self.active_meta[self.track] += new_meta
        return new_meta

    def _note_ons(self, td, do_other_step=True):
        notes_on = self.remaining_notes[self.track].do_timestep()
        self.position[self.track] += 1
        if do_other_step:
            self.deact_queue[self.track].adjust_timing(td)
        self.deact_queue[self.track].add_range(notes_on)
        return notes_on

    def _note_offs(self, td, do_other_step=True):
        notes_off = self.deact_queue[self.track].do_timestep()
        if do_other_step:
            self.remaining_notes[self.track].adjust_timing(td)
        return notes_off

    def do_timesteps(self):
        """
        This method yields all the timesteps for the selected track.
        Returns
        -------
        information : tuple
            A tuple of the following shape:
                (deltatime, note_on, note_off, meta_events)
        """
        value = 1
        while True:
            value = self.do_timestep()
            if value == None:
                break
            yield value
