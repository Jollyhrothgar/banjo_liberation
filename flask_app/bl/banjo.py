from bl.note import Note

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


def generate_moveable_chords(first_chord, name): 
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
  Returns:
    A dictionary mapping the normalized Note name (representing the pitch of the chord) to the
    frets that are depressed to play the chord.
  """

def generate_all_chords():
  """ Given the first shape for each chord class, generate the full list of chords"""
  first_alpha_major = (2, 0, 1, 2, 0) # E
  first_beta_major  = (2, 1, 0, 0, 0) # C
  first_gamma_major = (0, 0, 0, 0, 0) # G
  first_alpha_minor = (2, 0, 0, 2, 0) # Em
  first_beta_minor  = (1, 0, 1, 1, 0) # Cm
  first_gamma_minor = (1, 1, 0, 1, 0) # G#m

  # Create the arguments needed to generate a list of movable chords for each chord-type.
  base_chords = [
      {"base": first_alpha_major, "name": "alpha_major"},
      {"base": first_beta_major , "name": "beta_major" },
      {"base": first_gamma_major, "name": "gamma_major"},
      {"base": first_alpha_minor, "name": "alpha_minor"},
      {"base": first_beta_minor , "name": "beta_minor" },
      {"base": first_gamma_minor, "name": "gamma_minor"},
  ]
  moveable_chords = {}

  # Generate the list of movable chords for each chord type.
  for kwargs in base_chords:
    moveable_chords.update(generate_moveable_chords(**kwargs))
  return moveable_chords


def generate_moveable_chords(base, name):
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
  #TODO(mike): Do something with file_name
  Args:
    file_name: A string that contains the full path to the file to serialize the generated
    chords.
  Returns:
    A dictionary mapping the normalized Note name (representing the pitch of the chord) to the
    frets that are depressed to play the chord.
  """
  moveable_chords = {}

  for fret_position in range(0, 23):
    # These are all tuples that map strings to fret positions:
    # E.g. alpha = (
    #          first string fret position,
    #          second string fret position,
    #          third string fret position,
    #          fourth string fret position,
    #          fifth string fret position,
    #        )
    # Add the fret offset to each base chord, and don't add an offset to the fifth string.
    chord = tuple([banjo_string + fret_position if string_idx != 4 else banjo_string for string_idx, banjo_string in enumerate(base)])
    fretted_strings = fret_strings(chord)

    if name.startswith('alpha'):
      chord_name_idx = 1
    elif name.startswith('beta'):
      chord_name_idx = 2
    elif name.startswith('gamma'):
      chord_name_idx = 3
    else:
      raise ValueError(f"{name} does not have a defined note-lookup")

    # Make sure we're not playing frets that don't exist
    if any([fret > 22 for fret in chord]) or any([fret < 0 for fret in chord]):
      pass # Chord contains frets that are greater than 22 or less than 0.
    else:
      moveable_chords[f'{name}_' + fretted_strings[1].get_note_name()] = chord
  return moveable_chords


def roll_on_chord(roll_pattern, chord):
  """ Assume that a roll is 16h notes, an eight note roll
  repeated twice.
  Args:
    roll_pattern: a string such as T1I1M3 - this means Thumb on first string
      index on first string, middle on third string.
    chord: a tuple, such as alpha g5, e.g. (5, 3, 4, 5, 0) # fret
                                           (1, 2, 3, 4, 5) # string number
                                           (0, 1, 2, 3, 4) # tuple index
  Returns A time sequenced list of notes and durations and frets
    List[
      {
        'fret': 3 ,
        'time': 2,
        'string': convert roll pattern to string.
      }
    ]
  """
  string_index_lookup = {
      '1': 0,
      '2': 1,
      '3': 2,
      '4': 3,
      '5': 4
  }

  # roll_pattern T4I3M2 -> T4 I3 M2
  n = 2
  roll = [roll_pattern[i:i+n] for i in range(0, len(roll_pattern), n)]

  output = []

  for finger in roll:  
    string_number = finger[1]
    string_idx = string_index_lookup[string_number]

    # Get the right fret
    fret = chord[string_idx]

    # append the string, duration, and fret to the output object. 
    output.append(
        {
            'fret': fret,
            'time': 2,
            'string': int(string_number)
        }
    )
  return output

def prototab_to_ascii(proto_tab):
  """Takes prototab and returns ascii.
  
  Assume that no notes are played at the same time. Use the duration
  of each note to fill out each string in ascii with either a played
  note or '-' characters. Grow the ascii from left to right.
  """
                   #  1 ,    2,     3,     4,    5
  ascii_strings = [  '|',   '|',   '|',   '|',  '|']
  first_string = 0
  second_string = 1
  third_string = 2
  fourth_string = 3
  fifth_string = 4

  # trinary operator
  # value = option1 if condition true else option2

  for note in proto_tab:
    ascii_strings[first_string]  += str(note['fret']).ljust(note['time'], '-') if note['string'] == 1 else '-'.ljust(note['time'], '-')
    ascii_strings[second_string] += str(note['fret']).ljust(note['time'], '-') if note['string'] == 2 else '-'.ljust(note['time'], '-')
    ascii_strings[third_string]  += str(note['fret']).ljust(note['time'], '-') if note['string'] == 3 else '-'.ljust(note['time'], '-')
    ascii_strings[fourth_string] += str(note['fret']).ljust(note['time'], '-') if note['string'] == 4 else '-'.ljust(note['time'], '-')
    ascii_strings[fifth_string]  += str(note['fret']).ljust(note['time'], '-') if note['string'] == 5 else '-'.ljust(note['time'], '-')

  return ascii_strings

def roll_on_progression(progression, roll_pattern):
  measures = []
  for chord in progression:
    prototab = roll_on_chord(roll_pattern=roll_pattern, chord=chord)
    measures.append(prototab_to_ascii(prototab))
  return measures


def render_ascii_measures(measures):
  "Takes measures and converts to ascii tab"
  lines = [
    ''.join([m[0] for m in measures]),
    ''.join([m[1] for m in measures]),
    ''.join([m[2] for m in measures]),
    ''.join([m[3] for m in measures]),
    ''.join([m[4] for m in measures]),
  ]

  lines = [line + '|' for line in lines]

  return '\n'.join(lines)

CHORDS = generate_all_chords()

if __name__ == '__main__':
  measures = roll_on_progression(
      progression= [
        CHORDS['alpha_major_g5'],
        CHORDS['alpha_major_c6'],
        CHORDS['alpha_major_d6'],
        CHORDS['alpha_major_g5']
        ],
      roll_pattern = 'T4I3M2T3I2M1T4I3M2T3I2M1T512T3M1'
  )
  print(render_ascii_measures(measures))


