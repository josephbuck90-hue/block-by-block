// The only bridge between the game page and the desktop: file saves, window controls, quit.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('bbbDesktop', {
  store: {
    get: (k) => ipcRenderer.sendSync('store-get', String(k)),
    set: (k, v) => ipcRenderer.sendSync('store-set', String(k), String(v)),
    del: (k) => ipcRenderer.sendSync('store-del', String(k)),
  },
  setFullscreen: (on) => ipcRenderer.send('set-fullscreen', !!on),
  isFullscreen: () => ipcRenderer.sendSync('is-fullscreen'),
  setSize: (w, h) => ipcRenderer.send('set-size', w, h),
  quit: () => ipcRenderer.send('quit'),
  platform: process.platform,
});
