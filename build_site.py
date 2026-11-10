"""Build a standalone copy of the CPE Honeypot Watch dashboard for GitHub Pages.
It supplies a small stand-in for the dashboard runtime (dash.calc / draw / data / params)
and loads the four datasets from data/*.json.
python3 build_site.py DASH_INDEX.html OUT.html"""
import sys
src, out = sys.argv[1], sys.argv[2]
page = open(src, encoding='utf-8').read().replace('<meta name="dash-one-writer">', '')
# each dashboard script runs in its own block so top-level const names can repeat
page = page.replace('<script>', '<script>{').replace('</script>', '}</script>')
head = r"""<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CPE Honeypot Watch</title>
<meta name="description" content="What internet bots do to an ONU/router that leaves Telnet, SSH, HTTP and TR-069 open on the WAN side.">
<style>
:root{--cds-gap-xs:4px;--cds-gap-sm:8px;--cds-gap-md:16px;--cds-gap-lg:24px;--cds-gap-xl:32px;--cds-pad-xs:4px;--cds-pad-sm:8px;--cds-pad-md:12px;--cds-pad-lg:20px;--cds-radius:10px;
--cds-font-size-title:28px;--cds-font-size-heading:18px;--cds-font-size-body:15px;--cds-font-size-caption:12.5px;--cds-font-weight-medium:500;
--color-bg:#F5F5F7;--color-panel:#fff;--color-fg:#1D1D1F;--color-fg-muted:#6e6e73;--color-border-line:#e2e2e7;--color-bad:#d03b3b;--color-warn:#d68a1a;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--color-bg:#000;--color-panel:#1c1c1e;--color-fg:#F5F5F7;--color-fg-muted:#AAAAAA;--color-border-line:#2c2c2e;}}
:root[data-theme="dark"]{--color-bg:#000;--color-panel:#1c1c1e;--color-fg:#F5F5F7;--color-fg-muted:#AAAAAA;--color-border-line:#2c2c2e;}
body{margin:0;padding:16px;background:var(--color-bg);color:var(--color-fg);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Noto Sans Thai",system-ui,sans-serif}
.site-load{position:fixed;inset:auto 0 0 0;padding:.6rem;text-align:center;font-size:13px;color:var(--color-fg-muted)}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
(() => {
  const DATA = {}, calcs = {}, draws = [], onData = [], res = {};
  let params = {};
  try { params = JSON.parse(localStorage.getItem('hp-params') || '{}'); } catch (e) {}
  const run = () => {
    for (const [id, s] of Object.entries(calcs)) {
      try { res[id] = {status: 'ok', data: s.fn(...s.inputs.map((i) => DATA[i]))}; }
      catch (e) { console.error('calc', id, e); res[id] = {status: 'error'}; }
    }
    for (const [id, fn] of draws) document.querySelectorAll(`[data-draw="${id}"]`).forEach((el) => { try { fn(el); } catch (e) { console.error('draw', id, e); } });
    onData.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
  };
  window.dash = {
    calc(id, spec) { calcs[id] = spec; },
    draw(id, fn) { draws.push([id, fn]); },
    data(id) { return res[id] || {status: 'loading'}; },
    params() { return params; },
    setParams(p) { Object.assign(params, p); try { localStorage.setItem('hp-params', JSON.stringify(params)); } catch (e) {} run(); },
    setLink() {},
    onData(fn) { onData.push(fn); },
  };
  const names = ['honeypot', 'bots', 'geo', 'events', 'http'];
  const loaded = Promise.all(names.map((n) => fetch(`data/${n}.json`).then((r) => r.json()).then((j) => { DATA[n] = j.rows; })));
  document.addEventListener('DOMContentLoaded', () => loaded.then(() => { document.querySelector('.site-load')?.remove(); run(); })
    .catch((e) => { const m = document.querySelector('.site-load'); if (m) m.textContent = 'Could not load data: ' + e; }));
})();
</script>
</head><body><div class="site-load">Loading data…</div>
"""
open(out, 'w', encoding='utf-8').write(head + page + '\n</body></html>\n')
print('wrote', out)
