# Block by Block

A modern-day gangland real-time strategy game that runs in your browser. No install or account needed.

**Play:** open the GitHub Pages link for this repository (Settings → Pages shows it).

## Multiplayer (up to 6 players)
1. One player opens the game, chooses **Multiplayer**, enters a name and clicks **Host a game**.
2. They share the 5-letter room code. Everyone else opens the same link, chooses **Multiplayer**, enters the code and clicks **Join**.
3. Each player picks a gang. The host chooses how many gangs are on the map (the AI fills empty corners), the map size and the AI difficulty, then starts the war.

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
| M / P | Mute / Pause (the menu in multiplayer) |

The whole game is a single `index.html` file with no build step.
