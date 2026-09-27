# Zero-Time Interactive Educational Web Page Construction Prompt
## SEN0401: Special Topics in Software Engineering (Blockchain)

**Prompt Version**: 2.0.0  
**Date**: December 12, 2025  
**Methodology**: Research-First Prompt Engineering with Ontology-Driven Architecture  
**Expected Outcome**: Production-Grade Educational Web Application

---

## 🎯 EXECUTIVE SUMMARY

Create a comprehensive, interactive, adaptive HTML5 educational web application for SEN0401 (Blockchain course) following Zero-Time development principles and the WebPageConstruction Ontology specification. The deliverable will synthesize content from authoritative blockchain literature (Antonopoulos, 2017) and academic research reports into an engaging, pedagogically sound learning platform that achieves excellence metrics across correctness (100/100), usability (98+/100), and educational effectiveness (98+/100).

---

## 👤 ROLE AND CONTEXT DEFINITION

### Your Role
You are a **Senior Educational Technology Architect** specializing in:
- Zero-Time web application development using semantic ontologies
- Interactive educational interface design following constructivist learning principles
- Blockchain education content delivery with progressive complexity scaffolding
- Production-grade HTML/CSS/JavaScript implementation following web standards

### Context Sources (Available in Working Directory)

**Primary Content Sources**:
1. `/mnt/user-data/uploads/Chapter6_Transactions_Andreas_M__Antonopoulos_2017.txt`
   - Foundational blockchain transaction concepts (72 core concepts)
   - Transaction structure, UTXO model, script system fundamentals
   - Cryptographic primitives and digital signatures

2. `/mnt/user-data/uploads/Chapter_7_Advanced_Transactions_and_Scripting_Andreas_M__Antonopoulos_2017.txt`
   - Advanced transaction patterns (34 concepts)
   - Multisignature transactions, P2SH, timelocks
   - Payment channels and complex constructions

3. `/mnt/user-data/outputs/blockchain_transactions_research_report_academic.md`
   - Academically rigorous research report (22,000+ words)
   - Post-2017 protocol enhancements (85 concepts)
   - Segregated Witness, Taproot, Schnorr signatures, Lightning Network
   - 40+ scholarly citations with DOI/URL access
   - Pedagogical framework integration

**Structural Specifications**:
4. `/mnt/user-data/uploads/blockchain_transactions_ontology_v1.0.0.ttl`
   - Formal domain ontology (66 classes, 60 properties, 1,108 triples)
   - Transaction type hierarchy with 5-level depth
   - 13 SPARQL-validated competency questions
   - Complete concept inventory with relationships

5. `/mnt/user-data/uploads/WebPageConstruction_Ontology_v1_0_0_ENHANCED.ttl`
   - Web architecture specification (60 classes, 26 object properties)
   - Educational platform patterns and best practices
   - Interactive component specifications
   - Quality control framework (10 functional requirements, 20 test cases)

---

## 🎓 PEDAGOGICAL REQUIREMENTS

### Learning Objectives Alignment
The web application must support Bloom's Revised Taxonomy across six cognitive levels:

**Remembering** (Foundational Layer):
- Transaction structure components (Input, Output, UTXO, TXID)
- Basic script patterns (P2PKH)
- Cryptographic primitives (SHA256, RIPEMD160, ECDSA)

**Understanding** (Conceptual Layer):
- UTXO model vs account-based systems
- Script execution mechanics
- Transaction validation processes

**Applying** (Practical Layer):
- Script composition for spending conditions
- Multisignature scheme construction
- Timelock implementation patterns

**Analyzing** (Architectural Layer):
- Transaction malleability vulnerabilities
- Segregated Witness benefits and trade-offs
- Lightning Network security models

**Evaluating** (Comparative Layer):
- Legacy vs SegWit vs Taproot transaction efficiency
- On-chain vs off-chain scaling approaches
- Privacy implications of different transaction types

**Creating** (Synthesis Layer):
- Custom transaction structures
- Complex script patterns
- Payment channel protocols

### Progressive Complexity Structure
Content must be organized in three ascending tiers with clear visual differentiation:

**🟢 Tier 1: Foundational (Novice-Accessible)**
- No prerequisites beyond general computer science background
- Concepts: Transaction, Input, Output, UTXO, P2PKH, basic cryptography

**🟡 Tier 2: Intermediate (Building on Foundations)**
- Prerequisites: Tier 1 concepts
- Concepts: Multisig, P2SH, timelocks, transaction composition

**🔴 Tier 3: Advanced (Expert-Level)**
- Prerequisites: Tiers 1 & 2
- Concepts: SegWit, Taproot, Schnorr signatures, Lightning Network

---

## 🏗️ TECHNICAL ARCHITECTURE REQUIREMENTS

### Technology Stack Specification (Per WebPageConstruction Ontology)

**Document Format**: Single-file HTML5 with embedded CSS and JavaScript
- No external dependencies requiring CDN connectivity
- Self-contained artifact for offline educational use
- Maximum file size: 9MB (excluding embedded media as data URIs)

