from typing import Optional
from ..note import Note


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

    def note_off(self, note) -> Optional[Note]:
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
