# Prompt Engineering: Zero-Time Blockchain Wallets Ontology Development

## Original Prompt (Before Restructuring)
```
"I want a comprehensive ontology and included taxonomies in RDF/OWL syntax following the "Enhanced_Unified_Meta-Ontology_v1.0.1.ttl" satisfying the 98% quality conditions of "OQC Ontology Quality Control Ontology.ttl" for Block Chain Wallets covering the aspects of wallets, the phylosophy, their structure, architecture, use cases, applications, variations, design, implementation.
Use the excerpt chapter from the book which is attached as "Chapter 5 Wallets_Andreas M. Antonopoulos_2017.txt" as a base and conduct further a research using "Ontology for Research in Academy and Industry_Claude_26_10_2025.ttl" to discover the details that are not included in the book as well as all new enhancements after the publication of the book.
The ontology will be used as a base for Zero-Time interactive HTML Page in SEN0401: Special Topics in Software Engineering (Blockchain) course for description, explanation and discovery of the Wallets according to "Operationalizing Zero-Time Development The Double-Layer Architecture Specification_Gemini_04_12_2025.docx", and The Zero-Time Double-Layer Software Development Paradigm_Gemini_04_12_2025.docx"
```

---

# Restructured Prompt Using Prompt Engineering Best Practices

---

## 🎯 MASTER PROMPT: Blockchain Wallets Domain Ontology Development

```xml
<system_role>
You are an Expert Ontology Engineer and Semantic Web Architect with deep expertise in:
- OWL 2 DL ontology design and axiomatization
- Blockchain technology and cryptocurrency wallet architectures
- Zero-Time Software Development methodologies
- Educational content modeling for interactive learning systems
- Quality-controlled ontology engineering following OQuaRE/OntoQA frameworks

You operate within the Zero-Time Development paradigm, where ontologies serve as the 
"Single Source of Truth" (SSOT) that drives automatic generation of educational artifacts.
</system_role>

<context>
<!-- CO-STAR: Context -->
<domain>
Blockchain Cryptocurrency Wallets - encompassing the complete knowledge domain of 
digital asset custody, key management, and transaction authorization mechanisms.
</domain>

<academic_setting>
Course: SEN0401 - Special Topics in Software Engineering (Blockchain)
Institution: Istanbul Kültür University, Computer Engineering Department
Instructor: Prof. Dr. Yusuf Uzun
Semester: [Current Academic Term]
</academic_setting>

<paradigm>
Zero-Time Double-Layer Software Development Architecture:
- Layer 1 (Semantic Layer): OWL/SHACL ontology as declarative specification
- Layer 2 (Technical Layer): Auto-generated interactive HTML educational pages
- Transcompilation: AI4SE-driven transformation from semantics to syntax
</paradigm>

<reference_artifacts>
1. Enhanced_Unified_Meta-Ontology_v1.0.1.ttl - Structural template and design patterns
2. OQC_Ontology_Quality_Control_Ontology.ttl - Quality metrics and validation criteria
3. Ontology_for_Research_in_Academy_and_Industry_Claude_26_10_2025.ttl - Research methodology
4. Chapter_5_Wallets_Andreas_M_Antonopoulos_2017.txt - Foundational domain knowledge
5. Zero-Time Development Architecture Specifications - Implementation paradigm
</reference_artifacts>
</context>

<objective>
<!-- CO-STAR: Objective -->
<primary_goal>
Develop a comprehensive, production-ready Blockchain Wallets Domain Ontology in 
RDF/OWL Turtle syntax that achieves ≥98% quality score across all OQC dimensions.
</primary_goal>

<deliverables>
1. Complete OWL 2 DL ontology file (BlockchainWallets.ttl)
2. Hierarchical taxonomies for all wallet-related concepts
3. SHACL validation shapes for constraint enforcement
4. Competency questions with SPARQL verification queries
5. Educational annotations for Zero-Time HTML generation
</deliverables>

<quality_targets>
| Dimension         | Target | Measurement                                    |
|-------------------|--------|------------------------------------------------|
| Completeness      | ≥98%   | FR→CQ→VQ coverage, term mapping                |
| Correctness       | 100%   | Zero unsatisfiable classes, expert validated   |
| Consistency       | 100%   | Reasoner-verified, no logical contradictions   |
| Comprehensiveness | ≥98%   | Domain coverage vs. source materials           |
| Usability         | ≥95%   | Label coverage, SKOS annotations               |
| Adaptability      | ≥95%   | Version management, modular architecture       |
| Deepness          | ≥95%   | Hierarchy depth 5-8 levels, rich axioms        |
| Capacity          | ≥90%   | Reasoning time <5 min, scalable structure      |
</quality_targets>
</objective>

<style>
<!-- CO-STAR: Style -->
- Follow W3C OWL 2 DL Profile strictly
- Use consistent CamelCase for class names, camelCase for properties
- Apply "Open World + Validation Closure" pattern per Zero-Time methodology
- Include extensive skos:definition, skos:example, rdfs:comment annotations
- Implement Symbiotic Ontology Model with dual Human/Machine views
</style>

<audience>
<!-- CO-STAR: Audience -->
<primary>
Computer Engineering graduate students studying blockchain technology
</primary>
<secondary>
- AI4SE transcompilation engines for HTML generation
- SPARQL query engines for interactive discovery
- OWL reasoners for inference and validation
</secondary>
</audience>

<response_format>
<!-- CO-STAR: Response -->
<structure>
Produce the ontology in modular sections following this architecture:

PART 1: Ontology Header and Metadata
PART 2: Wallet Type Taxonomy (Classes)
PART 3: Wallet Components and Architecture (Classes + Properties)
PART 4: Key Management Concepts (HD Wallets, BIP Standards)
PART 5: Security and Cryptographic Foundations
PART 6: Use Cases and Applications
PART 7: Implementation Patterns and Best Practices
PART 8: SHACL Validation Shapes
PART 9: Competency Questions and SPARQL Queries
PART 10: Educational Annotations for Zero-Time Generation
</structure>

<syntax>
RDF/OWL Turtle (.ttl) format with:
- Standard prefix declarations (owl, rdfs, skos, dc, dcterms, prov, shacl)
- Custom namespace: <http://ikcu.edu.tr/ontology/blockchain/wallets#>
- Inline documentation with SKOS and Dublin Core annotations
</syntax>
</response_format>
```

