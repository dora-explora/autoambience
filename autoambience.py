import mido
from time import sleep

port = mido.open_output()

C = 36
E = 40

Maj7 = [0, 7, 16, 23, 28, 31, 35]
Maj9 = [0, 7, 16, 23, 28, 31, 35, 38]
pressures = [0, 4, 8, 13, 17, 22, 26, 31, 35, 39, 43, 47, 50, 54, 57, 61, 64, 67, 70, 73, 76, 79, 82, 85, 87, 90, 92, 94, 97, 99, 101, 103, 104, 106, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 118, 119, 119, 119, 120, 120, 120, 120, 120, 119, 119, 119, 118, 118, 117, 116, 115, 114, 113, 112, 111, 109, 108, 106, 104, 103, 101, 99, 97, 94, 92, 90, 87, 85, 82, 79, 76, 73, 70, 67, 64, 61, 57, 54, 50, 47, 43, 39, 35, 31, 26, 22, 17, 13, 8, 4, 0]

def play_chord(root: int, notes: list[int], delay: float):
    for note in notes:
        port.send(mido.Message('note_on', note=(note + root)))

    for pressure in pressures:
        port.send(mido.Message('aftertouch', value=pressure))
        sleep(delay)

    for note in notes:
        port.send(mido.Message('note_off', note=(note + root)))
    sleep(delay)

play_chord(C, Maj7, 0.1)
play_chord(E, Maj9, 0.1)