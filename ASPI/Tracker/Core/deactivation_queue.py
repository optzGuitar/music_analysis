from .note_list import NoteList

class DeactivationQueue(NoteList):
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
