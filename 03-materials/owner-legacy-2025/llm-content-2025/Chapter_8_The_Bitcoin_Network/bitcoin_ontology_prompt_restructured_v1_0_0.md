# Bitcoin Transaction Ontology Development Prompt (Restructured)

## META-INSTRUCTIONS FOR CLAUDE SONNET 4.5

### Execution Context
You are an expert ontology engineer specializing in blockchain domain modeling, with deep expertise in RDF/OWL semantics, formal knowledge representation, and academic rigor. You will develop a comprehensive Bitcoin transaction ontology through a systematic, phase-gated approach.

### Core Constraints
- **Structural Template**: Strictly follow `meta_v5_2_0.ttl` patterns for all classes, properties, and axioms
- **Quality Baseline**: Achieve minimum 98% compliance with `oqc_v1_2_0.ttl` quality criteria
- **Issue Mitigation**: Apply all remediation patterns from `redo_v1_2.ttl` to prevent known defects
- **Research Methodology**: Execute systematic research using `research_ontology_v6_phase4.ttl` framework
- **Domain Foundation**: Use `Chapter_8_The_Bitcoin_Network.txt` as base knowledge, then extend beyond book scope

### Anti-Hallucination Protocol
Execute these strategies continuously throughout all phases:

1. **Source Verification**
   - Every factual claim MUST link to verifiable source (academic paper, technical specification, or blockchain documentation)
   - Use dcterms:source property for all domain assertions
   - Maintain source_registry.json tracking all references with DOI/URL/ISBN

2. **Explicit Uncertainty Marking**
   - Mark any inference with rdfs:comment containing "INFERRED:" prefix
   - Flag speculative relationships with skos:note "Requires validation"
   - Distinguish between book content vs. post-publication research

3. **Cross-Validation Checkpoints**
   - After each phase, execute SPARQL queries against competency questions
   - Compare class hierarchies against Bitcoin Core source code documentation
   - Validate transaction taxonomies against BIP (Bitcoin Improvement Proposal) specifications

4. **Consistency Verification**
   - Run HermiT/Pellet reasoner after each incremental addition
   - Ensure no unsatisfiable classes introduced
   - Validate all domain/range constraints

5. **Grounding in Artifacts**
   - Link every Transaction subclass to actual Bitcoin transaction examples (txid from blockchain)
   - Associate script types with actual script examples from Bitcoin Core
   - Ground abstract concepts in concrete blockchain data

---

## PHASE 1: RESEARCH & CONTENT CONTROL (Complete Before Ontology Development)

### Objective
Establish comprehensive, validated knowledge base covering Bitcoin transactions with post-publication enhancements.

### Task 1.1: Core Content Extraction from Book
**Input**: `Chapter_8_The_Bitcoin_Network.txt`

**Actions**:
1. Extract all transaction-related concepts, their definitions, and relationships
2. Identify taxonomies: node types, transaction types, network protocols, validation methods
3. Map architectural concepts: P2P network structure, message types, consensus mechanisms
4. Document scripting concepts: script languages, opcodes, script templates

**Output**: `bitcoin_core_concepts.json` with structure:
```json
{
  "concepts": [
    {
      "name": "string",
      "definition": "string",
      "source": "Chapter 8, page X",
      "category": "transaction|network|script|validation",
      "relationships": ["related_concept_names"]
    }
  ]
}
```

**Validation**: Ensure 100% of transaction-related content from Chapter 8 is captured.

---

### Task 1.2: Systematic Post-Publication Research
**Research Areas** (execute in parallel):

#### 1.2.1: Bitcoin Transaction Taxonomy Evolution
**Research Protocol**:
- Query: "Bitcoin transaction types 2017-2025" + "SegWit transactions" + "Taproot transactions"
- Sources: Bitcoin Improvement Proposals (BIPs 141, 143, 341, 342), Bitcoin Core documentation
- **Deliverable**: `transaction_taxonomy_2025.md`
  - Standard transactions: P2PKH, P2SH, P2WPKH, P2WSH, P2TR
  - Special transactions: SegWit, Taproot, Lightning Network commitment transactions
  - Each type: structure, purpose, activation date, adoption metrics

#### 1.2.2: Bitcoin Scripting Language Evolution
**Research Protocol**:
- Query: "Bitcoin Script opcodes" + "SegWit script changes" + "Taproot script" + "Miniscript"
- Sources: BIP specifications, Bitcoin Core script documentation, bitcoin.sipa.be/miniscript
- **Deliverable**: `scripting_complete_2025.md`
  - Complete opcode inventory with semantic definitions
  - Script template patterns (standard scripts, multisig, timelock, etc.)
  - SegWit script witness structure
  - Taproot script path and key path spending
  - Miniscript policy language

