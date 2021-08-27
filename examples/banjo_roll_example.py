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


def make_alpha_minor(chord):
    pass

def make_alpha_seven(chord):
    pass

def make_alpha_minor_seven(chord):
    pass

def make_beta_minor(chord):
    pass

def make_beta_seven(chord):
    pass

def make_beta_minor_seven(chord):
    pass

def make_gamma_minor(chord):
    pass

def make_gamma_seven(chord):
    pass

def make_gamma_minor_seven(chord):
    pass

def generate_moveable_chords(file_name):
    """
    Given the first location of moveable chords represented as a tuple:
        chord = (
            first string fret,
            second string fret,
            third string fret,
            fourth string fret,
            fifth string fret
        )
    
    Generate all moveable chords on the banjo. Optionally, each chord can be transformed with a
    chord transformer (but the base shapes could also just be specified hardcoded).

    Args:
        file_name: A string that contains the full path to the file to serialize the generated
        chords.

    """
    first_alpha = (2, 0, 1, 2, 0) # e
    first_beta  = (2, 1, 0, 2, 0) # c
    first_gamma = (0, 0, 0, 0, 0) # g
    moveable_chords = {}

    for fret_position in range(0, 23):
        # These are all tuples that map strings to fret positions:
        # E.g. alpha = (
        #                  first string fret position,
        #                  second string fret position,
        #                  third string fret position,
        #                  fourth string fret position,
        #                  fifth string fret position,
        #              )
        # Add the fret offset to each base chord, and don't add an offset to the fifth string.
        alpha = tuple([banjo_string + fret_position if string_idx != 4 else banjo_string for string_idx, banjo_string in enumerate(first_alpha)])
        beta = tuple([banjo_string + fret_position if string_idx != 4 else banjo_string for string_idx, banjo_string in enumerate(first_beta)])
        gamma = tuple([banjo_string + fret_position if string_idx != 4 else banjo_string for string_idx, banjo_string in enumerate(first_gamma)])

        fretted_alpha = fret_strings(alpha)
        fretted_beta = fret_strings(beta)
        fretted_gamma = fret_strings(gamma)
        
        # Make sure we're not playing frets that don't exist
        if any([fret > 22 for fret in alpha]) and any([fret < 0 for fret in alpha]):
            pass # Chord contains frets that are greater than 22 or less than 0.
        else:
            moveable_chords['alpha_' + fretted_alpha[1].get_note_name()] = alpha

        if any([fret > 22 for fret in beta]) and any([fret < 0 for fret in beta]):
            pass # Chord contains frets that are greater than 22 or less than 0.
        else:
            moveable_chords['beta_' + fretted_beta[2].get_note_name()] = beta 

        if any([fret > 22 for fret in gamma]) and any([fret < 0 for fret in gamma]):
            pass # Chord contains frets that are greater than 22 or less than 0.
        else:
            moveable_chords['gamma_' + fretted_gamma[3].get_note_name()] = gamma
    
    return moveable_chords


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

    for name, chord in generate_moveable_chords(file_name=None).items():
        print(name, chord)


