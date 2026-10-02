#!/usr/bin/env python3
"""Make an exam release code with the instructor's private key (the key file is kept OUTSIDE the repository).
usage: sen0401_exam_release_v1_0_0.py KEYFILE CHAPTER EXAMCODE      e.g. ... key.json 6 M-12345
       EXAMCODE may be * (every exam of that chapter); CHAPTER * with EXAMCODE * releases everything.
The code is R1.<scope>.<signature>; the page checks the signature with the public key in course_page_config_v2_1_0.json."""
import sys, json, base64
__version__ = "1.0.0"
PREFIX = "sen0401-exam-release"
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def unb(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
def make(keyfile, chapter, code):
    k = json.load(open(keyfile))["private_jwk"]
    key = ec.derive_private_key(int.from_bytes(unb(k["d"]), "big"), ec.SECP256R1())
    scope = "%s:%s" % ("*" if chapter == "*" else "%02d" % int(chapter), code)
    der = key.sign((PREFIX + "|" + scope).encode(), ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(der)
    return "R1.%s.%s" % (scope, b64u(r.to_bytes(32, "big") + s.to_bytes(32, "big")))
if __name__ == "__main__":
    print(make(sys.argv[1], sys.argv[2], sys.argv[3]))
