// Packages a Windows x64 build into dist/, then stamps the icon and version info into the .exe.
const { packager } = require('@electron/packager');
const ResEdit = require('resedit');
const fs = require('fs');
const path = require('path');
(async () => {
  const pkg = require('./package.json');
  const [dir] = await packager({
    dir: __dirname, name: 'BlockByBlock', executableName: 'BlockByBlock', platform: 'win32', arch: 'x64',
    out: path.join(__dirname, 'dist'), overwrite: true, asar: true, prune: true,
    ignore: [/^\/dist/, /^\/node_modules\/(@fontsource|peerjs|resedit|@electron\/packager)/, /^\/build\.js$/, /^\/package-win\.js$/, /^\/icon\//],
    appCopyright: 'Copyright 2026 Joseph Buck', appVersion: pkg.version,
  });
  const exe = path.join(dir, 'BlockByBlock.exe');
  const data = fs.readFileSync(exe);
  const exeObj = ResEdit.NtExecutable.from(data, { ignoreCert: true });
  const res = ResEdit.NtExecutableResource.from(exeObj);
  const ico = ResEdit.Data.IconFile.from(fs.readFileSync(path.join(__dirname, 'icon', 'icon.ico')));
  ResEdit.Resource.IconGroupEntry.replaceIconsForResource(res.entries, 1, 1033, ico.icons.map((i) => i.data));
  const vi = ResEdit.Resource.VersionInfo.fromEntries(res.entries)[0];
  const v = pkg.version.split('.').map(Number);
  vi.setFileVersion(v[0], v[1], v[2], 0, 1033); vi.setProductVersion(v[0], v[1], v[2], 0, 1033);
  vi.setStringValues({ lang: 1033, codepage: 1200 }, { ProductName: 'Block by Block', FileDescription: 'Block by Block', CompanyName: 'Joseph Buck', LegalCopyright: 'Copyright 2026 Joseph Buck', OriginalFilename: 'BlockByBlock.exe' });
  vi.outputToResourceEntries(res.entries);
  res.outputResource(exeObj);
  fs.writeFileSync(exe, Buffer.from(exeObj.generate()));
  console.log('packaged:', dir);
})().catch((e) => { console.error(e); process.exit(1); });
