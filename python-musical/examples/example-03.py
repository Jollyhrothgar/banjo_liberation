import numpy

from musical.theory import Note
from musical.theory import Scale
from musical.audio import source
from musical.audio import play

# Define key and scale
key = Note('C4')
scale = Scale(key, 'major')

note = key
chunks = []
for i in range(len(scale)):
    third = scale.transpose(note, 2)
    chunks.append(source.sine(note, 0.5) + source.square(third, 0.5))
    note = scale.transpose(note, 1)
fifth = scale.transpose(key, 4)
chunks.append(source.sine(key, 1.5) + source.square(fifth, 1.5))

print("Rendering audio...")

data = numpy.concatenate(chunks)

# Reduce volume to 50%
data = data * 0.5

print("Playing audio...")

play(data)

print("Done!")