---

## 📋 TASK DECOMPOSITION (Chain-of-Thought Workflow)

```xml
<workflow>
<phase id="1" name="Domain Analysis and Knowledge Extraction">
  <step>1.1 Parse Chapter 5 (Antonopoulos 2017) and extract core concepts</step>
  <step>1.2 Identify taxonomy hierarchies: wallet types, key types, derivation methods</step>
  <step>1.3 Map relationships: wallet→key, wallet→address, seed→derivation</step>
  <step>1.4 Note temporal aspects: BIP-32 (2012), BIP-39 (2013), BIP-44 (2014)</step>
  
  <output>
  Concept inventory with preliminary class/property candidates
  </output>
</phase>

<phase id="2" name="Research Gap Analysis">
  <step>2.1 Apply Research Ontology methodology to identify gaps</step>
  <step>2.2 Conduct web search for post-2017 wallet innovations</step>
  <step>2.3 Research areas to investigate:
    - Multi-signature wallets (BIP-11, BIP-45, PSBT)
    - Hardware wallet ecosystem (Trezor, Ledger, Coldcard)
    - Smart contract wallets (Gnosis Safe, Argent)
    - MPC (Multi-Party Computation) wallets
    - Social recovery wallets (Argent, Loopring)
    - Account abstraction (ERC-4337)
    - Taproot/Schnorr implications (BIP-340, BIP-341)
    - Lightning Network wallet considerations
    - Cross-chain wallet architectures
  </step>
  <step>2.4 Document findings in structured format</step>
  
  <output>
  Comprehensive concept list including 2017-2025 innovations
  </output>
</phase>

<phase id="3" name="Ontology Architecture Design">
  <step>3.1 Define modular architecture aligned with Meta-Ontology patterns</step>
  <step>3.2 Establish class hierarchy with appropriate abstraction levels</step>
  <step>3.3 Design property taxonomy (object properties, data properties)</step>
  <step>3.4 Identify disjointness axioms (≥50 axioms per OQC requirements)</step>
  <step>3.5 Define property chains for transitive relationships</step>
  <step>3.6 Plan cardinality restrictions for critical relationships</step>
  
  <output>
  Architecture specification document with UML-style diagrams
  </output>
</phase>

<phase id="4" name="Ontology Implementation">
  <step>4.1 Create ontology header with metadata and versioning</step>
  <step>4.2 Implement class hierarchy with rdfs:subClassOf relations</step>
  <step>4.3 Define object properties with domain/range constraints</step>
  <step>4.4 Define data properties with datatype restrictions</step>
  <step>4.5 Add disjointness axioms for major class families</step>
  <step>4.6 Create defined classes (≥30% of total classes)</step>
  <step>4.7 Implement property chains and complex axioms</step>
  <step>4.8 Add comprehensive annotations (labels, definitions, examples)</step>
  
  <output>
  Complete OWL ontology in Turtle syntax
  </output>
</phase>

<phase id="5" name="SHACL Validation Layer">
  <step>5.1 Create NodeShapes for critical classes</step>
  <step>5.2 Define property constraints (cardinality, value types)</step>
  <step>5.3 Implement pattern constraints for identifiers (paths, addresses)</step>
  <step>5.4 Add severity levels (sh:Violation, sh:Warning, sh:Info)</step>
  
  <output>
  SHACL shapes file for validation
  </output>
</phase>

<phase id="6" name="Competency Questions and Testing">
  <step>6.1 Define 30-50 competency questions covering domain scope</step>
  <step>6.2 Translate each CQ to SPARQL verification query</step>
  <step>6.3 Create test instances covering major use cases</step>
  <step>6.4 Verify query coverage ≥95%</step>
  
  <output>
  Test suite with CQs, SPARQL queries, and expected results
  </output>
</phase>

<phase id="7" name="Zero-Time Educational Annotations">
  <step>7.1 Add :hasEducationalLevel annotations (Beginner/Intermediate/Advanced)</step>
  <step>7.2 Include :prerequisiteConcept links for learning paths</step>
  <step>7.3 Add :hasExample with practical illustrations</step>
  <step>7.4 Define :hasVisualization for diagram generation hints</step>
  <step>7.5 Include :interactiveExercise specifications</step>
  
  <output>
  Ontology enriched with Zero-Time HTML generation metadata
  </output>
</phase>

<phase id="8" name="Quality Assurance">
  <step>8.1 Run OWL reasoner (HermiT/Pellet) for consistency check</step>
  <step>8.2 Execute SHACL validation on test instances</step>
  <step>8.3 Calculate OQC metrics using SPARQL queries</step>
  <step>8.4 Verify all quality targets are met (≥98% overall)</step>
  <step>8.5 Document any gaps and remediation actions</step>
  
  <output>
  Quality Assessment Report with metric scores
  </output>
</phase>
</workflow>
```

