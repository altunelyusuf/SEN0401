#!/usr/bin/env python3
"""Prune make v1.0.0 (X3b): creates the NEW part versions of the mock families after the exam-wins removals (exclusion index v1.0.1).
For each family: new generator version (the old generator plus a REMOVED filter applied at the end; the draws stay identical, so every kept
template equals the previous version), new part file (written by the new generator), new checker version (the old checker with the
listed one-line edits, each edit asserted to occur exactly once). Old files are not touched. Holds no item text: only code lines and ids.
Usage: mock_family_prune_make_v1_0_0.py"""
import json, os, re, subprocess, sys, hashlib
P = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts"
PUB = "/home/claude/sen0401/08-tooling/exam/mock"
def rd(p): return open(p, encoding="utf-8").read()
def sub(text, old, new, what):
    assert text.count(old) == 1, (what, old[:60], text.count(old))
    return text.replace(old, new)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
log = []
def L(x): print(x); log.append(x)

FAMS = {
 "3x": dict(old="v1_0_3", new="v1_0_4", removed=["n3x_4"], chk_dir=PUB,
   gen_edit=[('    return {"chapter": 3, "family": "release_tags", "items": items}',
              '    items = [i for i in items if i["id"] not in REMOVED]   # v1.0.4: exam-wins removals (draws above unchanged)\n    return {"chapter": 3, "family": "release_tags", "items": items}')],
   chk_edit=[('if [i.get("id") for i in its] != ["n3x_4", "n3x_7"]: bad("templates are not exactly n3x_4 and n3x_7")', 'if [i.get("id") for i in its] != ["n3x_7"]: bad("templates are not exactly n3x_7 (n3x_4 removed in v1.0.4)")'),
             ('if total < 16: bad("fewer than 16 instances")', 'if total < 8 * len(its): bad("fewer than 8 instances per template")'),
             ('c["items"][1]["instances"][2]["stem"] = c["items"][1]["instances"][2]["stem"].replace("You are asked to", "Please")', 'c["items"][0]["instances"][2]["stem"] = c["items"][0]["instances"][2]["stem"].replace("You are asked to", "Please")'),
             ('elif n == 5: c["items"][1]["instances"][0]["stem"] = c["items"][1]["instances"][0]["stem"].replace("in text order", "in the text order", 1)', 'elif n == 5: c["items"][0]["instances"][0]["stem"] = c["items"][0]["instances"][0]["stem"].replace("in text order", "in the text order", 1)'),
             ('v1.0.3 (simple-calculation rule, repair E8c: two templates, lists of 4 to 6 tags)', 'v1.0.4 (v1.0.3 after the exam-wins removal of template n3x_4: one template, lists of 4 to 6 tags; per-template floors unchanged: 8 instances, 6 distinct keys)')]),
 "4x": dict(old="v1_0_0", new="v1_0_1", removed=["n4x_5", "n4x_6"], chk_dir=P,
   gen_edit=[("    return {'chapter': 4, 'family': 'hash_search', 'items': items}",
              "    items = [i for i in items if i['id'] not in REMOVED]   # v1.0.1: exam-wins removals (draws above unchanged)\n    return {'chapter': 4, 'family': 'hash_search', 'items': items}")],
   chk_edit=[("    if len(its) < 6: F.append('templates < 6')", "    if len(its) < 5: F.append('templates < 5')   # v1.0.1: floor 6 -> 5 after the removal of n4x_5 and n4x_6"),
             ("    if sum(len(i['instances']) for i in its) < 48: F.append('instances < 48')", "    if sum(len(i['instances']) for i in its) < 8 * len(its): F.append('instances < 8 per template')   # v1.0.1: was 48 for 6 or more templates"),
             ("    if sum(1 for i in its if i.get('can_be_4')) != 1: F.append('can_be_4 count')", "    if sum(1 for i in its if i.get('can_be_4')) != 0: F.append('can_be_4 count')   # v1.0.1: the one flagged template (n4x_6) is removed"),
             ("        if i != 'n4x_%d' % (k + 1) or it.get('type')", "        if i != ['n4x_1', 'n4x_2', 'n4x_3', 'n4x_4', 'n4x_7'][k] or it.get('type')"),
             ("d = copy.deepcopy(d); x = d['items'][5]['instances'][0]", "d = copy.deepcopy(d); x = d['items'][-1]['instances'][0]"),
             ('mock_check_ch4x v1.0.0 - checks', 'mock_check_ch4x v1.0.1 (after the exam-wins removal of n4x_5 and n4x_6) - checks')]),
 "5x": dict(old="v1_0_1", new="v1_0_2", removed=["n5x_1", "n5x_4"], chk_dir=P,
   gen_edit=[("    d = {'chapter': 5, 'family': 'gap_scan', 'items': items}",
              "    items = [i for i in items if i['id'] not in REMOVED]   # v1.0.2: exam-wins removals (draws above unchanged)\n    d = {'chapter': 5, 'family': 'gap_scan', 'items': items}")],
   chk_edit=[("    if not 6 <= len(its) <= 8: F.append('templates not 6 to 8')", "    if not 4 <= len(its) <= 8: F.append('templates not 4 to 8')   # v1.0.2: floor 6 -> 4 after the removal of n5x_1 and n5x_4"),
             ("        if i != 'n5x_%d' % (k + 1) or it.get('type')", "        if i != ['n5x_2', 'n5x_3', 'n5x_5', 'n5x_6'][k] or it.get('type')")]),
 "5y": dict(old="v1_0_1", new="v1_0_2", removed=["n5y_8"], chk_dir=P, gen_edit=[("    d = {'chapter': 5, 'family': 'recovery_code', 'items': items}",
              "    items = [i for i in items if i['id'] not in REMOVED]   # v1.0.2: exam-wins removals (draws above unchanged)\n    d = {'chapter': 5, 'family': 'recovery_code', 'items': items}")],
   chk_edit=[]),
}
for key, f in FAMS.items():
    o, n = f["old"], f["new"]
    gsrc = "%s/mock_numeric_gen_ch%s_%s.py" % (P, key, o); gdst = "%s/mock_numeric_gen_ch%s_%s.py" % (P, key, n)
    csrc = "%s/mock_check_ch%s_%s.py" % (f["chk_dir"], key, o); cdst = "%s/mock_check_ch%s_%s.py" % (f["chk_dir"], key, n)
    for q in (gdst, cdst):
        assert not os.path.exists(q), "exists, new versions only: " + q
    g = rd(gsrc)
    for old, new in f["gen_edit"]: g = sub(g, old, new, "gen " + key)
    # place REMOVED after the first import line block
    m = re.search(r"^(import [^\n]*\n)", g, re.M)
    g = g[:m.end()] + "REMOVED = %r   # %s: templates removed by the exam-wins rule (exclusion index v1.0.1); the docstring above describes the previous version\n" % (tuple(f["removed"]), n) + g[m.end():]
    open(gdst, "w", encoding="utf-8").write(g)
    c = rd(csrc)
    for old, new in f["chk_edit"]: c = sub(c, old, new, "check " + key)
    if key == "5y":
        pass
    open(cdst, "w", encoding="utf-8").write(c)
    # the new part file is written by the new generator
    dst = "%s/mock_bank_ch%s_%s.json" % (P, key, n); assert not os.path.exists(dst)
    r = subprocess.run([sys.executable, "-I", gdst, "--out", dst], capture_output=True, text=True, cwd=P)
    assert r.returncode == 0, r.stderr[:300]
    a = json.load(open("%s/mock_bank_ch%s_%s.json" % (P, key, o))); b = json.load(open(dst))
    ka = {i["id"]: i for i in a["items"]}
    assert [i["id"] for i in b["items"]] == [i["id"] for i in a["items"] if i["id"] not in f["removed"]], key
    assert all(ka[i["id"]] == i for i in b["items"]), "kept template differs from previous version: " + key
    L("family %s: %s -> %s; removed templates %s; kept %d templates, every kept template equal to the previous version: True; part sha256 %s" % (key, o, n, f["removed"], len(b["items"]), sha(dst)))
    L("   new generator %s sha256 %s; new checker %s sha256 %s" % (os.path.basename(gdst), sha(gdst), os.path.basename(cdst), sha(cdst)))
open(os.path.join(PUB, "mock_family_prune_make_log_v1_0_0.txt"), "w").write("\n".join(log) + "\n")
