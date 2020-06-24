# Ironseed-py
Iron Seed is a science-fiction DOS game from 1994, which was both developed and published by Channel 7.
Gameplay is real-time, featuring trading, research, manufacturing, diplomacy, "realistic" space combat, on-edge crew members, and strategy.
This repository contains an in-development Python 3 version of the game engine, using Pygame for sound and graphics support.
The engine, as it stands, is not 1 to 1 for functionality with the DOS version.  However, where possible, areas that have been implemented have been done so with modern mechanics in mind.  This generally extends to making the interfaces more pleasent to use, while using upscaled graphics and higher-resolution procedural textures where possible.  The native resolution of the original is 320x200, this version runs at 640x480 with the necessary logic for dynamic resolution sizes in the future.

It is very possible that several graphic/music/sound sets may be offered in the future, original, enhanced and... no, that'll be a surprise.  I am making this with the idea that those wanting to add mods will have an easier time in the future; the game state engine makes this simpler overall.

I am not interested in implementing this as a 3D engine at this time, this is a learning project, with the idea being to use ancient 2D and 2.5D techniques where possible; and sometimes the findings of an occasional professor who has worked out how to do some things better.  However, modern techniques using lighting could be implemented, like bump-mapping.

Note: Various early areas of the game engine are testable, including the intro, new game generator, planet scanner, and the ego synth manipulator.  The command deck, to tie all those together, is a big project in itself, so you can skip between them by changing the state target for each on state exit; at the code level, just look at the return parameter for each class/module, and where it is getting it, and where it would go if it was changed [see main ironSeed.py module for a list of all states].  I use this method for chain-testing modules.

From Nuke Bloodaxe on COVID-19 or SARS-COV2:  The lockdown may be over, but things have not gotten any easier.  I am working on the project as time is freed up, commits will occur infrequently for a while; probably when I get my next holiday break.  In the mean-time, I am experimenting with and learning from aidungeon.io .  I am very intrigued about how it works, and am thinking it might be a viable system for the crew and ship communications systems at a later date.