---

## 📐 STRUCTURAL SPECIFICATIONS

```xml
<taxonomy_requirements>
<wallet_type_hierarchy>
<!-- Root taxonomy for wallet types - MUST follow this structure -->

:Wallet (Abstract Root)
├── :SoftwareWallet
│   ├── :DesktopWallet
│   │   ├── :FullNodeWallet (e.g., Bitcoin Core)
│   │   └── :LightWallet (SPV)
│   ├── :MobileWallet
│   │   ├── :iOSWallet
│   │   └── :AndroidWallet
│   ├── :WebWallet
│   │   ├── :CustodialWebWallet
│   │   └── :NonCustodialWebWallet
│   └── :BrowserExtensionWallet (e.g., MetaMask)
├── :HardwareWallet
│   ├── :AirGappedWallet
│   ├── :USBConnectedWallet
│   └── :BluetoothWallet
├── :PaperWallet
│   ├── :SingleKeyPaperWallet
│   └── :BIP38EncryptedPaperWallet
└── :SmartContractWallet
    ├── :MultisigWallet
    ├── :SocialRecoveryWallet
    └── :AccountAbstractionWallet (ERC-4337)

</wallet_type_hierarchy>

<key_management_hierarchy>
:KeyManagementScheme
├── :NondeterministicKeyScheme (JBOK - Type 0)
├── :DeterministicKeyScheme
│   ├── :SequentialDeterministicScheme (Type 1)
│   └── :HierarchicalDeterministicScheme (HD - Type 2)
│       ├── :BIP32Scheme
│       ├── :BIP44Scheme
│       ├── :BIP49Scheme (SegWit-compatible)
│       ├── :BIP84Scheme (Native SegWit)
│       └── :BIP86Scheme (Taproot)
└── :MPCKeyScheme (Multi-Party Computation)
</key_management_hierarchy>
</taxonomy_requirements>

<required_properties>
<!-- Object Properties (minimum set) -->
:containsKey          domain: Wallet       range: CryptographicKey
:derivesFrom          domain: DerivedKey   range: MasterKey
:hasDerivationPath    domain: DerivedKey   range: DerivationPath
:signsTransaction     domain: Wallet       range: Transaction
:validatesAgainst     domain: Wallet       range: ValidationShape
:implementsStandard   domain: Wallet       range: BIPStandard
:hasSecurityFeature   domain: Wallet       range: SecurityFeature
:supportsBlockchain   domain: Wallet       range: Blockchain

<!-- Data Properties (minimum set) -->
:seedPhrase           domain: HDWallet     range: xsd:string
:mnemonicWordCount    domain: Mnemonic     range: xsd:integer [12,15,18,21,24]
:derivationDepth      domain: DerivedKey   range: xsd:integer
:hardenedDerivation   domain: DerivationPath range: xsd:boolean
:addressCount         domain: Wallet       range: xsd:nonNegativeInteger
</required_properties>
</xml>
```

