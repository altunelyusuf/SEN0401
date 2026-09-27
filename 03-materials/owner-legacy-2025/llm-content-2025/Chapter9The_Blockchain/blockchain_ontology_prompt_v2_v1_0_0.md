# Blockchain Ontology Development - Structured Prompt (v2.0)

## 1. ROLE & CONTEXT DEFINITION

### Primary Role
You are an expert ontology engineer specializing in blockchain technology and semantic web standards, with deep knowledge of RDF/OWL modeling, academic research methodologies, and quality assurance practices aligned with ISO/IEC 25010:2023.

### Task Context
Develop a comprehensive, academically rigorous blockchain ontology based on "Chapter 9: The Blockchain" from "Mastering Bitcoin (2nd Edition, 2017)" by Andreas M. Antonopoulos, supplemented with current research through 2025. The ontology must serve as a foundational knowledge base for blockchain education, development, and content generation.

### Key Constraints
- **Source Material**: `/mnt/user-data/uploads/Chapter_9_The_Blockchain_txt.txt` (primary)
- **Research Framework**: `/mnt/user-data/uploads/research_ontology_v6_phase4.ttl` (methodology reference)
- **Meta-Model**: `/mnt/user-data/uploads/meta_v5_2_0.ttl` (structural conformance)
- **Quality Standard**: `/mnt/user-data/uploads/oqc_v1_2_0.ttl` (98% minimum across all dimensions)
- **Anti-Patterns**: `/mnt/user-data/uploads/redo_v1_2.ttl` (issues to avoid)
- **Output Format**: RDF/OWL Turtle syntax (.ttl)
- **Target Quality**: 100% correctness, depth, academic rigor; 98% all other attributes

---

## 2. ANTI-HALLUCINATION STRATEGY

### 2.1 Grounding Requirements
**CRITICAL**: All ontology elements MUST be traceable to one of these sources:
1. **Direct Evidence**: Explicitly stated in Chapter 9 source text
2. **Research Evidence**: Found through web search with citations
3. **Inference Evidence**: Logically derived from source material with reasoning documented
4. **Standard Evidence**: From established standards (Bitcoin Core, BIPs, academic papers)

### 2.2 Prohibited Behaviors
- ❌ **DO NOT** invent blockchain concepts not in sources
- ❌ **DO NOT** assume knowledge from training cutoff without verification
- ❌ **DO NOT** create relationships without textual or logical evidence
- ❌ **DO NOT** use vague definitions like "related to blockchain functionality"
- ❌ **DO NOT** proceed to next phase without explicit validation completion

### 2.3 Verification Protocol
For EACH class, property, and axiom:
```sparql
# Internal validation query template
ASK WHERE {
  ?element :hasSourceEvidence ?evidence .
  ?evidence :sourceType ?type .  # DirectText | ResearchCitation | LogicalInference | Standard
  ?evidence :evidenceText ?text .
  ?evidence :confidence ?conf .
  FILTER(?conf >= 0.95)  # Minimum 95% confidence
}
```

### 2.4 Citation Format
```turtle
:BlockchainDataStructure
    rdfs:label "Blockchain Data Structure"@en ;
    skos:definition "Ordered, back-linked list of blocks of transactions"@en ;
    :sourceEvidence [
        :sourceType :DirectText ;
        :quotation "The blockchain data structure is an ordered, back-linked list of blocks of transactions" ;
        :sourceDocument "Chapter_9_The_Blockchain_txt.txt" ;
        :lineNumber "4" ;
        :confidence "1.0"^^xsd:decimal
    ] .
```

---

## 3. PHASED EXECUTION PLAN

### PHASE 1: Source Analysis & Knowledge Extraction (AUTO-START)
**Objective**: Extract and validate all blockchain concepts from source material

#### 3.1.1 Source Document Analysis
```bash
# Read complete source
view /mnt/user-data/uploads/Chapter_9_The_Blockchain_txt.txt

# Extract structured information:
- Core concepts (nouns)
- Processes (verbs/actions)
- Relationships (connections)
- Properties (attributes)
- Taxonomies (hierarchies)
```

