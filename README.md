# Ironseed-py
Iron Seed is a science-fiction DOS game from 1994, which was both developed and published by Channel 7.
Gameplay is real-time, featuring trading, diplomacy, and strategy.
This repository contains an in-development Python version of the game engine.
The engine, as it stands, is not 1 to 1 for functionality with the DOS version.  However, where possible, areas that have been implemented have been done so with modern mechanics in mind.  This generally extends to making the interfaces more pleasent to use, while using upscaled graphics and higher-resolution procedural textures where possible.  The native resolution of the original is 320x200, this version runs at 640x480 with the necessary logic for dynamic resolution sizes in the future.

It is very possible that several graphic sets may be offered in the future, original, enhanced and... no, that'll be a surprise.  I am making this with the idea that those wanting to add mods will have an easier time in the future; the game state engine makes this much easier overall.

I am not interested in implementing this as a 3D engine at this time, this is a learning project, with the idea being to use the ancient 2D and 2.5D techniques where possible.  However, modern techniques using lighting could be implemented, like bump-mapping.

Note: Various early areas of the game engine are testable, including the intro, new game generator and the ego synth manipulator.

From Nuke Bloodaxe on COVID-19 or SARS-COV2:  Updates will be real slow as I am working from home due to a countrywide lockdown in New Zealand, and have a lack of free time to do as much as I would like.  Commits will occur as time is freed up.
