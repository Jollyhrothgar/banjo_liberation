import copy

from musical.theory import Note
from musical.audio.playback import play
from timeline import Hit

ROLL_DICT = {
    'square_roll': (3, 2, 5, 1)
}

BANJO_TUNING = {
    1: Note('d5'),
    2: Note('b5'),
    3: Note('g4'),
    4: Note('d4'),
    5: Note('g5')
}

CHORD_DICT = {
    'gamma_g1': (0, 0, 0, 0, 0),
    'beta_c1': (2, 1, 0, 2, 0),
    'beta_d1': (4, 3, 2, 4, 0)
}

def render_roll(roll, note_length):
    """
    Given a roll (an array of Notes) and a note_length (in seconds), render the wave-form that the
    audio synthesizer needs to make some noise.

    Args:
        roll: an array of Notes
        note_length: how long to play each note.
    Returns:
        rendered notes (a wave-form that is played with an audio synthesizer)
    """
    return [Hit(note=note, length=note_length).render() for note in roll]

def play_roll(roll):
    """Play each note in a rendered roll sequentially"""
    for note in roll:
        play(note)


def fret_strings(chord):
    """
    Fret strings pulls BANJO_TUNING from the global namespace and frets the strings
    according to the supplied chord.

    chord: a tuple which maps the depressed fret to the banjo string, according to the schema:
        chord = (
            first string fret,
            second string fret,
            third string fret,
            fourth string fret,
            fifth string fret
        )
    Args:
        chord: a tuple of depressed frets
    Returns:
        A dictionary of banjo strings mapped to the note after the chord has been applied.
    """
    global BANJO_TUNING
    fretted_strings = dict(BANJO_TUNING)

    for str_idx, fret in enumerate(chord):
        banjo_string = str_idx + 1
        fretted_strings[banjo_string] = fretted_strings[banjo_string].transpose(fret)
    return fretted_strings


def make_roll(strings, roll_pattern):
    """
    Given a set of strings and a roll pattern, return the strings to be plucked in order of
    plucking.

    Args:
        strings: A banjo strings dictionary.
        roll_pattern: A tuple which determins what order to pluck the strings.

    Returns:
        An array of Notes.
    """
    return [strings[pluck] for pluck in roll_pattern]


if __name__ == '__main__':
    pass
