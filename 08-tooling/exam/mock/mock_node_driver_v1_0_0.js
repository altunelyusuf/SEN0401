// node driver: runs the SAME scoring.js and derive.js text as the page (optionally with a planted defect) on a job file.
// usage: node mock_node_driver_v1_0_0.js job.json   (job: {bank, patch, ops:[{op:'derive',k,seed}|{op:'score',k,seed,answers}|{op:'blind',k,seed,n,rngseed}]})
const fs = require('fs'), vm = require('vm'), path = require('path');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const here = __dirname;
let sc = fs.readFileSync(path.join(here, 'mock_scoring_v1_0_0.js'), 'utf8');
let dv = fs.readFileSync(path.join(here, 'mock_derive_v1_0_0.js'), 'utf8');
function patch(src, from, to) { if (src.indexOf(from) < 0) throw new Error('patch anchor missing: ' + from); return src.replace(from, to); }
const P = job.patch || 'none';
if (P === 'deduct') sc = patch(sc, '/*CH_WRONG*/', ' else if (isSet(ans)) { got = -1; }');
if (P === 'letter') dv = patch(dv, 'correct: target /*LETTERMAP*/', 'correct: it.answer');
if (P === 'slice') dv = patch(dv, 'var m = (k - 1) % 8; /*SLICE*/', 'var m = Math.floor((k - 1) / 2) % 8; /*SLICE*/');
const ctx = { console }; ctx.globalThis = ctx; vm.createContext(ctx);
vm.runInContext(sc, ctx); vm.runInContext(dv, ctx);
const bank = JSON.parse(fs.readFileSync(job.bank, 'utf8')).items;
function strip(m) { // drop bank back-references for compact output
  return { k: m.k, seed: m.seed, epoch: m.epoch, slice: m.slice, itemIds: m.itemIds, total: m.total,
    questions: m.questions.map(Q => ({ q: Q.q, items: Q.items.map(it => { const o = Object.assign({}, it); delete o.src; delete o.inst; return o; }) })) };
}
function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const out = [];
for (const op of job.ops) {
  if (op.op === 'derive') { out.push(strip(ctx.MockDerive.deriveMock(bank, op.k, op.seed))); }
  else if (op.op === 'score') { const m = ctx.MockDerive.deriveMock(bank, op.k, op.seed); out.push(ctx.MockScoring.scoreMock(m, op.answers)); }
  else if (op.op === 'blind') {
    const m = ctx.MockDerive.deriveMock(bank, op.k, op.seed), r = rng(op.rngseed); let s = 0, s2 = 0;
    for (let n = 0; n < op.n; n++) {
      const a = {};
      m.questions.forEach(Q => Q.items.forEach(it => {
        if (it.type === 'choice') a[it.uid] = Math.floor(r() * 5);
        else if (it.type === 'numeric') a[it.uid] = String(Math.floor(r() * 100000));
        else if (it.type === 'ordering') a[it.uid] = it.correct.map(() => 1 + Math.floor(r() * 5));
        else a[it.uid] = it.correct.map(() => Math.floor(r() * 5));
      }));
      const t = ctx.MockScoring.scoreMock(m, a).total; s += t; s2 += t * t;
    }
    out.push({ n: op.n, mean: s / op.n, var: s2 / op.n - (s / op.n) ** 2 });
  }
}
process.stdout.write(JSON.stringify(out));
