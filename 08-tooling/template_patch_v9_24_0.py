#!/usr/bin/env python3
"""SEN0401 template patch 9.24.0 (over the SEN0414 template 9.23.0, which is copied unchanged into this folder as
course_page_template_v9_23_0.html - byte-identical to advancedprogrammingwithpython/08-tooling/course_page_template_v9_23_0.html).

9.23.0 is SEN0414's template and carries SEN0414 facts that a second course must not inherit. This patch makes them
come from the course configuration (data.course, i.e. course_page_config_v2_1_0.json) and changes nothing else:

 1. Exam identity. The instructor's public key, the release-code prefix and the bonus were literals
    (XEX_PUB / XEX_PREFIX / XEX_BONUS = SEN0414's). They now come from data.course.exam {public_key, release_prefix, bonus_points};
    the course code and title written into the result file, the result PDF and the audit-log zip (format 'sen0414-exam-result',
    'sen0414-audit-log', course 'SEN0414', file names 'sen0414-ch..', the PDF heading 'SEN0414 Advanced Programming with Python',
    the audit README) come from data.course.exam.course / .title. Absent keys fall back to the old SEN0414 literals, so a
    SEN0414 configuration builds as before.
 2. Code Lab snippets: data.course.codelab_snippets ([[label, code], ...]) replaces CODELAB_SNIPPETS when present.
 3. SPARQL samples: data.course.sparql_samples ([[label, query], ...]) replaces SPARQL_SAMPLES when present; in a query
    {PFX} stands for the rdfs/owl/skos PREFIX lines and {FIRST_LEAF} for the lower-case label of the chapter's first concept.
 4. Step-through examples: data.course.trace_examples ([[label, code], ...]) replaces TRACE_EX when present, and the
    Step-through box opens with that list's first program (it was the literal 'total = 0 / for n in range...').
 5. Playground code patterns: data.course.code_patterns ([[label, code], ...]) replaces ED_TPL (the 'Code patterns' group
    of the Playground list) when present.
 6. Agent icons for SEN0401's subjects (verification, configuration, interface, client, block, assurance, linked data,
    curve, practice, identifier), which 0401's template 9.4.4 had and 9.23.0 lacks, are appended to the table.
 7. Multiple choice with several correct (9.23.0's new type) takes a concept's sentences from its definition and from `paras`; a concept whose text
    is ONE paragraph (every SEN0401 chapter written before the paragraph rewrite) has empty `paras`, so it offered one sentence at most and the type
    could not be made. Such a concept now contributes the sentences of its `body` as well.
 8. A version comment is added at the top.
The Playground default program stays data.course.playground (already configuration-driven in 9.23.0).
usage: template_patch_v9_24_0.py IN(course_page_template_v9_23_0.html) OUT(course_page_template_v9_24_0.html)"""
import sys
__version__ = "9.24.0"
s = open(sys.argv[1], encoding="utf-8").read()
CHANGES = []
def rep(a, b, n=1, what=""):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b); CHANGES.append(what or a[:60])

# 1 exam identity
a = s.index("const XEX_PUB={"); e = s.index("const XEX_CH=")
old = s[a:e]
assert old.rstrip().endswith("XEX_BONUS=10;") and "sen0414-exam-release" in old
pub_old = old[old.index("{"):old.index("}") + 1]
s = s[:a] + ("const XEX_CFG=D.course.exam||{},XEX_PUB=XEX_CFG.public_key||" + pub_old + ", XEX_PREFIX=XEX_CFG.release_prefix||'sen0414-exam-release', XEX_BONUS=XEX_CFG.bonus_points==null?10:XEX_CFG.bonus_points,\n"
             " XEX_COURSE=XEX_CFG.course||'SEN0414', XEX_SLUG=XEX_COURSE.toLowerCase(), XEX_TITLE=XEX_CFG.title||'SEN0414 Advanced Programming with Python';\n") + s[e:]
