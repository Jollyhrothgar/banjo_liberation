import copy

from musical.theory import Note
from musical.audio.playback import play
from musical.audio import Hit

ROLL_DICT = {
    'square_roll': (3, 2, 5, 1),
    'triple_forward_square': (4, 3, 2, 3, 2, 1, 4, 3, 2, 3, 2, 1, 5, 2, 3, 1),
    'forward_backward': (3, 2, 1, 2 , 1, 2, 3, 1),
}

BANJO_TUNING = {
    1: Note('d5'),
    2: Note('b4'),
    3: Note('g4'),
    4: Note('d4'),
    5: Note('g5')
}

MOVEABLE_CHORDS = {
    'gamma_g4': (0, 0, 0, 0, 0),
        
}




CHORD_DICT = {
    'gamma_g1': (0, 0, 0, 0, 0),
    'beta_c1': (2, 1, 0, 2, 0),
    'beta_d1': (4, 3, 2, 4, 0),
    'alpha_g1': (5, 3, 4, 5, 0),
    'alpha_c1': (10, 8, 9, 10, 0),
    'alpha_d1': (12, 10, 11 ,12, 0),
    'beta_c2': (14, 13, 12, 14, 0),
    'beta_g2': (9, 8, 7, 9, 0),
    'beta_d2': (16, 15, 14, 16, 0),
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

def generate_chords(file_name):
    global MOVEABLE_CHORDS
    for chord_name, strings in MOVEABLE_CHORDS.items():
        inversion, note_name = chord_name.split("_")
        
        if inversion == 'gamma':
            for fret in range(0, 23):
                #chord = (strings[0]+fret, strings[1]+fret, strings[2]+fret, strings[3]+fret, strings[4]+fret)
                chord = tuple([string+fret for string in strings])
                fretted_strings = fret_strings(chord) 
                print('gamma'+repr(fretted_strings[3]))
       


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
    chord_1 = fret_strings(chord=CHORD_DICT['alpha_g1'])
    chord_2 = fret_strings(chord=CHORD_DICT['alpha_c1'])
    chord_3 = fret_strings(chord=CHORD_DICT['alpha_d1'])
    chord_4 = fret_strings(chord=CHORD_DICT['alpha_g1'])

    generate_chords(file_name=None)

    print(Note('g4'))