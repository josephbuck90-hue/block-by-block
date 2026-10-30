// Builds desktop/app/ from the web game: bundles fonts and PeerJS locally so the game runs offline.
const fs = require('fs');
const path = require('path');
const root = __dirname;
const out = path.join(root, 'app');
const nm = (...p) => path.join(root, 'node_modules', ...p);
fs.mkdirSync(path.join(out, 'fonts'), { recursive: true });

const game = fs.readFileSync(path.join(root, '..', 'index.html'), 'utf8');
const fonts = [
  ['bungee', 'bungee-latin-400-normal.woff2', 'Bungee', 400],
  ['barlow-semi-condensed', 'barlow-semi-condensed-latin-400-normal.woff2', 'Barlow Semi Condensed', 400],
  ['barlow-semi-condensed', 'barlow-semi-condensed-latin-500-normal.woff2', 'Barlow Semi Condensed', 500],
  ['barlow-semi-condensed', 'barlow-semi-condensed-latin-600-normal.woff2', 'Barlow Semi Condensed', 600],
  ['barlow-semi-condensed', 'barlow-semi-condensed-latin-700-normal.woff2', 'Barlow Semi Condensed', 700],
  ['jetbrains-mono', 'jetbrains-mono-latin-500-normal.woff2', 'JetBrains Mono', 500],
  ['jetbrains-mono', 'jetbrains-mono-latin-700-normal.woff2', 'JetBrains Mono', 700],
];
let faces = '';
for (const [pkg, file, family, weight] of fonts) {
  fs.copyFileSync(nm('@fontsource', pkg, 'files', file), path.join(out, 'fonts', file));
  faces += `@font-face{font-family:'${family}';font-weight:${weight};font-style:normal;font-display:swap;src:url(fonts/${file}) format('woff2')}\n`;
}
fs.copyFileSync(nm('peerjs', 'dist', 'peerjs.min.js'), path.join(out, 'peerjs.min.js'));
fs.copyFileSync(path.join(root, 'icon', 'icon.png'), path.join(out, 'icon.png'));

let html = game
  .replace(/<link rel="preconnect"[^>]*>\s*/g, '')
  .replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>/, `<style>${faces}</style>`)
  .replace(/<meta charset="utf-8">/, '<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'self\' \'unsafe-inline\' data: blob:; connect-src * data: blob:; media-src * blob:; img-src \'self\' data: blob:">')
  .replace('<script>\n(() => {', '<script src="peerjs.min.js"></script>\n<script>\n(() => {');
if (html.includes('fonts.googleapis.com')) throw new Error('font link not replaced');
if (!html.includes('peerjs.min.js')) throw new Error('peerjs not injected');
fs.writeFileSync(path.join(out, 'index.html'), html);
console.log('desktop app built:', path.relative(root, out));
