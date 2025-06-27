import mido
from time import sleep
import random

port = mido.open_output()

C = 24
Db = 25
D = 26
Eb = 27
E = 28
F = 29
Gb = 30
G = 31
Ab = 32
A = 33
Bb = 34
B = 35

# Voicing -> MIDI key:
#
# Root: 0
# Fifth: 7
# Octave: 12
# Minor Third: 15
# Major Third: 16
# Fifth: 19
# Sixth: 21
# Minor 7th: 22
# Major 7th 23
# Octave: 24
# 9th: 26
#
# Up a fifth is +7
# Up a major third is +4
# Up a minor third is +3
# Whole step and half step are +2 and +1, of course

tension = 20 # how high the tension of the music is
tension_goal = 0 # how high the tension *should* be; set randomly

maj7 = [0, 7, 16, 23, 28, 31, 35]
maj6 = [0, 7, 16, 21, 28, 31, 33]
maj9 = [0, 7, 16, 23, 28, 31, 35, 38]
# maj9 = [0, 12, 19, 23, 26] # alternate voicing yoinked from Somebody Real
min7 = [0, 7, 15, 22, 27, 31, 34] 
# min7 = [0, 12, 19, 22, 26] # alternate voicing also yoinked from Somebody Real
min9 = [0, 7, 15, 22, 27, 31, 34, 38]
# min9 = [0, 12, 19, 22, 26] # alternate voicing also yoinked from Somebody Real
min11 = [0, 7, 15, 22, 27, 31, 34, 38, 41]

class Chord:
    def __init__(self, name: str, numeral: int, notes: list[int], tension: int):
        self.name = name
        self.numeral = numeral
        self.notes = notes
        self.tension = tension
        self.followups = [] # chords that would work well directly after
        self.followupkeys = [] # the changes in key center that those followups would cause

    def set_followups(self, followups: list['Chord'], followupkeys: list[int]):
        self.followups = followups
        self.followupkeys = followupkeys

I9 = Chord("I major 9", 1, [0, 12, 19, 23, 26, 33, 38], -8) # base I major 9 to start the song with
ii7 = Chord("ii minor 7", 2, [2, 9, 17, 24, 29, 33, 36, 43], -2) # simple ii minor 7 to move the song along
IV6_u3 = Chord("IV major 6, raising key by 3 semitones", 1, [5, 12, 21, 26, 33, 36, 38], +11) # IV major 6 that comes with a jump 3 tones up in key center

I9.set_followups([ii7], [0])
ii7.set_followups([IV6_u3], [3])
IV6_u3.set_followups([I9], [0])

def play_root_chord(root: int, notes: list[int], delay: float):
    for note in notes:
        port.send(mido.Message('note_on', note=(note + root)))

    for pressure in range(128):
        port.send(mido.Message('aftertouch', value=pressure))
        sleep(delay)

    for note in notes:
        port.send(mido.Message('note_off', note=(note + root)))
    sleep(delay * 3)

def play_chord(chord: Chord, delay: float) -> int:
    global tension
    tension += chord.tension
    print(f"chord name: {chord.name}\ntension: {tension}\nkey: {key}")
    for note in chord.notes:
        port.send(mido.Message('note_on', note=(note + key)))

    for pressure in range(128):
        port.send(mido.Message('aftertouch', value=pressure))
        sleep(delay)

    for note in chord.notes:
        port.send(mido.Message('note_off', note=(note + key)))
    sleep(delay * 3)

# # reference: Somebody Real by Evan Alderete
# play_chord(Ab, maj9, 0.1)
# play_chord(G, min7, 0.1)
# play_chord(F, min7, 0.1)

# small test progression
# play_root_chord(F, maj7, 0.1)
# play_root_chord(B, min11, 0.1)
# play_root_chord(D, maj7, 0.11)
# play_root_chord(Db, min7, 0.09)
# play_root_chord(A, maj9, 0.1)

key = 26
delay = 0.2
chord = I9
play_chord(chord, delay)
for i in range(7):
    next_chord_index = random.randint(0, len(chord.followups) - 1)
    key += chord.followupkeys[next_chord_index]
    chord = chord.followups[next_chord_index]
    play_chord(chord, delay)