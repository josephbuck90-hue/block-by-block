# Block by Block — desktop app

The web game (`../index.html`) wrapped as a Windows app with Electron.

- Saves and settings are JSON files in `%APPDATA%\block-by-block\saves`.
- Fonts and PeerJS are bundled, so single player works fully offline.
- F11 toggles fullscreen. Settings → Display has window sizes.

## Build on your PC

```
cd desktop
npm install
npm start              # run it
npm run package:win    # makes dist\BlockByBlock-win32-x64\BlockByBlock.exe
```

## Build on GitHub

Actions tab → **Desktop build** → **Run workflow**. The finished app is attached to the run as a download.