**Frontend Framework**: Vanilla JavaScript ES6+ with Modern Web APIs
- No React/Vue/Angular to maintain Zero-Time simplicity
- Progressive enhancement for graceful degradation
- Shadow DOM for component encapsulation where appropriate

**CSS Architecture**: Modern CSS3 with Custom Properties
- CSS Grid and Flexbox for responsive layouts
- CSS Custom Properties (variables) for theme management
- CSS Animations for engaging transitions
- Mobile-first responsive design (breakpoints: 320px, 768px, 1024px, 1440px)

**JavaScript Architecture**: Modular ES6 with Class-Based Components
- Module pattern for namespace organization
- Event-driven architecture for interactivity
- Local Storage API for progress tracking
- Intersection Observer API for scroll animations
- Web Components custom elements for reusable UI

**Accessibility Standards**: WCAG 2.1 Level AA Compliance
- Semantic HTML5 elements (article, section, nav, aside, figure)
- ARIA labels and roles where semantic HTML insufficient
- Keyboard navigation support (Tab, Arrow keys, Enter, Escape)
- Screen reader optimization
- Color contrast ratios ≥4.5:1 for normal text, ≥3:1 for large text

**Performance Requirements**:
- Lighthouse Performance Score: ≥90/100
- First Contentful Paint: <1.5s
- Time to Interactive: <3.0s
- Total Blocking Time: <200ms
- Cumulative Layout Shift: <0.1

---

## 🎨 VISUAL DESIGN REQUIREMENTS

### Color Palette (Success-Oriented, Joyful Theme)

**Primary Colors** (Warm, Energetic):
```css
--primary-blue: #2E86DE;      /* Trust, stability (Bitcoin brand association) */
--primary-green: #10AC84;     /* Success, growth (transaction confirmations) */
--primary-purple: #8E44AD;    /* Innovation, creativity (blockchain technology) */
--primary-orange: #F39C12;    /* Energy, enthusiasm (mining, PoW) */
```

**Secondary Colors** (Supporting, Functional):
```css
--success: #27AE60;           /* Correct answers, completed sections */
--info: #3498DB;              /* Informational callouts, tips */
--warning: #F39C12;           /* Important notes, prerequisites */
--danger: #E74C3C;            /* Incorrect answers, security warnings */
```

**Neutral Palette** (Background, Text):
```css
--bg-primary: #FFFFFF;        /* Main background */
--bg-secondary: #F8F9FA;      /* Section alternation */
--bg-tertiary: #E9ECEF;       /* Card backgrounds */
--text-primary: #2C3E50;      /* Main text (high contrast) */
--text-secondary: #7F8C8D;    /* Secondary text, captions */
--border: #DEE2E6;            /* Dividers, card borders */
```

**Gradient Accents** (Headers, CTAs):
```css
--gradient-primary: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
--gradient-success: linear-gradient(135deg, #F093FB 0%, #F5576C 100%);
--gradient-info: linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%);
```

### Typography Specification

**Font Stack**:
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Fira Code', 'Courier New', monospace;
--font-display: 'Poppins', 'Inter', sans-serif;
```

**Type Scale** (Modular scale: 1.250 - Major Third):
```css
--text-xs: 0.64rem;    /* 10.24px - Fine print */
--text-sm: 0.80rem;    /* 12.8px - Captions, labels */
--text-base: 1.00rem;  /* 16px - Body text */
--text-lg: 1.25rem;    /* 20px - Subheadings */
--text-xl: 1.563rem;   /* 25px - Section headers */
--text-2xl: 1.953rem;  /* 31.25px - Page headers */
--text-3xl: 2.441rem;  /* 39.06px - Hero text */
--text-4xl: 3.052rem;  /* 48.83px - Display text */
```

**Line Height**:
- Body text: 1.6 (optimal readability)
- Headings: 1.2 (visual impact)
- Code blocks: 1.4 (code readability)

### UI Component Specifications

**Navigation Menu** (Sticky, Always Visible):
```
Structure:
- Position: fixed top, z-index 1000
- Height: 64px (desktop), 56px (mobile)
- Background: Gradient primary with 95% opacity backdrop blur
- Shadow: 0 2px 8px rgba(0,0,0,0.1)
- Sections: Logo | Navigation Links | Progress Indicator | Theme Toggle

Features:
- Auto-hide on scroll down, reveal on scroll up
- Active section highlighting
- Smooth scroll to anchors
- Mobile hamburger menu with slide-in drawer
- Keyboard accessible (Tab navigation, Escape to close)
```

**Content Cards** (Modular, Reusable):
```
Structure:
- Border radius: 12px
- Shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06)
- Hover: Transform translateY(-4px), shadow elevation
- Transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- Padding: 24px (desktop), 16px (mobile)

