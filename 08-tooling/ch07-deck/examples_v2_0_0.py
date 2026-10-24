"""Every code listing of the SEN0401 chapter 7 deck 2.0.0 (task TK_Ch07_Deck_Build, 2026-10-23) and the source of the chapter-code manifest that the page's chapter-code tab reads.
One entry per code slide, in SLIDE ORDER. A listing is a list of GROUPS; a group is a few single-line statements and the plain-language note that explains them (the deck standard asks for
an explanation beside every code box). Every statement is ONE line, because the deck's own check re-runs each '>>> ' row of a slide, one paragraph at a time, in one namespace after the
PRELUDE. The last row of a listing is an expression (`final`, which is also in `show`): the slide prints its value under it, the only REPL text of the slide; the full result of the example is
drawn as a chart or a table beside the listing from the recorded `show` values (examples_run_v2_0_0.py), never typed. A statement is at most 56 characters, so that a code line never wraps (D12).
The names the statements use (L, K, p2pkh, old_joined, LOCK, CLTV, CSV, RED, MOH_LEAVES, MOH_ITEMS, moh_tap, moh_wsh) are those of PRELUDE of examples_v1_0_0.py (unchanged); the page gets
the same names from sen0401_ch07_deck_lib_v1_0_0.py (SETUP below)."""
__version__ = "2.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import PRELUDE            # the chapter library and its helpers, unchanged

G = lambda note, *lines: {"lines": list(lines), "note": note}

