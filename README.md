# Ironseed-py
Iron Seed is a science-fiction DOS game from 1994, developed and published by Channel 7.

Gameplay is real-time, featuring trading, research, manufacturing, diplomacy, "realistic" space combat, on-edge crew members, and strategy.
The procedural nature of the game engine creates a rogue-like universe for each new playthrough, featuring ten core empires and a multitude of others which can evolve during the game.  

This repository contains an in-development Python 3 version of the game engine, using Pygame for sound and graphics support.

## The Story

Humanity has entered the thirty-eighth century, and Earth is but a dream, a dead world evacuated in desperation to a terraformed Mars.
Mars is ruled by the iron fist of the Pentiarch, a group of five priests leading this newly arisen democratic technocracy.

In a bold attempt to eliminate their political rivals, the Pentiarch initiated the Purgation Trials, an inquisition-like movement seeking to purge all who would oppose them.
With their rule almost absolute, their rivals enslaved in the mines of Phobos or permanently imprisoned in ego-synth-banks, a counter-movement initiated a daring plan.
A virus was spread throughout the personality matrix of Mars, timed to detonate its payload in 1000 days and destroy the personalities of all whom it infected.

The IronSeed movement, as it was called, evacuated Mars during a violent final confrontation, leaving behind their bodies and taking with them the personality files of the oppressed.  Using a stolen ship, and now existing only as beings of synthetic liquid in sealed jars, they powered their engines to full and departed Mars, intending to return after the Virus had destroyed the Pentiarch.  However, the best-laid plans seldom proceed as intended, and after a buffer-overflow bug in the chronometer of the ship's computer, their stasis of 1000 days became 1000 years.

As PRIME and the Laird of the crew, you are rudely awakened by an Alien battle armada.  After a terse exchange of words, they attack, and you come off second-best.
The game begins after the battle has ended.

## The State of Play

The engine, as it stands, is not 1 to 1 for functionality with the DOS version.  However, where possible, areas that have been implemented have been done so with modern mechanics in mind.  This generally extends to making the interfaces more pleasant while using upscaled graphics and higher-resolution procedural textures where possible.  The native resolution of the original is 320x200; this version runs at 640x480 with the necessary logic for dynamic resolution sizes in the future.  Where necessary, some graphical elements have been repaired compared to the original, as some graphics were "less than optimal" when they shipped due to the tools the developers were using at the time.  The original also utilised the palette cycling feature of the Pascal language. For simplicity, I am using masks and modular graphics where possible; this will also enhance portability to other languages while avoiding the limitations of the gamepy and SDL shim.

### Future plans

Several graphic/music/sound sets may be offered in the future, original, enhanced and... no, that'll be a surprise.  I am making this with the idea that those wanting to add mods will have an easier time later; the game state engine simplifies this.

## Engine Aim

I am not interested in implementing this as a 3D engine at this time; this is a learning project, with the idea being to use ancient 2D and 2.5D techniques where possible, and sometimes the findings of an occasional professor who has worked out how to do some things better.  However, modern techniques using lighting could be implemented, like bump-mapping.

## What is Happening Where

The Projects tab for this repository contains the areas being worked on, and progress in each.  Due to the highly modular nature of IronSeed, these can be treated as independent sub-projects for the most part.

##  Stuff that "Runs"; Like a Three-Legged Horse

Various early areas of the game engine are testable, including the intro, new game generator, planet scanner, and the ego synth manipulator.  The command deck has enough functionality to use the cube button interface, and you can go to some of the in-development areas mentioned above.

#### Execution Routine of Alpha
In the terminal, navigate to the IronSeed folder.  Run the following command set, assuming you already have pip installed.
1) python3 -m pip install -r requirements.txt
2) python3
3) import ironSeed
4) game = ironSeed.IronSeed()
5) Now wait until the initialisation is finished, a true test of the computational power of your PC.  (We Are GO!)
6) game.main_loop()

## Data Storage

Many systems and data were stored in binary, which created its own issues.  These have been converted to plain text and open standard graphics and sound where possible.  Save games and associated data will be stored in plain text, allowing cheating and easy portability + version upgrades + "exotic testing".  With plain-text save games, it is also possible to insert Mods into previously existing games, enhancing flexibility further.

# Developer Notice

From Nuke Bloodaxe on COVID-19 or SARS-COV2:  As essential personnel during this time, I have to work; harder.  I am adding to this project as time is freed up; commits will occur infrequently for a while, probably until I get my next holiday break, which always seems to elude my grasp.  In the meantime, I am experimenting with and learning from aidungeon.io .  I am intrigued by its functionality, primitive as it is, and think it might be a viable system for the crew and ship communications systems later.

06/12/2021:  My holiday break is approaching, and Otzen inspired me in terms of some of the things he was looking at.  The critical area of work is an initialisation screen, which revealed some double-load bugs that have now been corrected.  The screen will be expanded with extra functions, including load timers, prettier bars, etc, in the future.  Once that is mostly ready, I have a variety of screens which need their button functions implemented.

04/01/2023:  2022 was a challenging year, and 2023 looks to be much the same, so I'll add code here and there as I can.  Some optimization is already being added to improve the rendering speed of planets.  I am particularly interested in the pixel-spray functionality required by the interface cube on the main deck.

23/07/2023:  Work is not slowing down, that is for sure.  I've acquired a VisionFive 2, this is RISC-V, which I'll have as an extra target platform for Ironseed-py.  At the moment, gamepy and other critical tools are not running on it, but this is very much a prototype, so in the future, I hope it'll just work; then, I can do some benchmarks.

I've also turned on the discussion forum. Please join in and ask those questions you've wanted to ask without making a formal issue request.