Variants:
1. Concept Card (Foundational knowledge)
2. Code Example Card (Interactive snippets)
3. Visualization Card (Diagrams, animations)
4. Quiz Card (Assessment questions)
5. Reference Card (Citations, external links)
```

**Interactive Visualizations** (Embedded Explanations):
```
Required Visualizations:
1. Transaction Structure Diagram (Interactive SVG)
   - Click elements to reveal details
   - Animated data flow (inputs → outputs)
   - Color-coded by component type

2. UTXO Graph Visualization (D3.js-style Canvas)
   - Nodes: Transaction outputs
   - Edges: Spending relationships
   - Pan/zoom controls
   - Highlight spending chains

3. Script Execution Stack Animation
   - Step-by-step opcode evaluation
   - Stack state visualization
   - Play/pause/reset controls
   - Speed adjustment

4. SegWit Transaction Comparison
   - Side-by-side legacy vs SegWit
   - Witness data highlighting
   - Size/weight calculations
   - Malleability demonstration

5. Lightning Network Channel State
   - Commitment transaction evolution
   - HTLC lifecycle animation
   - Balance updates
   - Penalty mechanism illustration

6. Taproot MAST Tree Explorer
   - Collapsible tree structure
   - Script path selection
   - Privacy demonstration (revealed vs hidden paths)
   - Key/script path comparison
```

**Code Snippet Component** (Executable, Educational):
```html
<div class="code-snippet" data-language="python" data-executable="true">
  <div class="code-header">
    <span class="code-title">Example: UTXO Selection Algorithm</span>
    <button class="code-run">▶ Run</button>
    <button class="code-copy">📋 Copy</button>
  </div>
  <pre><code class="language-python">
# Code with syntax highlighting
  </code></pre>
  <div class="code-output" style="display:none;">
    <div class="output-console">Console output appears here</div>
  </div>
  <div class="code-explanation">
    Step-by-step breakdown of algorithm with inline annotations
  </div>
</div>

Features:
- Syntax highlighting (Prism.js lite embedded)
- Line numbers
- Copy to clipboard
- In-browser execution via Web Workers (for Python: Pyodide lite)
- Step debugger with variable inspection
- Visual output rendering (for visualizations)
- Error handling with educational feedback
```

**Assessment Component** (Kahoot-Style Quizzes):
```html
<div class="quiz-container" data-difficulty="intermediate">
  <div class="quiz-header">
    <span class="quiz-number">Question 3 of 10</span>
    <span class="quiz-timer">⏱ 30s</span>
    <span class="quiz-score">Score: 250 pts</span>
  </div>
  
  <div class="quiz-question">
    <h3>Which transaction type provides the best privacy for complex spending conditions?</h3>
    <p class="quiz-context">Consider scenarios where multiple spending paths exist but only one is executed.</p>
  </div>
  
  <div class="quiz-options">
    <button class="quiz-option" data-correct="false">
      <span class="option-letter">A</span>
      <span class="option-text">P2PKH (Pay-to-Public-Key-Hash)</span>
    </button>
    <button class="quiz-option" data-correct="false">
      <span class="option-letter">B</span>
      <span class="option-text">P2SH (Pay-to-Script-Hash)</span>
    </button>
    <button class="quiz-option" data-correct="true">
      <span class="option-letter">C</span>
      <span class="option-text">P2TR (Pay-to-Taproot) with MAST</span>
    </button>
    <button class="quiz-option" data-correct="false">
      <span class="option-letter">D</span>
      <span class="option-text">P2WPKH (Pay-to-Witness-Public-Key-Hash)</span>
    </button>
  </div>
  
  <div class="quiz-explanation" style="display:none;">
    <h4>✅ Correct! Here's why:</h4>
    <p>Pay-to-Taproot (P2TR) with Merkelized Abstract Syntax Trees (MAST) provides superior privacy because:</p>
    <ul>
      <li><strong>Script Path Hiding</strong>: Only the executed script branch is revealed; unexecuted paths remain hidden.</li>
      <li><strong>Key Path Indistinguishability</strong>: Complex conditions can be resolved via simple key-path spending, appearing identical to standard single-sig transactions.</li>
      <li><strong>Comparison</strong>: P2SH reveals the full redeem script at spending time, exposing all possible spending conditions.</li>
    </ul>
    <div class="quiz-references">
      <strong>Learn More</strong>: <a href="#taproot-section">Taproot Protocol Section</a> | <a href="#mast-visualization">MAST Tree Visualization</a>
    </div>
  </div>
  
  <div class="quiz-stats">
    <span>65% of students answered correctly</span>
    <span>Average time: 18 seconds</span>
  </div>
</div>