#### 1.2.3: Transaction Validation & Consensus Rules
**Research Protocol**:
- Query: "Bitcoin transaction validation rules" + "consensus rules 2025"
- Sources: Bitcoin Core validation.cpp, BIP specifications, developer documentation
- **Deliverable**: `validation_rules_2025.md`
  - Pre-SegWit validation rules
  - SegWit validation additions
  - Taproot validation specifics
  - Mempool policy rules vs. consensus rules

#### 1.2.4: Block-Transaction Relationships
**Research Protocol**:
- Query: "Bitcoin block structure" + "Merkle tree" + "block header" + "SegWit block structure"
- Sources: Bitcoin protocol documentation, BIP 141
- **Deliverable**: `block_transaction_structure.md`
  - Block anatomy: header, transaction list, witness data
  - Merkle tree construction and transaction verification
  - Block size limits: legacy vs. SegWit weight units

#### 1.2.5: Transaction Use Cases & Applications
**Research Protocol**:
- Query: "Bitcoin transaction use cases" + "payment channels" + "atomic swaps" + "DLCs"
- Sources: Lightning Network paper, atomic swap specifications, DLC specifications
- **Deliverable**: `transaction_applications_2025.md`
  - Payment use cases: simple send, multi-party, batching
  - Smart contract primitives: HTLCs, PTLCs, timelocks
  - Layer 2 applications: Lightning channels, sidechains
  - Advanced contracts: Discreet Log Contracts, vaults

**Research Quality Criteria**:
- ✓ Every claim backed by specific BIP number, commit hash, or academic paper
- ✓ All source URLs verified accessible and archived
- ✓ Post-2017 developments clearly dated with activation block heights
- ✓ Technical accuracy validated against Bitcoin Core 25.0+ behavior

**Phase 1 Gate**: All 5 deliverables complete, cross-validated, with comprehensive source registry → Only then proceed to Phase 2

---

## PHASE 2: ONTOLOGY ARCHITECTURE & TAXONOMY DESIGN

### Objective
Design complete class hierarchy and property structure before implementation.

### Task 2.1: Top-Level Ontology Structure
**Using**: `meta_v5_2_0.ttl` as structural template

**Design Decisions Document** (`ontology_architecture.md`):

#### 2.1.1: Namespace & Metadata
```turtle
@prefix btc: <http://example.org/bitcoin-transaction#> .
@prefix btx: <http://example.org/bitcoin-transaction/taxonomy#> .
@prefix bsc: <http://example.org/bitcoin-script#> .

<http://example.org/bitcoin-transaction> a owl:Ontology ;
    dcterms:title "Bitcoin Transaction Ontology"@en ;
    dcterms:description "Comprehensive formal model of Bitcoin transactions..."@en ;
    dcterms:created "2025-12-19"^^xsd:date ;
    dcterms:source <Chapter_8_Reference>, <BIP_141>, <BIP_341>, ... ;
    owl:versionInfo "1.0.0" ;
    owl:imports <http://example.org/ontology-engineering> .
```

#### 2.1.2: Root Class Hierarchy
**Primary Taxonomies**:
1. **Transaction Taxonomy** (btc:Transaction as root)
   - Organized by script type (P2PKH, P2SH, SegWit, Taproot)
   - Organized by function (standard, coinbase, commitment)
   - Organized by validation status (confirmed, unconfirmed, invalid)

2. **Script Taxonomy** (bsc:Script as root)
   - Script types: PubKeyScript, ScriptSig, Witness
   - Script templates: StandardScript, MultisigScript, TimelockScript, etc.

3. **Network Component Taxonomy** (btc:NetworkComponent as root)
   - Node types from Chapter 8
   - Protocol layers

4. **Blockchain Structure** (btc:BlockchainComponent as root)
   - Block, BlockHeader, Merkle tree structures

**Output**: Complete class hierarchy diagram in OWL Manchester Syntax

---

### Task 2.2: Property Architecture
**Design property framework before instantiation**:

#### 2.2.1: Transaction Properties
**Object Properties**:
- `btc:hasInput` (domain: Transaction, range: TransactionInput)
- `btc:hasOutput` (domain: Transaction, range: TransactionOutput)
- `btc:hasScriptSig` (domain: TransactionInput, range: Script)
- `btc:hasScriptPubKey` (domain: TransactionOutput, range: Script)
- `btc:hasWitness` (domain: SegWitTransaction, range: WitnessData)
- `btc:spends` (domain: TransactionInput, range: UTXO)
- `btc:includedInBlock` (domain: Transaction, range: Block)

