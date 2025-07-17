# Auto Ambience
**An automatic ambient music generator made with Python and Vital!**

## Installation and Usage
1. Clone the repository
2. [Install Vital](https://vital.audio/) (which unfortunately requires an account 😭)
3. Open Vital, click the ≡ icon, and select "Open External Preset"
4. Navigate to the repository and select "autoambience.vital"

To use, you can either run "pip install -r requirements.txt" in the repository and then run "main.py" or use one of the executables included in the release (sorry Mac users, I don't have one to compile on)

Then program, relax, zone out, or do whatever to some infinite ambient music!

## Controls
When run in a terminal, AutoAmbience has a text interface that can be used to play/pause the chords, change the tension mode, and change the rate at which chords are played.

The leftmost button is a simply play/pause button. Pressing it starts playing the music after beginning the program. Pressing it again waits for the current chord to finish before stopping it.

The middle button rotates the tension setting between these 3 options:
1. High Tension - the script will be more likely to choose more tense or exciting options
2. Low tension - the script will be more likely to choose more calm or common options
3. Oscillating tension - the script will change between the two modes automatically, switching when the cumulative tension is high or low

The last button rotates between 5 values for the chord rate, measured in seconds per chord. These values are 9 s/c, 12 s/c, 15 s/c, 18 s/c, and 21 s/c.

Below the buttons, there is also a small display that shows the chord playing currently, and the three chords before it. Unfortunately, due to limitations imposed by the TUI library I'm using (urwird), this doesn't update unless a graphics update is imposed, like switching between the buttons or resizing the window. 

<div align="center">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>