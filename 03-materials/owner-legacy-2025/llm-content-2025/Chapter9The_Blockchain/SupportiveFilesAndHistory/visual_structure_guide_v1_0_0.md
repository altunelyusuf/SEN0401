# Blockchain Ontology - Visual Structure Guide

## 1. COMPLETE BLOCK STRUCTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────┐
│                            BLOCK                                     │
│  Class: bc:Block                                                     │
│  "Container data structure aggregating transactions"                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  RELATIONSHIPS (Object Properties):                                  │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ hasBlockHeader (1..1) ──────────> BlockHeader              │    │
│  │ hasBlockHash (1..1) ────────────> BlockHash                │    │
│  │ containsTransaction (1..*) ─────> Transaction              │    │
│  │ hasParentBlock (0..1) ──────────> Block (parent)           │    │
│  │ hasChildBlock (0..*) ───────────> Block (children)         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  DATA PROPERTIES:                                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ blockSize: xsd:nonNegativeInteger                           │    │
│  │   "Size in bytes (not including 4-byte size field itself)"  │    │
│  │                                                              │    │
│  │ blockHeight: xsd:nonNegativeInteger                         │    │
│  │   "Position in blockchain (genesis = 0)"                    │    │
│  │   Note: NOT UNIQUE during forks!                            │    │
│  │                                                              │    │
│  │ blockWeight: xsd:nonNegativeInteger                         │    │
│  │   "SegWit weight units (max 4,000,000)"                     │    │
│  │   Introduced: 2017 (SegWit)                                 │    │
│  │                                                              │    │
│  │ transactionCounter: xsd:nonNegativeInteger                  │    │
│  │   "Count of transactions (VarInt: 1-9 bytes)"               │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  BLOCK TYPES (Subclasses):                                           │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ GenesisBlock  - First block (height=0, no parent)           │    │
│  │ RegularBlock  - Standard blocks                             │    │
│  │ OrphanBlock   - Valid but not in main chain                 │    │
│  │ StaleBlock    - Superseded by longer chain                  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  CONSTRAINTS:                                                        │
│  ✓ MUST have exactly 1 BlockHeader                                  │
│  ✓ MUST have at least 1 Transaction                                 │
│  ✓ GenesisBlock has blockHeight = 0                                 │
│  ✓ Regular blocks have exactly 1 parent                             │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. BLOCK HEADER STRUCTURE (80 BYTES)

```
┌───────────────────────────────────────────────────────────────────┐
│                       BLOCK HEADER (80 bytes)                      │
│  Class: bc:BlockHeader                                             │
├───────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FIELD STRUCTURE:                                                  │
│  ┌──────────────────────┬───────────┬─────────────────────────┐  │
│  │ Field                │ Size      │ Data Property           │  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Version              │ 4 bytes   │ version                 │  │
│  │                      │           │ (xsd:nonNegativeInteger)│  │
│  │                      │           │ Tracks protocol upgrades│  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Previous Block Hash  │ 32 bytes  │ previousBlockHash       │  │
│  │                      │           │ (xsd:hexBinary)         │  │
│  │                      │           │ Links to parent block   │  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Merkle Root          │ 32 bytes  │ merkleRoot              │  │
│  │                      │           │ (xsd:hexBinary)         │  │
│  │                      │           │ Root of transaction tree│  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Timestamp            │ 4 bytes   │ timestamp               │  │
│  │                      │           │ (xsd:dateTime)          │  │
│  │                      │           │ Unix epoch seconds      │  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Difficulty Target    │ 4 bytes   │ difficultyTarget        │  │
│  │                      │           │ (xsd:hexBinary)         │  │
│  │                      │           │ PoW target threshold    │  │
│  ├──────────────────────┼───────────┼─────────────────────────┤  │
│  │ Nonce                │ 4 bytes   │ nonce                   │  │
│  │                      │           │ (xsd:nonNegativeInteger)│  │
│  │                      │           │ PoW counter             │  │
│  └──────────────────────┴───────────┴─────────────────────────┘  │
│                                                                     │
│  RELATIONSHIPS:                                                     │
│  └─ hasMerkleRoot (1..1) ──────────> MerkleTreeRoot               │
│                                                                     │
│  CONSTRAINTS:                                                      │
│  ✓ Each field has cardinality = 1 (exactly one value)             │
│  ✓ Total size = exactly 80 bytes                                  │
│  ✓ Double SHA256 hash of header = BlockHash                       │
│                                                                     │
└───────────────────────────────────────────────────────────────────┘
```