Quiz Features:
- Randomized option order
- Optional time limits (adjustable)
- Immediate feedback with explanations
- Point system (correct answer: +100pts, speed bonus: up to +50pts)
- Streak tracking
- Difficulty adaptation (wrong answer → easier, correct → harder)
- Progress saving to localStorage
- Detailed answer analytics
- Reference links to relevant course sections
- Retry mechanism
- Quiz history and performance tracking
```

---

## 📋 CONTENT STRUCTURE SPECIFICATION

### Page Architecture (Hierarchical Organization)

```
┌─────────────────────────────────────────────────────────────┐
│  STICKY HEADER (Always Visible)                            │
│  Logo | Nav Links | Progress | Theme Toggle                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  HERO SECTION                                               │
│  - Course Title: SEN0401 Blockchain                         │
│  - Subtitle: From Fundamentals to Advanced Protocols        │
│  - Visual: Animated blockchain network background           │
│  - CTA: "Begin Learning Journey" scroll to content          │
│  - Quick Stats: 157 Concepts | 40+ Sources | 12 Weeks       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LEARNING PATHS (Interactive Roadmap)                       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐              │
│  │🟢 Tier 1  │→ │🟡 Tier 2  │→ │🔴 Tier 3  │              │
│  │Foundation │  │Intermediate│  │  Advanced │              │
│  └───────────┘  └───────────┘  └───────────┘              │
│  Click to filter content by tier                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 1: TRANSACTION FUNDAMENTALS 🟢                      │
│  ├─ 1.1 What is a Transaction?                             │
│  │   ├─ Concept Card: Definition + Examples               │
│  │   ├─ Visualization: Transaction Anatomy                │
│  │   └─ Quick Quiz: 3 questions                           │
│  ├─ 1.2 UTXO Model                                         │
│  │   ├─ Concept Card: UTXO vs Account-Based              │
│  │   ├─ Interactive Demo: UTXO Graph                      │
│  │   ├─ Code Example: UTXO Selection                      │
│  │   └─ Quick Quiz: 5 questions                           │
│  ├─ 1.3 Transaction Structure                              │
│  │   ├─ Detailed Breakdown: Inputs, Outputs, Metadata    │
│  │   ├─ Interactive SVG: Clickable Components            │
│  │   └─ Code Example: Parsing Transaction Hex            │
│  └─ Module Assessment: 10-question quiz                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 2: SCRIPT SYSTEM 🟢                                 │
│  ├─ 2.1 Bitcoin Script Basics                              │
│  ├─ 2.2 Stack-Based Execution                              │
│  ├─ 2.3 Common Opcodes                                      │
│  ├─ 2.4 P2PKH Script Pattern                               │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 3: CRYPTOGRAPHIC FOUNDATIONS 🟢                     │
│  ├─ 3.1 Hash Functions                                      │
│  ├─ 3.2 Digital Signatures (ECDSA)                         │
│  ├─ 3.3 Public-Private Key Pairs                           │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 4: ADVANCED TRANSACTION PATTERNS 🟡                 │
│  ├─ 4.1 Multisignature Transactions                        │
│  ├─ 4.2 Pay-to-Script-Hash (P2SH)                          │
│  ├─ 4.3 Timelock Mechanisms                                │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 5: SEGREGATED WITNESS 🔴                            │
│  ├─ 5.1 Transaction Malleability Problem                   │
│  ├─ 5.2 SegWit Architecture                                │
│  ├─ 5.3 New Transaction Types (P2WPKH, P2WSH)             │
│  ├─ 5.4 Bech32 Addresses                                   │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 6: TAPROOT & SCHNORR SIGNATURES 🔴                  │
│  ├─ 6.1 Schnorr Signature Advantages                       │
│  ├─ 6.2 Taproot Construction                               │
│  ├─ 6.3 MAST (Merkelized Abstract Syntax Trees)           │
│  ├─ 6.4 Key Path vs Script Path                           │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MODULE 7: LIGHTNING NETWORK 🔴                             │
│  ├─ 7.1 Payment Channels                                    │
│  ├─ 7.2 HTLCs (Hashed Timelock Contracts)                 │
│  ├─ 7.3 Multi-Hop Routing                                  │
│  ├─ 7.4 Channel Lifecycle                                  │
│  └─ Module Assessment                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  COMPREHENSIVE FINAL ASSESSMENT                             │
│  - 50 questions across all modules                          │
│  - Adaptive difficulty                                      │
│  - Detailed performance report                              │
│  - Certificate generation (>80% score)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  REFERENCE SECTION                                          │
│  ├─ Glossary (157 terms with definitions)                  │
│  ├─ Bibliography (40+ citations with links)                │
│  ├─ Code Repository (All examples downloadable)            │
│  └─ External Resources (BIPs, Documentation)               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  FOOTER                                                     │
│  - Course Info | Contact | Feedback | Legal                │
│  - Back to Top Button                                       │
└─────────────────────────────────────────────────────────────┘
```

### Content Mapping Strategy

**For Each Concept from Research Report**:
1. **Extract** concept name, definition, examples from academic report
2. **Classify** by complexity tier (Tier 1/2/3)
3. **Map** to appropriate module section
4. **Enrich** with:
   - Visual diagram (if applicable)
   - Code example (if applicable)
   - Interactive demo (if applicable)
   - 2-3 quiz questions
   - References to source material (Antonopoulos chapters, BIPs)

**For Each Code Example**:
1. **Language**: Python, JavaScript, or Pseudocode
2. **Structure**:
   - Problem statement
   - Step-by-step solution with comments
   - Complexity analysis
   - Execution button
   - Expected output
   - Common pitfalls
3. **Visualization**: Where possible, animate execution steps

---

## ⚙️ PHASED EXECUTION PLAN

### Phase 1: Foundation & Infrastructure (Output: Phase1.html)

**Deliverables**:
- Complete HTML skeleton with semantic structure
- Embedded CSS with full design system
- JavaScript architecture and utility functions
- Sticky navigation with all sections
- Hero section with animations
- Learning path roadmap (interactive)

**Technical Implementation**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SEN0401: Blockchain Transactions - Interactive Course</title>
  <style>
    /* Design system implementation */
    /* Component styles */
    /* Responsive breakpoints */
    /* Animations */
  </style>
</head>
<body>
  <nav id="sticky-nav"><!-- Navigation --></nav>
  <header id="hero"><!-- Hero section --></header>
  <section id="learning-paths"><!-- Roadmap --></section>
  
  <!-- Module containers (empty, populated in later phases) -->
  <main id="course-content"></main>
  
  <footer><!-- Footer --></footer>
  
  <script>
    // JavaScript architecture
    // Navigation logic
    // Progress tracking
    // Theme toggle
    // Scroll animations
  </script>
</body>
</html>
```

