# 2026-10-06 consolidation of the four Turtle files in this tree

By the owner's ruling of 2026-10-06 ("No need to exceptions. Apply the same standards to the
remaining files."), the BP-D53 three-file structure and the BP-D6/BP-D7 naming and version rules
were applied to the Turtle files of this 2025 tree, which until then were kept byte-identical.
Only the four `.ttl` files changed; every other file is untouched, and
`../legacy_inventory_v1_0_0.json` remains the unedited record of the 2026-09-27 byte-identical
copy, now describing the git history of these four rather than the working tree.

| was | is now |
|---|---|
| `Chapter_5_Wallets/BlockchainWallets_Ontology_v1.1_v1_0_0.ttl` (T+A+S) | `blockchain_wallets_tbox_v1_1_0.ttl` + `blockchain_wallets_abox_v1_1_0.ttl` + `blockchain_wallets_shacl_v1_1_0.ttl` |
| `Chapter_5_Wallets/BlockchainWallets_Ontology_v1_0_0.ttl` (superseded v1.0) | removed per one-current-version (BP-D7); in git history |
| `Chapter_6_Transactions/OntologyReportProduction/blockchain_transactions_ontology_v1.0.0_v1_0_0.ttl` (T+A) | `blockchain_transactions_tbox_v1_0_0.ttl` + `blockchain_transactions_abox_v1_0_0.ttl` |
| `Chapter9The_Blockchain/blockchain_ontology_v1_0_0_v1_0_0.ttl` (T+A) | `blockchain_tbox_v1_0_0.ttl` + `blockchain_abox_v1_0_0.ttl` |

Each split was verified by graph isomorphism: the union of the role files minus their two added
ontology headers is isomorphic to the original (1382, 1108 and 989 triples respectively).
