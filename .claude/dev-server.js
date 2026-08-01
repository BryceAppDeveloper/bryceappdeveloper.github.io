// Minimal static server for local visual checks only. Mirrors worker.js routing:
// "/" -> index.html, extensionless -> path + ".html". Never deployed (.assetsignore
// excludes .claude) and not a substitute for the real worker.
const http = require('http');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.pdf': 'application/pdf',
  '.xml': 'application/xml', '.txt': 'text/plain', '.woff2': 'font/woff2', '.json': 'application/json'
};

http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  let file = path.normalize(path.join(root, p));
  if (!file.startsWith(root)) { res.writeHead(403); return res.end(); }
  if (!fs.existsSync(file) && !path.extname(file)) file += '.html';
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'content-type': types[path.extname(file).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
}).listen(process.env.PORT || 8790, () => console.log('static server ready on ' + (process.env.PORT || 8790)));
