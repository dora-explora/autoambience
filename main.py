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

def display_key(key: int) -> str:
    return f"{note_name(key)}{(key // 12 + 1)}"

def display_chord(chord: Chord, key: int) -> str:
    return f"{note_name(key + chord.root)} {chord.name}"

def display_recent_chords(recent_chords: list[tuple[Chord, int]]) -> str:
    return f"{display_chord(recent_chords[0][0], recent_chords[0][1])} | {display_chord(recent_chords[1][0], recent_chords[1][1])} | {display_chord(recent_chords[2][0], recent_chords[2][1])}"

def play_chord(chord: Chord, delay: float):
    global tension
    tension += chord.tension
    print(f"\nPlaying", display_chord(chord, key))
    print("Key:", display_key(key))
    print(f"Tension:", tension)
    print(f"Tension rising:", tension_rising)
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

def too_similar(candidate: tuple[Chord, int], recent_chords: list[tuple[Chord, int]]) -> bool:
    if candidate == recent_chords[1] and candidate[0].root != 0:
        return True
    elif candidate == recent_chords[2] and recent_chords[0] == recent_chords[3]:
        return True
    else:
        return False

def main():
    global tension
    global tension_rising
    tension = 10 # how high the tension of the music is
    tension_rising = True # if tension is supposed to be rising

    global key
    key = randint(30, 36)
    delay = 9
    chord = IM9
    recent_chords = [(IM9, key), (IM9, key), (IM9, key), (IM9, key), (IM9, key)]
    play_chord(chord, delay)

    while True:
        offset = 0
        chord_options = len(chord.followups)
        if chord_options > 1:
            if tension_rising: offset = 1
            weights = []
            for i in range(chord_options):
                weights.append((((i + 1) / (chord_options + 1)) - 1) ** 2) # dont even ask
            while True:
                next_chord_index = choices(range(chord_options), weights=weights, k=1)[0]
                next_chord_index += offset
                next_chord_index %= chord_options
                if too_similar((chord.followups[next_chord_index], key + chord.followupkeys[next_chord_index]), recent_chords): 
                    weights[next_chord_index - offset] = 0
                else: break
        key += chord.followupkeys[next_chord_index]
        chord = chord.followups[next_chord_index]
        if key > 38 and (chord == IM7 or chord == IM9):
            key -= 12
            chord = IM_d12
        
        recent_chords.pop()
        recent_chords.insert(0, (chord, key))

        if (tension >= 25 and tension_rising) or ((tension <= 5) and not tension_rising):
            tension ^= True

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