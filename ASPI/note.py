import mido
from fractions import Fraction
from decimal import Decimal
from math import floor

LETTER_TO_KEYNUMBER = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "E#": 5,
    "Fb": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
    "B#": 0,
    "Cb": 11,
}


class Note:
    """
    This is a basic representation of a note in python.
    This class features additionaly to a note length parameter also one for the distance
    to the previous note. This allows to express every rhythmical combination of two notes without the need of
    adding some sort of pause-object.
    """

    def __init__(
        self, note, velocity, position, distance, length=0, track=0, channel=0
    ):
        self._note = note
        self._velocity = velocity
        self._length = length
        self._position = position
        self._track = track
        self._distance = distance
        self._channel = channel

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def track(self):
        return self._track

    @track.setter
    def track(self, value):
        self._track = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def __eq__(self, obj):
        if isinstance(obj, Note):
            return (
                self.note == obj.note
                and self.velocity == obj.velocity
                and self.length == obj.length
                and self.position == obj.position
                and self.track == obj.track
                and self.distance == obj.distance
                and self.channel == obj.channel
            )
        return False

    def __str__(self):
        return f"Note({self.note},{self.velocity},{self.position},{self.length},{self.distance},{self.track},{self.channel})"

    def to_asp(
        self,
        ticks_per_beat=480,
        limit_denom=32,
        snap=True,
        snap_points=None,
        denom_limit=32,
    ) -> str:
        """
        Converts this Note object into its ASP representation.
        Returns
        -------
        atom : str
                This Note-object as an ASP atom.
        """

        if snap:
            if snap_points:
                self.snap(snap_points)
            else:
                self.snap()

        # if self.length == 0:
        #     print("WARNING: note.length was zero!")

        len_frac = Fraction(Decimal(str(self.length))).limit_denominator(
            denom_limit
        ) / Fraction(4)
        dis_frac = Fraction(Decimal(str(self.distance))).limit_denominator(
            denom_limit
        ) / Fraction(4)

        return f"note({self.track},{self.position},{self.channel},{self.note},{self.velocity},({len_frac.numerator},{len_frac.denominator}),({dis_frac.numerator},{dis_frac.denominator}))."

    def snap(self, points=[0, 0.25, 0.5, 0.75, 1]) -> None:
        """This snaps the note.length and note.position to the points given. The standard value is a 16th note.
        Parameters
        ----------
        points : list
                Contains all the points the note should snap to as values between 0 and 1 (both included).
        """

        def helper(points, value):
            min_dist = 1
            floor_ = floor(value)
            tmp_ = value - floor_
            min_id = None
            for point in points:
                dist = abs(tmp_ - point)
                if dist < min_dist:
                    min_dist = dist
                    min_id = points.index(point)
            return floor_ + points[min_id]

        self.length = helper(points, self.length)
        self.distance = helper(points, self.distance)

    def to_mido(self, type, distance=None, ticks_per_beat=480) -> mido.Message:
        """
        Converts this Note-object into a mido.Message object.
        Parameters
        ----------
        type : str
                Eather note_on or note_off
        distance : int
                The distance (in midi timeing) for this note. If this is None the distance of this note obejct will be used.
        ticksper_beat : int
                Midi ticks per beat for note.distance conversion
        Returns
        -------
        message : mido.Message
                A mido Message which can be added to a mido.MidiTrack
        """

        if distance is None:
            distance = int(self.distance * ticks_per_beat)
        message = mido.Message(
            type,
            time=distance,
            velocity=self.velocity,
            note=self.note,
            channel=self.channel,
        )
        return message

    def __repr__(self):
        return self.__str__()
