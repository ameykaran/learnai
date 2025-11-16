
const fs = require('fs');
const katex = require('katex');
const input = fs.readFileSync(0, 'utf8');
const mode = process.argv[2] === 'display';
try {
  const out = katex.renderToString(input, { displayMode: mode, throwOnError: false });
  process.stdout.write(out);
} catch (err) {
  process.stdout.write(JSON.stringify({error: String(err)}));
  process.exit(1);
}