#### 3.1.2 Concept Inventory Creation
Create `blockchain_concepts_inventory.json`:
```json
{
  "concepts": [
    {
      "term": "Blockchain",
      "type": "Class",
      "definition": "...",
      "source_line": "4",
      "source_quote": "...",
      "confidence": 1.0
    }
  ],
  "properties": [...],
  "relationships": [...]
}
```

#### 3.1.3 Validation Checkpoint 1A
- [ ] All concepts have source line references
- [ ] All definitions are direct quotes or paraphrases
- [ ] No concepts from training data alone
- [ ] Inventory reviewed for completeness

**OUTPUT**: `/mnt/user-data/outputs/phase1_concept_inventory.json`

---

### PHASE 2: Research Enhancement (PARALLEL CAPABLE)

**Objective**: Expand knowledge base with post-2017 developments

#### 3.2.1 Research Query Generation
Based on concept inventory, generate targeted queries:
```python
research_queries = [
    "blockchain fork types after 2017",
    "merkle tree optimizations Bitcoin 2018-2025",
    "proof-of-work difficulty adjustments recent research",
    "blockchain immutability formal definitions",
    # ... systematic query list
]
```

#### 3.2.2 Web Search Protocol
For EACH query:
```bash
# Execute search
web_search("blockchain merkle tree enhancements 2018-2025")

# For each result:
# 1. Verify publication date (2018-2025)
# 2. Verify academic/technical credibility
# 3. Extract relevant concepts
# 4. Document citation metadata
```

#### 3.2.3 Research Integration Rules
```turtle
# Pattern for research-derived concepts
:SegWit a owl:Class ;
    rdfs:label "Segregated Witness"@en ;
    skos:definition "Transaction format upgrade separating signature data"@en ;
    :sourceEvidence [
        :sourceType :ResearchCitation ;
        :citationURL <https://...> ;
        :publicationYear "2017"^^xsd:gYear ;
        :addedInVersion "bitcoin-core-0.13.1" ;
        :confidence "0.98"^^xsd:decimal
    ] ;
    rdfs:comment "Post-2017 enhancement not in source book"@en .
```

#### 3.2.4 Validation Checkpoint 2A
- [ ] All research sources dated 2017-2025
- [ ] All sources credible (academic, Bitcoin Core, BIPs)
- [ ] No Wikipedia-only citations
- [ ] All enhancements relevant to ontology scope

**OUTPUT**: `/mnt/user-data/outputs/phase2_research_citations.json`

---

### PHASE 3: Ontology Architecture Design

**Objective**: Design comprehensive class hierarchy and property framework

#### 3.3.1 Upper Ontology Structure
Following `meta_v5_2_0.ttl` patterns:
```turtle
# Top-level categories
:BlockchainConcept a owl:Class ;
    rdfs:label "Blockchain Concept"@en ;
    skos:definition "Root class for all blockchain-related concepts"@en .

:BlockchainStructure rdfs:subClassOf :BlockchainConcept .
:BlockchainProcess rdfs:subClassOf :BlockchainConcept .
:BlockchainProtocol rdfs:subClassOf :BlockchainConcept .
:BlockchainApplication rdfs:subClassOf :BlockchainConcept .
:BlockchainComponent rdfs:subClassOf :BlockchainConcept .
```

#### 3.3.2 Taxonomy Development
Create hierarchies for:
- **Block Structures**: Genesis → Regular → Orphan → Stale
- **Hash Functions**: SHA256 → Block Hash → Merkle Root
- **Consensus Mechanisms**: PoW → Difficulty → Nonce
- **Network Layers**: Storage → Validation → Propagation
- **Transaction Types**: Coinbase → Standard → Segregated

