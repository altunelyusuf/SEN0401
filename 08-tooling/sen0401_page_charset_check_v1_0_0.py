#!/usr/bin/env python3
"""Page charset check v1.0.0 (Python 3.13, standard library only).

Usage: python3 -B sen0401_page_charset_check_v1_0_0.py FILE...
A file PASSES only when (1) a meta charset declaration for utf-8 lies fully within
the first 1024 bytes and (2) those 1024 bytes decode as UTF-8 (a multibyte sequence
merely cut by the end of the window is not an error; any other invalid byte is).
Missing file or no tag = FAIL. Exit 0 only when every file passes. Files are only read.
"""
import re
import sys
import codecs

WINDOW = 1024
TAG = re.compile(rb"<meta\s+charset\s*=\s*([\"']?)\s*utf-8\s*\1\s*/?\s*>", re.IGNORECASE)


def check(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        return False, f"cannot read file ({e.strerror})"
    head = data[:WINDOW]
    m = TAG.search(data)
    if m is None:
        tag_msg = "no utf-8 meta charset tag in file"
        ok_tag = False
    else:
        ok_tag = m.end() <= WINDOW
        tag_msg = f"tag at byte {m.start()}" + ("" if ok_tag else f" (beyond byte {WINDOW})")
    # incomplete trailing sequence is fine only when the window really cuts the file
    dec = codecs.getincrementaldecoder("utf-8")()
    try:
        dec.decode(head, final=(len(data) <= WINDOW))
        ok_dec = True
        dec_msg = "first 1024 bytes decode as UTF-8"
    except UnicodeDecodeError as e:
        ok_dec = False
        dec_msg = f"invalid UTF-8 at byte {e.start} ({e.reason})"
    return ok_tag and ok_dec, f"{tag_msg}; {dec_msg}"


def main(argv):
    if not argv:
        print("usage: sen0401_page_charset_check_v1_0_0.py FILE...")
        return 2
    allok = True
    for p in argv:
        ok, msg = check(p)
        allok &= ok
        print(f"{'PASS' if ok else 'FAIL'} {p}: {msg}")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