---

## 🔍 QUALITY CONTROL CHECKLIST (OQC Compliance)

```xml
<oqc_checklist>
<completeness>
□ All functional requirements have associated competency questions
□ All competency questions have SPARQL verification queries
□ All domain terms from Chapter 5 are mapped to ontology components
□ BIP standards (32, 39, 43, 44, 49, 84, 86) fully modeled
</completeness>

<correctness>
□ Zero unsatisfiable classes (reasoner verified)
□ No logical contradictions in axioms
□ Test cases produce expected inferences
□ Property domains/ranges are semantically accurate
</correctness>

<consistency>
□ Naming conventions uniformly applied
□ Annotation properties consistently used
□ Hierarchical relationships properly structured
□ No redundant or circular definitions
</consistency>

<comprehensiveness>
□ Wallet types: All major categories covered
□ Key management: BIP standards comprehensively modeled
□ Security: Attack vectors and mitigations documented
□ Use cases: At least 10 distinct scenarios modeled
□ Post-2017 innovations: MPC, smart contract wallets, social recovery
</comprehensiveness>

<usability>
□ 100% of classes have rdfs:label
□ ≥80% of classes have skos:definition
□ ≥50% of classes have skos:example
□ Consistent language (English) throughout
</usability>

<adaptability>
□ Version management metadata present
□ Change log structure defined
□ Module boundaries clearly delineated
□ Extension points documented
</adaptability>

<deepness>
□ Taxonomy depth: 5-8 levels for major branches
□ ≥50 disjointness axioms defined
□ ≥30% of classes are defined (complex) classes
□ Property chains for transitive relationships
</deepness>
</oqc_checklist>
```

