import mido
from random import randint, choices
import time
import asyncio
from urwid import * # type: ignore
import threading
import sys

class Chord:
    def __init__(self, name: str, root: int, notes: list[int], tension: int, keychange: int):
        self.name = name
        self.root = root
        self.notes = notes
        self.tension = tension
        self.keychange = keychange
        self.followups = [] # chords that would work well directly after
        self.followupkeys = [] # the changes in key center that those followups would cause

    def set_followups(self, followups: list['Chord']):
        self.followups = followups
        self.followupkeys = []
        for chord in followups:
            self.followupkeys.append(chord.keychange)

IM9 = Chord("major 9", 0, [0, 12, 19, 23, 26, 33, 38], -10, 0) # base I major 9 to start the song with
iim7 = Chord("minor 7", 2, [2, 9, 17, 24, 29, 33, 36, 43], +2, 0) # simple ii minor 7 to move the song along
IVM69_u3 = Chord("major 6-9, raising the key by a minor third", 5, [5, 12, 21, 26, 33, 36, 38, 40, 43], +11, +3) # IV major 6 that comes with a jump 3 tones up in key center
VM6_sii = Chord("major 6 / ii, setting up a ii-V-I", 7, [2, 7, 14, 19, 23, 28, 31, 35, 38, 40], +5, 0)
IM7 = Chord("major 7 with the 3rd on top", 0, [0, 7, 12, 16, 19, 23, 24, 28, 31, 35, 36, 40], -8, 0)
IM_d12 = Chord("major 7, pushing  the key down an octave", 0, [0, 12, 19, 24, 31, 35, 36, 40, 43, 47], -6, -12)
IVM7 = Chord("major 7", 5, [5, 12, 17, 24, 28, 29, 33, 35, 36, 40, 41, 45], -3, 0)
III7 = Chord("dominant 7, setting up a IV-III-I", 4, [4, 11, 16, 23, 26, 28, 32, 35, 38, 40, 44], +14, 0)
IM9_u5 = Chord("major 9, raising the key by a fourth", 0, [0, 7, 12, 19, 23, 26, 28, 31, 35, 38], -4, +5)


IM9.set_followups([IVM7, iim7])
iim7.set_followups([VM6_sii, IVM69_u3])
VM6_sii.set_followups([IM7, IVM69_u3])
IM7.set_followups([IVM7, iim7])

IVM7.set_followups([IM7, III7])
III7.set_followups([IM7, IM9_u5, iim7])
IM9_u5.set_followups([IM9, IM7, iim7])

IVM69_u3.set_followups([IM9, IM7])
IM_d12.set_followups([IVM7, iim7, IVM69_u3])

port = mido.open_output() # type: ignore
playing = False

tension = 10 # how high the tension of the music is
tension_rising = True # if tension is supposed to be rising
tension_oscillating = True

key = randint(30, 35)
delay = 15
chord = IM9
recent_chords = [(IM9, key), (IM9, key), (IM9, key), (IM9, key)]

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

def update_current_chord(chord: Chord, key: int):
    current_chord.base_widget.set_text(f"Currently playing: {display_chord(chord, key)}") # type: ignore
    recent_chord_A.base_widget.set_text(display_chord(recent_chords[1][0], recent_chords[1][1])) # type: ignore
    recent_chord_B.base_widget.set_text(display_chord(recent_chords[2][0], recent_chords[2][1])) # type: ignore
    recent_chord_C.base_widget.set_text(display_chord(recent_chords[3][0], recent_chords[3][1])) # type: ignore

async def play_chord(chord: Chord, delay: float):
    global tension
    tension += chord.tension
    update_current_chord(chord, key)
    current_chord.base_widget._invalidate()
    for note in chord.notes:
        port.send(mido.Message('note_on', note=(note + key)))
    port.send(mido.Message('note_on', note=0))
    await asyncio.sleep(0.01)
    port.send(mido.Message('note_off', note=0))

    for pressure in range(128):
        port.send(mido.Message('aftertouch', value=pressure))
        await asyncio.sleep(delay / 128)

    for note in chord.notes:
        port.send(mido.Message('note_off', note=(note + key)))
    await asyncio.sleep(delay / 40)