---

## 3. MERKLE TREE STRUCTURE & RELATIONSHIPS

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MERKLE TREE ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  CONCEPTUAL HIERARCHY:                                               │
│                                                                       │
│          MerkleTree (Abstract)                                       │
│          ├─ MerkleTreeRoot (stored in BlockHeader)                  │
│          └─ MAST (Merkelized Alternative Script Trees - Taproot)    │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  EXAMPLE: 4 Transactions → Merkle Tree                              │
│                                                                       │
│                    ┌─────────────────┐                               │
│                    │  Merkle Root    │ ◄─── Stored in BlockHeader   │
│                    │   Hash_ABCD     │      (32 bytes)               │
│                    └────────┬────────┘                               │
│                             │                                         │
│              ┌──────────────┴──────────────┐                         │
│              │                             │                         │
│         ┌────▼─────┐                  ┌────▼─────┐                  │
│         │ Hash_AB  │                  │ Hash_CD  │                  │
│         └────┬─────┘                  └────┬─────┘                  │
│              │                             │                         │
│         ┌────┴────┐                   ┌────┴────┐                   │
│         │         │                   │         │                   │
│    ┌────▼───┐ ┌──▼────┐         ┌────▼───┐ ┌──▼────┐              │
│    │Hash_A  │ │Hash_B │         │Hash_C  │ │Hash_D │              │
│    └────┬───┘ └───┬───┘         └────┬───┘ └───┬───┘              │
│         │         │                  │         │                   │
│         │         │                  │         │                   │
│    ┌────▼────┐ ┌─▼─────┐       ┌────▼────┐ ┌─▼─────┐             │
│    │ TX_A    │ │ TX_B  │       │ TX_C    │ │ TX_D  │             │
│    │(Coinbase│ │       │       │         │ │       │             │
│    └─────────┘ └───────┘       └─────────┘ └───────┘             │
│         ▲         ▲                  ▲         ▲                   │
│         └─────────┴──────────────────┴─────────┘                   │
│                 Transactions in Block                               │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MERKLE TREE PROPERTIES:                                             │
│  ✓ Binary tree structure                                            │
│  ✓ Leaves = transaction hashes                                      │
│  ✓ Nodes = hash(left child + right child)                           │
│  ✓ Root = single 32-byte hash                                       │
│  ✓ Efficient proof of transaction inclusion                         │
│  ✓ If odd number of transactions, duplicate last hash               │
│                                                                       │
│  EXAMPLE CALCULATION:                                                │
│  Hash_A   = SHA256(SHA256(TX_A))                                    │
│  Hash_B   = SHA256(SHA256(TX_B))                                    │
│  Hash_AB  = SHA256(SHA256(Hash_A + Hash_B))                         │
│  Hash_CD  = SHA256(SHA256(Hash_C + Hash_D))                         │
│  Root     = SHA256(SHA256(Hash_AB + Hash_CD))                       │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. TRANSACTION STRUCTURE & TYPES

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRANSACTION                                   │
│  Class: bc:Transaction                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  DATA PROPERTIES:                                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ transactionID: xsd:hexBinary                                │    │
│  │   "Unique transaction identifier (TXID)"                    │    │
│  │   Note: SegWit fixes malleability by separating witness     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  TRANSACTION TYPES (Subclasses):                                     │
│                                                                       │
│  1. CoinbaseTransaction                                              │
│     ┌──────────────────────────────────────────────────────┐       │
│     │ • First transaction in every block                    │       │
│     │ • Creates new bitcoin (mining reward)                 │       │
│     │ • No input from previous transactions                 │       │
│     │ • Must mature 100 blocks before spending              │       │
│     │ • Example: 6.25 BTC reward (current)                  │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                       │
│  2. StandardTransaction                                              │
│     ┌──────────────────────────────────────────────────────┐       │
│     │ • Regular peer-to-peer value transfer                 │       │
│     │ • Has inputs from previous transactions               │       │
│     │ • Has outputs to recipient addresses                  │       │
│     │ • Average size: 250+ bytes                            │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                       │
│  3. SegWitTransaction (Introduced 2017)                              │
│     ┌──────────────────────────────────────────────────────┐       │
│     │ • Segregated Witness format (BIP-141)                 │       │
│     │ • Witness data separated from transaction data        │       │
│     │ • Witness data counts as 1/4 weight                   │       │
│     │ • Fixes transaction malleability                      │       │
│     │ • Enables Lightning Network                           │       │
│     │ • Max block weight: 4,000,000 units                   │       │
│     └──────────────────────────────────────────────────────┘       │
│                                                                       │
│  CONSTRAINTS:                                                        │
│  ✓ Transaction types are DISJOINT (mutually exclusive)              │
│  ✓ Every block MUST have at least 1 transaction                     │
│  ✓ First transaction MUST be CoinbaseTransaction                    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. COMPLETE RELATIONSHIP MAP

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BLOCK → COMPONENTS RELATIONSHIP MAP                   │
└─────────────────────────────────────────────────────────────────────────┘

                              BLOCK
                                │
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
   hasBlockHeader          hasBlockHash          containsTransaction
   (exactly 1)             (exactly 1)           (at least 1)
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
  ┌──────────┐           ┌──────────┐           ┌─────────────┐
  │  BLOCK   │           │  BLOCK   │           │ TRANSACTION │
  │  HEADER  │           │   HASH   │           │  (Multiple) │
  │ (80 byte)│           │(32 byte) │           └──────┬──────┘
  └────┬─────┘           └──────────┘                  │
       │                                                │
       │ hasMerkleRoot                                  │
       │ (exactly 1)                                    │
       ▼                                                │
  ┌──────────────┐                                      │
  │ MERKLE TREE  │ ◄────────────────────────────────────┘
  │     ROOT     │      Computed from all transactions
  │  (32 byte)   │
  └──────────────┘

BLOCK HEADER FIELDS (6 required):
├─ version (4 bytes)
├─ previousBlockHash (32 bytes) ──► Links to PARENT BLOCK
├─ merkleRoot (32 bytes) ──────────► MERKLE TREE ROOT
├─ timestamp (4 bytes)
├─ difficultyTarget (4 bytes)
└─ nonce (4 bytes)

BLOCKCHAIN LINKING:
Parent Block ◄───hasParentBlock─── Current Block ───hasChildBlock───► Child Block(s)
                (functional)                          (0 or more)
```

---

## 6. MERKLE TREE TO TRANSACTIONS: DETAILED RELATIONSHIP

```
┌─────────────────────────────────────────────────────────────────────┐
│         HOW MERKLE ROOT SUMMARIZES ALL TRANSACTIONS                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  BLOCK                                                               │
│  ├─ BlockHeader                                                      │
│  │  ├─ version: 2                                                   │
│  │  ├─ previousBlockHash: 0x123abc...                              │
│  │  ├─ merkleRoot: 0x7f83b... ◄──────────┐                         │
│  │  ├─ timestamp: 2025-12-21              │                         │
│  │  ├─ difficultyTarget: 0x1d00ffff       │                         │
│  │  └─ nonce: 2573394689                  │                         │
│  │                                         │                         │
│  └─ Transactions (500 in this block)      │                         │
│     ├─ TX_0: Coinbase (6.25 BTC)          │                         │
│     ├─ TX_1: Alice → Bob (0.5 BTC)        │                         │
│     ├─ TX_2: Carol → Dave (1.2 BTC)       │ Merkle Tree             │
│     ├─ TX_3: Eve → Frank (0.8 BTC)        │ Computation             │
│     ├─ ...                                 │                         │
│     └─ TX_499: Last transaction            │                         │
│                                            │                         │
│  MERKLE TREE CONSTRUCTION:                 │                         │
│                                            │                         │
│  Step 1: Hash each transaction             │                         │
│  H(TX_0), H(TX_1), H(TX_2), ..., H(TX_499) │                         │
│                                            │                         │
│  Step 2: Pair and hash recursively         │                         │
│  Level 1: 500 hashes (leaf nodes)          │                         │
│  Level 2: 250 hashes (H(H0+H1), ...)       │                         │
│  Level 3: 125 hashes                       │                         │
│  Level 4: 63 hashes (duplicate last)       │                         │
│  Level 5: 32 hashes                        │                         │
│  Level 6: 16 hashes                        │                         │
│  Level 7: 8 hashes                         │                         │
│  Level 8: 4 hashes                         │                         │
│  Level 9: 2 hashes                         │                         │
│  Level 10: 1 hash = MERKLE ROOT ───────────┘                         │
│                                                                       │
│  PROPERTIES:                                                         │
│  ✓ Any change to ANY transaction changes the root                   │
│  ✓ Can prove transaction inclusion with log(n) hashes               │
│  ✓ Root stored in header (80 bytes) summarizes all TX (>125KB)     │
│  ✓ Efficient verification without downloading all transactions      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. BLOCK LINKING CHAIN STRUCTURE

```
┌──────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN LINKING MECHANISM                       │
└──────────────────────────────────────────────────────────────────────┘

GENESIS BLOCK                BLOCK 1                  BLOCK 2
(Height 0)                  (Height 1)               (Height 2)
┌─────────────┐            ┌─────────────┐          ┌─────────────┐
│ Header:     │            │ Header:     │          │ Header:     │
│  prevHash:  │            │  prevHash:  │          │  prevHash:  │
│  0000...    │◄───────────│  000019d6...│◄─────────│  00000000...│
│  merkleRoot │            │  merkleRoot │          │  merkleRoot │
│  ...        │            │  ...        │          │  ...        │
├─────────────┤            ├─────────────┤          ├─────────────┤
│ Hash:       │            │ Hash:       │          │ Hash:       │
│ 000019d6... │            │ 00000000... │          │ 000000fa... │
└─────────────┘            └─────────────┘          └─────────────┘
      │                          │                        │
      │ hasChildBlock            │ hasChildBlock          │
      └──────────────────────────┴────────────────────────┘

PROPERTIES:
├─ hasParentBlock (FUNCTIONAL) - exactly 1 parent (except genesis)
├─ hasChildBlock (NON-FUNCTIONAL) - can have multiple during fork
│
└─ CASCADE EFFECT:
   Change Block 1 → Changes Hash → Block 2's prevHash invalid
                  → Must recalculate Block 2
                  → Block 2's hash changes
                  → Block 3's prevHash invalid
                  → Must recalculate entire chain
                  → Ensures IMMUTABILITY
```

---

## 8. FORK SCENARIO: MULTIPLE CHILDREN

```
┌──────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN FORK STRUCTURE                          │
└──────────────────────────────────────────────────────────────────────┘

                     BLOCK 99
                   (Height 99)
                  ┌───────────┐
                  │  Hash:    │
                  │  0xABC... │
                  └─────┬─────┘
                        │
         ───────────────┼────────────────
        │                               │
        │ hasChildBlock                │ hasChildBlock
        ▼                               ▼
   BLOCK 100a                      BLOCK 100b
  (Height 100)                    (Height 100)
 ┌────────────┐                  ┌────────────┐
 │ prevHash:  │                  │ prevHash:  │
 │ 0xABC...   │                  │ 0xABC...   │
 │ (same)     │                  │ (same)     │
 │            │                  │            │
 │ Miner: A   │                  │ Miner: B   │
 │ Found at:  │                  │ Found at:  │
 │ 10:00:01   │                  │ 10:00:02   │
 └─────┬──────┘                  └─────┬──────┘
       │                               │
       ▼                               ▼
   BLOCK 101a                      [Orphaned]
  (Height 101)                     Block 100b becomes
 ┌────────────┐                    OrphanBlock when
 │ Chain A    │                    Chain A is longer
 │ WINS       │
 └────────────┘

RESOLUTION:
├─ Longest chain (most cumulative PoW) becomes main chain
├─ Chain A continues → Block 100b becomes OrphanBlock
├─ ForkResolution process determines canonical chain
└─ Blocks in losing chain are valid but not in main blockchain
```

---

## 9. SEGWIT BLOCK STRUCTURE (POST-2017)

```
┌──────────────────────────────────────────────────────────────────────┐
│              SEGWIT BLOCK STRUCTURE (BIP-141, 2017)                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  TRADITIONAL BLOCK (Pre-SegWit):                                     │
│  ┌────────────┬─────────────────────┐                                │
│  │   Header   │    Transactions     │                                │
│  │  (80 byte) │   (all data mixed)  │                                │
│  └────────────┴─────────────────────┘                                │
│  Size limit: 1 MB                                                     │
│                                                                        │
│  SEGWIT BLOCK (Post-2017):                                           │
│  ┌────────────┬─────────────────┬─────────────────┐                 │
│  │   Header   │  Transaction    │  Witness Data   │                 │
│  │  (80 byte) │  (base data)    │  (signatures)   │                 │
│  └────────────┴─────────────────┴─────────────────┘                 │
│                      ▲                    ▲                           │
│                      │                    │                           │
│              Weight: 4 units      Weight: 1 unit                     │
│                                                                        │
│  WEIGHT CALCULATION:                                                  │
│  Block Weight = (Base Size × 4) + (Witness Size × 1)                │
│  Max Weight: 4,000,000 units (≈ 4MB equivalent)                     │
│                                                                        │
│  PROPERTY: blockWeight                                               │
│  ├─ Domain: Block                                                    │
│  ├─ Range: xsd:nonNegativeInteger                                   │
│  ├─ Max Value: 4,000,000                                            │
│  └─ Introduced: SegregatedWitness (August 24, 2017)                 │
│                                                                        │
│  BENEFITS:                                                           │
│  ✓ Effective block size increase (~4x)                               │
│  ✓ Transaction malleability fix                                     │
│  ✓ Enables Lightning Network                                        │
│  ✓ Backward compatible (soft fork)                                  │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 10. OWL CLASS RELATIONSHIPS IN RDF

```turtle
# COMPLETE CLASS STRUCTURE IN TURTLE NOTATION

# Block with all its relationships
:Block a owl:Class ;
    rdfs:subClassOf :DataStructure ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty :hasBlockHeader ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty :containsTransaction ;
        owl:minCardinality "1"^^xsd:nonNegativeInteger
    ] .

