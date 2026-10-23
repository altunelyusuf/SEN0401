#!/usr/bin/env python3
"""sen0401_lineage_close_stories v1_1_0 - closes (T_Complete -> Done) the stories whose every task is Done, in one new version (G125: a story is Done when its tasks are Done on controlled evidence; the controls are recorded in the versions named in each story's audit notes). Refuses a story with a task that is not Done. Usage: ... [--split-ch11] STORY [STORY...]   (--split-ch11 first moves the criterion AC3T_Ch11, whose page work waits in ST_Section_Links for the owner's answer on ex:CR3_PageClick, from ST_Page_Template to ST_Section_Links: the L4 remedy of splitting the remainder out of a story committed to a closed iteration; the criterion itself is not edited)"""
__version__ = "1.1.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
args = sys.argv[1:]; split = "--split-ch11" in args; args = [a for a in args if a != "--split-ch11"]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
if split:
    i, j = T.blk(t, "ST_Page_Template"); b = t[i:j]; assert "ex:AC3T_Ch10, ex:AC3T_Ch11, ex:AC3T_Ch12" in b; t = t[:i] + b.replace("ex:AC3T_Ch10, ex:AC3T_Ch11, ex:AC3T_Ch12", "ex:AC3T_Ch10, ex:AC3T_Ch12", 1) + t[j:]
    i, j = T.blk(t, "ST_Section_Links"); b = t[i:j]; m = re.search(r"backlog:hasAcceptanceCriterion ([^;]*?)\s*;", b); assert m and "AC3T_Ch11" not in m.group(1)
    t = t[:i] + b.replace(m.group(0), "backlog:hasAcceptanceCriterion %s, ex:AC3T_Ch11 ;" % m.group(1).rstrip(), 1) + t[j:]
    why = "Split %s UTC in v%s (the L4 remedy for a story committed to an iteration that has closed): the criterion ex:AC3T_Ch11 (the chapter 11 page, whose work waits for the owner's answer on ex:CR3_PageClick and is carried by TK_SecLinks_Ch11_Page of ST_Section_Links) moves from ST_Page_Template, committed to Iter_13, to ST_Section_Links; the criterion is not edited, and nothing is declared met. ST_Page_Template keeps AC3T_Ch08, AC3T_Ch10, AC3T_Ch12 and AC3T_Ch14, which are met." % (now, nxt)
    L.append("ex:ST_Page_Template backlog:hasAuditNote %s .\nex:ST_Section_Links backlog:hasAuditNote %s .\n" % (lit(why), lit(why)))
for sid in args:
    i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:InProgress" in b, sid
    tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1)); bad = [k for k in tks if "backlog:hasState backlog:Done" not in t[T.blk(t, k)[0]:T.blk(t, k)[1]]]
    assert not bad, "%s has tasks not Done: %s" % (sid, bad)
    fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks)))
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, sid
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % (m.group(1), fin, now), 1) + t[j:]
    L.append(C.transition("Done31T_" + sid, sid, "T_Complete", now, "Closed %s UTC in v%s: all %d tasks of the story are Done on controlled, bridge-verified evidence (the controls are recorded in the audit notes of the story and of the tasks); the last task finished %s UTC. The story stays closed (G125)." % (now, nxt, len(tks), fin), sid + " completed"))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, "Stories closed because every task is Done: %s." % ", ".join(args))))