**Success Criteria**:
- ✅ All design system colors, typography defined
- ✅ Sticky navigation functional (hide/reveal on scroll)
- ✅ Responsive at all breakpoints
- ✅ Smooth scroll behavior
- ✅ Theme toggle working (light/dark)
- ✅ Progress indicator functional
- ✅ Keyboard navigation operational
- ✅ Valid HTML5, CSS3 (W3C validators)

**Estimated Tokens**: 15,000-20,000  
**Download**: Phase1.html

---

### Phase 2: Tier 1 Content (Modules 1-3) (Output: Phase2.html)

**Deliverables**:
- Module 1: Transaction Fundamentals (complete with all subsections)
- Module 2: Script System (complete with all subsections)
- Module 3: Cryptographic Foundations (complete with all subsections)
- All Tier 1 content cards
- All Tier 1 visualizations
- All Tier 1 code examples
- All Tier 1 quiz questions

**Content Requirements** (Extracted from Sources):

**Module 1.1: What is a Transaction?**
```
Source: Antonopoulos Ch6, Research Report §2.2
Concepts to Cover:
- Definition: Data structure encoding value transfer
- Components: Inputs, Outputs, Version, Locktime
- TXID calculation: Double SHA256 of transaction data
- Transaction lifecycle: Creation → Propagation → Validation → Confirmation

Visualization: Transaction anatomy diagram (interactive SVG)
- Click on Input → Show: Previous TXID, vout index, scriptSig
- Click on Output → Show: Value (satoshis), scriptPubKey
- Click on Locktime → Explain absolute timelock

Code Example:
```python
import hashlib
import json

def calculate_txid(tx_data):
    """Calculate Transaction ID from transaction data"""
    # Serialize transaction (simplified)
    tx_serialized = json.dumps(tx_data, sort_keys=True).encode()
    # First SHA256
    first_hash = hashlib.sha256(tx_serialized).digest()
    # Second SHA256 (reverse byte order for display)
    txid = hashlib.sha256(first_hash).digest()[::-1].hex()
    return txid

# Example transaction
tx = {
    "version": 1,
    "inputs": [{
        "prev_txid": "abc123...",
        "vout": 0,
        "scriptSig": "304502... 0392..."
    }],
    "outputs": [{
        "value": 50000000,  # 0.5 BTC in satoshis
        "scriptPubKey": "OP_DUP OP_HASH160 89ab... OP_EQUALVERIFY OP_CHECKSIG"
    }],
    "locktime": 0
}

print(f"TXID: {calculate_txid(tx)}")
```

Quiz Questions:
Q1: What is a Transaction ID (TXID)?
  A) The address of the sender ❌
  B) A double SHA256 hash of the transaction data ✅
  C) The signature of the transaction ❌
  D) The block height where transaction is confirmed ❌
  
Q2: Which component of a transaction specifies where bitcoins are going?
  A) Input ❌
  B) Output ✅
  C) Locktime ❌
  D) Version ❌

Q3: True or False: A transaction can have multiple inputs but only one output.
  A) True ❌
  B) False ✅
  Explanation: Transactions can have multiple outputs (e.g., payment + change).
```

**Module 1.2: UTXO Model**
```
Source: Antonopoulos Ch6, Research Report §2.2
[Similar detailed specification for UTXO model]
```

**[Continue for all Tier 1 content...]**

**Success Criteria**:
- ✅ All Tier 1 concepts from research report integrated
- ✅ 20+ interactive visualizations working
- ✅ 15+ executable code examples
- ✅ 50+ quiz questions with explanations
- ✅ All module assessments functional
- ✅ Progress tracking updating correctly
- ✅ All content citations included

