class noteList:
    """
    This class is a helper for the ASP_to_Midi function.
    It tracks the distances of the notes to each other.
    Furthermore it retruns note objects at the right time for the MIDI
    note_on signal.
    """

    def __init__(self):
        self._notes = []
        self._position = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        """Should be used with great care!"""
        self._position = value

    def add(self, note):
        """
        Add a note to the inenr collection.
        """
        self._notes.append(note)

    def add_range(self, notes):
        """
        Adds all note objects inside the iterable.
        """
        for note in notes:
            self.add(note)

    def get_next_timestep(self) -> int:
        """
        This returns the minimal timestep.
        """
        min_time = None
        for note in self._notes:
            if self._position == note.position:
                min_time = note.distance
                break

        if self._notes:
            return min_time
        return None

    def do_timestep(self) -> list:
        """
        This method performs a timestep and applies the distance bonus.
        """
        new_on = []
        for note in self._notes:
            if note.position == self._position:
                note.distance
                new_on.append(note)
            else:
                break
        self._notes = list(filter(lambda x: x not in new_on, self._notes))
        self._position += 1
        return new_on

    def adjust_timing(self, stepsize) -> None:
        """
        Here a given stepsize is substracted from all notes at the current position.
        This is useful when a note_off message but no note_on message occures.
        """
        for note in self._notes:
            if note.position == self.position:
                note.distance -= stepsize
                if note.distance < 0:
                    raise RuntimeError(
                        f"The stepsize was to big! Most probably the note atoms are not coherent! One note has a remaining distance of {note.distance}")

    def __str__(self):
        return str(self._notes)

    def __repr__(self):
        return self._notes.__repr__()


class deactivationQueue(noteList):
    """
    This class is used to track when a note needs to be turned of inside a MIDI file.
    It is used in the ASP_to_Midi method for this exact reason.
    """

    def __init__(self):
        super().__init__()

    def get_next_timestep(self) -> int:
        """
        Returns the minimal timestep.
        """
        min_step = None
        if self._notes:
            min_step = self._notes[0].length
        for note in self._notes:
            if note.length < min_step:
                min_step = note.length

        return min_step

    def do_timestep(self) -> list:
        """
        Returns a list of notes to turn off.
        """
        min_step = min_step = self.get_next_timestep()
        new_off = []

        for note in self._notes:
            note.length -= min_step
            if note.length <= 0:
                new_off.append(note)
        self._notes = list(filter(lambda x: x not in new_off, self._notes))

        return new_off

    def adjust_timing(self, stepsize) -> None:
        min_step = stepsize

        for note in self._notes:
            note.length -= min_step
            if note.length <= 0:
                raise RuntimeError(
                    f"The stepsize was to big! One note has a remaining length of {note.length}. Seems like the Midi-Atoms are not coherent!")