EXAMPLES = [
  {"id": "ex01", "name": "Stack arithmetic: 2 3 OP_ADD 5 OP_EQUAL", "branch": "ScriptLanguage", "final": "res",
   "groups": [G("A script is read left to right; numbers are pushed and operations use the top items.", "ok = L.run('2 3', 'OP_ADD 5 OP_EQUAL')"),
              G("Change the five to a six and the same script fails.", "bad = L.run('2 3', 'OP_ADD 6 OP_EQUAL')"),
              G("The assembler turns the five words into five bytes.", "code = L.assemble('2 3 OP_ADD 5 OP_EQUAL').hex()", "res = [ok, bad, code]", "res")],
   "show": ["res"]},
  {"id": "ex02", "name": "The OP_RETURN bug of 2010", "branch": "ScriptLanguage", "final": "res",
   "groups": [G("The first software joined both scripts into one program that stopped at OP_RETURN.", "joined = old_joined('OP_1 OP_RETURN', LOCK)"),
              G("Today the scripts run apart, and OP_RETURN makes the spend fail.", "now = L.run('OP_1 OP_RETURN', LOCK, flags=())"),
              G("Only the real secret opens the lock, in both engines.", "key = '0x06' + b'secret'.hex()", "real = L.run(key, LOCK, flags=())", "res = [joined, now, real]", "res")],
   "show": ["res"]},
  {"id": "ex03", "name": "Pay to public key hash: the right key and the wrong one", "branch": "KeyLocking", "final": "res",
   "groups": [G("The lock holds a 20-byte hash of the public key and fills 25 bytes.", "spk = L.p2pkh_script(L.hash160(K.pub(1)))", "kind = (len(spk), L.classify(spk)[0])"),
              G("Three spends are tried: the right key, a wrong key, a changed amount.", "a = p2pkh()", "b = p2pkh(signer=2)", "c = p2pkh(amount_after=99999)", "res = (a, b, c)", "res")],
   "show": ["kind", "res"]},
  {"id": "ex04", "name": "A DER signature, strict and loose", "branch": "KeyLocking", "final": "res",
   "groups": [G("A signature is made over the hash of a message.", "sig = L.ecdsa_sign(K.secret(1), L.sha256(b'pay Bob'))"),
              G("With its hash type it is 72 bytes, starts with 0x30 and has a low s.", "full = sig + b'\\x01'", "facts = [len(full), full[0], L.is_low_s(full)]"),
              G("A padded signature passes old rules but fails the strict DER rule.", "nod = L.MAINNET_FLAGS - {'DERSIG'}", "old = p2pkh(loose=True, flags=nod)", "res = [old, p2pkh(loose=True)]", "res")],
   "show": ["facts", "res"]},
  {"id": "ex05", "name": "A 2-of-3 multisignature and its extra element", "branch": "ScriptedMultisig", "final": "res",
   "groups": [G("Signatures must follow the order of the keys; one signature is too few.", "ok = K.ms_spend(2, 3, [0, 2])", "swap = K.ms_spend(2, 3, [2, 0])", "few = K.ms_spend(2, 3, [1])"),
              G("CHECKMULTISIG pops one item too many; a non-empty dummy is refused.", "dummy = K.ms_spend(2, 3, [0, 1], dummy=b'\\x01')"),
              G("The script itself is 105 bytes, mostly three public keys.", "res = [ok, swap, few]", "res")],
   "show": ["res", "dummy", "len(RED)"]},
  {"id": "ex06", "name": "Pay to script hash and the redeem script", "branch": "PayToScriptHash", "final": "res",
   "groups": [G("The lock holds only the 20-byte hash of the script: 23 bytes.", "spk = L.p2sh_script(L.hash160(RED))", "addr = L.script_to_address(spk)"),
              G("The spender reveals the script; a script that does not hash to the lock fails.", "ok = K.ms_spend(2, 3, [0, 1], wrap='p2sh')", "bad = K.p2sh_spend(RED, hashed=RED + b'\\x00')"),
              G("Addresses of this kind start with a 3.", "res = [addr[:6], len(spk), ok, bad]", "res")],
   "show": ["res"]},
  {"id": "ex07", "name": "OP_CHECKLOCKTIMEVERIFY: not before block 800,000", "branch": "DataAndTime", "final": "res",
   "groups": [G("The sequence must not be final, or the lock time is ignored.", "seq = 0xfffffffe", "ok = K.key_spend(CLTV, locktime=800000, sequence=seq)"),
              G("A lock time one block too early fails.", "early = K.key_spend(CLTV, locktime=799999, sequence=seq)"),
              G("A final sequence switches the lock time off, and the script fails.", "final = K.key_spend(CLTV, locktime=800000)", "res = [ok, early, final]", "res")],
   "show": ["res"]},
  {"id": "ex08", "name": "OP_CHECKSEQUENCEVERIFY: a wait of 4,320 blocks", "branch": "DataAndTime", "final": "off",
   "groups": [G("Version 2 and a sequence of 4,320 satisfy the script: thirty days of blocks.", "ok = K.key_spend(CSV, version=2, sequence=4320)"),
              G("One block short fails, and so does version 1.", "early = K.key_spend(CSV, version=2, sequence=4319)", "v1 = K.key_spend(CSV, version=1, sequence=4320)"),
              G("Bit 31 set disables the relative lock, and the script fails.", "bit31 = 0x80000000 | 4320", "off = K.key_spend(CSV, version=2, sequence=bit31)", "off")],
   "show": ["ok", "early", "v1", "off"]},
  {"id": "ex09", "name": "Mohammed's capital account: three paths", "branch": "FlowControl", "final": "p3",
   "groups": [G("Path one needs two of three partners and no waiting.", "size = len(K.moh_script())", "p1 = K.moh_spend(1)"),
              G("Path two: the lawyer and one partner, after 4,320 blocks.", "p2 = [K.moh_spend(2, sequence=s) for s in (4320, 4319)]"),
              G("Path three: the lawyer alone, after 12,960 blocks.", "p3 = [K.moh_spend(3, sequence=s) for s in (12960, 4320)]", "p3")],
   "show": ["size", "p1", "p2", "p3"]},
  {"id": "ex10", "name": "Pay to witness public key hash", "branch": "SegwitScripts", "final": "addr",
   "groups": [G("A witness key-hash spend works directly and nested in a script hash.", "ok = [K.wpkh_spend(), K.wpkh_spend(nested=True)]"),
              G("The signature commits to the amount, so a wrong amount fails.", "wrong = K.wpkh_spend(signed_amount=99999)"),
              G("The address is bech32 and begins with bc1q.", "prog = L.p2wpkh_script(L.hash160(K.pub(1)))", "addr = L.script_to_address(prog)", "addr")],
   "show": ["ok", "wrong", "addr"]},
  {"id": "ex11", "name": "A script tree: the proof grows with the logarithm", "branch": "TreesAndTweaks", "final": "depth",
   "groups": [G("Each of three scripts needs its sibling hashes as a proof.", "proof = [len(p) for p in K.tap_tree(MOH_LEAVES)[1]]"),
              G("A tree of n scripts needs about log2 of n hashes per spend.", "ns = (3, 8, 1024, 2**20)", "depth = [(n - 1).bit_length() for n in ns]", "depth")],
   "show": ["proof", "ns", "depth"]},
  {"id": "ex12", "name": "Taproot: a key path spend", "branch": "TaprootBranch", "final": "res",
   "groups": [G("The output key is the internal key plus a tweak; here there is no script.", "par, q = L.taproot_tweak_pubkey(K.xpub(1), b'')"),
              G("The address begins with bc1p and the key takes 32 bytes.", "addr = L.script_to_address(L.p2tr_script(q))", "kind = (addr[:6], len(q))"),
              G("One 64-byte signature spends it; an untweaked key is refused.", "r, wit, wt = K.tr_keypath(1)", "bad = K.tr_keypath(1, MOH_LEAVES, tamper='untweaked')[0]", "res = (r, len(wit[0]), wt, bad)", "res")],
   "show": ["kind", "res"]},
  {"id": "ex13", "name": "Taproot: three script path spends", "branch": "TaprootBranch", "final": "res",
   "groups": [G("Each of the three leaves of the account script can be spent.", "res = [moh_tap(i)[0] for i in range(3)]"),
              G("Weight units of each spend as a taproot script path.", "tap = [moh_tap(i)[2] for i in range(3)]"),
              G("The same three paths as a witness script hash spend.", "wsh = [moh_wsh(p) for p in (1, 2, 3)]", "res")],
   "show": ["res", "tap", "wsh"]},
  {"id": "ex14", "name": "OP_CHECKSIGADD: 2-of-3 in tapscript", "branch": "TaprootBranch", "final": "res",
   "groups": [G("The same 2-of-3 rule written with CHECKSIGADD is a byte shorter.", "s = K.csa_script([0, 1, 2], 2)", "sizes = (len(s), len(RED))"),
              G("Two valid signatures and one empty slot satisfy it.", "items = [b'', ('sig', 1), ('sig', 0)]", "ok = K.tr_spend([s], 0, items)[0]"),
              G("With only one valid signature the count stays below two and the script fails.", "few = K.tr_spend([s], 0, [b'', b'', ('sig', 0)])[0]", "res = [ok, few]", "res")],
   "show": ["sizes", "res"]},
  {"id": "ex15", "name": "OP_SUCCESS: opcodes kept for upgrades", "branch": "TaprootBranch", "final": "res",
   "groups": [G("In tapscript, 87 opcode values succeed on sight.", "n = sum(1 for o in range(256) if L.is_op_success(o))"),
              G("A tapscript with opcode 152 succeeds at once.", "ok = K.tr_spend([bytes([0x51, 152])], 0, [])[0]"),
              G("The same word, a disabled shift, fails in an old script.", "old = L.run('OP_1 OP_LSHIFT', 'OP_1', flags=())", "res = [n, ok, old]", "res")],
   "show": ["res"]},
]
for e in EXAMPLES:
    e["code"] = [ln for g in e["groups"] for ln in g["lines"]]        # every statement, in order; the last is the final expression

# what the page runs before every example (the chapter library of the page: the wheel with the two modules named here)
SETUP = ("# setup: the chapter's script library and the worked-example helpers; the page runs this before every example\n"
         "import sen0401_ch07_script_lib_v1_0_0 as L\n"
         "import sen0401_ch07_deck_lib_v1_0_0 as K\n"
         "from sen0401_ch07_deck_lib_v1_0_0 import p2pkh, old_joined, LOCK, CLTV, CSV, RED, MOH_LEAVES, MOH_ITEMS, moh_tap, moh_wsh\n")
