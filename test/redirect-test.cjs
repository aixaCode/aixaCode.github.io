const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const routes = JSON.parse(fs.readFileSync(path.join(root, 'redirects.json'), 'utf8'));
assert.equal(Object.keys(routes).length, 22);
for (const [file, target] of [...Object.entries(routes), ['404.html', 'https://besz.me/missing/path']]) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  const script = text.match(/<script>([\s\S]*?)<\/script>/)[1];
  for (const [search, hash] of [['', ''], ['?from=github&name=a%20b', '#feedback'], ['?next=https%3A%2F%2Fexample.com', '#part%202']]) {
    let result;
    vm.runInNewContext(script, {window: {location: {
      pathname: '/missing/path', search, hash, replace: value => {result = value;}
    }}});
    assert.equal(result, target + search + hash);
    assert.equal(new URL(result).origin, 'https://besz.me');
  }
  assert.match(text, /<meta http-equiv="refresh"/);
  assert.match(text, /<link rel="canonical" href="https:\/\/besz.me\//);
  assert.match(text, /<a href="https:\/\/besz.me\//);
}
console.log('22 legacy routes, 404 fallback and query/fragment preservation passed');