**Estimated Tokens**: 40,000-50,000  
**Download**: Phase2.html

---

### Phase 3: Tier 2 Content (Module 4) (Output: Phase3.html)

**Deliverables**:
- Module 4: Advanced Transaction Patterns (complete)
  - 4.1 Multisignature Transactions
  - 4.2 Pay-to-Script-Hash (P2SH)
  - 4.3 Timelock Mechanisms
- All Tier 2 visualizations
- All Tier 2 code examples  
- All Tier 2 quiz questions

**Content Requirements** (Intermediate Complexity):

**Module 4.1: Multisignature Transactions**
```
Source: Antonopoulos Ch7, Research Report §2.5
Concepts to Cover:
- M-of-N signature schemes
- CHECKMULTISIG opcode
- Use cases: Escrow, corporate accounts, enhanced security
- 2-of-3 multisig example (Alice-Bob-Arbitrator)
- Standard limits (15-key maximum)

Visualization: Multisig scenario animation
- Show 2-of-3 escrow: Buyer, Seller, Arbitrator
- Demonstrate signature collection process
- Show successful spending (2 valid sigs)
- Show failed spending (only 1 sig)

Code Example:
```python
class MultisigTransaction:
    def __init__(self, m, n, public_keys):
        self.m = m  # Required signatures
        self.n = n  # Total possible signers
        self.public_keys = public_keys
        assert m <= n, "m must be <= n"
        assert n <= 15, "Standard max is 15 keys"
    
    def create_redeem_script(self):
        """Create P2SH redeem script for multisig"""
        script = f"OP_{self.m} "
        for pubkey in self.public_keys:
            script += f"{pubkey} "
        script += f"OP_{self.n} OP_CHECKMULTISIG"
        return script
    
    def verify_signatures(self, signatures):
        """Verify M signatures from N possible"""
        valid_sigs = [sig for sig in signatures if self.verify_sig(sig)]
        return len(valid_sigs) >= self.m

# Example: 2-of-3 escrow
escrow = MultisigTransaction(
    m=2, 
    n=3,
    public_keys=["alice_pubkey", "bob_pubkey", "arbitrator_pubkey"]
)
print(escrow.create_redeem_script())
```

Quiz Questions:
[5-7 questions covering multisig concepts]
```

**[Continue for all Tier 2 content...]**

**Success Criteria**:
- ✅ All Tier 2 concepts from research report integrated
- ✅ 10+ advanced visualizations
- ✅ 10+ complex code examples
- ✅ 30+ quiz questions
- ✅ Prerequisite checking functional (Tier 1 → Tier 2)

**Estimated Tokens**: 35,000-45,000  
**Download**: Phase3.html

---

### Phase 4: Tier 3 Content (Modules 5-7) (Output: Phase4.html)

**Deliverables**:
- Module 5: Segregated Witness (complete)
- Module 6: Taproot & Schnorr Signatures (complete)
- Module 7: Lightning Network (complete)
- All Tier 3 visualizations (most complex)
- All Tier 3 code examples
- All Tier 3 quiz questions

**Content Requirements** (Advanced Complexity):

**Module 5: Segregated Witness**
```
Source: Research Report §3.1 (18 SegWit concepts)
BIP References: BIP141, BIP143, BIP144, BIP173

[Detailed specifications for SegWit module]
- Transaction malleability explanation
- Witness data separation
- Weight units calculation
- P2WPKH and P2WSH formats
- Bech32 address format
```

**Module 6: Taproot & Schnorr**
```
Source: Research Report §3.2 (30 Taproot concepts)
BIP References: BIP340, BIP341, BIP342

[Detailed specifications for Taproot module]
- Schnorr signature advantages
- Key aggregation
- MAST tree structure
- Key path vs script path spending
- Privacy improvements
```

**Module 7: Lightning Network**
```
Source: Research Report §3.3 (34 Lightning concepts)

[Detailed specifications for Lightning module]
- Payment channel architecture
- HTLC mechanism
- Multi-hop routing
- Penalty-based security
```

**Success Criteria**:
- ✅ All Tier 3 concepts integrated
- ✅ 15+ expert-level visualizations
- ✅ 15+ advanced code examples
- ✅ 50+ challenging quiz questions
- ✅ BIP citations with links

**Estimated Tokens**: 45,000-55,000  
**Download**: Phase4.html

---

### Phase 5: Assessment & Reference (Output: Phase5_FINAL.html)

**Deliverables**:
- Comprehensive final assessment (50 questions)
- Glossary with all 157 terms
- Bibliography with all 40+ citations
- Code repository section
- Performance analytics dashboard
- Certificate generation system

**Features**:
1. **Final Assessment**:
   - Adaptive difficulty
   - Time tracking
   - Detailed performance report
   - Comparison to class average (simulated)
   - Certificate for >80% score

2. **Glossary** (from Research Report + Ontology):
   - Alphabetical listing
   - Search functionality
   - Cross-references
   - Related concepts linking

