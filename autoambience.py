import mido
from time import sleep

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

maj7 = [0, 7, 16, 23, 28, 31, 35]
maj9 = [0, 7, 16, 23, 28, 31, 35, 38]
# maj9 = [0, 12, 16, 19, 23, 24, 26, 28, 31, 35, 36, 38] alternate voicing, also yoinked from Somebody Real
min7 = [0, 7, 15, 22, 27, 31, 34]
min9 = [0, 7, 15, 22, 27, 31, 34, 38]
min11 = [0, 7, 15, 22, 27, 31, 34, 38, 41]

def play_chord(root: int, notes: list[int], delay: float):
    for note in notes:
        port.send(mido.Message('note_on', note=(note + root)))

    for pressure in range(128):
        port.send(mido.Message('aftertouch', value=pressure))
        sleep(delay)

    for note in notes:
        port.send(mido.Message('note_off', note=(note + root)))
    sleep(delay * 3)

# reference: Somebody Real by Evan Alderete
play_chord(Ab, maj9, 0.1)
play_chord(G, min9, 0.1)

# play_chord(F, maj7, 0.1)
# play_chord(B, min11, 0.1)
# play_chord(D, maj7, 0.11)
# play_chord(Db, min7, 0.09)
# play_chord(A, maj9, 0.1)