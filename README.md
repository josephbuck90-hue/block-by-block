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
- **City events:** armored trucks to rob, parades, blackouts, police crackdowns, truces and payday at a business.
- **Day and night:** matches start at dusk and roll through night, dawn and day. You see less at night.
- **City layouts:** Classic, Random, Downtown, Industrial and Waterfront.
- **Saves:** single-player games autosave. Use Continue on the main menu.
- **Bigger units:** toggle in the pause menu.

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