# Block Header with 6 required fields
:BlockHeader a owl:Class ;
    rdfs:subClassOf :DataStructure ;
    rdfs:subClassOf [
        owl:onProperty :version ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        owl:onProperty :previousBlockHash ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        owl:onProperty :merkleRoot ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        owl:onProperty :timestamp ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        owl:onProperty :difficultyTarget ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] ;
    rdfs:subClassOf [
        owl:onProperty :nonce ;
        owl:cardinality "1"^^xsd:nonNegativeInteger
    ] .

# Merkle Tree Root relationship
:BlockHeader rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty :hasMerkleRoot ;
    owl:cardinality "1"^^xsd:nonNegativeInteger
] .

# Transaction types (disjoint)
[] a owl:AllDisjointClasses ;
    owl:members ( 
        :CoinbaseTransaction 
        :StandardTransaction 
        :SegWitTransaction 
    ) .
```

---

## 11. SPARQL QUERY EXAMPLES

### Query 1: Get Complete Block Structure
```sparql
PREFIX bc: <http://example.org/blockchain#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Retrieve all properties and relationships of Block class
SELECT ?property ?type ?domain ?range ?cardinality
WHERE {
    {
        ?property rdfs:domain bc:Block .
        ?property a ?type .
        OPTIONAL { ?property rdfs:range ?range }
    }
    UNION
    {
        bc:Block rdfs:subClassOf ?restriction .
        ?restriction a owl:Restriction .
        ?restriction owl:onProperty ?property .
        OPTIONAL { ?restriction owl:cardinality ?cardinality }
    }
}
```

### Query 2: Trace Merkle Tree Relationships
```sparql
PREFIX bc: <http://example.org/blockchain#>

