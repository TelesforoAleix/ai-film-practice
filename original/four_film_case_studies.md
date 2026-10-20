# Four film case studies

These cases were manually inspected in the live signed-out browser on 19 October 2026. Counts below are computed from the exported records, not inferred from UI percentages.

## Cosmic tracks

- Project: https://higgsfield.ai/@ahmed_atef/projects/cosmic-tracks
- Creator: ahmed_atef
- Approach: A multi-world fantasy with character continuity and deliberately different environments.
- Export: 195 distinct generations, 193 generation records with a nonempty primary prompt, 16 folders and 239 asset entities.
- Models observed: Nano Banana 2, Seedance 2.0, Gemini Omni Flash 1.1, Seedance 2.5, Nano Banana Pro, Soul Cinematic, FLUX.2, GPT Image 2.0, Cinematic Studio Soul Location, GPT Image 2.5, Seedream 4.5, Voiceover.

The brief specifies contemporary realism, a 1930s speakeasy, a neon city and an ancient world. The visible organization separates Main character and Scene 1–4, with nested resources. The model stack is broad. The inspected poster prompt explicitly separates subject, environment, world regions, lighting, composition and style.

**Manual cross-check.** Browser: 6:18, 195 generations, All assets 255; poster generation Nano Banana 2, 2k, 3168×1344. The API returns 231 recursive item rows and 195 unique generation IDs. A direct-folder recovery pass adds uploads and placements omitted by the recursive response; the generation count reconciles.

**Public folder structure.**

- /Cosmic tracks
- /Cosmic tracks/All assets
- /Cosmic tracks/Main character
- /Cosmic tracks/Main character/Assets
- /Cosmic tracks/Scene 1
- /Cosmic tracks/Scene 1/S1 Assets
- /Cosmic tracks/Scene 1/Videos
- /Cosmic tracks/Scene 2
- /Cosmic tracks/Scene 2/S2 Assets
- /Cosmic tracks/Scene 2/Videos
- /Cosmic tracks/Scene 3
- /Cosmic tracks/Scene 3/S3 Assets
- /Cosmic tracks/Scene 3/Videos
- /Cosmic tracks/Scene 4
- /Cosmic tracks/Scene 4/videos
- /Cosmic tracks/Watermarks

**Qualification.** This case is retained as a supplemental pilot outside the selected/popular 186-film set.

## The Kiss

- Project: https://higgsfield.ai/@seifhussam/projects/the-kiss
- Creator: seifhussam
- Approach: A character-driven jealousy narrative combining a candy-game world with spatial references.
- Export: 391 distinct generations, 383 generation records with a nonempty primary prompt, 13 folders and 429 asset entities.
- Models observed: Seedream 5.0 Pro, Nano Banana Pro, Seedance 2.5, Cinematic Video Editor, Cinema Studio 4.0, GPT Image 2.0, Soul Cinema Studio, Higgsfield Soul V2, Seedream 4.5, Soul Cinematic, Seedance 2.0.

The project separates Characters, Locations, Props, Editing, Sound, Scene folders, Test_Images and Test_Videos. The observed location prompt uses a 3D layout/blockout, named scene objects and a world-style reference. Several brief headings retain generic template placeholder text; their presence does not establish that the corresponding production planning was completed.

**Manual cross-check.** Browser: 3:46, 391 generations, All assets 393. The inspected image uses Seedream 5.0 Pro, 2k, 2720×1536. API: 393 item rows and 391 unique generations.

**Public folder structure.**

- /AI Film Festival
- /AI Film Festival/Characters
- /AI Film Festival/Editing
- /AI Film Festival/Locations
- /AI Film Festival/Props
- /AI Film Festival/Scene_01
- /AI Film Festival/Scene_02
- /AI Film Festival/Scene_03
- /AI Film Festival/Scene_05
- /AI Film Festival/Sound
- /AI Film Festival/Test_Images
- /AI Film Festival/Test_Videos
- /AI Film Festival/Watermarks

**Qualification.** The initial UI prompt substitutes human-readable reference labels for raw reference tokens; raw token text is preserved in the dataset.

