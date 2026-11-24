"""Library match check (course ruling of 2026-11-24): the lab libraries, the chapter pages and the lab sessions must carry the same code.

Usage: python3 lib_match_check_v1_0_0.py SOURCE_DIR PAGE.html [PAGE.html ...] [--kit KIT_ENGINE_PY_DIR]
SOURCE_DIR is the folder with the library sources (this tooling folder). For every page the wheels it embeds are opened and
every library file in them is compared, byte for byte, with the file of the same name in SOURCE_DIR; the names that py_boot imports
must be in the wheels. With --kit, every file of the kit's engine/py must equal the source of the same name."""
import hashlib, io, json, os, re, sys, zipfile
def sha(b): return hashlib.sha256(b).hexdigest()[:16]
def main(argv):
    kit = None
    if "--kit" in argv:
        i = argv.index("--kit"); kit = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    src, pages = argv[0], argv[1:]
    bad = 0
    def ok(c, m):
        nonlocal bad
        print(("PASS " if c else "FAIL ") + m); bad += (not c)
    for page in pages:
        t = open(page, encoding="utf-8").read()
        m = re.search(r'"py_wheels": (\[.*?\]), "py_boot": "(.*?)(?<!\\)"', t, re.S)
        if not m: ok(False, os.path.basename(page) + ": no py_wheels / py_boot"); continue
        wheels = json.loads(m.group(1)); boot = json.loads('"' + m.group(2) + '"')
        have = {}
        for w in wheels:
            z = zipfile.ZipFile(io.BytesIO(bytes.fromhex(w["hex"])))
            for n in z.namelist():
                if n.endswith(".py"): have[n[:-3]] = z.read(n)
        for name, data in sorted(have.items()):
            f = os.path.join(src, name + ".py")
            ok(os.path.exists(f) and open(f, "rb").read() == data, "%s: %s equals the source file (%s)" % (os.path.basename(page), name, sha(data)))
        for name in sorted({n for line in boot.splitlines() if re.match(r"\s*(import|from)\s", line) for n in re.findall(r"sen0401_\w+", line)}):
            ok(name in have, "%s: py_boot imports %s, which is in the page's wheels" % (os.path.basename(page), name))
    if kit:
        for f in sorted(os.listdir(kit)):
            if f.endswith(".py"):
                s = os.path.join(src, f)
                ok(os.path.exists(s) and open(s, "rb").read() == open(os.path.join(kit, f), "rb").read(), "kit: %s equals the source file" % f)
    print("ALL MATCH" if not bad else "%d MISMATCH(ES)" % bad)
    return 1 if bad else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
