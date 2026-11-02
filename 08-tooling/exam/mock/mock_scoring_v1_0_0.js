/* ===== SCORING section (scoring.js) - SEN0401 mock exam, v1.0.0 =====
   Rule of the real midterm: a right answer scores its points; a wrong or empty answer scores 0.
   No deduction, no bonus. Pure functions: no DOM access, tested by node and by the page.
   Answer shapes (by item id):
     choice   : integer 0..4 (displayed position) or null
     numeric  : string of digits (at most five) or null / ''
     matching : array of 4 integers 0..4 (displayed response) or null per row
     ordering : array of 5 integers 1..5 (place of each displayed statement) or null per step
     fill     : array of 2 integers 0..4 (displayed bank entry) or null per blank */
(function (root) {
  'use strict';
  function digitsValue(s) {
    if (s === null || s === undefined) return null;
    var d = String(s).replace(/[^0-9]/g, '');
    if (d === '' || d.length > 5) return null;
    return parseInt(d, 10);
  }
  function isSet(a) { return a !== null && a !== undefined && a !== ''; }
  function maxOf(item) {
    switch (item.type) {
      case 'choice': return item.points;
      case 'numeric': return item.points;
      case 'matching': return item.rowPoints.reduce(function (s, x) { return s + x; }, 0);
      case 'ordering': return item.correct.length * item.stepPoints;
      case 'fill': return item.blankPoints.reduce(function (s, x) { return s + x; }, 0);
    }
    throw new Error('unknown item type ' + item.type);
  }
  /* returns {got, max, rows:[points per place], right:[bool per place]} */
  function scoreItem(item, ans) {
    var got = 0, rows = [], right = [], i;
    switch (item.type) {
      case 'choice':
        if (isSet(ans) && Number(ans) === item.correct) { got = item.points; } /*CH_WRONG*/
        rows = [got]; right = [got > 0];
        break;
      case 'numeric':
        var v = digitsValue(ans);
        if (v !== null && v === item.key) { got = item.points; } /*NU_WRONG*/
        rows = [got]; right = [got > 0];
        break;
      case 'matching':
        for (i = 0; i < item.correct.length; i++) {
          var a = ans ? ans[i] : null;
          var p = (isSet(a) && Number(a) === item.correct[i]) ? item.rowPoints[i] : 0; /*MA_WRONG*/
          rows.push(p); right.push(p > 0); got += p;
        }
        break;
      case 'ordering':
        for (i = 0; i < item.correct.length; i++) {
          var b = ans ? ans[i] : null;
          var q = (isSet(b) && Number(b) === item.correct[i]) ? item.stepPoints : 0; /*OR_WRONG*/
          rows.push(q); right.push(q > 0); got += q;
        }
        break;
      case 'fill':
        for (i = 0; i < item.correct.length; i++) {
          var c = ans ? ans[i] : null;
          var r = (isSet(c) && Number(c) === item.correct[i]) ? item.blankPoints[i] : 0; /*FI_WRONG*/
          rows.push(r); right.push(r > 0); got += r;
        }
        break;
      default: throw new Error('unknown item type ' + item.type);
    }
    return { got: got, max: maxOf(item), rows: rows, right: right };
  }
  /* mock: {questions:[{q, items:[...]}]}; answers: {id: answer}. returns {total, max, byQuestion:{q:{got,max}}, items:{id:{...}}} */
  function scoreMock(mock, answers) {
    var total = 0, max = 0, byQ = {}, items = {};
    mock.questions.forEach(function (Q) {
      var g = 0, m = 0;
      Q.items.forEach(function (it) {
        var r = scoreItem(it, answers[it.uid]);
        items[it.uid] = r; g += r.got; m += r.max;
      });
      byQ[Q.q] = { got: g, max: m };
      total += g; max += m;
    });
    return { total: total, max: max, byQuestion: byQ, items: items };
  }
  var api = { digitsValue: digitsValue, maxOf: maxOf, scoreItem: scoreItem, scoreMock: scoreMock };
  root.MockScoring = api;
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
})(typeof window !== 'undefined' ? window : globalThis);