**Datatype Properties**:
- `btc:txid` (domain: Transaction, range: xsd:hexBinary)
- `btc:versionNumber` (domain: Transaction, range: xsd:integer)
- `btc:locktime` (domain: Transaction, range: xsd:nonNegativeInteger)
- `btc:amount` (domain: TransactionOutput, range: xsd:decimal)

#### 2.2.2: Script Properties
**Object Properties**:
- `bsc:containsOpcode` (domain: Script, range: Opcode)
- `bsc:evaluatesTo` (domain: Script, range: ScriptResult)

**Datatype Properties**:
- `bsc:opcodeHex` (domain: Opcode, range: xsd:hexBinary)
- `bsc:opcodeDecimal` (domain: Opcode, range: xsd:integer)
- `bsc:scriptHex` (domain: Script, range: xsd:hexBinary)

**Output**: Complete property specification with domains, ranges, cardinalities, disjointness axioms

---

### Task 2.3: Competency Questions & SPARQL Queries
**Define what the ontology must answer** (minimum 20 questions):

**Transaction Queries**:
1. "Retrieve all SegWit transaction types" → SPARQL query
2. "Find all transactions that use P2PKH scripts" → SPARQL query
3. "List all standard transaction templates" → SPARQL query

**Script Queries**:
4. "What opcodes are valid in Taproot scripts?" → SPARQL query
5. "Find all scripts with timelock constraints" → SPARQL query

**Validation Queries**:
6. "List all validation rules for SegWit transactions" → SPARQL query
7. "What are the consensus rules for Taproot?" → SPARQL query

**Architecture Queries**:
8. "Show the hierarchy of transaction types" → SPARQL query
9. "Find all block-transaction relationships" → SPARQL query

**Use Case Queries**:
10. "Identify transactions suitable for Lightning Network channels" → SPARQL query

**Output**: `competency_questions.ttl` with formal CQ instances and verification queries

**Phase 2 Gate**: Architecture reviewed against meta_v5.2.0 patterns, all CQs formalized, property framework complete → Proceed to Phase 3

---

## PHASE 3: INCREMENTAL ONTOLOGY CONSTRUCTION

### Execution Strategy
Build ontology in testable increments, validating after each module.

### Module 3.1: Core Transaction Classes (Implement First)
**Scope**: Base Transaction class and immediate subclasses

**Implementation Order**:
1. `btc:Transaction` (root class with core properties)
2. `btc:StandardTransaction` vs. `btc:NonStandardTransaction`
3. `btc:P2PKHTransaction`, `btc:P2SHTransaction`, `btc:P2WPKHTransaction`, etc.
4. Add cardinality restrictions: transaction must have ≥1 input, ≥1 output
5. Add disjointness axioms: SegWit disjoint with legacy, etc.

**Validation Protocol**:
- Load into Protégé, run HermiT reasoner
- Execute CQ1-3 SPARQL queries
- Verify no unsatisfiable classes
- Check compliance with oqc_v1_2_0.ttl SHACL shapes

**Output**: `btc_transactions_v0.1.ttl` → Present to user for download

---

### Module 3.2: Transaction Input/Output Structure
**Scope**: UTXO model, inputs, outputs

**Implementation**:
1. `btc:TransactionInput` with properties: previousTxid, vout, scriptSig, sequence
2. `btc:TransactionOutput` with properties: amount, scriptPubKey
3. `btc:UTXO` (Unspent Transaction Output) class
4. Relationship axioms: `spends`, `createsUTXO`

**Validation**: Test with actual transaction examples from blockchain
**Output**: `btc_io_v0.2.ttl` → Present to user

---

### Module 3.3: Bitcoin Script Ontology
**Scope**: Complete script language formalization

**Implementation**:
1. `bsc:Script` hierarchy: ScriptSig, ScriptPubKey, WitnessScript
2. `bsc:Opcode` class with all 200+ opcodes as individuals
3. Script templates: `bsc:P2PKHScriptTemplate`, `bsc:MultisigTemplate`, etc.
4. Script evaluation semantics

**Grounding**: Link each opcode to Bitcoin Core implementation (functional.h line numbers)
**Validation**: Verify opcode inventory against Bitcoin Core 25.0
**Output**: `bsc_scripts_v0.3.ttl` → Present to user

---

### Module 3.4: SegWit & Taproot Extensions
**Scope**: Post-2017 transaction types

