from musical.theory import Note
from musical.audio import source
from musical.audio import play

import matplotlib.pyplot as plt 

class Hit:

  ''' Rough draft of Hit class. Stores information about the hit and generates
      the audio array accordingly. Currently implements a basic cache to avoid
      having to rerender identical hits
  '''

  cache = {}

  def __init__(self, note, length):
    self.note = note
    self.length = length

  def render(self):
    # Render hit of "key" for "length" amound of seconds
    # XXX: Currently only uses a string pluck
    key = (str(self.note), self.length)
    if key not in Hit.cache:
      Hit.cache[key] = source.pluck(self.note, self.length)
    return Hit.cache[key]


g3 = Note('g3')

hit_note = Hit(note=g3, length=2)

rendered_note = hit_note.render()

print(rendered_note)

plt.plot(rendered_note)
plt.show()

play(rendered_note)