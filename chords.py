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


IM9 = Chord("major 9", 0, [0, 12, 19, 23, 26, 33, 38], -10, 0) # base I major 9 to start the song with
iim7 = Chord("minor 7", 2, [2, 9, 17, 24, 29, 33, 36, 43], +2, 0) # simple ii minor 7 to move the song along
IVM69_u3 = Chord("major 6-9, raising the key by a minor third", 5, [5, 12, 21, 26, 33, 36, 38, 40, 43], +11, +3) # IV major 6 that comes with a jump 3 tones up in key center
VM6_sii = Chord("major 6 / ii, setting up a ii-V-I", 7, [2, 7, 14, 19, 23, 28, 31, 35, 38, 40], +5, 0)
IM7 = Chord("major 7 with the 3rd on top", 0, [0, 7, 12, 16, 19, 23, 24, 28, 31, 35, 36, 40], -8, 0)
IM_d12 = Chord("major 7, pushing key down an octave", 0, [0, 12, 19, 24, 31, 35, 36, 40, 43, 47], -6, -12)
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