**Implementation**:
1. `btc:SegWitTransaction` with witness data structure
2. `btc:TaprootTransaction` with key path and script path spending
3. Weight units vs. size calculations
4. Witness commitment structure

**Validation**: Test against actual SegWit/Taproot transactions from blockchain
**Output**: `btc_modern_v0.4.ttl` → Present to user

---

### Module 3.5: Block-Transaction Integration
**Scope**: How transactions fit into blocks

**Implementation**:
1. `btc:Block`, `btc:BlockHeader` classes
2. Merkle tree structure: `btc:MerkleNode`, `btc:MerkleRoot`
3. Transaction ordering and inclusion rules
4. Coinbase transaction special properties

**Output**: `btc_blocks_v0.5.ttl` → Present to user

---

### Module 3.6: Validation & Consensus Rules
**Scope**: Formal rules for transaction validity

**Implementation**:
1. `btc:ValidationRule` hierarchy
2. `btc:ConsensusRule` vs. `btc:PolicyRule` distinction
3. Specific rule instances: "SegWit validation rule", "Taproot activation rule", etc.
4. Link rules to BIP specifications

**Output**: `btc_validation_v0.6.ttl` → Present to user

---

### Module 3.7: Use Cases & Applications
**Scope**: How transactions are used in practice

**Implementation**:
1. `btc:UseCase` taxonomy: Payment, SmartContract, Layer2
2. Specific patterns: HTLC, multisig, timelock combinations
3. Lightning Network transaction types
4. DLC transaction structures

**Output**: `btc_usecases_v0.7.ttl` → Present to user

---

## PHASE 4: INTEGRATION & QUALITY ASSURANCE

### Task 4.1: Ontology Merging
**Actions**:
1. Merge all module files into single coherent ontology
2. Resolve any inter-module inconsistencies
3. Add global disjointness axioms
4. Optimize property hierarchy

**Output**: `bitcoin_transaction_ontology_v1.0.ttl`

---

### Task 4.2: Comprehensive Validation

#### 4.2.1: Reasoning Validation
- Run Pellet, HermiT, and ELK reasoners
- Verify consistent classification
- Check for unintended inferences

#### 4.2.2: OQC Quality Assessment
**Execute against oqc_v1_2_0.ttl criteria**:

**Target Scores** (honest assessment):
- **Correctness**: 100% (no logical errors, consistent classification)
- **Depth**: 100% (appropriate granularity: 4-6 class hierarchy levels)
- **Completeness**: 98% (covers all transaction types, scripts, validation rules)
- **Consistency**: 98% (uniform naming, pattern application)
- **Comprehensiveness**: 98% (includes edge cases, covers post-publication enhancements)
- **Academic Rigor**: 100% (all claims sourced, formal semantics)
- **Usability**: 98% (clear labels, comprehensive documentation)
- **Interoperability**: 95% (follows OWL 2 DL, uses standard vocabularies)

**Assessment Method**:
1. Execute SHACL validation against oqc_v1_2_0.ttl shapes
2. Generate quality report with specific metrics
3. Document any deviations from 98% baseline

---

### Task 4.3: Competency Question Verification
**Execute all 20+ SPARQL queries against final ontology**:
- Document query results
- Verify results against expected answers
- Calculate coverage: % of CQs answered satisfactorily

**Gate**: 100% of CQs must execute without error, 95% must return expected results

---

### Task 4.4: Remediation Cycles
**If quality scores < target**:

**Iteration Protocol**:
1. Identify specific deficiency (e.g., "Missing documentation for 12 classes")
2. Apply targeted fix (e.g., "Add skos:definition for each missing class")
3. Re-validate with OQC metrics
4. Document remediation in ontology metadata

**Maximum Iterations**: 3 cycles
**Quality Gate**: Final assessment must show:
- Correctness ≥ 100%
- Depth ≥ 100%
- Academic Rigor ≥ 100%
- All other dimensions ≥ 98%

---

## PHASE 5: DOCUMENTATION & DELIVERY

### Task 5.1: Comprehensive Documentation
**Generate**:
1. **Technical Documentation** (`ONTOLOGY_SPECIFICATION.md`):
   - Complete class/property inventory
   - Design rationale for each major decision
   - Mapping between ontology and Bitcoin protocol

2. **User Guide** (`USER_GUIDE.md`):
   - How to query the ontology
   - Example SPARQL queries for common tasks
   - Integration guide for developers

3. **Quality Report** (`QUALITY_ASSESSMENT.pdf`):
   - Final OQC scores with evidence
   - Competency question results
   - Source provenance documentation