## Fallen Leaves

- Project: https://higgsfield.ai/@jacob_everett/projects/fallen-leaves
- Creator: jacob_everett
- Approach: A naturalistic historical short with a relatively flat project organization.
- Export: 356 distinct generations, 356 generation records with a nonempty primary prompt, 2 folders and 369 asset entities.
- Models observed: Seedance 2.5, GPT Image 2.0, Seedance 2.0.

The brief describes a Sengoku-period setting, naturalistic camera movement, winter lighting and film emulation. The public folder panel has All assets and Watermarks rather than a detailed scene hierarchy. The inspected reference-sheet prompt specifies geography, supporting angles, textures and an explicit Avoid section. An embedded title-card prompt is preserved in the raw brief document.

**Manual cross-check.** Browser: 5:39, 356 generations, All assets 357. Inspected location-sheet image: GPT Image 2, High quality, 2688×1520. API: 357 item rows and 356 unique generations.

**Public folder structure.**

- /Fallen Leaves
- /Fallen Leaves/Watermarks

**Qualification.** Its visible production history is dominated by Seedance 2.5, in contrast with the broader stack of Cosmic tracks.

## Don't Poison Ivy

- Project: https://higgsfield.ai/@joeysnoisygroup/projects/don-t-poison-ivy
- Creator: joeysnoisygroup
- Approach: A stylized, dialogue-free animated film with a handmade visual aesthetic.
- Export: 553 distinct generations, 552 generation records with a nonempty primary prompt, 27 folders and 725 asset entities.
- Models observed: Seedance 2.5, Nano Banana Pro, Cinematic Video Editor, Seedream 5.0 Pro.

The brief describes character sheets in Nano Banana Pro, scene plates in Seedream 5.0 Pro and video in Seedance 2.5. Folders separate Characters, Locations, Props, Score and Video Generations, with nested folders. The brief describes exaggerated character features, detailed clothing and deliberate color/surface rules. An observed short edit prompt changes only paint on a pot, illustrating a local revision rather than a fresh scene description.

**Manual cross-check.** Browser: 15:38, 553 generations, All assets 608. Inspected pot edit: Nano Banana Pro, 4k, 5504×3072; generation author bydany differs from project owner joeysnoisygroup. API: 604 recursive item rows and 553 unique generations.

**Public folder structure.**

- /Don't Poison Ivy
- /Don't Poison Ivy/Characters
- /Don't Poison Ivy/Characters/Daughter
- /Don't Poison Ivy/Characters/Extras
- /Don't Poison Ivy/Characters/Mom
- /Don't Poison Ivy/Characters/Outfits
- /Don't Poison Ivy/Locations
- /Don't Poison Ivy/Locations/Bedrooms
- /Don't Poison Ivy/Locations/City
- /Don't Poison Ivy/Locations/Elementary School
- /Don't Poison Ivy/Locations/Grocery store
- /Don't Poison Ivy/Locations/Home Exterior
- /Don't Poison Ivy/Locations/Home Interior
- /Don't Poison Ivy/Props
- /Don't Poison Ivy/Score
- /Don't Poison Ivy/Video Generations
- /Don't Poison Ivy/Video Generations/Act 1: Town Intro
- /Don't Poison Ivy/Video Generations/Act 2: Privilege
- /Don't Poison Ivy/Video Generations/Act 3: Art Secret
- /Don't Poison Ivy/Video Generations/Act 4: The Break
- /Don't Poison Ivy/Video Generations/Act 5: The Coda
- /Don't Poison Ivy/Video Generations/Bloopers
- /Don't Poison Ivy/Video Generations/Misc BROLL
- /Don't Poison Ivy/Video Generations/Potential Replacement Scenes
- /Don't Poison Ivy/Video Generations/Trailer
- /Don't Poison Ivy/Video Generations/Transitional Scenes
- /Don't Poison Ivy/Watermarks

**Qualification.** Root recursive response rows and UI totals have different counting behavior. Direct-folder recovery supplements the exported resource placements; generation totals reconcile.
