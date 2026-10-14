#!/usr/bin/env python3
"""sen0401_lineage_page_key_substitute v1_0_0 - makes a COPY of a SEN0401 chapter page whose embedded exam-release public key is replaced by the public half of a
TEST key, so that the page test can run its mock-exam release step on a machine that does not hold the instructor's private key
(/home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json is not on this machine). The repository page is never changed. A pass obtained this way
proves the page's logic (it verifies a release code signed by a key it trusts); it proves nothing about the real instructor key.
Ported from sen0414_page_key_substitute_v1_0_0.py. The TEST key is read from TEST_KEY (default /home/claude/instructor_keys_test/test_key.json); if absent a fresh one is made there.
Usage: sen0401_lineage_page_key_substitute_v1_0_0.py NN PAGEVER OUTDIR     e.g. 05 9_41_0 /tmp/x   (writes OUTDIR/page.html and OUTDIR/test_key.json)
"""
__version__ = "1.0.0"
import base64, json, os, shutil, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the public key the SEN0401 pages carry (x, y of the P-256 key in course_page_config_v2_10_0.json, exam.public_key)
PLACEHOLDER = ("0Sa8MtDE94xNCAAucUwWWoWgdLIgKRY42weFJWUDVrU", "PQfE3vB8fPYCKQ4RPxZZovRuFZ4yQz9u4pmiObDqjus")
TEST_KEY = os.environ.get("TEST_KEY", "/home/claude/instructor_keys_test/test_key.json")


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def make_key():
    from cryptography.hazmat.primitives.asymmetric import ec
    key = ec.generate_private_key(ec.SECP256R1()); num = key.private_numbers(); pub = num.public_numbers
    jwk = {"kty": "EC", "crv": "P-256", "d": b64u(num.private_value.to_bytes(32, "big")), "x": b64u(pub.x.to_bytes(32, "big")), "y": b64u(pub.y.to_bytes(32, "big"))}
    os.makedirs(os.path.dirname(TEST_KEY), exist_ok=True)
    json.dump({"private_jwk": jwk, "note": "TEST-ONLY key; not the instructor's"}, open(TEST_KEY, "w"))


def main():
    n, pv, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    if not os.path.exists(TEST_KEY):
        make_key()
    jwk = json.load(open(TEST_KEY))["private_jwk"]
    shutil.copy(TEST_KEY, os.path.join(out, "test_key.json"))
    src = os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0401_ch%s_page_v%s.html" % (n, pv))
    s = open(src, encoding="utf-8").read()
    a, b = PLACEHOLDER
    assert s.count(a) >= 1 and s.count(b) >= 1, "the page does not carry the SEN0401 public key"
    s = s.replace(a, jwk["x"]).replace(b, jwk["y"])
    open(os.path.join(out, "page.html"), "w", encoding="utf-8").write(s)
    print("public key replaced by the TEST key's:", a[:8], "->", jwk["x"][:8])


if __name__ == "__main__":
    main()