#### 3.3.3 Property Framework
```turtle
# Object Properties
:hasParentBlock rdfs:domain :Block ; rdfs:range :Block .
:containsTransaction rdfs:domain :Block ; rdfs:range :Transaction .
:referencesBlock rdfs:domain :BlockHeader ; rdfs:range :Block .

# Data Properties
:blockHeight rdfs:domain :Block ; rdfs:range xsd:nonNegativeInteger .
:timestamp rdfs:domain :BlockHeader ; rdfs:range xsd:dateTime .
:nonce rdfs:domain :BlockHeader ; rdfs:range xsd:nonNegativeInteger .
```

#### 3.3.4 Axiom Specification
```turtle
# Disjoint classes
[ a owl:AllDisjointClasses ;
  owl:members ( :GenesisBlock :RegularBlock :OrphanBlock )
] .

# Cardinality constraints
:Block rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty :hasParentBlock ;
    owl:cardinality "1"^^xsd:nonNegativeInteger
] .

# Functional properties
:hasBlockHash a owl:FunctionalProperty .
```

#### 3.3.5 Validation Checkpoint 3A
- [ ] Taxonomy depth 4-6 levels (avoiding over/under-modeling)
- [ ] All classes have superclasses (except root)
- [ ] Disjoint axioms prevent logical inconsistencies
- [ ] Property domains/ranges correctly specified

**OUTPUT**: `/mnt/user-data/outputs/phase3_architecture_design.ttl`

---

### PHASE 4: Comprehensive Ontology Construction

**Objective**: Build complete, validated ontology file

#### 3.4.1 Metadata Header
```turtle
@prefix : <http://example.org/blockchain#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/blockchain> a owl:Ontology ;
    dcterms:title "Blockchain Technology Ontology"@en ;
    dcterms:description """Comprehensive ontology of blockchain technology based on 
        'Mastering Bitcoin' (2nd Edition, Antonopoulos, 2017) with enhancements 
        reflecting developments through 2025."""@en ;
    dcterms:created "2025-12-21"^^xsd:date ;
    dcterms:source <https://www.oreilly.com/library/view/mastering-bitcoin-2nd/9781491954379/> ;
    dcterms:conformsTo <http://example.org/meta/v5.2.0> ,
                        <http://example.org/quality/v1.2.0> ;
    owl:versionInfo "1.0.0" ;
    prov:wasGeneratedBy [
        a prov:Activity ;
        rdfs:label "Systematic Blockchain Ontology Engineering"@en ;
        prov:startedAtTime "2025-12-21T00:00:00Z"^^xsd:dateTime
    ] .
```

#### 3.4.2 Class Definitions (All From Sources)
Systematically define ALL classes with:
- `rdfs:label` (English)
- `skos:definition` (precise, source-based)
- `skos:altLabel` (synonyms)
- `skos:example` (concrete instances)
- `rdfs:comment` (additional context)
- `:sourceEvidence` (traceability)

#### 3.4.3 Property Definitions
All properties with:
- Domain/range constraints
- Characteristics (functional, inverse, transitive, symmetric)
- Cardinality restrictions
- SHACL constraints for validation

#### 3.4.4 Instance Examples
Create representative instances:
```turtle
:GenesisBlock_Bitcoin a :GenesisBlock ;
    rdfs:label "Bitcoin Genesis Block"@en ;
    :blockHash "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f" ;
    :blockHeight 0 ;
    :timestamp "2009-01-03T18:15:05Z"^^xsd:dateTime ;
    :sourceEvidence [
        :sourceType :DirectText ;
        :sourceDocument "Chapter_9_The_Blockchain_txt.txt" ;
        :lineNumber "90"
    ] .
```

#### 3.4.5 Validation Checkpoint 4A
- [ ] Reasoner consistency check (Pellet/HermiT)
- [ ] SHACL validation against `oqc_v1_2_0.ttl`
- [ ] No undefined prefixes
- [ ] No circular definitions
- [ ] All axioms logically sound

**OUTPUT**: `/mnt/user-data/outputs/blockchain_ontology_v1.0.0.ttl`

---

### PHASE 5: Quality Assessment & Remediation

**Objective**: Achieve 100% correctness/depth, 98% all other dimensions

