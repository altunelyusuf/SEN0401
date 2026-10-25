"""The key concepts of chapter 12 for the deck 3.0.0 (Mining and Consensus; a NEW file, nothing earlier is edited).
It reads deck_concepts_v2_0_0.py (committed, unchanged) and derives the list for the deck 3.0.0 from it:
 (1) the seventh part 'From chapter 11' and its 41 cards are dropped: they were the labels of the chapter 11 research, which the repaired research (v1_1_0) no longer carries;
 (2) the 28 concepts of the v2_0_0 list that are also concepts of the repaired research 03-materials/ch12/rdodi/sen0401_ch12_research_v1_1_0.ttl keep their cards;
 (3) the 12 concepts of that research that had no card (coinbase fields, coinbase data and tags, the extra nonce space, covert ASICBoost, regtest never retargets, regtest halves every 150 blocks,
     Stratum protocols, the top pool against the thresholds, BIP 34 activation, BIP 8 lock-in by height, Segwit activation in 2017, BIP 54 consensus cleanup) get a card with a one-sentence meaning
     taken from the research comment and one everyday analogy.
The result is the 40 primary-source concepts of the repaired research, each spelled exactly as the research spells it, in six parts; K3 keeps the order in which the cards are shown."""
__version__ = "3.0.0"
import deck_concepts_v2_0_0 as K2

BRANCHES = [b for b in K2.BRANCHES if b != "RecapChapter11"]
LAB = {b: K2.LAB[b] for b in BRANCHES}
SHORT = {b: K2.SHORT[b] for b in BRANCHES}
L1 = {b: K2.L1[b] for b in BRANCHES}
GROUPS = {b: K2.GROUPS[b] for b in BRANCHES}

NEW = {
    "Regtest halves every 150 blocks": ("MoneyCreation", "the private test chain halves the reward every 150 blocks, so a halving can be watched in minutes.", "a time-lapse film of a four-year calendar"),
    "Coinbase fields of Bitcoin Core today": ("BuildingTheCandidateBlock", "Core 31.1 fills in the lock time, the sequence and the end of the script in ways the book's table does not show.", "a form that the clerk now fills in for you"),
    "Coinbase data and tags": ("BuildingTheCandidateBlock", "the free bytes of the coinbase script, two to one hundred in all, are where pools sign their blocks.", "the baker's mark pressed into each loaf"),
    "The extra nonce space": ("BuildingTheCandidateBlock", "eight extra bytes in the coinbase script give a miner 2 to the 96 headers to try.", "a second, far larger drum behind the lottery drum"),
    "Regtest never retargets": ("ProofOfWork", "a chain parameter switches the difficulty adjustment off, so the difficulty of regtest stays the same.", "a thermostat that has been unplugged"),
    "Covert ASICBoost": ("MiningCompetition", "a way of building the block header so that mining hardware does less work per hash.", "a baker who reuses one batch of dough for many loaves"),
    "Stratum protocols": ("MiningCompetition", "the language a pool and a mining machine speak, in use since 2012 and followed by a second version.", "the radio code between a dispatcher and a taxi"),
    "The top pool against the thresholds": ("MiningCompetition", "the largest pool of the last year found about 28 percent of the blocks, between one quarter and one third.", "a team ahead in the league, but not yet far enough ahead to rule it"),
    "BIP 34 activation": ("ChangingConsensusRules", "the first soft fork switched on by counting block versions: 750, then 950, of the last 1,000 blocks.", "a show of hands among the last thousand voters"),
    "BIP 8 lock-in by height": ("ChangingConsensusRules", "it counts in block heights, not time, and can force the lock-in when the timeout comes.", "a deadline set by page number, not by the clock"),
    "Segwit activation in 2017": ("ChangingConsensusRules", "miners held it back under BIP 9 until BIP 91 and BIP 148; it became active on 24 August 2017.", "a vote that stalled until everyone was given a deadline"),
    "BIP 54 consensus cleanup": ("ChangingConsensusRules", "a proposal that would fix the time warp attack and limit signature operations and transaction size.", "a spring clean of an old rulebook"),
}
AFTER = {  # the new card is shown after this card of its part
    "Regtest halves every 150 blocks": "The fees of block 840,000",
    "Coinbase fields of Bitcoin Core today": "Block template", "Coinbase data and tags": "Coinbase fields of Bitcoin Core today",
    "The extra nonce space": "Witness commitment",
    "Regtest never retargets": "The BIP 94 branch",
    "Covert ASICBoost": "Version rolling", "Stratum protocols": "Pool shares and fees", "The top pool against the thresholds": "The selfish-mining threshold",
    "BIP 34 activation": "The Bitcoin Cash fork of 2017", "BIP 8 lock-in by height": "The BIP 9 state machine", "Segwit activation in 2017": "BIP 8 lock-in by height",
    "BIP 54 consensus cleanup": "Buried deployments",
}
K3 = {}
for k, v in K2.K3.items():
    if v[0] == "RecapChapter11": continue
    K3[k] = v
# each new card is placed directly after its anchor; a card anchored on another new card follows it
for n in AFTER:
    if AFTER[n] not in NEW: 
        items = list(K3.items()); pos = [k for k, _ in items].index(AFTER[n]) + 1
        items.insert(pos, (n, NEW[n])); K3 = dict(items)
for n in AFTER:
    if AFTER[n] in NEW:
        items = list(K3.items()); pos = [k for k, _ in items].index(AFTER[n]) + 1
        items.insert(pos, (n, NEW[n])); K3 = dict(items)