---

## 📝 EXAMPLE ONTOLOGY FRAGMENT (Pattern Reference)

```turtle
# Example fragment demonstrating expected quality and style

@prefix : <http://ikcu.edu.tr/ontology/blockchain/wallets#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix bip: <http://ikcu.edu.tr/ontology/blockchain/bip#> .
@prefix zt: <http://ikcu.edu.tr/ontology/zerotime#> .

#=============================================================================
# HIERARCHICAL DETERMINISTIC WALLET - Example Class Definition
#=============================================================================

:HierarchicalDeterministicWallet rdf:type owl:Class ;
    rdfs:subClassOf :DeterministicWallet ;
    rdfs:subClassOf [
        rdf:type owl:Restriction ;
        owl:onProperty :hasMasterSeed ;
        owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
        owl:onClass :MasterSeed
    ] ;
    rdfs:subClassOf [
        rdf:type owl:Restriction ;
        owl:onProperty :implementsStandard ;
        owl:someValuesFrom bip:BIP32
    ] ;
    owl:disjointWith :NondeterministicWallet ;
    rdfs:label "Hierarchical Deterministic Wallet"@en ;
    rdfs:label "Hiyerarşik Deterministik Cüzdan"@tr ;
    skos:altLabel "HD Wallet"@en ;
    skos:altLabel "Type-2 Wallet"@en ;
    skos:definition """A deterministic wallet that derives all keys from a single 
        master seed using a tree-like hierarchical structure, as defined in BIP-32. 
        The tree structure enables organizational separation of keys (e.g., receiving 
        vs. change addresses) and allows derivation of public keys without access 
        to private keys."""@en ;
    skos:example """A BIP-44 compliant HD wallet with path m/44'/0'/0'/0/0 
        representing the first receiving address of the first Bitcoin account."""@en ;
    skos:scopeNote """HD wallets are the industry standard for modern cryptocurrency 
        wallets due to their backup simplicity (single seed phrase) and 
        organizational flexibility."""@en ;
    dcterms:source <https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki> ;
    # Zero-Time Educational Annotations
    zt:educationalLevel zt:Intermediate ;
    zt:prerequisiteConcept :DeterministicWallet, :CryptographicHashFunction ;
    zt:hasVisualization "tree-diagram" ;
    zt:interactiveExercise "derive-child-key-exercise" ;
    zt:learningObjective """Students will understand how a single seed can 
        generate an infinite tree of cryptographic keys."""@en .

#=============================================================================
# DERIVATION PATH - Example with Cardinality and Pattern Constraints
#=============================================================================

:DerivationPath rdf:type owl:Class ;
    rdfs:subClassOf :WalletComponent ;
    rdfs:label "Derivation Path"@en ;
    skos:definition """A hierarchical path notation (e.g., m/44'/0'/0'/0/0) that 
        specifies the location of a key within an HD wallet tree structure."""@en ;
    skos:example "m/44'/0'/0'/0/2 - Third receiving address of primary Bitcoin account" ;
    skos:notation "m / purpose' / coin_type' / account' / change / address_index" .

:hasPathString rdf:type owl:DatatypeProperty ;
    rdfs:domain :DerivationPath ;
    rdfs:range xsd:string ;
    rdfs:label "has path string"@en ;
    skos:definition "The string representation of the derivation path."@en ;
    # SHACL will enforce pattern: ^m(/\d+'?)+$
    skos:example "m/44'/0'/0'/0/0" .
```

---

## 🎓 ZERO-TIME INTEGRATION SPECIFICATIONS

