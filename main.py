import mido
from time import sleep
from random import randint, choices
from chords import *
import os
from sys import exit

port = mido.open_output() # type: ignore

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
    print(f"Current key center: {note_name(key)}{(key // 12 + 1)}")

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
        sleep(delay / 128)

    for note in chord.notes:
        port.send(mido.Message('note_off', note=(note + key)))
    sleep(delay / 40)

def main():
    global tension
    tension = 10 # how high the tension of the music is
    tension_goal = 0 # how high the tension *should* be; set randomly
    tension_rising = False # if tension is supposed to be rising

    global key
    key = 36
    delay = 15
    chord = IM9
    recent_chords = [IM9, IM9, IM9]
    play_chord(chord, delay)
    while True:
        if ((tension >= tension_goal) and tension_rising) or ((tension <= tension_goal) and not tension_rising):
            if tension_rising == True:
                tension_rising = False
                tension_goal = randint(0, 10)
                print(f"\nhigh tension met!\nnew tension goal: {tension_goal}\n")
            else:
                tension_rising = True
                tension_goal = randint(20, 30)
                print(f"\nlow tension met!\nnew tension goal: {tension_goal}\n")

        next_chord_index = 0
        chord_options = len(chord.followups)
        if chord_options > 1:
            if tension_rising: next_chord_index = 1
            weights = []
            for i in range(chord_options):
                weights.append((((i + 1) / (chord_options + 1)) - 1) ** 2) # dont even ask
            next_chord_index += choices(range(chord_options), weights=weights, k=1)[0]
            next_chord_index %= chord_options
        key += chord.followupkeys[next_chord_index]
        chord = chord.followups[next_chord_index]
        recent_chords.pop()
        recent_chords.insert(0, chord)
        if key > 38 and (chord == IM7 or chord == IM9):
            key -= 12
            chord = IM_d12
        play_chord(chord, delay)

# thank you stack overflow
try:
    main()
except KeyboardInterrupt:
    print("\nbye!")
    port.reset()
    try:
        exit(130)
    except SystemExit:
        os._exit(130)