#### 3.5.1 Automated Quality Evaluation
```python
quality_dimensions = {
    "Correctness": {
        "target": 1.00,
        "tests": ["reasoner_consistency", "axiom_validity", "no_contradictions"]
    },
    "Completeness": {
        "target": 0.98,
        "tests": ["concept_coverage", "property_coverage", "documentation_coverage"]
    },
    "Depth": {
        "target": 1.00,
        "tests": ["taxonomy_depth_4_6", "granularity_appropriate", "specificity_score"]
    },
    "Comprehensiveness": {
        "target": 0.98,
        "tests": ["domain_coverage", "edge_cases", "variant_coverage"]
    },
    "Consistency": {
        "target": 0.98,
        "tests": ["naming_conventions", "definition_style", "annotation_uniformity"]
    },
    "Academic_Rigor": {
        "target": 1.00,
        "tests": ["citation_coverage", "formal_definitions", "research_alignment"]
    }
    # ... 8 more dimensions from OQC
}
```

#### 3.5.2 Manual Quality Review
For EACH dimension below 98%:
1. Identify specific deficiencies
2. Document remediation plan
3. Implement fixes
4. Re-evaluate
5. Iterate until target met

#### 3.5.3 Honest Assessment Protocol
```python
# NO optimistic bias - be critical
def honest_evaluate(ontology, dimension):
    """
    Rules:
    - Deduct points for ANY missing documentation
    - Deduct points for ANY logical inconsistency
    - Deduct points for vague/ambiguous definitions
    - Deduct points for missing source citations
    - Round DOWN, not up
    """
    score = calculate_score(ontology, dimension)
    return min(score, expected_target)  # Cap at realistic maximum
```

#### 3.5.4 Validation Checkpoint 5A
- [ ] Correctness: 100% (reasoner passes, no contradictions)
- [ ] Depth: 100% (appropriate granularity verified)
- [ ] Academic Rigor: 100% (all citations present)
- [ ] All other dimensions: ≥98%
- [ ] Assessment honest (not inflated)

**OUTPUTS**: 
- `/mnt/user-data/outputs/quality_assessment_report.json`
- `/mnt/user-data/outputs/blockchain_ontology_v1.0.0_final.ttl`

---

### PHASE 6: Documentation & Deliverables

**Objective**: Produce publication-ready documentation

#### 3.6.1 Technical Documentation
Create `blockchain_ontology_documentation.md`:
- Ontology purpose and scope
- Conceptual architecture diagram
- Class hierarchy visualization
- Property inventory
- Usage examples with SPARQL
- Competency questions and answers
- Quality assessment summary
- References and citations

#### 3.6.2 Quality Report
Create `quality_report.md`:
- Methodology description
- Assessment results per dimension
- Remediation activities log
- Final scores with evidence
- Honest assessment statement

#### 3.6.3 Usage Guide
Create `usage_guide.md`:
- Loading the ontology
- Query examples
- Integration patterns
- Extension guidelines
- Maintenance recommendations

**OUTPUTS**:
- `/mnt/user-data/outputs/blockchain_ontology_documentation.md`
- `/mnt/user-data/outputs/quality_report.md`
- `/mnt/user-data/outputs/usage_guide.md`

---

## 4. EXECUTION PROTOCOL

### 4.1 Sequential Execution
Phases MUST complete in order:
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
   ↓         ↓         ↓         ↓         ↓         ↓
Validate  Validate  Validate  Validate  Validate  Final
```

### 4.2 Incremental Delivery
After EACH phase completion:
1. Run validation checkpoint
2. Generate phase output file
3. Call `present_files` with output
4. Wait for user acknowledgment before proceeding

### 4.3 Parallel Processing Opportunities
Within phases, parallelize:
- **Phase 2**: Multiple web searches simultaneously
- **Phase 4**: Class definitions can be written in batches
- **Phase 5**: Multiple dimension assessments concurrently

### 4.4 Error Handling
If validation fails:
```python
if checkpoint_fails():
    log_failure_details()
    attempt_remediation()
    re_validate()
    if still_fails():
        halt_and_report()  # DO NOT proceed
