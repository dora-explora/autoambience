import mido
from time import sleep
import random

port = mido.open_output() # type: ignore

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
    def __init__(self, name: str, root: int, notes: list[int], tension: int):
        self.name = name
        self.root = root
        self.notes = notes
        self.tension = tension
        self.followups = [] # chords that would work well directly after
        self.followupkeys = [] # the changes in key center that those followups would cause

    def set_followups(self, followups: list['Chord'], followupkeys: list[int]):
        self.followups = followups
        self.followupkeys = followupkeys

def note_name(n: int) -> str: # type: ignore
    match ((n) % 12):
        case 0:
            return "C"
        case 1:
            return "Db"
        case 2:
            return "D"
        case 3:
            return "Eb"
        case 4:
            return "E"
        case 5:
            return "F"
        case 6:
            return "Gb"
        case 7:
            return "G"
        case 8:
            return "Ab"
        case 9:
            return "A"
        case 10:
            return "Bb"
        case 11:
            return "B"

def display_chord(chord: Chord):
    print(f"Playing {note_name(key + chord.root)} {chord.name}")
    print(f"Current key: {note_name(key)}{(key // 12 + 1)}")

def play_chord(chord: Chord, delay: float):
    global tension
    tension += chord.tension
    display_chord(chord)
    print(f"tension: {tension}")
    for note in chord.notes:
        port.send(mido.Message('note_on', note=(note + key)))
    port.send(mido.Message('note_on', note=0))
    sleep(0.01)
    port.send(mido.Message('note_off', note=0))

    for pressure in range(128):
        port.send(mido.Message('aftertouch', value=pressure))
        sleep(delay)

    for note in chord.notes:
        port.send(mido.Message('note_off', note=(note + key)))
    sleep(delay * 3)

IM9 = Chord("major 9", 0, [0, 9, 12, 19, 23, 26, 33, 38], -8) # base I major 9 to start the song with
iim7 = Chord("minor 7", 2, [2, 9, 17, 24, 29, 33, 36, 43], +2) # simple ii minor 7 to move the song along
IVM6_u3 = Chord("major 6, raising the key by a minor third", 5, [5, 12, 21, 26, 33, 36, 38, 40], +11) # IV major 6 that comes with a jump 3 tones up in key center
VM6_sii = Chord("major 6 / ii, setting up a ii-V-I", 7, [2, 7, 14, 19, 23, 28, 31, 35, 38, 40], +5)
IM7 = Chord("major 7 with the 3rd on top", 0, [0, 7, 12, 19, 23, 24, 28, 31, 35, 36, 40], -8)
# IM6_d12 = Chord("major 6, pushing key down an octave", 0, [0, 12, 19, 24, 31, 33, 36, 40, 43, 45], -1)
IVM7 = Chord("major 7", 5, [5, 12, 17, 24, 28, 29, 33, 36, 40, 41, 45], -3)
III7 = Chord("dominant 7, setting up a IV-III-I", 4, [4, 11, 16, 23, 26, 28, 32, 35, 38, 40, 44], +14)
IM9_u5 = Chord("major 9, raising the key by a fourth", 0, [0, 7, 12, 19, 23, 26, 28, 31, 35, 38], -11)

IM9.set_followups([iim7, IVM7], [0, 0])
# iim7.set_followups([VM6_sii, IM6_d12, IVM6_u3], [0, -12, +3])
iim7.set_followups([VM6_sii, IVM6_u3], [0, +3])
VM6_sii.set_followups([IM7, IVM6_u3], [0, +3])
# IM7.set_followups([IM6_d12, iim7, IVM7], [-12, 0, 0])
IM7.set_followups([IVM7, iim7], [0, 0])

IVM7.set_followups([IM7, III7], [0, 0])
III7.set_followups([IM9_u5, IM7], [5, 0])
# IM9_u5.set_followups([IM6_d12, iim7], [-12, 0])
IM9_u5.set_followups([iim7], [-0])

# IVM6_u3.set_followups([IM9, IM6_d12], [0, -12])
IVM6_u3.set_followups([IM9], [0])
# IM6_d12.set_followups([IM9, IVM6_u3], [0, +3])

key = 36
delay = 0.1
chord = IM9
play_chord(chord, delay)
for i in range(12):
    next_chord_index = random.randint(0, len(chord.followups) - 1)
    key += chord.followupkeys[next_chord_index]
    chord = chord.followups[next_chord_index]
    play_chord(chord, delay)