def too_similar(candidate: tuple[Chord, int], recent_chords: list[tuple[Chord, int]]) -> bool:
    if candidate == recent_chords[1] and candidate[0].root != 0:
        return True
    elif candidate == recent_chords[2] and recent_chords[0] == recent_chords[3]:
        return True
    else:
        return False

async def play_chords():
    global chord
    global key
    global tension
    await play_chord(chord, delay)
    while playing:
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
        
        if tension_oscillating:
            if (tension >= 25 and tension_rising) or ((tension <= 5) and not tension_rising): tension ^= True

        await play_chord(chord, delay)

def play(loop: asyncio.EventLoop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(play_chords())

def on_play_pause_press(button: Button):
    global playing
    loop = asyncio.new_event_loop()
    if button.label == "Start":
        button.set_label("Pause")
        playing = True
        threading.Thread(target=play, args=(loop,), daemon=True).start()
    else:
        button.set_label("Start")
        playing = False
        # port.reset()
        current_chord.base_widget.set_text("Make sure Vital is open before playing!") # type: ignore
        recent_chord_A.base_widget.set_text("^That^ will display the current chord") # type: ignore
        recent_chord_B.base_widget.set_text("These will display the most recent chords") # type: ignore
        recent_chord_C.base_widget.set_text("") # type: ignore
        
def on_tension_press(button: Button):
    global tension_rising
    global tension_oscillating
    if button.label == "Tension: High":
        tension_rising = False
        button.set_label("Tension: Low")
    elif button.label == "Tension: Low":
        tension_rising = True
        button.set_label("Tension: Oscillating")
    elif button.label == "Tension: Oscillating":
        tension_rising = True
        tension_oscillating = False
        button.set_label("Tension: High")

def on_speed_press(button: Button):
    global delay
    if button.label == "Speed: 9 s/c":
        delay = 12
        button.set_label("Speed: 12 s/c")
    elif button.label == "Speed: 12 s/c":
        delay = 15
        button.set_label("Speed: 15 s/c")
    elif button.label == "Speed: 15 s/c":
        delay = 18
        button.set_label("Speed: 18 s/c")
    elif button.label == "Speed: 18 s/c":
        delay = 21
        button.set_label("Speed: 21 s/c")
    elif button.label == "Speed: 21 s/c":
        delay = 9
        button.set_label("Speed: 9 s/c")

def stop():
    raise ExitMainLoop

title = Padding(Text("Welcome to AutoAmbience!\nTo quit, press 'q', and then exit Vital.", 'center'), 'center', 'pack')

play_pause_button = Button("Start", on_play_pause_press, align='center')
tension_button = Button("Tension: Oscillating", on_tension_press, align='center')
speed_button = Button("Speed: 15 s/c", on_speed_press, align='center')
current_chord = Padding(Text(f"Make sure Vital is open before playing!", 'center'), 'center', 'pack')
recent_chord_A = Padding(AttrMap(Text(f"", 'center'), 'recent'), 'center', 'pack')
recent_chord_B = Padding(AttrMap(Text(f"Recently played chords go here!", 'center'), 'recent'), 'center', 'pack')
recent_chord_C = Padding(AttrMap(Text(f"", 'center'), 'recent'), 'center', 'pack')
buttons = Columns([play_pause_button, tension_button, speed_button], 2)

divider = Divider('-', 1, 1)
pile = Pile([title, divider, buttons, divider, current_chord, recent_chord_A, recent_chord_B, recent_chord_C])

main = Overlay(
    Filler(Padding(pile, 'center', 'pack', left=2, right=2)),
    SolidFill('#'),
    align=CENTER,
    width=(RELATIVE, 100),
    valign=MIDDLE,
    height=(RELATIVE, 100),
    left=1,
    right=1,
    top=1,
    bottom=1
)

palette = [
    ('recent', 'dark gray',  'default'),
]

on_play_pause_press(play_pause_button)
main_loop = MainLoop(main, palette = palette, unhandled_input = lambda key: stop() if key in ('q', 'Q') else None).run()

port.reset()