# Show how MerkleRoot connects to BlockHeader and Block
SELECT ?block ?header ?merkleRoot
WHERE {
    ?block bc:hasBlockHeader ?header .
    ?header bc:hasMerkleRoot ?merkleRoot .
}
```

### Query 3: Get Transaction Types and Properties
```sparql
PREFIX bc: <http://example.org/blockchain#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

# List all transaction types with definitions
SELECT ?txType ?label ?definition
WHERE {
    ?txType rdfs:subClassOf+ bc:Transaction .
    ?txType rdfs:label ?label .
    ?txType skos:definition ?definition .
}
```

### Query 4: Verify Block Constraints
```sparql
PREFIX bc: <http://example.org/blockchain#>

# Check that Block has required cardinality constraints
SELECT ?restriction ?property ?cardinality
WHERE {
    bc:Block rdfs:subClassOf ?restriction .
    ?restriction a owl:Restriction .
    ?restriction owl:onProperty ?property .
    ?restriction owl:cardinality ?cardinality .
}
```

---

## 12. PYTHON CODE: Exploring Relationships

```python
from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.namespace import SKOS

# Load ontology
g = Graph()
g.parse("blockchain_ontology_v1_0_0.ttl", format="turtle")

BC = Namespace("http://example.org/blockchain#")