CHANGES.append("exam constants from data.course.exam")
rep("format:'sen0414-exam-result',format_version:1,course:'SEN0414'", "format:XEX_SLUG+'-exam-result',format_version:1,course:XEX_COURSE", 1, "exam result file format and course")
rep("format:'sen0414-audit-log',format_version:1,course:'SEN0414'", "format:XEX_SLUG+'-audit-log',format_version:1,course:XEX_COURSE", 1, "audit log format and course")
rep("'sen0414-ch'+XEX_CH+'-'+rec.code", "XEX_SLUG+'-ch'+XEX_CH+'-'+rec.code", 1, "result file name")
rep("return 'sen0414-ch'+XEX_CH+'-audit-'", "return XEX_SLUG+'-ch'+XEX_CH+'-audit-'", 1, "audit zip name")
rep("put('SEN0414 Advanced Programming with Python',22,false,'#5B6B7B',2)", "put(XEX_TITLE,22,false,'#5B6B7B',2)", 1, "result PDF heading")
rep("data:'SEN0414 chapter '+D.chapter+' - audit log of this browser", "data:XEX_COURSE+' chapter '+D.chapter+' - audit log of this browser", 1, "audit README")

# 2 Code Lab snippets
rep("const CODELAB_SNIPPETS=[\n", "const CODELAB_SNIPPETS=(D.course.codelab_snippets&&D.course.codelab_snippets.length)?D.course.codelab_snippets:[\n", 1, "Code Lab snippets from configuration")
# 3 SPARQL samples
rep("const SPARQL_SAMPLES=[\n", "const SPQ_FIX=q=>q.split('{PFX}').join(PFX).split('{FIRST_LEAF}').join(String(((D.nodes.find(n=>+n.level>=3)||D.nodes[0]||{}).label)||'').toLowerCase().replace(/\"/g,''));\n"
    "const SPARQL_SAMPLES=(D.course.sparql_samples&&D.course.sparql_samples.length)?D.course.sparql_samples.map(x=>[x[0],SPQ_FIX(x[1])]):[\n", 1, "SPARQL samples from configuration")
# 4 step-through examples
a = s.index("const TRACE_EX=["); e = s.index("\n", a)
line = s[a:e]; assert line.endswith("]];")
s = s[:a] + "const TRACE_EX=(D.course.trace_examples&&D.course.trace_examples.length)?D.course.trace_examples.map(x=>x.slice()):" + line[len("const TRACE_EX="):] + s[e:]
CHANGES.append("Step-through examples from configuration")
rep('aria-label="Program to step through">total = 0\\nfor n in range(1, 5):\\n    total = total + n\\nprint(total)</textarea>', "aria-label=\"Program to step through\">'+esc(TRACE_EX[0][1])+'</textarea>", 1, "Step-through default program is the list's first")
# 5 code patterns
a = s.index("const ED_TPL=["); e = s.index("\n", a)
line = s[a:e]; assert line.endswith("]];")
s = s[:a] + "const ED_TPL=(D.course.code_patterns&&D.course.code_patterns.length)?D.course.code_patterns:" + line[len("const ED_TPL="):] + s[e:]
CHANGES.append("Playground code patterns from configuration")
# 6 icons
rep("[/programs?/i,'\U0001F3AC']];", "[/programs?/i,'\U0001F3AC'],[/verif/i,'✅'],[/configur/i,'\U0001F39B️'],[/rpc|interface/i,'\U0001F50C'],[/client/i,'\U0001F4DF'],[/block/i,'\U0001F9F1'],[/assurance|trust/i,'\U0001F50F'],[/linked/i,'\U0001F310'],[/curve/i,'\U0001F4D0'],[/practice/i,'\U0001F6E0️'],[/identif/i,'\U0001FAAA']];", 1, "agent icons for SEN0401 subjects")
# 7 xSents also reads the body of a one-paragraph concept
rep("const raw=[n.definition||''].concat((n.paras||[]).map(p=>p.text));", "const raw=[n.definition||''].concat(n.paras&&n.paras.length?n.paras.map(p=>p.text):[n.body||'']);", 1, "multiple choice, several correct: one-paragraph concepts contribute their body")
# 8 version comment
s = "<!-- course_page_template version 9.24.0 (SEN0401): 9.23.0 with exam identity, Code Lab snippets, SPARQL samples, Step-through examples and Playground code patterns read from the course configuration, agent icons for SEN0401's subjects, and sentences from one-paragraph concepts for the several-correct question type. See template_patch_v9_24_0.py. -->" + s
CHANGES.append("version comment")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s)); print("\n".join(" - " + c for c in CHANGES))
