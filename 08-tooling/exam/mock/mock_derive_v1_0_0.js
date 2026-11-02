/* ===== DERIVE section - SEN0401 mock exam, v1.0.0 =====
   Seeded generator (mulberry32). Mock number k (1..8) takes the k-th slice of a seed-fixed permutation per unit type,
   so mocks 1..8 share no item; mock 9 and later wrap around (items of earlier mocks come back, none from the real exam).
   Which items form mock k depends on k only. The seed of the mock only shuffles the order, the options and the letters.
   No item text is in this file. */
(function (root) {
  'use strict';
  var BANK_SEED = 20261103;
  var NCH = 6;

  function hashStr(s) {
    var h = 2166136261 >>> 0;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h >>> 0;
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function shuffled(arr, rnd) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function natKey(id) {
    return String(id).replace(/\d+/g, function (d) { return ('0000' + d).slice(-4); });
  }
  function byId(a, b) { var x = natKey(a.id), y = natKey(b.id); return x < y ? -1 : x > y ? 1 : 0; }
  function range(n) { var r = []; for (var i = 0; i < n; i++) r.push(i); return r; }
  function defaultSeed(k) { return 1000 + 37 * k; }

  function indexBank(items) {
    var by = { choice: [], numeric: [], matching: [], ordering: [], fill: [] };
    items.forEach(function (it) { if (by[it.type]) by[it.type].push(it); });
    Object.keys(by).forEach(function (t) { by[t].sort(byId); });
    return by;
  }
  function chaptersOf(list) {
    var s = {}; list.forEach(function (x) { s[x.chapter] = 1; });
    return Object.keys(s).map(Number).sort(function (a, b) { return a - b; });
  }
  function ofChapter(list, c) { return list.filter(function (x) { return x.chapter === c; }); }

  /* round-robin over chapters (each chapter list seed-permuted): consecutive entries come from different chapters */
  function interleave(list, rngFor, tag) {
    var chs = chaptersOf(list);
    chs = shuffled(chs, rngFor(tag + ':order'));
    var lists = chs.map(function (c) { return shuffled(ofChapter(list, c), rngFor(tag + ':' + c)); });
    var out = [], more = true, r = 0;
    while (more) {
      more = false;
      lists.forEach(function (l) { if (r < l.length) { out.push(l[r]); more = true; } });
      r++;
    }
    return out;
  }

  /* which bank units form mock k: {choice:[items], numeric:[{t:template, i:instanceIndex}], matching:[2], ordering:[1], fill:[3]} */
  function selectUnits(items, k) {
    var by = indexBank(items);
    var epoch = Math.floor((k - 1) / 8);
    var m = (k - 1) % 8; /*SLICE*/
    /* permutations are fixed (epoch-free), so mock 9 and later can only reuse units used by mocks 1..8;
       from mock 9 on, each unit type is read at a shifted slice, so the units are recombined */
    function rngFor(label) { return mulberry32(hashStr(label + ':' + BANK_SEED)); }
    var mc = (m + epoch) % 8, mn = (m + 3 * epoch) % 8, mx = (m + 5 * epoch) % 8;
    var sel = { epoch: epoch, m: m };

    /* choice: chapter window design - 3-point items in three consecutive chapters, 4-point items fill the rest,
       one chapter (m mod 6) doubled; so every chapter appears and no chapter has more than 2 items. */
    var chs = chaptersOf(by.choice);
    if (chs.length !== NCH) throw new Error('bank has ' + chs.length + ' chapters of choice items, need ' + NCH);
    var p3 = [], p4 = [], n3 = [], n4 = [];
    chs.forEach(function (c, ci) {
      var L = ofChapter(by.choice, c);
      p3.push(shuffled(L.filter(function (x) { return x.points === 3; }), rngFor('c3:' + c)));
      p4.push(shuffled(L.filter(function (x) { return x.points === 4; }), rngFor('c4:' + c)));
      n3.push(0); n4.push(0);
    });
    var pick = [];
    for (var mm = 0; mm <= mc; mm++) {
      var S = {}; for (var j = 0; j < 3; j++) S[(3 * mm + j) % NCH] = 1;
      for (var ci = 0; ci < NCH; ci++) {
        var n = 1 + (ci === mm % NCH ? 1 : 0), s = S[ci] ? 1 : 0, t = n - s, u;
        for (u = 0; u < s; u++) { var a = p3[ci][n3[ci]++]; if (!a) throw new Error('not enough 3-point choice items in chapter ' + chs[ci]); if (mm === mc) pick.push(a); }
        for (u = 0; u < t; u++) { var b = p4[ci][n4[ci]++]; if (!b) throw new Error('not enough 4-point choice items in chapter ' + chs[ci]); if (mm === mc) pick.push(b); }
      }
    }
    sel.choice = pick;

    /* numeric (composition v4): one instance of each family present in the bank (up to six) + the rest (2 when all six exist) from the
       kept main-bank templates (templates flagged "dropped" are never drawn). A missing family is filled from the kept main templates.
       Instance index is a seed-fixed permutation of the instances of each template taken at position mn: no (template, instance)
       twice in mocks 1..8. Points: the shell raises one random numeric place to 4. */
    var famT = {}, mainT = [];
    by.numeric.forEach(function (t) { if (t.dropped) return; if (t.family) { (famT[t.family] = famT[t.family] || []).push(t); } else mainT.push(t); });
    var famNames = Object.keys(famT).sort();
    var mp = shuffled(mainT.slice().sort(byId), rngFor('mainnum'));
    var famUsed = {}, chosen = [], nfam = 0;
    famNames.forEach(function (fam) {
      var L = shuffled(famT[fam].slice().sort(byId), rngFor('fam:' + fam));
      famUsed[fam] = true; nfam++; chosen.push(L[mn % L.length]);
    });
    var nmain = 8 - nfam;
    if (nmain > mp.length) throw new Error('not enough kept main numeric templates');
    for (var jn = 0; jn < nmain; jn++) chosen.push(mp[(nmain * mn + jn) % mp.length]);
    sel.families = famUsed;
    sel.numeric = chosen.map(function (tpl) {
      var perm = shuffled(range(tpl.instances.length), rngFor('ni:' + tpl.id));
      return { t: tpl, i: perm[mn % perm.length] };
    });

    var mat = interleave(by.matching, rngFor, 'm'), ord = interleave(by.ordering, rngFor, 'o'), fil = interleave(by.fill, rngFor, 'f');
    sel.matching = [mat[2 * mx], mat[2 * mx + 1]];
    sel.ordering = [ord[mx]];
    sel.fill = [fil[3 * mx], fil[3 * mx + 1], fil[3 * mx + 2]];
    ['matching', 'ordering', 'fill'].forEach(function (t) {
      sel[t].forEach(function (x) { if (!x) throw new Error('not enough ' + t + ' units for mock ' + k); });
    });
    return sel;
  }

  function uidOf(sel) {
    var ids = [];
    sel.choice.forEach(function (x) { ids.push(x.id); });
    sel.numeric.forEach(function (x) { ids.push(x.t.id + '#' + x.i); });
    sel.matching.forEach(function (x) { ids.push(x.id); });
    sel.ordering.forEach(function (x) { ids.push(x.id); });
    sel.fill.forEach(function (x) { ids.push(x.id); });
    return ids;
  }

  function buildChoice(it, target, rnd, label) {
    var others = shuffled([0, 1, 2, 3, 4].filter(function (i) { return i !== it.answer; }), rnd);
    var disp = [], q = 0;
    for (var pos = 0; pos < 5; pos++) {
      if (pos === target) disp.push({ text: it.options[it.answer], orig: it.answer });
      else { var o = others[q++]; disp.push({ text: it.options[o], orig: o }); }
    }
    return { uid: it.id, type: 'choice', label: label, chapter: it.chapter, points: it.points, stem: it.stem, tip: it.tip,
      options: disp, correct: target /*LETTERMAP*/, src: it };
  }
  function buildMatching(it, rowPoints, rnd, label) {
    var perm = shuffled(range(5), rnd);
    var disp = perm.map(function (o) { return { text: it.responses[o], orig: o }; });
    var inv = []; perm.forEach(function (o, d) { inv[o] = d; });
    return { uid: it.id, type: 'matching', label: label, chapter: it.chapter, intro: it.intro, tip: it.tip, premises: it.premises.slice(),
      responses: disp, correct: it.answer.map(function (o) { return inv[o]; }), rowPoints: rowPoints, src: it };
  }
  function buildOrdering(it, label) {
    return { uid: it.id, type: 'ordering', label: label, chapter: it.chapter, intro: it.intro, tip: it.tip, steps: it.steps.slice(),
      correct: it.answer.slice(), stepPoints: 1, src: it };
  }
  function buildFill(it, blankPoints, rnd, label) {
    var perm = shuffled(range(5), rnd);
    var disp = perm.map(function (o) { return { text: it.bank[o], orig: o }; });
    var inv = []; perm.forEach(function (o, d) { inv[o] = d; });
    return { uid: it.id, type: 'fill', label: label, chapter: it.chapter, stem: it.stem, tip: it.tip, bank: disp,
      blanks: it.blanks.map(function (b) { return { sentence: b.sentence }; }),
      correct: it.blanks.map(function (b) { return inv[b.answer]; }), blankPoints: blankPoints, src: it };
  }

  function deriveMock(items, k, seed) {
    var sel = selectUnits(items, k);
    var rnd = mulberry32(hashStr('mock:' + k + ':' + seed));
    var L = 'abcdefgh';
    /* Q1 */
    var q1src = shuffled(sel.choice, rnd);
    var base = shuffled([0, 1, 2, 3, 4], rnd);
    var targets = shuffled(base.concat([Math.floor(rnd() * 5), Math.floor(rnd() * 5)]), rnd);
    var Q1 = q1src.map(function (it, i) { return buildChoice(it, targets[i], rnd, '1' + L[i]); });
    /* Q2 */
    var nsel = shuffled(sel.numeric, rnd);
    var four = Math.floor(rnd() * nsel.length);
    var Q2 = nsel.map(function (x, i) {
      var ins = x.t.instances[x.i];
      return { uid: x.t.id + '#' + x.i, type: 'numeric', label: '2' + L[i], chapter: x.t.chapter, points: i === four ? 4 : 3,
        stem: ins.stem, unit: x.t.unit, tip: x.t.tip, key: ins.key_value, src: x.t, inst: ins, instIndex: x.i };
    });
    /* Q3 */
    var msel = shuffled(sel.matching, rnd);
    var Q3 = [buildMatching(msel[0], [3, 3, 3, 3], rnd, '3a'), buildMatching(msel[1], [2, 2, 2, 2], rnd, '3b'), buildOrdering(sel.ordering[0], '3c')];
    /* Q4 */
    var fsel = shuffled(sel.fill, rnd), FP = [[4, 4], [4, 4], [5, 4]];
    var Q4 = fsel.map(function (it, i) { return buildFill(it, FP[i], rnd, '4' + L[i]); });
    var mock = { k: k, seed: seed, epoch: sel.epoch, slice: sel.m,
      questions: [
        { q: 1, title: 'Question 1 - Reading and choice (25 points)', items: Q1 },
        { q: 2, title: 'Question 2 - Calculation (25 points)', items: Q2 },
        { q: 3, title: 'Question 3 - Matching and ordering (25 points)', items: Q3 },
        { q: 4, title: 'Question 4 - Filling the blanks (25 points)', items: Q4 }] };
    mock.itemIds = uidOf(sel);
    mock.families = sel.families;
    var tot = 0;
    mock.questions.forEach(function (Q) {
      var s = 0; Q.items.forEach(function (x) { s += root.MockScoring.maxOf(x); });
      if (s !== 25) throw new Error('question ' + Q.q + ' has ' + s + ' points, expected 25');
      tot += s;
    });
    if (tot !== 100) throw new Error('mock has ' + tot + ' points, expected 100');
    mock.total = tot;
    return mock;
  }

  root.MockDerive = { BANK_SEED: BANK_SEED, hashStr: hashStr, mulberry32: mulberry32, shuffled: shuffled, defaultSeed: defaultSeed,
    selectUnits: selectUnits, uidOf: uidOf, deriveMock: deriveMock };
  if (typeof module !== 'undefined' && module.exports) { module.exports = root.MockDerive; }
})(typeof window !== 'undefined' ? window : globalThis);