# Function 1: Get all properties of a class
def get_class_properties(class_uri):
    """Retrieve all properties (data and object) for a class"""
    query = f"""
    PREFIX bc: <http://example.org/blockchain#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?property ?label ?range
    WHERE {{
        ?property rdfs:domain <{class_uri}> .
        ?property rdfs:label ?label .
        OPTIONAL {{ ?property rdfs:range ?range }}
    }}
    """
    
    results = list(g.query(query))
    return [(str(r.label), str(r.range) if r.range else 'N/A') 
            for r in results]

# Function 2: Get cardinality constraints
def get_cardinality_constraints(class_uri):
    """Retrieve cardinality restrictions for a class"""
    query = f"""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?property ?cardinality ?minCard ?maxCard
    WHERE {{
        <{class_uri}> rdfs:subClassOf ?restriction .
        ?restriction a owl:Restriction .
        ?restriction owl:onProperty ?property .
        OPTIONAL {{ ?restriction owl:cardinality ?cardinality }}
        OPTIONAL {{ ?restriction owl:minCardinality ?minCard }}
        OPTIONAL {{ ?restriction owl:maxCardinality ?maxCard }}
    }}
    """
    
    results = list(g.query(query))
    constraints = []
    for r in results:
        prop = str(r.property).split('#')[-1]
        if r.cardinality:
            constraints.append(f"{prop}: exactly {r.cardinality}")
        elif r.minCard:
            constraints.append(f"{prop}: at least {r.minCard}")
        elif r.maxCard:
            constraints.append(f"{prop}: at most {r.maxCard}")
    return constraints

