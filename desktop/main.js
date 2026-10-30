// Block by Block desktop shell: one window, saves as JSON files in the user's app data folder.
const { app, BrowserWindow, ipcMain, Menu, shell, session } = require('electron');
const path = require('path');
const fs = require('fs');

let win = null;
const saveDir = () => path.join(app.getPath('userData'), 'saves');
const fileFor = (k) => path.join(saveDir(), String(k).replace(/[^a-z0-9_-]/gi, '_') + '.json');

function readSettings() {
  try { return JSON.parse(fs.readFileSync(fileFor('bbb-settings'), 'utf8')); } catch (_) { return {}; }
}

ipcMain.on('store-get', (e, k) => {
  try { e.returnValue = fs.readFileSync(fileFor(k), 'utf8'); } catch (_) { e.returnValue = null; }
});
ipcMain.on('store-set', (e, k, v) => {
  try {
    fs.mkdirSync(saveDir(), { recursive: true });
    const f = fileFor(k);
    fs.writeFileSync(f + '.tmp', String(v));
    fs.renameSync(f + '.tmp', f); // write then swap, so a crash never leaves a half-written save
    e.returnValue = true;
  } catch (_) { e.returnValue = false; }
});
ipcMain.on('store-del', (e, k) => {
  try { fs.unlinkSync(fileFor(k)); } catch (_) {}
  e.returnValue = true;
});
ipcMain.on('set-fullscreen', (_e, on) => { if (win) win.setFullScreen(!!on); });
ipcMain.on('is-fullscreen', (e) => { e.returnValue = !!(win && win.isFullScreen()); });
ipcMain.on('set-size', (_e, w, h) => {
  if (!win) return;
  win.setFullScreen(false);
  win.setContentSize(Math.max(1024, w | 0), Math.max(640, h | 0));
  win.center();
});
ipcMain.on('quit', () => app.quit());

function createWindow() {
  const s = readSettings();
  const [w, h] = String(s.win || '1600x900').split('x').map(Number);
  win = new BrowserWindow({
    width: w || 1600, height: h || 900, useContentSize: true, minWidth: 1024, minHeight: 640,
    backgroundColor: '#0b0e12', title: 'Block by Block', show: false, autoHideMenuBar: true,
    fullscreen: !!s.fs,
    icon: path.join(__dirname, 'app', 'icon.png'),
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false, sandbox: true, devTools: !app.isPackaged },
  });
  Menu.setApplicationMenu(null);
  win.once('ready-to-show', () => win.show());
  // links open in the normal browser, never inside the game window
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https?:/.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (ev, url) => { if (!url.startsWith('file:')) { ev.preventDefault(); shell.openExternal(url); } });
  win.loadFile(path.join(__dirname, 'app', 'index.html'));
}

if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });
  app.whenReady().then(() => {
    // voice chat needs the microphone; nothing else is allowed
    session.defaultSession.setPermissionRequestHandler((_wc, perm, cb) => cb(perm === 'media' || perm === 'fullscreen'));
    createWindow();
  });
  app.on('window-all-closed', () => app.quit());
}
