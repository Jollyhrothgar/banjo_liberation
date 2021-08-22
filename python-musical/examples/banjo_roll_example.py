from musical.theory import Note
from musical.theory import Scale
from musical.theory import Chord
from musical.audio.playback import play
from timeline import Hit
from timeline import Timeline


def play_notes_from_list(notes, note_length):
    """Take a list of Note classes, play notes all at the same length.
    
    Args:
        notes: [Note, ...]
        note_length: float (length of note in seconds)
    """
    for note in notes:
        rendered = Hit(note, length=note_length).render()
        play(rendered)

ROLL_DICT = {
    'square_roll': (0, 4, 12, 7) 
}

def make_roll_from_absolute_intervals(note, roll_pattern):
    """
    Given a reference Note, note, return a list of Notes that would be
    played in a square roll pattern "down the neck".

    Args:
        note: An instance of the class Note
        roll_pattern: A list of absolute half-step intervals relative
            to the `note` argument that will form the roll.
    Returns:
        A list of Notes in a roll pattern.
    """
    return [note.transpose(interval) for interval in roll_pattern]
    

if __name__ == '__main__':
    note_list = make_roll_from_absolute_intervals(
                    note=Note('g4'),
                    roll_pattern=ROLL_DICT['square_roll'])
    print(note_list)
    play_notes_from_list(note_list, note_length=0.5)