# Function 3: Trace Merkle Tree to Transactions
def trace_merkle_to_transactions():
    """Show relationship chain: Block → Header → MerkleRoot → Transactions"""
    print("\n=== MERKLE TREE RELATIONSHIP CHAIN ===\n")
    print("Block")
    print("  └─ hasBlockHeader → BlockHeader")
    print("      └─ hasMerkleRoot → MerkleTreeRoot")
    print("          └─ (computed from all Transactions)")
    print("\nBlock")
    print("  └─ containsTransaction → Transaction (multiple)")
    print("      └─ hashed and aggregated into MerkleTreeRoot")

# Usage examples
print("=== BLOCK CLASS STRUCTURE ===\n")
print("Properties:")
for prop, range_type in get_class_properties(BC.Block):
    print(f"  • {prop}: {range_type}")

print("\nCardinality Constraints:")
for constraint in get_cardinality_constraints(BC.Block):
    print(f"  • {constraint}")

print("\n=== BLOCK HEADER STRUCTURE ===\n")
print("Properties:")
for prop, range_type in get_class_properties(BC.BlockHeader):
    print(f"  • {prop}: {range_type}")

print("\nCardinality Constraints:")
for constraint in get_cardinality_constraints(BC.BlockHeader):
    print(f"  • {constraint}")

trace_merkle_to_transactions()
```

---

## 13. KEY INSIGHTS FROM STRUCTURE ANALYSIS

### ✅ Well-Defined Relationships

1. **Block → BlockHeader** (1:1, required)
   - Constraint: `owl:cardinality "1"`
   - Every block has exactly one header

2. **Block → Transaction** (1:many, required)
   - Constraint: `owl:minCardinality "1"`
   - Every block has at least one transaction

3. **BlockHeader → MerkleTreeRoot** (1:1, required)
   - Constraint: `owl:cardinality "1"`
   - Every header has exactly one merkle root

4. **Block → ParentBlock** (0:1, functional)
   - Property: `hasParentBlock` (functional)
   - Every block except genesis has exactly one parent

5. **Block → ChildBlock** (0:many)
   - Property: `hasChildBlock` (inverse of hasParentBlock)
   - Blocks can have multiple children during forks

### 📊 Merkle Tree Details Available

The ontology provides:
- ✅ MerkleTree class hierarchy
- ✅ MerkleTreeRoot as specialized subclass
- ✅ Relationship to BlockHeader via hasMerkleRoot
- ✅ Implicit relationship to Transactions (computed from)
- ✅ MAST (Merkelized Alternative Script Trees) for Taproot
- ✅ Documentation of merkle tree purpose and function

### 🔗 Transaction Relationships

- ✅ Three transaction types (disjoint)
- ✅ CoinbaseTransaction must be first
- ✅ SegWitTransaction for post-2017 blocks
- ✅ Relationship to Block via containsTransaction
- ✅ Relationship to MerkleRoot (via computation)

---

**End of Visual Structure Guide**
