/* ===== UI section - SEN0401 mock exam, v1.0.0 (no item text; reads the embedded bank) ===== */
(function () {
  'use strict';
  var BANK = JSON.parse(document.getElementById('mock-bank').textContent);
  var ITEMS = BANK.items;
  var LET = 'ABCDE';
  var S = { mock: null, checked: false, result: null, k: 1, seed: 0 };

  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (a) {
      if (a === 'class') e.className = attrs[a];
      else if (a === 'text') e.textContent = attrs[a];
      else if (a.slice(0, 2) === 'on') e.addEventListener(a.slice(2), attrs[a]);
      else e.setAttribute(a, attrs[a]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* storage not available: page works without it */ } }

  function tipText(t) { return 'Tip: ' + String(t).replace(/^\s*Tip:\s*/i, ''); }
  function intention(stem) {
    var m = /You are asked to[^]*$/.exec(stem || '');
    return m ? m[0] : '';
  }
  function letterSub(text, item) {
    /* {oN} in a solution text names the option with original index N; print the letter it has after the shuffle */
    var map = {};
    var list = item.options || item.responses || item.bank || [];
    list.forEach(function (o, d) { map[o.orig] = LET[d]; });
    return String(text).replace(/\{o(\d)\}/g, function (_, n) { return map[n] !== undefined ? map[n] : '?'; });
  }

  /* ---------- paper ---------- */
  function choiceNode(it) {
    var wrap = h('div', { class: 'opts', role: 'group', 'aria-label': 'Answer ' + it.label });
    it.options.forEach(function (o, d) {
      var b = h('button', { type: 'button', class: 'opt', 'data-idx': String(d), 'aria-pressed': 'false', onclick: function () {
        if (S.checked) return;
        var on = b.getAttribute('aria-pressed') === 'true';
        Array.prototype.forEach.call(wrap.children, function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', on ? 'false' : 'true');
        persist();
      } }, [h('span', { class: 'let', text: LET[d] }), h('span', { class: 'txt', text: o.text }), h('span', { class: 'pbox' })]);
      wrap.appendChild(b);
    });
    return wrap;
  }
  function numericNode(it) {
    var boxes = h('span', { class: 'digits' });
    var spans = [];
    for (var i = 0; i < 5; i++) { var s = h('span', { class: 'dbox' }); spans.push(s); boxes.appendChild(s); }
    var inp = h('input', { type: 'text', inputmode: 'numeric', maxlength: '5', class: 'digin', autocomplete: 'off', 'aria-label': 'Answer ' + it.label + ' in digits', oninput: function () {
      var v = inp.value.replace(/[^0-9]/g, '').slice(0, 5); if (v !== inp.value) inp.value = v;
      for (var j = 0; j < 5; j++) spans[j].textContent = '';
      for (var q = 0; q < v.length; q++) spans[5 - v.length + q].textContent = v[q];
      persist();
    } });
    var u = h('span', { class: 'unit', text: it.unit ? it.unit : '' });
    return h('div', { class: 'numrow' }, [h('span', { class: 'digwrap' }, [boxes, inp]), u]);
  }
  function selectNode(n, offset, cls) {
    var s = h('select', { class: cls || 'sel' });
    s.appendChild(h('option', { value: '', text: '-' }));
    for (var i = 0; i < n; i++) s.appendChild(h('option', { value: String(i), text: offset === 'L' ? LET[i] : String(i + 1) }));
    s.addEventListener('change', persist);
    return s;
  }
  function itemCard(it) {
    var card = h('article', { class: 'item', 'data-uid': it.uid, 'data-type': it.type });
    var head = h('div', { class: 'ihead' }, [h('span', { class: 'lab', text: it.label + '.' }), h('span', { class: 'pts', text: ptsText(it) })]);
    card.appendChild(head);
    if (it.type === 'choice') {
      card.appendChild(h('p', { class: 'stem', text: it.stem }));
      if (it.tip) card.appendChild(h('p', { class: 'tip', text: tipText(it.tip) }));
      card.appendChild(choiceNode(it));
    } else if (it.type === 'numeric') {
      card.appendChild(h('p', { class: 'stem', text: it.stem }));
      if (it.tip) card.appendChild(h('p', { class: 'tip', text: tipText(it.tip) }));
      card.appendChild(h('p', { class: 'how', text: 'Write the answer in ' + (it.unit || 'the unit named') + ', one digit in each box, starting from the right.' }));
      card.appendChild(numericNode(it));
    } else if (it.type === 'matching') {
      card.appendChild(h('p', { class: 'stem', text: it.intro }));
      if (it.tip) card.appendChild(h('p', { class: 'tip', text: tipText(it.tip) }));
      var rows = h('div', { class: 'rows' });
      it.premises.forEach(function (p, r) {
        var sel = selectNode(5, 'L', 'sel');
        rows.appendChild(h('div', { class: 'row', 'data-row': String(r) }, [h('span', { class: 'rn', text: (r + 1) + '.' }), h('span', { class: 'rt', text: p }),
          h('span', { class: 'ans' }, [sel, h('span', { class: 'pbox' }), h('span', { class: 'mark' })])]));
      });
      card.appendChild(rows);
      var bl = h('ol', { class: 'bank', type: 'A' });
      it.responses.forEach(function (o) { bl.appendChild(h('li', { text: o.text })); });
      card.appendChild(h('p', { class: 'how', text: 'Write in the box beside each situation the letter of its response.' }));
      card.appendChild(bl);
    } else if (it.type === 'ordering') {
      card.appendChild(h('p', { class: 'stem', text: it.intro }));
      if (it.tip) card.appendChild(h('p', { class: 'tip', text: tipText(it.tip) }));
      var rows2 = h('div', { class: 'rows' });
      it.steps.forEach(function (p, r) {
        rows2.appendChild(h('div', { class: 'row', 'data-row': String(r) }, [h('span', { class: 'rn', text: String.fromCharCode(65 + r) + '.' }), h('span', { class: 'rt', text: p }),
          h('span', { class: 'ans' }, [selectNode(5, 'N', 'sel'), h('span', { class: 'pbox' }), h('span', { class: 'mark' })])]));
      });
      card.appendChild(h('p', { class: 'how', text: 'Write in the box beside each statement its place, 1 to 5.' }));
      card.appendChild(rows2);
    } else if (it.type === 'fill') {
      card.appendChild(h('p', { class: 'stem', text: it.stem }));
      if (it.tip) card.appendChild(h('p', { class: 'tip', text: tipText(it.tip) }));
      var bl2 = h('ol', { class: 'bank', type: 'A' });
      it.bank.forEach(function (o) { bl2.appendChild(h('li', { text: o.text })); });
      card.appendChild(bl2);
      var rows3 = h('div', { class: 'rows' });
      it.blanks.forEach(function (b, r) {
        var parts = b.sentence.split('____');
        var sel = selectNode(5, 'L', 'sel');
        var line = h('span', { class: 'rt' }, [parts[0], h('span', { class: 'ans' }, [sel, h('span', { class: 'pbox' }), h('span', { class: 'mark' })]), parts.slice(1).join('____')]);
        rows3.appendChild(h('div', { class: 'row', 'data-row': String(r) }, [h('span', { class: 'rn', text: (r + 1) + '.' }), line]));
      });
      card.appendChild(h('p', { class: 'how', text: 'Write in the box of each blank the letter of the bank entry that makes the sentence true.' }));
      card.appendChild(rows3);
    }
    card.appendChild(h('div', { class: 'fb' }));
    return card;
  }
  function ptsText(it) {
    if (it.type === 'choice' || it.type === 'numeric') return it.points + (it.points === 1 ? ' point' : ' points');
    if (it.type === 'matching') return it.rowPoints[0] + ' points a row';
    if (it.type === 'ordering') return '1 point a step';
    return it.blankPoints.join(' + ') + ' points';
  }

  function render() {
    var mock = S.mock;
    var paper = $('#paper'); paper.textContent = '';
    paper.appendChild(h('div', { class: 'phead' }, [h('h1', { text: 'SEN0401 Special Topics: Blockchain - Practice midterm ' + mock.k }),
      h('p', { class: 'meta', text: 'Chapters 1 to 6. 100 points. Seed ' + mock.seed + '. A right answer scores its points; a wrong or empty answer scores 0. Two answers in one place count as no answer.' }),
      h('p', { class: 'meta printonly', text: 'Name: ____________________   (practice paper; no personal data is stored)' })]));
    mock.questions.forEach(function (Q) {
      var sec = h('section', { class: 'question', 'data-q': String(Q.q) }, [h('h2', { text: Q.title })]);
      Q.items.forEach(function (it) { sec.appendChild(itemCard(it)); });
      sec.appendChild(h('p', { class: 'qscore noprint', 'data-qscore': String(Q.q) }));
      paper.appendChild(sec);
    });
    $('#result').hidden = true; $('#result').textContent = '';
    $('#btn-sol').disabled = true; $('#btn-check').disabled = false;
    S.checked = false; S.result = null;
    var note = $('#notice');
    var fam = mock.families || {}, fl = Object.keys(fam).sort().map(function (x) { return x.replace(/_/g, ' '); });
    note.textContent = (mock.k > 8 ? 'Items of earlier mocks come back from mock 9 on; none is from the real exam.' : 'Mocks 1 to 8 share no item with each other; none is from the real exam.') + ' The bank gives 8 fully disjoint mocks.' + (fl.length ? ' Question 2 has one place from each of these families: ' + fl.join(', ') + '.' : '');
    $('#in-k').value = mock.k; $('#in-seed').value = mock.seed;
    try { var hh = '#k=' + mock.k + '&seed=' + mock.seed; if (location.hash !== hh) history.replaceState(null, '', hh); } catch (e) { /* ignore */ }
    restore();
  }

  /* ---------- answers ---------- */
  function collect() {
    var ans = {};
    S.mock.questions.forEach(function (Q) {
      Q.items.forEach(function (it) {
        var card = $('[data-uid="' + (window.CSS && CSS.escape ? CSS.escape(it.uid) : it.uid) + '"]');
        var a = null;
        if (it.type === 'choice') {
          var on = card.querySelector('.opt[aria-pressed="true"]'); a = on ? Number(on.getAttribute('data-idx')) : null;
        } else if (it.type === 'numeric') {
          a = card.querySelector('.digin').value || null;
        } else {
          a = Array.prototype.map.call(card.querySelectorAll('select'), function (s) { return s.value === '' ? null : Number(s.value) + (it.type === 'ordering' ? 1 : 0); });
        }
        ans[it.uid] = a;
      });
    });
    return ans;
  }
  function apply(ans) {
    S.mock.questions.forEach(function (Q) {
      Q.items.forEach(function (it) {
        var card = $('[data-uid="' + (window.CSS && CSS.escape ? CSS.escape(it.uid) : it.uid) + '"]');
        var a = ans[it.uid];
        if (a === null || a === undefined) return;
        if (it.type === 'choice') {
          var b = card.querySelector('.opt[data-idx="' + a + '"]'); if (b) b.setAttribute('aria-pressed', 'true');
        } else if (it.type === 'numeric') {
          var inp = card.querySelector('.digin'); inp.value = a; inp.dispatchEvent(new Event('input'));
        } else {
          Array.prototype.forEach.call(card.querySelectorAll('select'), function (s, i) { if (a[i] !== null && a[i] !== undefined) s.value = String(a[i] - (it.type === 'ordering' ? 1 : 0)); });
        }
      });
    });
  }
  function storeKey() { return 'sen0401mock:' + S.mock.k + ':' + S.mock.seed; }
  function persist() { if (!S.mock || S.checked) return; lsSet(storeKey(), JSON.stringify(collect())); }
  function restore() { var v = lsGet(storeKey()); if (v) { try { apply(JSON.parse(v)); } catch (e) { /* ignore */ } } }

  /* ---------- check ---------- */
  function check() {
    if (S.checked) return;
    persist();
    var ans = collect();
    var res = window.MockScoring.scoreMock(S.mock, ans);
    S.checked = true; S.result = res; S.answers = ans;
    $('#btn-check').disabled = true; $('#btn-sol').disabled = false;
    var R = $('#result'); R.hidden = false; R.textContent = '';
    R.appendChild(h('h2', { text: 'Result' }));
    R.appendChild(h('p', { id: 'score-total', 'data-score': String(res.total), 'data-max': String(res.max), text: 'Total: ' + res.total + ' / ' + res.max }));
    var ul = h('ul', { id: 'score-q' });
    S.mock.questions.forEach(function (Q) {
      var r = res.byQuestion[Q.q];
      ul.appendChild(h('li', { 'data-q': String(Q.q), 'data-score': String(r.got), text: 'Question ' + Q.q + ': ' + r.got + ' / ' + r.max }));
      var qs = $('[data-qscore="' + Q.q + '"]'); qs.textContent = 'Question ' + Q.q + ': ' + r.got + ' / ' + r.max;
    });
    R.appendChild(ul);
    R.appendChild(h('p', { class: 'meta', text: 'Right = its points. Wrong or empty = 0. No deduction, no bonus.' }));
    S.mock.questions.forEach(function (Q) {
      Q.items.forEach(function (it) { markItem(it, res.items[it.uid], ans[it.uid]); });
    });
    Array.prototype.forEach.call(document.querySelectorAll('#paper select, #paper input, #paper .opt'), function (e) { e.disabled = true; });
    showSolutions(true);
    R.scrollIntoView && R.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function markItem(it, r, a) {
    var card = $('[data-uid="' + (window.CSS && CSS.escape ? CSS.escape(it.uid) : it.uid) + '"]');
    var cls = r.got === r.max ? 'ok' : (r.got > 0 ? 'part' : (isBlank(it, a) ? 'blank' : 'bad'));
    card.classList.add('done', cls);
    $('.pts', card).textContent = r.got + ' / ' + r.max;
    if (it.type === 'choice') {
      Array.prototype.forEach.call(card.querySelectorAll('.opt'), function (b, d) {
        if (d === it.correct) b.classList.add('isright');
        if (a !== null && Number(a) === d && d !== it.correct) b.classList.add('iswrong');
      });
    } else if (it.type === 'numeric') {
      card.querySelector('.digwrap').classList.add(r.got ? 'isright' : 'iswrong');
    } else {
      Array.prototype.forEach.call(card.querySelectorAll('.row'), function (row, i) {
        var m = $('.mark', row); m.textContent = r.right[i] ? ' ✓' : ' ✗'; m.classList.add(r.right[i] ? 'isright' : 'iswrong');
      });
    }
  }
  function isBlank(it, a) {
    if (a === null || a === undefined || a === '') return true;
    if (Array.isArray(a)) return a.every(function (x) { return x === null || x === undefined; });
    return false;
  }

  /* ---------- solutions (built only after the check) ---------- */
  function ol(arr, item) { var o = h('ol', { class: 'sol-steps' }); arr.forEach(function (s) { o.appendChild(h('li', { text: letterSub(typeof s === 'string' ? s : s.text, item) })); }); return o; }
  function solutionNode(it) {
    var src = it.src, box = h('div', { class: 'sol' });
    function line(label, txt) { box.appendChild(h('p', {}, [h('strong', { text: label + ' ' }), txt])); }
    var inten = intention(it.stem || it.intro || (it.inst && it.inst.stem) || '');
    if (it.type === 'numeric') inten = intention(it.stem);
    if (inten) line('Intention:', inten);
    if (it.type === 'choice') {
      line('Right answer:', LET[it.correct] + '. ' + it.options[it.correct].text);
      box.appendChild(h('strong', { text: 'Steps' })); box.appendChild(ol(src.steps || [], it));
      line('Why it is right:', letterSub(src.why_right || '', it));
      var wl = h('ul', { class: 'sol-wrong' });
      it.options.forEach(function (o, d) {
        if (d === it.correct) return;
        wl.appendChild(h('li', { text: LET[d] + '. ' + letterSub((src.why_wrong || {})[String(o.orig)] || 'This option does not follow from the facts.', it) }));
      });
      box.appendChild(h('strong', { text: 'Why each other option fails' })); box.appendChild(wl);
    } else if (it.type === 'numeric') {
      line('Right answer:', String(it.key) + (it.unit ? ' ' + it.unit : ''));
      box.appendChild(h('strong', { text: 'Steps' })); box.appendChild(ol(it.inst.steps || [], it));
      line('Why it is right:', it.inst.why_right || '');
      var cw = h('ul', { class: 'sol-wrong' });
      (it.inst.common_wrong || []).forEach(function (w) { cw.appendChild(h('li', { text: w.value + ' - ' + w.why })); });
      box.appendChild(h('strong', { text: 'Common wrong answers' })); box.appendChild(cw);
    } else if (it.type === 'matching') {
      line('Right answers:', it.correct.map(function (d, r) { return (r + 1) + '-' + LET[d]; }).join('   '));
      box.appendChild(h('strong', { text: 'Steps' })); box.appendChild(ol(src.steps || [], it));
      line('Why it is right:', letterSub(src.why_right || '', it));
      var ml = h('ul', { class: 'sol-wrong' });
      (src.why_wrong_rows || []).forEach(function (w, r) { ml.appendChild(h('li', { text: 'Row ' + (r + 1) + ' (right: ' + LET[it.correct[r]] + '). ' + letterSub(w, it) })); });
      box.appendChild(h('strong', { text: 'Why the other responses fail' })); box.appendChild(ml);
    } else if (it.type === 'ordering') {
      line('Right places:', it.correct.map(function (p, r) { return String.fromCharCode(65 + r) + '-' + p; }).join('   '));
      box.appendChild(h('strong', { text: 'Steps' })); box.appendChild(ol(src.steps_solution || [], it));
      line('Why it is right:', src.why_right || '');
      var ql = h('ul', { class: 'sol-wrong' });
      (src.why_wrong_rows || []).forEach(function (w, r) { ql.appendChild(h('li', { text: 'Statement ' + String.fromCharCode(65 + r) + ' (place ' + it.correct[r] + '). ' + w })); });
      box.appendChild(h('strong', { text: 'Why the other places fail' })); box.appendChild(ql);
    } else if (it.type === 'fill') {
      line('Right entries:', it.correct.map(function (d, r) { return (r + 1) + '-' + LET[d]; }).join('   '));
      box.appendChild(h('strong', { text: 'Steps' })); box.appendChild(ol(src.steps || [], it));
      line('Why it is right:', letterSub(src.why_right || '', it));
      var fl = h('ul', { class: 'sol-wrong' });
      it.bank.forEach(function (o, d) {
        var w = (src.why_wrong_entries || {})[String(o.orig)];
        if (w) fl.appendChild(h('li', { text: LET[d] + '. ' + letterSub(w, it) }));
      });
      box.appendChild(h('strong', { text: 'Why the other bank entries fail' })); box.appendChild(fl);
    }
    var wq = (it.inst && it.inst.why_question) || (it.src && it.src.why_question);
    if (wq) box.appendChild(h('p', { class: 'whyq', 'data-whyq': '1', text: String(wq) }));
    return box;
  }
  function showSolutions(on) {
    S.mock.questions.forEach(function (Q) {
      Q.items.forEach(function (it) {
        var card = $('[data-uid="' + (window.CSS && CSS.escape ? CSS.escape(it.uid) : it.uid) + '"]');
        var fb = $('.fb', card); fb.textContent = '';
        if (on) { var d = h('details', { class: 'noprint', open: 'open' }, [h('summary', { text: 'Worked solution ' + it.label }), solutionNode(it)]); fb.appendChild(d); }
      });
    });
    S.solutionsShown = on;
    $('#btn-sol').textContent = on ? 'Hide solutions' : 'Show solutions';
  }

  /* ---------- controls ---------- */
  function derive(k, seed) {
    k = Math.max(1, Math.floor(Number(k) || 1));
    seed = Math.floor(Number(seed));
    if (!isFinite(seed)) seed = window.MockDerive.defaultSeed(k);
    S.mock = window.MockDerive.deriveMock(ITEMS, k, seed);
    S.k = k; S.seed = seed;
    render();
    return S.mock;
  }
  function setFs(px) {
    px = Math.max(16, Math.min(26, px));
    document.documentElement.style.setProperty('--fs', px + 'px');
    lsSet('sen0401mock:fs', String(px));
    S.fs = px;
  }
  function init() {
    var fs = Number(lsGet('sen0401mock:fs')); S.fs = (fs >= 16 && fs <= 26) ? fs : 17; setFs(S.fs);
    $('#bank-note').textContent = BANK.synthetic ? 'SAMPLE BANK (synthetic test items - not for students)' : '';
    $('#btn-check').addEventListener('click', check);
    $('#btn-sol').addEventListener('click', function () { if (S.checked) showSolutions(!S.solutionsShown); });
    $('#btn-print').addEventListener('click', function () { window.print(); });
    $('#btn-derive').addEventListener('click', function () { derive(S.k + 1, window.MockDerive.defaultSeed(S.k + 1) + Math.floor(Math.random() * 90000)); });
    $('#btn-load').addEventListener('click', function () { derive($('#in-k').value, $('#in-seed').value); });
    $('#btn-reset').addEventListener('click', function () { try { window.localStorage.removeItem(storeKey()); } catch (e) { /* ignore */ } derive(S.k, S.seed); });
    $('#fs-up').addEventListener('click', function () { setFs(S.fs + 1); });
    $('#fs-down').addEventListener('click', function () { setFs(S.fs - 1); });
    var k = (window.MOCK_PRESET && window.MOCK_PRESET.k) || 1, seed = null;
    var m = /k=(\d+)&seed=(-?\d+)/.exec(location.hash || '');
    if (m && !(window.MOCK_PRESET && window.MOCK_PRESET.lock)) { k = Number(m[1]); seed = Number(m[2]); }
    derive(k, seed === null ? window.MockDerive.defaultSeed(k) : seed);
  }
  window.MockApp = { derive: derive, getMock: function () { return S.mock; }, collect: collect, apply: apply, check: check,
    state: S, items: ITEMS, showSolutions: showSolutions };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