```

---

## 5. QUALITY CONTROL FRAMEWORK

### 5.1 Meta-Model Conformance Checks
```sparql
# Every class must conform to meta:Class pattern
ASK WHERE {
  ?class a owl:Class .
  FILTER NOT EXISTS {
    ?class rdfs:label ?label .
    ?class skos:definition ?def .
  }
}
# Should return FALSE (no classes lacking documentation)
```

### 5.2 OQC Dimension Scoring
```python
def score_dimension(ontology, dimension):
    metrics = load_metrics_from_oqc(dimension)
    scores = [evaluate_metric(ontology, m) for m in metrics]
    return weighted_average(scores)
```

### 5.3 REDO Anti-Pattern Avoidance
From `redo_v1_2.ttl`, avoid:
- Vague class definitions
- Missing domain/range constraints
- Inconsistent naming conventions
- Insufficient documentation
- Weak source citations
- Over-generalization
- Under-specification

---

## 6. SUCCESS CRITERIA

### 6.1 Functional Criteria
- [ ] Loads without errors in Protégé
- [ ] Passes OWL 2 DL consistency check
- [ ] Answers all competency questions
- [ ] Supports use case scenarios

### 6.2 Quality Criteria
- [ ] Correctness: 100/100
- [ ] Depth: 100/100
- [ ] Academic Rigor: 100/100
- [ ] Completeness: ≥98/100
- [ ] Comprehensiveness: ≥98/100
- [ ] Consistency: ≥98/100
- [ ] Clarity: ≥98/100
- [ ] Maintainability: ≥98/100
- [ ] [All 14 OQC dimensions]: ≥98/100

### 6.3 Documentation Criteria
- [ ] All classes documented
- [ ] All properties documented
- [ ] All instances have examples
- [ ] All assertions have sources
- [ ] Complete user guide
- [ ] Quality report honest and detailed

---

## 7. EXECUTION COMMAND

**TO START EXECUTION:**

"Begin Phase 1: Source Analysis & Knowledge Extraction. Read the complete blockchain chapter, extract all concepts with source line references, create the concept inventory JSON file, validate completeness, and present the phase 1 output for review before proceeding to Phase 2."

---

## 8. METADATA

- **Prompt Version**: 2.0.0
- **Created**: 2025-12-21
- **Methodology**: Structured Prompt Engineering with Anti-Hallucination Controls
- **Quality Standard**: OQC v1.2.0 + Meta v5.2.0
- **Expected Duration**: 6-8 hours (with validation)
- **Deliverables**: 7 files (1 ontology + 6 documentation/quality files)

---

## APPENDIX A: Competency Questions Template

The ontology MUST answer these questions:

1. What is the structure of a blockchain?
2. How are blocks linked together?
3. What is a block hash and how is it computed?
4. What is a genesis block?
5. How does the blockchain achieve immutability?
6. What is a blockchain fork and how is it resolved?
7. What are the components of a block header?
8. How does the Merkle tree work in blockchain?
9. What is the relationship between block height and block hash?
10. How does proof-of-work relate to blockchain security?
11. What are the different types of blocks?
12. How does the cascade effect work in blockchain?
13. What storage mechanisms exist for blockchain?
14. How are transactions included in blocks?
15. What consensus mechanisms operate in blockchain?

---

## APPENDIX B: Validation Checklist

### Pre-Flight Checks
- [ ] All source files accessible
- [ ] Meta-model loaded
- [ ] OQC framework understood
- [ ] Research tools available

### Per-Phase Validation
- [ ] Source traceability documented
- [ ] No unsupported assertions
- [ ] Quality targets on track
- [ ] No placeholder content

### Final Validation
- [ ] Reasoner consistency: PASS
- [ ] SHACL validation: PASS
- [ ] Competency questions: ALL ANSWERED
- [ ] Quality scores: ALL MET
- [ ] Documentation: COMPLETE
- [ ] Honest assessment: CONFIRMED

---

**END OF STRUCTURED PROMPT**