3. **Bibliography**:
   - All Antonopoulos chapter citations
   - All BIP citations with links
   - All academic paper citations with DOIs
   - All research report references

4. **Performance Dashboard**:
   - Module completion percentages
   - Quiz performance by topic
   - Time spent per module
   - Strength/weakness analysis
   - Recommended review topics

**Success Criteria**:
- ✅ Final assessment covers all modules
- ✅ Glossary complete (157 terms)
- ✅ Bibliography complete (40+ sources)
- ✅ Certificate generation working
- ✅ Analytics accurate

**Estimated Tokens**: 20,000-25,000  
**Download**: **Phase5_FINAL.html** (Complete Application)

---

## 🎯 QUALITY ASSURANCE CRITERIA

### Functional Requirements Validation

**FR1: Content Completeness** ✅
- [ ] All 72 base concepts (Antonopoulos Ch6-7) integrated
- [ ] All 85 post-2017 concepts (Research Report) integrated
- [ ] All 157 total concepts covered
- [ ] No content gaps identified

**FR2: Pedagogical Structure** ✅
- [ ] Three-tier progressive complexity implemented
- [ ] Clear prerequisite relationships
- [ ] Bloom's Taxonomy alignment verified
- [ ] Learning objectives stated for each module

**FR3: Interactivity** ✅
- [ ] 50+ interactive visualizations functional
- [ ] 40+ executable code examples working
- [ ] 150+ quiz questions with instant feedback
- [ ] Progress tracking operational

**FR4: Accessibility** ✅
- [ ] WCAG 2.1 Level AA compliance
- [ ] Keyboard navigation complete
- [ ] Screen reader compatible
- [ ] Color contrast ratios verified

**FR5: Performance** ✅
- [ ] Lighthouse Performance ≥90
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <3.0s
- [ ] Total file size <2MB

**FR6: Usability** ✅
- [ ] Intuitive navigation
- [ ] Mobile-responsive (320px-1440px+)
- [ ] Sticky menu always visible
- [ ] Clear visual hierarchy

**FR7: Educational Effectiveness** ✅
- [ ] Content accurate (triple-sourced)
- [ ] Examples concrete and relevant
- [ ] Explanations clear and concise
- [ ] Assessments aligned with content

### Scoring Rubric (Per Requirements)

**Correctness** (Target: 100/100):
- Technical accuracy verified against sources: 30 points
- No factual errors: 25 points
- Proper terminology usage: 25 points
- Correct code examples: 20 points

**Completeness** (Target: 100/100):
- All 157 concepts covered: 40 points
- All modules implemented: 30 points
- All assessments included: 20 points
- Bibliography complete: 10 points

**Comprehensiveness** (Target: 100/100):
- Depth of explanations: 30 points
- Variety of learning materials: 25 points
- Progressive complexity: 25 points
- Reference completeness: 20 points

**Readability** (Target: 100/100):
- Clear, concise writing: 30 points
- Logical organization: 25 points
- Visual clarity: 25 points
- Typography quality: 20 points

**Understandability** (Target: 100/100):
- Concept clarity: 35 points
- Effective examples: 30 points
- Visual aids quality: 20 points
- Progressive learning: 15 points

**Cohesiveness** (Target: 100/100):
- Consistent design: 30 points
- Unified navigation: 25 points
- Cross-referencing: 25 points
- Narrative flow: 20 points

**Modularity** (Target: 100/100):
- Component reusability: 30 points
- Section independence: 25 points
- Maintainability: 25 points
- Extensibility: 20 points

**Usability** (Target: 98+/100):
- Intuitive interface: 35 points
- Responsive design: 30 points
- Accessibility: 23 points
- Performance: 10 points

**User Experience** (Target: 98+/100):
- Visual appeal: 30 points
- Engagement level: 30 points
- Interaction smoothness: 25 points
- Error handling: 13 points

**Aesthetics** (Target: 98+/100):
- Color scheme execution: 30 points
- Typography quality: 25 points
- Visual consistency: 25 points
- Animation polish: 18 points

---

## 📤 OUTPUT SPECIFICATIONS

### Deliverable Format

**File Structure**:
```
Phase1.html         (Foundation, ~500 KB)
Phase2.html         (+ Tier 1 Content, ~900 KB)
Phase3.html         (+ Tier 2 Content, ~1.3 MB)
Phase4.html         (+ Tier 3 Content, ~1.7 MB)
Phase5_FINAL.html   (Complete, ~2.0 MB)
```

**Each Phase Output Includes**:
1. **Download Link**: Immediate file download at phase completion
2. **Phase Summary**: What was added, token usage, file size
3. **Validation Report**: Success criteria checklist
4. **Preview**: Key features to test
5. **Continuation Prompt**: "Ready for Phase X? Type 'CONTINUE' or request adjustments."

### Final Deliverable Documentation

