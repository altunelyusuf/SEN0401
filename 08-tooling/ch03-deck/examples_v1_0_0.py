__version__ = "1.0.0"
# Every computation the SEN0401 chapter 3 deck shows. The outputs come from executing them, never from typing.
# PRELUDE defines what the slides name but do not print in full: the 388 hex characters the book prints for Alice's
# transaction, the 13 transaction identifiers of block 123456 the book prints, and the header fields of that block.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); EVID = os.path.join(HERE, "..", "ch03-evidence")
TX_HEX = open(os.path.join(EVID, "alice_tx_hex_book_v1_0_0.txt")).read().strip()
HDR = json.load(open(os.path.join(EVID, "block_123456_header_v1_0_0.json")))
TXIDS = ("5b75086dafeede555fc8f9a810d8b10df57c46f9f176ccc3dd8d2fa20edd685b e3d0425ab346dd5b76f44c222a4bb5d16640a4247050ef82462ab17e229c83b4 "
         "137d247eca8b99dee58e1e9232014183a5c5a9e338001a0109df32794cdcc92e 5fd167f7b8c417e59106ef5acfe181b09d71b8353a61a55a2f01aa266af5412d "
         "60925f1948b71f429d514ead7ae7391e0edf965bf5a60331398dae24c6964774 d4d5fc1529487527e9873256934dfb1e4cdcb39f4c0509577ca19bfad6c5d28f "
         "7b29d65e5018c56a33652085dbb13f2df39a1a9942bfe1f7e78e97919a6bdea2 0b89e120efd0a4674c127a76ff5f7590ca304e6a064fbc51adffbd7ce3a3deef "
         "603f2044da9656084174cfb5812feaf510f862d3addcf70cacce3dc55dab446e 9a4ed892b43a4df916a7a1213b78e83cd83f5695f635d535c94b2b65ffb144d3 "
         "dda726e3dad9504dce5098dfab5064ecd4a7650bfe854bb2606da3152b60e427 e46ea8b4d68719b65ead930f07f1f3804cb3701014f8e6d76c4bdbc390893b94 "
         "864a102aeedf53dd9b2baab4eeb898c5083fde6141113e0606b664c41fe15e1f").split()
# the function the Merkle slide shows; the slide's text must equal this text (checked)
MERKLE_SRC = ("def merkle_root(txids):\n"
              "    level = [bytes.fromhex(t)[::-1] for t in txids]\n"
              "    while len(level) > 1:\n"
              "        if len(level) % 2: level.append(level[-1])\n"
              "        level = [dsha(level[i] + level[i + 1]) for i in range(0, len(level), 2)]\n"
              "    return level[0][::-1].hex()")
PRELUDE = ("import hashlib, struct\n"
           "dsha = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()\n"
           "TX_HEX = %r\nTXIDS = %r\nPREV = %r\nROOT = %r\n" % (TX_HEX, TXIDS, HDR["previousblockhash"], HDR["merkle_root"]) + MERKLE_SRC + "\n")
# each group runs in one namespace after PRELUDE; a row is one statement or expression
EX = {
 "resources": ["400 * 10 / 1000", "400 * 30 / 1000"],
 "identifiers": ["raw = bytes.fromhex(TX_HEX)", "len(raw)", "dsha(raw)[::-1].hex()"],
 "txid": ["raw = bytes.fromhex(TX_HEX)", "stripped = raw[:4] + raw[6:-71] + raw[-4:]", "len(stripped)", "dsha(stripped)[::-1].hex()"],
 "weight": ["w = 4 * 125 + (194 - 125)", "w", "-(-w // 4)"],
 "block": ["123456 + 651742 - 1", "4 * 4179", "round(0xffff * 256**(0x1d - 3) / (0x6a93b3 * 256**(0x1a - 3)), 10)"],
 "merkle": ["merkle_root(TXIDS)", "merkle_root(TXIDS) == ROOT"],
 "header": ["h = struct.pack('<I', 1) + bytes.fromhex(PREV)[::-1] + bytes.fromhex(ROOT)[::-1] + struct.pack('<III', 1305200806, 0x1a6a93b3, 2436437219)", "len(h)", "dsha(h)[::-1].hex()"],
 "subsidy": ["subsidy = 50 * 10**8 >> (775072 // 210000)", "subsidy", "subsidy + 8_799_108 == 633_799_108", "586_300_566_521 / 10**8"],
}
