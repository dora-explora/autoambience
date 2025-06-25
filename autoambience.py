import mido
from time import sleep
import numpy

port = mido.open_output()

notes = [60, 64, 67, 71]
pressures = [0, 4, 8, 13, 17, 22, 26, 31, 35, 39, 43, 47, 50, 54, 57, 61, 64, 67, 70, 73, 76, 79, 82, 85, 87, 90, 92, 94, 97, 99, 101, 103, 104, 106, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 118, 119, 119, 119, 120, 120, 120, 120, 120, 119, 119, 119, 118, 118, 117, 116, 115, 114, 113, 112, 111, 109, 108, 106, 104, 103, 101, 99, 97, 94, 92, 90, 87, 85, 82, 79, 76, 73, 70, 67, 64, 61, 57, 54, 50, 47, 43, 39, 35, 31, 26, 22, 17, 13, 8, 4, 0]

for note in notes:
    port.send(mido.Message('note_on', note=note))

for pressure in pressures:
    port.send(mido.Message('aftertouch', value=pressure))
    sleep(0.05)

for note in notes:
    port.send(mido.Message('note_off', note=note))