**Phase5_FINAL.html Must Include** (Embedded as Comments):
```html
<!--
=============================================================================
SEN0401: SPECIAL TOPICS IN SWE(BLOCKCHAIN) - INTERACTIVE TRANSACTİONS PAGE
=============================================================================

PROJECT METADATA:
- Version: 1.0.0
- Date: December 12, 2025
- Institution: Istanbul Kültür University
- Course Code: SEN0401
- Course Title: Special Topics in Software Engineering (Blockchain)

CONTENT SOURCES:
1. Antonopoulos, A.M. (2017). Mastering Bitcoin (2nd Ed.), Chapters 6-7
2. Blockchain Transactions Research Report (Academic), 22,000 words
3. Blockchain Transactions Ontology v1.0.0 (66 classes, 60 properties)
4. WebPageConstruction Ontology v1.0.0 Enhanced

TECHNICAL SPECIFICATIONS:
- HTML5 with Semantic Structure
- CSS3 with Custom Properties
- Vanilla JavaScript ES6+
- Zero external dependencies
- Total Size: ~2MB
- Mobile-first responsive design
- WCAG 2.1 Level AA compliant

CONTENT STATISTICS:
- Chapter 6 Transactions
- Chapter 7 Chapter 7 Advanced Transactions and Scripting
- Total Concepts: 157 (72 base + 85 post-2017)
- Modules: 7 major modules
- Visualizations: 50+
- Citations: 40+ with links
- Glossary Terms: 157

QUALITY SCORES (Self-Assessment):
- Correctness: 100/100
- Completeness: 100/100
- Comprehensiveness: 100/100
- Readability: 100/100
- Understandability: 100/100
- Cohesiveness: 100/100
- Modularity: 100/100
- Usability: 98/100
- User Experience: 98/100
- Aesthetics: 98/100

USAGE INSTRUCTIONS:
1. Open Phase5_FINAL.html in modern browser (Chrome 90+, Firefox 88+, Safari 14+)
2. No server required - fully offline functional
3. Enable JavaScript for full interactivity
4. Recommended viewport: 1024px+ for optimal experience
5. Progress saved to browser localStorage

FEEDBACK:
For issues or suggestions, contact: yusuf.altunel@iku.edu.tr

LICENSE:
Educational use only. Content sourced from cited academic materials.
=============================================================================
-->
```

---

## 🎬 EXECUTION PROTOCOL

### How to Proceed

1. **Acknowledge Understanding**: Confirm you understand all requirements before beginning Phase 1.

2. **Request Content Access**: Explicitly request to view source files:
   ```
   Please view:
   - /mnt/user-data/uploads/Chapter6_Transactions_Andreas_M__Antonopoulos_2017.txt
   - /mnt/user-data/uploads/Chapter_7_Advanced_Transactions_and_Scripting_Andreas_M__Antonopoulos_2017.txt
   - /mnt/user-data/outputs/blockchain_transactions_research_report_academic.md
   - /mnt/user-data/uploads/blockchain_transactions_ontology_v1.0.0.ttl
   ```

3. **Phase-by-Phase Development**:
   - Complete each phase fully before proceeding
   - Provide download link after each phase
   - Wait for user confirmation before next phase

4. **Quality Validation**: After each phase, check against success criteria.

5. **User Feedback Loop**: After each phase, ask:
   - "Does Phase X meet your expectations?"
   - "Any adjustments needed before Phase X+1?"
   - "Ready to proceed with Phase X+1? (Type 'CONTINUE')"

---

## ❓ CLARIFICATIONS & CONSTRAINTS

### Constraints
- **Token Limit**: Respect 190,000 token context limit; phase appropriately
- **File Size**: Keep final HTML under 9MB
- **Browser Compatibility**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **No External Dependencies**: All CSS/JS embedded; no CDN requirements
- **Offline Functional**: Must work without internet connection

### Clarifications
- **"Complete Coverage"**: Every concept from research report must appear
- **"No Missing Details"**: Use full explanations from source materials
- **"Kahoot-Style Quizzes"**: Immediate feedback, timer optional, points system, animations
- **"Appealing Colors"**: Use specified success-oriented palette (no dark theme as default)
- **"Always Visible Sticky Menu"**: Fixed position, auto-hide on scroll down, reveal on scroll up
- **"Interactive Learning"**: Click, hover, scroll animations; executable code; responsive visualizations

---

## ✅ PRE-EXECUTION CHECKLIST

Before beginning Phase 1, confirm:
- [ ] All 5 source files accessible in working directory
- [ ] Understanding of WebPageConstruction Ontology structure
- [ ] Understanding of phased execution requirements
- [ ] Clarity on quality scoring criteria
- [ ] Confirmation of color palette and design requirements
- [ ] Agreement on file size and token constraints

---

**READY TO BEGIN?**

Please confirm understanding of this prompt and request to view the source files. Once confirmed, we'll proceed with **Phase 1: Foundation & Infrastructure**.

Type `CONFIRMED - BEGIN PHASE 1` to start, or ask any clarifying questions first.
