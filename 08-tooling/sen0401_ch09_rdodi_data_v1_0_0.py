"""SEN0401 chapter 9 (Transaction Fees) for the RDODI build (generic builder sen0401_rdodi_build_v1_1_0.py).
The data module assembles: the source table (sen0401_ch09_sources_v1_0_0), the taxonomy and executed expressions (sen0401_ch09_leaves_v1_0_0),
and the teaching paragraphs (sen0401_ch09_text_a..d_v1_0_0). Every expression is executed by the checks against the saved sources and the two Bitcoin Core 31.1 regtest records."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch09_sources_v1_0_0 as SRC
import sen0401_ch09_leaves_v1_0_0 as LV
import sen0401_ch09_text_a_v1_0_0 as TA
import sen0401_ch09_text_b_v1_0_0 as TB
import sen0401_ch09_text_c_v1_0_0 as TC
import sen0401_ch09_text_d_v1_0_0 as TD

CH = 9
DATE = "2026-10-15"          # the day every source was opened and every claim executed
PYVER = "3.14.6"
VERSION = "1_0_0"
TITLE = "Transaction Fees"
QUESTION = ("What does Chapter 9 of Mastering Bitcoin (3rd edition) say about transaction fees, which of its statements can be recomputed or run on Bitcoin Core 31.1 "
            "and on the real chain, and what has changed in Bitcoin Core, the BIPs and the fee market since the book went to print?")
CQS = ("Which claims of the chapter can be checked by computation, and what does the computation give?",
       "What in the chapter has changed since the book went to print, and on what source?")
LABELS = {
    "FeeNeedsSpendersSignature": "Fee needs the spender's signature",
    "MinRelayFee": "Minimum relay fee",
    "EstimateSmartFeeCall": "The estimatesmartfee call",
    "FullRbfDefault": "Full RBF by default",
    "OptInSignalRule": "Opt-in signal rule (BIP 125)",
    "ReplaceByFee": "Replace by fee (RBF)",
    "ChildPaysForParent": "Child pays for parent (CPFP)",
    "SubmitPackageRpc": "The submitpackage RPC",
    "PayToAnchor": "Pay to anchor (P2A)",
    "TrucPolicy": "TRUC policy",
    "TrucLimits": "TRUC limits",
    "TrucSiblingEviction": "TRUC sibling eviction",
    "TrucVersionMixing": "TRUC version mixing",
    "TrucPinningBound": "TRUC pinning bound",
    "AncestorFeerateMining": "Ancestor feerate mining",
    "FeeFilterMessage": "The feefilter message",
    "FeerateDiagramRule": "Feerate diagram rule",
    "LockTimeDefense": "Lock time defense against fee sniping",
    "WalletLockTimeRule": "Wallet lock time rule",
    "MainnetPrevHeightShare": "Share of mainnet transactions with the previous height",
    "CarveOut": "CPFP carve out",
    "CarveOutRule": "Carve out rule",
    "CarveOutRemoved": "Carve out removed",
    "ClusterMempool": "Cluster mempool",
    "TaprootAntiSniping": "Taproot anti-fee-sniping (BIP 326)",
    "ConfirmationTargetLimits": "Confirmation target limits",
    "MinimumRelayProblem": "The minimum relay problem",
    "AbsurdFeeGuard": "Absurd fee guard",
    "FeesVsSubsidy": "Fees versus subsidy",
    "FeeOnlyFuture": "A future with fees only",
    "FeeIsABid": "A fee is a bid",
    "EphemeralDust": "Ephemeral dust",
}
S = "Antonopoulos and Harding, 2023"
PUBS = [(r[0], r[2], r[3], r[5] == "primary") for r in SRC.S]
CONCEPTS = [("Section", x) for x in (
    "Who Pays the Transaction Fee?", "Fees and Fee Rates", "Estimating Appropriate Fee Rates", "Replace By Fee (RBF) Fee Bumping",
    "Child Pays for Parent (CPFP) Fee Bumping", "Package Relay", "Transaction Pinning", "CPFP Carve Out and Anchor Outputs",
    "Adding Fees to Transactions", "Timelock Defense Against Fee Sniping")] + [("Concept", x) for x in (
    "Bitcoin Core", "CPFP (child pays for parent) fee bumping", "RBF (replace by fee) fee bumping", "absurd fees", "ancestor fee rate mining",
    "anchor outputs (CPFP)", "blocks", "carve outs (CPFP)", "change output", "conflicting transactions", "estimating fee rates", "excessive fees",
    "fee bumping", "fee rates", "fee sniping", "fees", "inputs", "lock time", "outputs", "overpaying transaction fees", "package fee rate",
    "package relay", "payments", "timelocks", "transaction fees", "transaction pinning", "transactions")] + [("Concept", "BIP 125 opt-in replaceability signal")]
FINDINGS = [   # (id, section, text, cites)
 ("F1", "Background", "The chapter holds that a transaction carries no fee field and that the fee is the difference between the inputs and the outputs, paid by the spender and collected by the miner of the block (Antonopoulos and Harding, 2023). A parse of the raw bytes of a transaction of the Bitcoin Core 31.1 test chain found version, inputs, outputs and lock time and no fee, and a forgotten change output of a 20-bitcoin input made the node refuse the transaction with max-fee-exceeded (Bitcoin Core, 2026).", ["P01", "P69"]),
 ("F2", "Background", "The chapter states that the fee is a bid for room in a block, the idea that the original paper already described as an incentive that replaces the subsidy over time (Nakamoto, 2008). A block template of the test node listed ten transactions in descending order of fee rate, from 50 to 1 satoshi per virtual byte (Bitcoin Core, 2026).", ["P01", "P59", "P31"]),
 ("F3", "Background", "The fee market is an economic subject with an early literature: fees depend on size and priority, and a fee market can exist without a block size limit (Moeser and Boehme, 2015); (Rizun, 2015). The chapter is consistent with it, since the chapter ties the fee to the block space a transaction takes up (Antonopoulos and Harding, 2023).", ["P61", "P63", "P01"]),
 ("F4", "Contemporary developments", "Erratum: the book defines the fee rate as a transaction's size divided by weight, which is a pure number with no price in it. The fee rate is the fee divided by the size, 2.0 satoshis per virtual byte for the run's 141-byte transaction that paid 282 satoshis, whereas size over weight is 0.2513 (Antonopoulos and Harding, 2023); (Lombrozo et al., 2015).", ["P01", "P07"]),
 ("F5", "Contemporary developments", "Changed default: the minimum relay fee rate fell from 1 to 0.1 satoshi per virtual byte in Bitcoin Core 30.0, so that the node accepted 15 satoshis for a 141-byte transaction and refused 14, while the wallet keeps its own minimum of 1 satoshi per virtual byte and refused 0.5 and 0.1 (Bitcoin Core developers, 2025); (Bitcoin Core, 2026).", ["P25", "P27", "P70"]),
 ("F6", "Contemporary developments", "Changed default: full replace-by-fee is the default since Bitcoin Core 28.0, so a transaction that does not signal replaceability is replaced on the 31.1 node, and the option -mempoolfullrbf was removed in 29.0 and is refused by 31.1 with exit code 1. The book describes only the opt-in rule of BIP 125 (Bitcoin Core developers, 2024); (Bitcoin Core developers, 2025); (Harding, 2015).", ["P23", "P24", "P06"]),
 ("F7", "Contemporary developments", "The change of the default followed a public discussion in December 2022 in which Peter Todd posted on full replace-by-fee on 2022-12-12 and release 24.0.1 announced the option -mempoolfullrbf (Todd, 2022); (Bitcoin Core developers, 2022); (Bitcoin Optech, 2022).", ["P41", "P22", "P54"]),
 ("F8", "Contemporary developments", "Package relay is partly realized: Bitcoin Core 28.0 accepts a package of one parent and one child through submitpackage, so that a child can pay for a parent that is below the minimum relay fee (the test node took a parent of 0 fee and a child of 10,000 satoshis), while the peer-to-peer ancestor package relay of BIP 331 is still a Draft (Bitcoin Core developers, 2024); (Zhao, 2022).", ["P23", "P16", "P11"]),
 ("F9", "Contemporary developments", "Erratum: the book gives the extra child of the CPFP carve-out as 1,000 virtual bytes and the limit as 100,000, while the code constant EXTRA_DESCENDANT_TX_SIZE_LIMIT is 10,000 and the descendant size limit is 101,000; the carve-out was added in release 0.19.0.1, not 0.19.0, which was tagged and never released (Antonopoulos and Harding, 2023); (Bitcoin Core developers, 2019); (Corallo, 2018).", ["P01", "P21", "P40"]),
 ("F10", "Contemporary developments", "Changed policy: the cluster mempool of Bitcoin Core 31.0 replaces the 25-transaction ancestor and descendant limits by a limit of 64 transactions per cluster, and the carve-out of the old limits is removed, and the run shows the quadratic work of the old limits (625 package updates, and 2,500 at double the limit) (Bitcoin Core developers, 2026); (Daftuar et al., 2024).", ["P26", "P18", "P42"]),
 ("F11", "Contemporary developments", "Version-3 (TRUC) transactions of Bitcoin Core 28.0 limit a transaction to one unconfirmed parent and one child, at most 10,000 virtual bytes for the transaction and 1,000 for the child. In the run the cost of replacing a pinned parent fell from 450,780 to 5,145 satoshis, 88 times less than for an unrestricted large child (Zhao, 2024); (Bitcoin Core, 2026).", ["P12", "P30", "P51"]),
 ("F12", "Contemporary developments", "Anchor outputs gained a standard form: the pay-to-anchor output script 51024e73 of BIP 433 can be spent by anyone, and release 29.0 relays a zero-fee parent with an ephemeral dust output when a child spends the dust in the same package. The lightning anchor commitments of BOLT 3 are the application the chapter names (Sanders, 2025); (Bitcoin Core developers, 2025); (Lightning developers, 2026).", ["P13", "P24", "P56"]),
 ("F13", "Comparative analysis", "Erratum: the book's remark that the block subsidy is much higher than the fees is true of some blocks and not of others. In block 840,000, the halving block of 2024-04-20, the fees were 3,762,561,499 satoshis, 92.33 percent of the reward, while in block 971,489 they were 0.46 percent (Mempool Space, 2026); (Antonopoulos and Harding, 2023).", ["P64", "P66", "P01", "P36"]),
 ("F14", "Comparative analysis", "Erratum: the book's summary of the default mempool as about one day's worth of transactions does not match the code, which holds 300 megabytes and forgets a transaction after 336 hours, 14 days; and the glossary's minimum fee of 0.5 millibitcoin, 50,000 satoshis, is a historical value that the node no longer applies (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023).", ["P28", "P01", "P04"]),
 ("F15", "Comparative analysis", "The estimatesmartfee call accepts a target of 1 to 1008 blocks but can look back only as far as its history; on a chain 231 blocks high the target of 144 was answered for 60 blocks, and the default mode has been economical since 28.0, so that the default answer differs from the conservative one at 144 blocks (Bitcoin Core, 2026); (Bitcoin Core developers, 2024).", ["P37", "P71", "P23"]),
 ("F16", "Comparative analysis", "The replacement hazards are real and measured: three versions of one payment of 0.4 bitcoin made the payee receive 0.8 bitcoin when a miner kept the first and then mined the last, and a large child pins a parent at a cost of 450,780 satoshis to replace. The replacement cycling attack of 2023 is described in the sources but was not run (Bitcoin Optech, 2023); (Bitcoin Optech, 2026).", ["P55", "P51", "P53"]),
 ("F17", "Comparative analysis", "The incentive question of the last section is modelled by Carlsten and colleagues, who show that a chain without a subsidy is unstable because a miner gains by undercutting the block of a rival (Narayanan, 2016), and the probability that a miner with the hash share x wins a sniping race is (x / (1 - x)) squared: 1.23 percent at 10 percent, 66.94 percent at 45 percent (Carlsten et al., 2016); (Poon and Dryja, 2016).", ["P60", "P72", "P62", "P52"]),
 ("F18", "Conclusion", "Erratum: the lock time rule of the book and its chapter 6 is off by one: a transaction is final in a block when its lock time is less than the block height, so a lock time equal to the height of the next block is refused on the node. The wallet sets the lock time to the current height, which 89 of 599 transactions of block 840,000 do (Bitcoin Core, 2026); (Kerin, 2015); (Antonopoulos and Harding, 2023).", ["P35", "P68", "P01", "P02", "P33"]),
 ("F19", "Conclusion", "Taken together, the chapter's teaching on fees, replacement, child-pays-for-parent and anti-sniping remains right in its principles, but five of its defaults and limits are outdated for Bitcoin Core 28 to 31, and the sources show the direction: policy is moving from fixed limits and opt-in signals to cluster-based rules, TRUC transactions and anchors (Bitcoin Core developers, 2026); (Bitcoin Optech, 2026).", ["P26", "P48", "P01"]),
 ("F20", "Conclusion", "Bitcoin Core's own documentation describes the replacement rules in force, including an incremental relay fee of 0.1 satoshi per virtual byte, so a replacement of a 141-byte transaction that had paid 564 satoshis needed at least 579 satoshis in the run (Bitcoin Core, 2026); (Harding, 2015).", ["P15", "P29", "P06"]),
]
TAX = [(t, m, l, ex, d, ((e.replace("\n", "; "), r) if e and r is not None else None)) for t, m, l, ex, d, e, r in LV.LEAVES]   # one line each: the ABox holds it as a string literal
_ALL = {}
for _x in (TA.A, TB.B, TC.C, TD.D):
    _ALL.update(_x)
_LAB = lambda c: LABELS.get(c) or (lambda t: t[0].upper() + t[1:])("".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip())
BODY = dict(_ALL)
for _t, _m, _l, *_ in TAX:
    pass
_mem = {}
for _t, _m, _l, *_ in TAX:
    _mem.setdefault(_t, [])
    if _m not in _mem[_t]:
        _mem[_t].append(_m)
    _mem.setdefault(_m, []).append(_l)
for _c in _mem:
    _intro = TD.TOP[_c] if _c in TD.TOP else TD.MID[_c]
    BODY[_c] = _intro + " This subject covers " + "; ".join(_LAB(x) for x in _mem[_c]) + "."
BODY = {k: v.replace('"', "'").replace("\n", " ") for k, v in BODY.items()}
_P = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch09_lib_v1_0_0 as L; "
CLAIMS = [
 (_P + "r = L.quotes_report(); (r[0], r[2], r[3])", "(72, [], [])"),
 (_P + "L.index_report()", "(72, 72, [])"),
]
BEH = [
 ("The virtual size of a 561-weight transaction", "print(-(-561 // 4))", "141"),
 ("The fee rate of 282 satoshis for 141 virtual bytes", "print(282 / 141)", "2.0"),
 ("The block subsidy after the fourth halving, in satoshis", "print(50 * 10 ** 8 >> 4)", "312500000"),
 ("Minimum replacement fee: 564 satoshis plus 141 bytes at 0.1 sat/vB rounded up", "print(564 + -(-141 // 10))", "579"),
]