4. **Release Notes** (`CHANGELOG.md`):
   - What's covered from book (Chapter 8 content)
   - Post-publication enhancements
   - Known limitations/future work

---

### Task 5.2: Final Deliverables Package
**Bundle for user**:
```
bitcoin_transaction_ontology_v1.0/
├── bitcoin_transaction_ontology_v1.0.ttl (main file)
├── competency_questions.ttl
├── source_registry.json
├── ONTOLOGY_SPECIFICATION.md
├── USER_GUIDE.md
├── QUALITY_ASSESSMENT.pdf
├── CHANGELOG.md
├── examples/
│   ├── example_queries.sparql
│   └── sample_transactions.ttl (real blockchain examples)
└── validation/
    ├── hermit_report.txt
    ├── oqc_validation_report.ttl
    └── shacl_validation_report.ttl
```

---

## PARALLEL EXECUTION OPPORTUNITIES

Execute these tasks concurrently where possible:

**Phase 1 Parallel Groups**:
- Group A: Tasks 1.2.1, 1.2.2, 1.2.3 (all research queries)
- Group B: Tasks 1.2.4, 1.2.5 (structure and applications)

**Phase 3 Parallel Groups**:
- After Module 3.1 complete, develop 3.2 and 3.3 in parallel
- After 3.4 complete, develop 3.5, 3.6, 3.7 in parallel

**Phase 4 Parallel Groups**:
- Run all three reasoners (Pellet, HermiT, ELK) simultaneously
- Execute OQC validation while running CQ queries

---

## INCREMENTAL DELIVERY PROTOCOL

**User Access Points** (download available without interrupting workflow):

1. After Phase 1: All research deliverables (`research_package_v0.zip`)
2. After each Module 3.x: Individual module file (e.g., `btc_transactions_v0.1.ttl`)
3. After Task 4.1: Merged draft ontology (`bitcoin_transaction_ontology_draft.ttl`)
4. After Task 4.4: Quality-validated ontology (`bitcoin_transaction_ontology_v1.0.ttl`)
5. After Phase 5: Complete documentation package

**Notification Pattern**:
```
✓ Module 3.X completed: [brief_summary]
📦 Available for download: [filename]
⏭️ Proceeding to Module 3.(X+1)...
```

---

## SUCCESS CRITERIA CHECKLIST

**Research Quality (Phase 1)**:
- [ ] 100% of Chapter 8 transaction content extracted
- [ ] All 5 research domains covered comprehensively
- [ ] Every technical claim linked to verifiable source
- [ ] Post-2017 enhancements clearly documented

**Architectural Quality (Phase 2)**:
- [ ] Class hierarchy follows meta_v5.2.0 patterns
- [ ] All properties have explicit domains/ranges
- [ ] 20+ competency questions defined with SPARQL queries
- [ ] Property framework supports all CQs

**Implementation Quality (Phase 3)**:
- [ ] All 7 modules implemented and individually validated
- [ ] No unsatisfiable classes at any stage
- [ ] Each module grounded in real blockchain data
- [ ] Incremental deliveries provided to user

**Final Quality (Phase 4)**:
- [ ] Correctness: 100% (logically consistent, no reasoning errors)
- [ ] Depth: 100% (4-6 hierarchy levels, appropriate granularity)
- [ ] Academic Rigor: 100% (all claims sourced, formal semantics)
- [ ] All other OQC dimensions: ≥98%
- [ ] 100% CQ execution success, 95% correct results
- [ ] Passes all SHACL constraints from oqc_v1_2_0.ttl
- [ ] Applies all remediation patterns from redo_v1_2.ttl

**Documentation Quality (Phase 5)**:
- [ ] Technical specification complete
- [ ] User guide with 10+ example queries
- [ ] Quality report with honest assessment
- [ ] Source provenance fully documented

---

## EXECUTION COMMAND

Claude Sonnet 4.5, execute this prompt as specified:
1. Begin with Phase 1, complete all research before proceeding
2. Maintain strict phase gates - no advancement without validation
3. Apply anti-hallucination protocol continuously
4. Provide incremental deliveries at specified checkpoints
5. Conduct honest quality assessment (no grade inflation)
6. Document all decisions and sources
7. Execute parallel tasks where indicated
8. Present final package with comprehensive documentation

**Estimated Timeline**: 4-6 hours of focused ontology engineering
**Final Deliverable**: Production-ready Bitcoin transaction ontology with 98%+ quality scores across all dimensions, 100% in correctness, depth, and academic rigor.

Execute now.