```xml
<zerotime_requirements>
<layer1_semantic_requirements>
The ontology must include annotations enabling automatic generation of:
1. Interactive concept explorer (collapsible taxonomy trees)
2. Definition cards with examples and related concepts
3. Visual diagrams (class hierarchies, property relationships)
4. Quiz/exercise generators based on competency questions
5. Prerequisite-aware learning paths
</layer1_semantic_requirements>

<annotation_vocabulary>
# Custom Zero-Time vocabulary for educational artifacts
@prefix zt: <http://ikcu.edu.tr/ontology/zerotime#> .

zt:educationalLevel     - Values: zt:Beginner, zt:Intermediate, zt:Advanced
zt:prerequisiteConcept  - Links to required prior knowledge
zt:hasVisualization     - Diagram type hints for generators
zt:interactiveExercise  - Exercise template identifiers
zt:learningObjective    - Bloom's taxonomy aligned objectives
zt:estimatedLearningTime - Duration in minutes
zt:assessmentCriteria   - Evaluation rubric references
</annotation_vocabulary>

<transcompilation_hints>
<!-- Hints for AI4SE HTML generation -->
<hint class="HierarchicalDeterministicWallet">
  <visualization type="tree-diagram">
    Display key derivation tree with m at root, 
    showing hardened (') vs normal derivation
  </visualization>
  <interactive type="path-builder">
    Allow students to construct BIP-44 paths and 
    see resulting key positions
  </interactive>
</hint>
</transcompilation_hints>
</zerotime_requirements>
```

---

## ⚡ EXECUTION INSTRUCTIONS

```xml
<execution_protocol>
<step_1>
THINK: Before writing any ontology code, mentally trace through the complete 
wallet domain from Antonopoulos Chapter 5. Identify the core abstractions:
- Wallet as keychain (not coin container)
- Deterministic vs Non-deterministic distinction
- HD tree structure and derivation mechanics
- BIP standards as formal specifications
</step_1>

<step_2>
RESEARCH: Conduct web searches for post-2017 innovations:
- "cryptocurrency wallet types 2024"
- "MPC wallets blockchain"
- "ERC-4337 account abstraction wallets"
- "social recovery wallet design"
- "BIP-86 Taproot wallets"
</step_2>

<step_3>
DESIGN: Create the class hierarchy following Meta-Ontology patterns:
- Apply disjointness axioms between sibling classes
- Use defined classes for complex concepts
- Ensure property chains for transitive relationships
</step_3>

<step_4>
IMPLEMENT: Write the ontology in Turtle syntax, section by section:
- Start with header and prefixes
- Build class hierarchy top-down
- Add properties with proper restrictions
- Include comprehensive annotations
</step_4>

<step_5>
VALIDATE: Perform quality checks:
- Verify syntax with RDF parser
- Check reasoning consistency
- Calculate OQC metrics
- Ensure ≥98% target achievement
</step_5>

<step_6>
DOCUMENT: Add Zero-Time annotations for HTML generation:
- Educational levels for each concept
- Prerequisite links for learning paths
- Visualization hints for diagram generators
</step_6>
</execution_protocol>
```

---

## 📊 SUCCESS CRITERIA

```
The deliverable is considered successful when:

✅ Ontology parses without errors in Protégé/RDF validators
✅ HermiT/Pellet reasoner reports zero unsatisfiable classes
✅ OQC metrics achieve ≥98% on completeness, correctness, comprehensiveness
✅ All 2017 concepts from Antonopoulos Chapter 5 are modeled
✅ Post-2017 innovations (MPC, smart contract wallets, etc.) are included
✅ ≥50 competency questions with SPARQL verification
✅ SHACL shapes validate test instances correctly
✅ Zero-Time annotations enable HTML generation pipeline
✅ Educational annotations support learning path construction
✅ Documentation is sufficient for student self-study
```

---

## 🔗 REFERENCE LINKS

```
# Standards
BIP-32: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
BIP-39: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
BIP-44: https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
ERC-4337: https://eips.ethereum.org/EIPS/eip-4337

# Ontology Standards
OWL 2: https://www.w3.org/TR/owl2-overview/
SHACL: https://www.w3.org/TR/shacl/
SKOS: https://www.w3.org/TR/skos-reference/

# Quality Frameworks
OQuaRE: ISO 25000 for ontology quality
OntoQA: Ontology quality metrics
```
