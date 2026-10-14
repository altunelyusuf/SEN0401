#!/usr/bin/env python3
"""sen0401_page_key_substitute v1.0.0 - makes a COPY of a SEN0401 chapter page whose embedded exam-release public key is replaced by the public half
of a freshly made TEST key, so that the page test can run its mock-exam release step on a machine that does not hold the instructor's private key
(SEN0401's key lives outside every repository: /home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json, absent on a build machine without it).
The repository page is never changed. A pass obtained this way proves the page's logic (it verifies a release code signed by a key it trusts); it proves
nothing about the real instructor key. Port of sen0414_page_key_substitute_v1_0_0.py; the placeholder is SEN0401's public key (course configuration, exam.public_key).
Usage: sen0401_page_key_substitute_v1_0_0.py NN PAGEVER OUTDIR     e.g. 07 9_41_0 /tmp/x    (writes OUTDIR/page.html and OUTDIR/test_key.json)
Environment: SEN0401_ROOT = the repository root (default: the parent of this file's folder), so that a scratch copy of the repository can be used."""
__version__ = "1.0.0"
import base64, json, os, sys
from cryptography.hazmat.primitives.asymmetric import ec

REPO = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = ("0Sa8MtDE94xNCAAucUwWWoWgdLIgKRY42weFJWUDVrU", "PQfE3vB8fPYCKQ4RPxZZovRuFZ4yQz9u4pmiObDqjus")


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def main():
    n, pv, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    key = ec.generate_private_key(ec.SECP256R1())
    num = key.private_numbers(); pub = num.public_numbers
    jwk = {"kty": "EC", "crv": "P-256", "d": b64u(num.private_value.to_bytes(32, "big")), "x": b64u(pub.x.to_bytes(32, "big")), "y": b64u(pub.y.to_bytes(32, "big"))}
    json.dump({"private_jwk": jwk, "note": "TEST-ONLY key made by sen0401_page_key_substitute; not the instructor's"}, open(os.path.join(out, "test_key.json"), "w"))
    src = os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v%s.html" % (n, pv))
    s = open(src, encoding="utf-8").read()
    a, b = PLACEHOLDER
    assert s.count(a) >= 1 and s.count(b) >= 1, "the page does not carry SEN0401's public key (configuration exam.public_key)"
    s = s.replace(a, jwk["x"]).replace(b, jwk["y"])
    open(os.path.join(out, "page.html"), "w", encoding="utf-8").write(s)
    print("placeholders replaced:", a[:8], b[:8])


if __name__ == "__main__":
    main()
