# Block by Block

A modern-day gangland real-time strategy game that runs in your browser. No install or account needed.

**Play:** open the GitHub Pages link for this repository (Settings → Pages shows it).

## Multiplayer (up to 6 players)
1. One player opens the game, chooses **Multiplayer**, enters a name and clicks **Host a game**.
2. They share the 5-letter room code. Everyone else opens the same link, chooses **Multiplayer**, enters the code and clicks **Join**.
3. Each player picks a gang. The host chooses how many gangs are on the map (the AI fills empty corners), the map size and the AI difficulty, then starts the war.

**Voice chat:** click **Join voice chat** in the lobby, or **Voice** (key **T**) during a match. Your browser asks for the microphone once. Press **T** again to mute. Names glow while people talk, and anyone can listen without turning on their own mic.

The host's browser runs the match, so the host should keep the game tab open. Players connect peer-to-peer with WebRTC (PeerJS). A few strict networks block these connections.

## How to play
- Pick your crew, how many gangs are on the map (2–6), the map size and the difficulty.
- Runners collect cash from neighborhood businesses. Build a Clubhouse to train fighters, upgrade buildings to unlock stronger units, and take down every rival Hideout.
- Watch your heat. Push it too high and police squads roll out of the station downtown.

## Controls
| Input | Action |
|---|---|
| Left-drag | Select your crew |
| Right-click | Move, attack, collect, or hide in a building |
| Q / E | Attack-move / Stop |
| Z X C V B | Build, train or upgrade |
| G | Lay low (from the Hideout) |
| F / . | Select fighters / next idle runner |
| W A S D, arrows, screen edge | Pan |
| Mouse wheel | Zoom |
| Space | Jump to Hideout |
| T | Voice chat: join, then mute or unmute (multiplayer) |
| M / P | Mute / Pause (the menu in multiplayer) |

The whole game is a single `index.html` file with no build step.

## What's in the game

- **Modes:** Single player, Multiplayer (up to 6), a 6-mission **Campaign**, and a guided **Tutorial**.
- **Turf:** park your crew in a block until its border fills in. Held blocks pay you every second.
- **Veterans:** units that get takedowns rank up (Veteran, Elite, Legend) and hit harder.
- **Gang powers:** upgrade your Hideout to Headquarters, then press **R**. Each gang has its own power.
- **Characters:** every unit and pedestrian is a 3D Blender render in 8 directions with walk, idle and attack poses (`art/blender/characters.py`). Clothing takes the gang's colours.
- **A city that's seen better days:** cracked and patched streets, potholes, stains, litter, trash bags, dumpsters, tire piles and dumped mattresses.
- **Graffiti:** old tags cover the walls, and every block you hold gets your gang's tag in your colour.
- **Español:** switch the whole game to Spanish under Settings > Language (it picks Spanish automatically when your browser is set to it). Translations live in `i18n/es.json`.
- **Trap House:** every map has one. It holds the most cash of any business, but each pickup brings heavy heat.
- **City events:** armored trucks to rob, parades, blackouts, police crackdowns, truces and payday at a business.
- **Day and night:** matches start at dusk and roll through night, dawn and day. You see less at night.
- **City layouts:** Classic, Random, Downtown, Industrial and Waterfront.
- **Saves:** single-player games autosave. Use Continue on the main menu.
- **Bigger units:** toggle in the pause menu.
- **Painted buildings:** gang buildings, storefronts and the city's apartment blocks, offices and warehouses use painted isometric art (made with SpriteCook), and vehicles are 3D renders from Blender in 16 directions (`art/blender/cars.py`) that takes each gang's colour. Switch to the classic look under Settings > Building art.

## Game modes

Pick one on the setup screen (or in the multiplayer lobby):

- **Conquest:** destroy every rival crew.
- **Turf control:** hold half of the city's blocks for 2 minutes.
- **Cash race:** first to collect the target ($15k / $20k / $25k by map size).
- **King of the Hill:** hold the flagged center block for 2:30 in total.
- **Timed:** 20 minutes, most points wins (turf, cash, takedowns, buildings).
- **Regicide:** every gang has a Boss. Kill him and that gang is finished.
- **Heist:** first to 5 big scores (rob armored trucks, grab Payday cash first).
- **Survival** (single player): just you against escalating police waves. Tracks your best time.
- **Sandbox:** unlimited cash, everything unlocked, no police, rivals stay home.

Extra rules for any mode: **Teams** (2 or 3, allies share vision and can't hurt each other) and **Hardcore** (lose your Hideout and you're out).

## Strategy features

- **Research:** select a building and press **Y**. Hideout research covers the economy (Bigger Bags, Counting House, Laundering, Protection). Clubhouse, Chop Shop, Lookout and Safehouse each have their own upgrades.
- **Production across buildings:** select several of the same building and train. Each order goes to the one with the shortest queue.
- **Rally points:** right-click a spot, a business (Runners start collecting), a building site (Runners help build) or one of your fighters (new crew follow him).
- **Follow:** right-click one of your own units with others selected and they escort him.
- **Formations:** group moves keep brawlers in front and guns behind, and the group travels at its slowest member's speed.
- **Height bonus:** crew hiding in taller buildings shoot farther and harder.
- **Stash houses:** neutral, guarded outposts on the map. Clear the guards and walk up for $800.
- **Co-op vs AI** (multiplayer lobby): every player on one team against the AI crews. The AI gets richer for each extra player.
