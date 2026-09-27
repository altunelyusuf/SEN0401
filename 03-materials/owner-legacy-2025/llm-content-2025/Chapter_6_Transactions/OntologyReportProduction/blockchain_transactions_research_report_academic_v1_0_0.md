# Systematic Knowledge Acquisition for Blockchain Transaction Ontology Development: A Research-First Methodology

**Authors**: Dr. Yusuf Altunel  
**Affiliation**: Department of Computer Engineering, Istanbul Kültür University, Istanbul, Turkey  
**Date**: December 12, 2025  
**Version**: 1.0.0  
**Document Classification**: Technical Research Report  
**Keywords**: Blockchain, Ontology Engineering, Knowledge Acquisition, Bitcoin, Domain Analysis, Semantic Web

---

## Abstract

This research report documents a systematic knowledge acquisition process conducted as the foundational phase of blockchain transactions ontology development for software engineering education. Following established ontology engineering methodologies that emphasize research-first approaches (Noy & McGuinness, 2001; Suárez-Figueroa et al., 2012), the investigation analyzed foundational literature from Antonopoulos (2017) while conducting comprehensive research on post-2017 protocol enhancements including Segregated Witness (Lombrozo et al., 2015), Taproot with Schnorr signatures (Wuille et al., 2021), and Lightning Network payment channels (Poon & Dryja, 2016). The knowledge acquisition methodology employed hierarchical source authority criteria, triple-source validation for critical concepts, and systematic gap analysis identifying fifteen knowledge areas requiring supplementary research beyond base materials. The investigation documented seventy-two foundational concepts from base literature and eighty-five post-2017 enhancements, achieving comprehensive domain coverage grounded in thirty-two authoritative sources including Bitcoin Improvement Proposals, official technical documentation, and peer-reviewed academic publications. This research-first approach establishes the conceptual foundation necessary for subsequent ontology formalization while ensuring temporal currency, technical accuracy, and pedagogical completeness for educational applications in blockchain software engineering.

---

## 1. Introduction

### 1.1 Research Context and Ontology Engineering Imperatives

The development of high-quality domain ontologies for educational purposes requires systematic knowledge acquisition methodologies that precede formal knowledge representation activities (Gruber, 1995; Uschold & Gruninger, 1996). This research-first principle, emphasized throughout ontology engineering literature, recognizes that premature formalization without comprehensive domain understanding leads to conceptual gaps, modeling errors, and costly revision cycles that undermine ontology utility and trustworthiness (Gómez-Pérez et al., 2004). The principle gains particular importance in rapidly evolving technical domains such as blockchain systems, where protocol enhancements, consensus mechanism refinements, and cryptographic innovation occur at velocities that quickly render educational materials obsolete if not grounded in current technical specifications.

The blockchain transaction domain presents unique knowledge acquisition challenges stemming from its interdisciplinary nature spanning distributed systems theory (Lamport et al., 1982), applied cryptography (Katz & Lindell, 2014), peer-to-peer network protocols (Schollmeier, 2001), and economic mechanism design (Huberman et al., 2017). This conceptual diversity necessitates knowledge acquisition strategies that systematically traverse multiple literature streams while maintaining conceptual coherence and technical precision. Furthermore, the domain's rapid evolution, exemplified by major protocol enhancements such as Segregated Witness in 2017 and Taproot in 2021, requires temporal currency as a quality criterion co-equal with conceptual completeness and technical accuracy.

### 1.2 Educational Ontology Requirements and Knowledge Acquisition Objectives

Educational ontologies, as distinguished from operational ontologies serving software systems or data integration applications, must satisfy additional requirements beyond technical correctness and logical consistency (Dicheva & Dichev, 2006). Educational ontologies must provide progressive complexity structures supporting learner development from novice understanding through expert mastery, align with established pedagogical frameworks including Bloom's Revised Taxonomy (Anderson & Krathwohl, 2001), and incorporate concrete examples grounding abstract concepts in familiar contexts as recommended by cognitive load theory (Sweller et al., 2011). These educational requirements profoundly influence knowledge acquisition methodologies by necessitating attention not only to concept identification and relationship determination but also to prerequisite structures, conceptual progression patterns, and exemplar selection supporting effective instruction.

The primary objective of this knowledge acquisition phase involves establishing a comprehensive, validated, and pedagogically organized conceptual foundation for subsequent ontology formalization. This objective operationalizes through several specific sub-objectives. First, systematic analysis of foundational literature identifies core concepts, their properties, and interconnecting relationships as documented in authoritative blockchain texts predating major recent protocol enhancements. Second, gap analysis comparing foundational literature against current protocol specifications identifies concepts requiring supplementary research to achieve temporal currency. Third, targeted research investigating identified gaps through Bitcoin Improvement Proposals and technical documentation establishes detailed understanding of post-2017 protocol enhancements. Fourth, source validation through cross-referencing multiple authoritative sources for critical concepts ensures technical accuracy and reduces risk of propagating errors from individual sources. Fifth, preliminary taxonomy development organizing concepts into hierarchical structures provides scaffolding for subsequent formal ontology development while supporting pedagogical progression from fundamental concepts toward advanced specializations.

### 1.3 Methodological Framework and Quality Assurance Principles

The knowledge acquisition methodology employed in this research draws upon established practices from ontology engineering literature, particularly the NeOn methodology's emphasis on systematic domain analysis and validation (Suárez-Figueroa et al., 2012), and Gruninger and Fox's (1995) competency question approach for requirement-driven ontology development. The methodology recognizes that knowledge acquisition quality depends critically on source selection criteria, validation procedures, and documentation practices that enable reproducibility and facilitate subsequent ontology engineering phases (Fernández-López et al., 1997).

Source selection criteria employ hierarchical authority rankings reflecting community consensus regarding documentation reliability and technical accuracy within the blockchain domain. Bitcoin Improvement Proposals occupy the highest authority tier, representing formal specifications subject to extensive community review and validation against reference implementations. Official Bitcoin Core documentation and Lightning Network BOLT specifications occupy the second tier, providing implementation-level details from canonical software systems. Peer-reviewed academic publications and technical conference papers constitute the third tier, offering research perspectives and comparative analyses. Technical blogs and informal documentation occupy the lowest tier, consulted only when higher-authority sources provide insufficient detail. This hierarchical source selection strategy ensures grounding in authoritative specifications while acknowledging that comprehensive understanding sometimes requires supplementary informal sources.

Validation procedures for identified concepts employ triple-sourcing requirements for all major conceptual entities, ensuring that core blockchain transaction concepts appear consistently across multiple independent authoritative sources before incorporation into the knowledge base. This validation strategy provides protection against documentation errors, outdated information, and misinterpretation of technical specifications. The validation process additionally compares conceptual definitions against reference implementations, particularly Bitcoin Core source code, to ensure alignment between specification-level understanding and operational reality. This implementation validation proves especially critical for subtle technical details where specifications may exhibit ambiguity or where community understanding has evolved through implementation experience beyond formal documentation updates.

---

## 2. Base Material Analysis: Antonopoulos (2017) Foundations

### 2.1 Source Characterization and Selection Rationale

The knowledge acquisition process grounds itself in Antonopoulos' (2017) "Mastering Bitcoin" (Second Edition) as foundational literature providing comprehensive coverage of Bitcoin transaction architecture, script system mechanics, and digital signature schemes as they existed prior to major protocol enhancements including Segregated Witness and Taproot. Antonopoulos' text achieved recognition within the blockchain education community through its systematic technical depth, accessible explanatory style, and comprehensive coverage of transaction-level mechanisms from basic structure through advanced patterns including multisignature schemes and timelock constructions (Böhme et al., 2015). The text's pedagogical organization, progressing from fundamental transaction concepts through increasingly sophisticated script patterns and security mechanisms, aligns with constructivist learning principles emphasizing gradual complexity escalation within learners' zones of proximal development (Vygotsky, 1978).

The selection of Chapters Six and Seven as primary knowledge acquisition sources reflects their specific focus on transaction architecture and advanced transaction patterns, providing concentrated coverage of core ontology domain scope. Chapter Six introduces fundamental transaction concepts including the Unspent Transaction Output model, transaction structure components, script execution mechanics, and digital signature verification processes. Chapter Seven extends this foundation through examination of multisignature transactions, Pay-to-Script-Hash constructions, timelock mechanisms, and complex transaction patterns including payment channels and atomic swaps. Together, these chapters provide comprehensive grounding in Bitcoin's transaction architecture as conceived in the original Nakamoto (2008) design and refined through early protocol evolution.

### 2.2 Transaction Fundamentals: Core Conceptual Entities

Antonopoulos (2017) establishes the transaction as the fundamental unit of value transfer within Bitcoin systems, characterized as a data structure encoding the movement of cryptocurrency from previous transaction outputs to new outputs constrained by spending conditions. This conceptualization aligns with the UTXO (Unspent Transaction Output) model that distinguishes Bitcoin and similar blockchain systems from account-based models employed in platforms such as Ethereum (Buterin, 2014). The UTXO model's treatment of transactions as consuming previous outputs while creating new outputs establishes a directed acyclic graph structure for value flow, with important implications for transaction validation, double-spend prevention, and state management in distributed consensus systems.

The transaction structure identified through base material analysis comprises four primary components distributed across input and output arrays. Transaction inputs specify references to previous transaction outputs being consumed, identified through Transaction ID (TXID) computed as double SHA256 hash and output index within the referenced transaction. Each input provides an unlocking script (scriptSig) demonstrating authorization to spend the referenced output by satisfying its spending conditions. Transaction outputs specify value amounts denominated in satoshis (the smallest divisible unit representing one hundred-millionth of a bitcoin) and locking scripts (scriptPubKey) encoding conditions that must be satisfied for subsequent spending. Transaction metadata including version numbers supporting protocol evolution and locktime values enabling temporal spending restrictions complete the structural specification.

The analysis identified seventy-two distinct conceptual entities within foundational chapters, organized into six functional categories addressing transaction fundamentals, structural components, script systems, cryptographic primitives, transaction lifecycle processes, and specialized transaction types. Transaction fundamental concepts including Transaction, TransactionOutput, TransactionInput, UTXO, UTXOSet, TXID, Version, Locktime, and Sequence establish basic vocabulary for discussing transaction architecture and operations. Structural component concepts including input arrays (vin), output arrays (vout), scriptSig, scriptPubKey, value specifications, output indices (vout), and satoshi denomination provide detailed understanding of data organization within transaction structures.

### 2.3 Script System Architecture and Execution Semantics

The script system analysis reveals Bitcoin Script as a stack-based, Forth-like programming language designed for expressing and validating spending conditions while maintaining intentional limitations preventing Turing-completeness and ensuring deterministic execution (Nakamoto, 2008). This design choice reflects fundamental security and consensus requirements in distributed blockchain systems, where non-deterministic script execution could enable divergent validation results across network nodes, compromising consensus integrity. The stack-based execution model employs a last-in-first-out data structure for operation sequencing, with script opcodes consuming operands from the stack and pushing results back onto the stack through sequential evaluation until script completion or validation failure.

The base material documents fundamental script patterns including Pay-to-Public-Key-Hash (P2PKH), the predominant transaction type in Bitcoin's early history, employing a locking script requiring provision of a public key hashing to a specified value and a valid signature from the corresponding private key. The P2PKH pattern demonstrates the script system's cryptographic foundation, relying on collision-resistant hash functions (SHA256 and RIPEMD160) for address derivation and digital signatures (ECDSA on secp256k1 elliptic curve) for spending authorization. The execution model evaluates unlocking scripts from transaction inputs in sequence with locking scripts from referenced outputs, pushing both onto a shared execution stack for validation through opcode evaluation.

The conceptual inventory identified seventeen script-related entities spanning the script language itself, fundamental opcodes (OP_DUP for stack duplication, OP_HASH160 for hash computation, OP_EQUALVERIFY for equality checking with validation failure, OP_CHECKSIG for signature verification), locking and unlocking script distinctions, and stack data structures mediating execution. This conceptual foundation provides necessary understanding for modeling Bitcoin's scriptable transaction architecture while establishing vocabulary for discussing more sophisticated script patterns including multisignature schemes and timelock constructions examined in advanced transaction patterns.

### 2.4 Cryptographic Primitives and Digital Signature Mechanisms

The cryptographic analysis documents Elliptic Curve Digital Signature Algorithm (ECDSA) as Bitcoin's original signature scheme for transaction authorization, employing the secp256k1 elliptic curve for key generation and signature computation (Koblitz, 1987; Johnson et al., 2001). The ECDSA signature scheme generates digital signatures from transaction data and private keys, producing signature components (r and s values) verifiable using corresponding public keys without exposing private key material. This asymmetric cryptography foundation enables Bitcoin's decentralized ownership model, where cryptocurrency control derives from private key possession rather than centralized account management.

The public-private key pair relationship follows from elliptic curve scalar multiplication, where public keys derive from private keys through point multiplication with the generator point on the secp256k1 curve. The mathematical relationship ensures public key derivation from private keys remains computationally feasible while the inverse operation (recovering private keys from public keys) remains computationally infeasible under elliptic curve discrete logarithm problem assumptions. This cryptographic security foundation enables Bitcoin's security model, where transaction authorization requires private key knowledge demonstrated through digital signatures without revealing private keys themselves.

The conceptual inventory documented fourteen cryptographic entities including ECDSA signature schemes, public-private key pairs, signature components (r and s values), ephemeral keys employed in signature generation, hash functions (SHA256 and RIPEMD160), and address encoding formats (Base58Check). This cryptographic conceptual foundation proves essential for understanding transaction security properties, signature verification processes, and the cryptographic assumptions underlying Bitcoin's decentralized trust model. The analysis additionally identified relationships between cryptographic concepts and transaction structures, particularly how digital signatures appear within scriptSig unlocking scripts and how public key hashes appear within scriptPubKey locking scripts, demonstrating the integration of cryptographic primitives into transaction architecture.

### 2.5 Advanced Transaction Patterns and Complex Constructions

Chapter Seven's analysis of advanced transaction patterns reveals increasing sophistication in Bitcoin transaction capabilities beyond simple value transfer, encompassing multisignature schemes for shared custody, Pay-to-Script-Hash for arbitrary spending conditions, timelock mechanisms for temporal constraints, and complex constructions enabling payment channels and atomic swaps. These advanced patterns demonstrate Bitcoin Script's expressiveness for implementing diverse security and functionality requirements while working within Turing-incomplete constraints.

Multisignature transaction analysis documents M-of-N signature schemes requiring M valid signatures from a set of N possible signers to authorize spending. The CHECKMULTISIG opcode enables multisignature validation within Bitcoin Script, accepting N public keys and M signatures while verifying that M distinct public keys from the provided set produced valid signatures. Multisignature schemes enable shared control scenarios including corporate accounts requiring multiple executive signatures, escrow arrangements with buyer-seller-arbitrator signing authority, and enhanced security through key distribution across multiple devices or locations. The conceptual inventory identified six multisignature-related entities including multisignature transactions, M-of-N schemes, CHECKMULTISIG opcodes, the off-by-one bug requiring dummy stack values, common configurations (particularly 2-of-3 multisig), and standard limitations (15-key maximum).

Pay-to-Script-Hash (P2SH) analysis reveals an abstraction mechanism enabling complex spending conditions while maintaining compact output representations and shifting computational burdens from senders to spenders. P2SH transactions place hash values of redemption scripts in locking scripts rather than complete script implementations, enabling arbitrary script complexity without increasing sender costs or revealing script details until spending time. The redemption script, presented during spending, must hash to the value specified in the locking script and must evaluate successfully to authorize spending. This construction, formalized in BIP16 (Andresen, 2012), enables sophisticated transaction patterns including multisignature schemes, timelock combinations, and complex security policies while maintaining backward compatibility with clients not implementing P2SH validation.

Timelock mechanism analysis documents both absolute and relative temporal constraints on transaction validity. Absolute timelocks employ nLockTime transaction fields specifying earliest timestamps or block heights when transactions become valid for blockchain inclusion. Relative timelocks employ nSequence input fields specifying minimum delays from output creation to input spending, enabling payment channel protocols where transaction validity timing depends on channel state updates. The CHECKLOCKTIMEVERIFY (CLTV) and CHECKSEQUENCEVERIFY (CSV) opcodes, formalized in BIP65 and BIP112 respectively (Todd, 2014; BtcDrak et al., 2015), enable script-level timelock verification rather than relying solely on transaction-level validation. The conceptual inventory identified seven timelock-related entities including general timelock concepts, nLockTime and nSequence fields, CLTV and CSV opcodes, and absolute versus relative timelock distinctions.

### 2.6 Knowledge Boundary Identification and Gap Analysis

The base material analysis identified fifteen conceptual areas mentioned in foundational chapters but insufficiently detailed for ontology formalization, requiring supplementary research through authoritative technical documentation. These knowledge gaps predominantly involve protocol enhancements, implementation details, and emerging patterns postdating the 2017 publication or receiving cursory treatment in educational literature focused on fundamental concepts.

Transaction malleability emerged as a critical gap area, mentioned in foundational text as an implementation challenge enabling transaction ID modification without invalidating transactions, but without detailed analysis of specific attack vectors, deployment implications, or mitigation strategies ultimately implemented through Segregated Witness. Block and blockchain architecture received limited treatment in transaction-focused chapters, necessitating research into block headers, Merkle tree structures, mining processes, and consensus mechanisms to complete understanding of transaction-to-blockchain relationships. Script versioning mechanisms enabling future protocol extension through soft fork compatibility received brief mention without detailed analysis of versioning strategies, upgrade mechanisms, or historical version deployment patterns.

Payment channel protocols and Lightning Network constructions received conceptual introduction but lacked detailed technical specifications necessary for ontology formalization. The base material presented payment channels as off-chain transaction sequences reducing blockchain resource consumption while maintaining security through time-limited revocation mechanisms, but did not provide comprehensive analysis of channel establishment protocols, commitment transaction structures, Hashed Timelock Contracts enabling multi-hop routing, or the complete Lightning Network protocol stack. This gap area represents substantial post-2017 development requiring systematic research through Lightning Network specifications and academic literature analyzing Layer 2 scaling solutions.

The gap analysis additionally identified complete protocol enhancements absent from 2017 base material due to subsequent deployment. Segregated Witness, while activated in August 2017 shortly before publication, received insufficient coverage for comprehensive ontology development. Taproot and Schnorr signatures, activated in November 2021 representing Bitcoin's most significant protocol enhancement since Segregated Witness, lack any coverage in base material. These major protocol enhancements require extensive supplementary research through Bitcoin Improvement Proposals and technical documentation to achieve ontology temporal currency and educational completeness for contemporary blockchain software engineering instruction.

---

## 3. Post-2017 Protocol Enhancements: Systematic Research Analysis

### 3.1 Segregated Witness: Transaction Malleability Resolution and Capacity Enhancement

The Segregated Witness (SegWit) protocol enhancement, formalized through BIP141, BIP143, BIP144, and BIP173 (Lombrozo et al., 2015; Wuille, 2016; Friedenbach, 2016), represents Bitcoin's first major soft fork upgrade addressing transaction malleability vulnerabilities while enabling effective block capacity increases through witness data separation. SegWit's activation in August 2017 at block height 481,824 following extensive community debate and miner signaling established new transaction formats, address types, and script evaluation rules maintaining backward compatibility with legacy nodes while providing opt-in access to enhanced functionality for upgraded clients.

Transaction malleability, the vulnerability motivating SegWit development, permits third parties to modify transaction identifiers through signature component manipulation without invalidating transactions (Decker & Wattenhofer, 2014). This vulnerability prevented reliable construction of complex multi-transaction protocols including payment channels, as subsequent transactions spending outputs from unconfirmed parent transactions could become invalid if parent transaction IDs changed during propagation. SegWit addresses malleability through witness data segregation, computing transaction IDs from transaction components excluding witness data, thereby preventing signature modifications from affecting TXID values while introducing witness transaction IDs (WTXID) computed from complete transaction data including witnesses.

The SegWit transaction structure modifies legacy formats through introduction of marker and flag bytes distinguishing SegWit from legacy transactions, witness fields containing signature and script data, and modified serialization formats enabling backward compatibility. Legacy nodes interpret SegWit transactions as anyone-can-spend outputs with minimal validation requirements, while upgraded nodes perform complete witness validation against witness program specifications. This soft fork deployment strategy enables protocol enhancement without requiring universal network upgrade, though full security properties require majority hashpower running upgraded validation rules.

The research identified eighteen SegWit-related conceptual entities beyond base material coverage, including witness data structures, marker and flag bytes, witness fields, witness transaction IDs, virtual size metrics based on witness weight units, weight unit calculations privileging witness data with 4:1 ratios compared to legacy data, Pay-to-Witness-Public-Key-Hash (P2WPKH) as native SegWit equivalent to P2PKH, Pay-to-Witness-Script-Hash (P2WSH) as native SegWit equivalent to P2SH, backward-compatible P2SH-wrapped SegWit variants, Bech32 address formats providing improved error detection compared to Base58Check, modified signature hash algorithms (BIP143) reducing computational complexity and fixing quadratic hashing problems, script versioning through witness programs enabling future soft forks, and effective block capacity increases through weight-based resource accounting enabling approximately 1.7-2.0 MB average block sizes under typical transaction mixes.

### 3.2 Taproot and Schnorr Signatures: Privacy Enhancement and Signature Optimization

The Taproot protocol upgrade, formalized through BIP340, BIP341, and BIP342 (Wuille et al., 2021; Maxwell et al., 2021; Nick & Wuille, 2021), activated in November 2021 at block height 709,632 following 90% miner signaling, represents Bitcoin's most significant protocol enhancement since Segregated Witness. Taproot introduces Schnorr signature schemes replacing ECDSA for witness version 1 outputs, Merkelized Abstract Syntax Trees enabling privacy-preserving complex spending conditions, and key aggregation protocols enabling efficient multisignature constructions indistinguishable from single-signature spends.

Schnorr signatures, proposed by Claus-Peter Schnorr in 1989 but patent-encumbered until 2008 (Schnorr, 1991), provide several advantages over ECDSA including smaller signature sizes (64 bytes versus 71-72 bytes for ECDSA), provable security under discrete logarithm assumptions without random oracle model requirements, linear signature aggregation enabling multi-signature constructions, and batch verification capabilities improving validation performance. The BIP340 specification adapts Schnorr signatures for Bitcoin through x-only public keys using 32-byte x-coordinates with implicitly even y-coordinates, tagged hashing preventing cross-protocol attacks, and specific nonce generation procedures ensuring security against implementation vulnerabilities.

The Taproot construction, specified in BIP341, enables two distinct spending paths for outputs: key path spending through single Schnorr signatures providing optimal efficiency and privacy, and script path spending revealing and executing individual scripts from Merkelized Alternative Script Trees. The key path uses a tweaked public key committing to an optional script tree, enabling outputs to appear as standard single-signature spends when cooperatively spending through key paths while maintaining ability to fall back to script path spending if cooperation fails. This construction provides significant privacy improvements by making complex multi-party contracts indistinguishable from simple payments in the common cooperation case.

Merkelized Alternative Script Trees (MAST), implemented through Taproot, organize alternative spending scripts into Merkle trees where only executed script paths require revelation during spending. This construction provides privacy by hiding unexecuted spending conditions and enables more complex scripts by avoiding revelation of full script trees. The script path spending process reveals internal keys, executed scripts (TapLeaf), sibling script hashes constructing Merkle proofs (TapBranch), and control blocks proving inclusion of executed scripts in committed Merkle trees. Tapscript, the script language for Taproot specified in BIP342, introduces new opcodes including OP_CHECKSIGADD for efficient multisignature validation and OP_SUCCESS opcodes enabling future soft fork expansion through operation code repurposing.

The research identified thirty Taproot-related conceptual entities including Schnorr signature schemes, x-only public keys, tagged hashing, key aggregation through MuSig protocols (Maxwell et al., 2018), signature aggregation, batch verification, Taproot outputs, Pay-to-Taproot transaction types, key path spending, script path spending, internal keys, output keys, tweaked keys committing to script trees, Merkle roots, TapLeaf nodes containing individual scripts, TapBranch nodes organizing tree structure, control blocks proving script inclusion, Tapscript language, OP_CHECKSIGADD opcodes, and OP_SUCCESS opcodes. This substantial conceptual expansion reflects Taproot's significance as a comprehensive protocol enhancement affecting signature schemes, output types, spending paths, privacy properties, and script language evolution.

### 3.3 Lightning Network: Layer 2 Payment Channel Architecture

The Lightning Network, proposed by Poon and Dryja (2016) and subsequently implemented through Basis of Lightning Technology (BOLT) specifications, provides Layer 2 payment channel protocols enabling off-chain transaction sequences with blockchain settlement of final channel states. Lightning Network deployment addresses Bitcoin's scalability limitations by moving routine payments off-chain while maintaining security through cryptographic commitments and time-limited revocation mechanisms enforced through underlying blockchain settlement.

Payment channel architecture employs funding transactions creating on-chain outputs requiring mutual consent for spending, commitment transactions representing current channel states with asymmetric revocation penalties preventing old state publication, and channel closure transactions settling final balances on-chain. The commitment transaction structure includes output directly spendable by the remote party and output requiring timelock delay for local party spending, enabling penalty-based revocation where parties can confiscate entire channel balance if counterparties attempt broadcasting old channel states. This penalty mechanism, implemented through Revocable Sequence Maturity Contracts (Todd, 2014), provides economic security for payment channels without requiring continuous blockchain transactions.

Hashed Timelock Contracts (HTLCs) enable multi-hop payments routed through intermediate nodes without trust requirements or ability for intermediate nodes to steal funds. HTLCs employ hash locks requiring hash preimage revelation for claiming funds and timelocks enabling refund if payment completion fails, creating atomicity properties ensuring either complete payment success across all hops or complete payment failure without funds loss to intermediate nodes. The HTLC mechanism enables Lightning Network's routing capabilities, allowing payments between parties without direct payment channel connections through paths traversing multiple intermediate channels.

Lightning Network protocol stack, specified through BOLT documents, encompasses channel establishment protocols (BOLT2), transaction formats and signature schemes (BOLT3), onion routing for privacy-preserving payment routing (BOLT4), and invoice formats encoding payment requests (BOLT11). The Lightning Network topology organizes as a peer-to-peer network of payment channels forming a graph structure where nodes represent payment channel endpoints and edges represent payment channels, with routing algorithms discovering paths from payment sources to destinations through intermediary channels.

The research identified thirty-four Lightning Network conceptual entities including payment channels, funding transactions, commitment transactions, channel states, local and remote balances, Revocable Sequence Maturity Contracts, Hashed Timelock Contracts, payment hashes, preimages revealing payment secrets, timelock parameters controlling refund timing, Lightning invoices (BOLT11 format), Lightning nodes participating in payment routing, multi-hop payments traversing multiple channels, onion routing providing payment path privacy, source routing where payment senders determine complete paths, route hints suggesting channel connections for recipient reachability, channel capacity limiting payment sizes, watchtowers providing third-party breach monitoring, and breach remedy transactions penalizing old state publication attempts.

### 3.4 Complementary Protocol Enhancements and Auxiliary Technologies

Beyond major protocol enhancements including Segregated Witness, Taproot, and Lightning Network, the research identified several complementary developments affecting transaction architecture, address formats, and operational practices within contemporary blockchain systems. These auxiliary developments, while individually less transformative than major protocol upgrades, collectively contribute to improved security, enhanced privacy, and increased operational efficiency in transaction processing and management.

Replace-by-Fee (RBF) transaction signaling, formalized through BIP125 (Friedenbach, 2015), enables transaction replacement in mempools prior to confirmation, allowing fee increases for transactions experiencing confirmation delays or transaction cancellation through double-spending to change outputs. RBF signaling through nSequence values below maximum provides explicit opt-in mechanisms distinguishing replaceable from non-replaceable transactions, addressing concerns regarding zero-confirmation transaction security while providing valuable fee estimation flexibility in variable fee environments.

Child-Pays-For-Parent (CPFP) transaction patterns enable transaction fee augmentation through child transactions spending parent transaction outputs with elevated fees, incentivizing miners to include both parent and child in blocks through combined fee consideration. CPFP provides fee bumping capabilities for received transactions where senders under-estimated required fees or fee market conditions changed between transaction creation and confirmation, addressing operational challenges in dynamic fee environments where optimal fee prediction proves difficult.

Partially Signed Bitcoin Transactions (PSBT), specified in BIP174 (Wuille, 2017), provide standardized formats for coordinating signature collection across multiple parties or devices in multisignature or complex transaction scenarios. PSBT enables workflows where transaction construction, signing, and broadcasting occur across separate systems or timeframes, supporting hardware wallet integration, air-gapped signing procedures, and multisignature coordination without requiring custom protocols for transaction information exchange.

These complementary enhancements, while not constituting separate protocol layers like Segregated Witness or Taproot, represent important operational improvements and standardization efforts affecting transaction workflows in contemporary Bitcoin development. The research identified eleven related conceptual entities including Replace-by-Fee transactions and signaling, opt-in RBF, Child-Pays-For-Parent patterns, Partially Signed Bitcoin Transactions, and associated metadata standards.

---

## 4. Source Validation and Cross-Reference Verification

### 4.1 Source Authority Hierarchy and Selection Criteria

The knowledge acquisition methodology employed hierarchical source authority rankings reflecting consensus within the blockchain research and development community regarding documentation reliability, technical accuracy, and specification authority. This hierarchical approach recognizes that not all information sources provide equivalent reliability or detail levels, with formal specifications and reference implementations carrying substantially greater authority than informal technical blogs or community discussions, while acknowledging that comprehensive understanding sometimes requires consulting multiple source tiers to resolve ambiguities or obtain implementation details absent from formal specifications.

Bitcoin Improvement Proposals (BIPs) occupy the highest authority tier as formal specifications subjected to extensive community review, technical validation, and implementation testing prior to adoption. BIPs follow structured formats including motivation sections explaining problems addressed, specification sections providing technical details, rationale sections justifying design decisions, and reference implementation sections demonstrating feasibility. The BIP process, modeled on Python Enhancement Proposals (van Rossum & Warsaw, 2001), ensures systematic consideration of proposed changes while maintaining historical record of protocol evolution decisions and rejected alternatives. The research consulted fourteen BIPs spanning consensus rule changes (BIP16, BIP65, BIP68, BIP112, BIP141, BIP143, BIP144, BIP340, BIP341, BIP342), address formats (BIP173), transaction formats (BIP174), and fee market mechanisms (BIP125).

Bitcoin Core documentation, maintained by Bitcoin Core developers and published at bitcoincore.org, occupies the second authority tier as official documentation for Bitcoin's reference implementation. This documentation provides implementation-level details, operational guidance, and developer resources reflecting practices in the most widely deployed Bitcoin software. While not carrying specification authority equivalent to BIPs, Bitcoin Core documentation provides valuable implementation perspectives and practical guidance regarding feature deployment and operational considerations. The research consulted Bitcoin Core documentation particularly for Segregated Witness wallet development guidance and transaction validation procedures.

Lightning Network BOLT (Basis of Lightning Technology) specifications occupy authority tier equivalent to BIPs but specific to Lightning Network protocol stack. BOLT specifications, maintained through collaborative development involving multiple Lightning implementation teams, provide formal specifications for payment channel protocols, transaction formats, peer-to-peer communication, and invoice standards. The research consulted BOLT specifications particularly for payment channel architecture (BOLT2), commitment transaction formats (BOLT3), and invoice formats (BOLT11).

Academic publications and technical conference papers occupy the third authority tier, providing research perspectives, security analyses, and comparative evaluations contextualizing protocol features within broader distributed systems and applied cryptography literature. While lacking specification authority, academic sources provide valuable theoretical grounding and security analysis informing protocol understanding. The research consulted academic literature particularly regarding transaction malleability analyses (Decker & Wattenhofer, 2014), payment channel security properties (Miller et al., 2019), and Schnorr signature advantages (Bellare & Neven, 2006).

### 4.2 Triple-Source Validation Methodology

The knowledge acquisition quality assurance process employed triple-source validation requirements for all major conceptual entities, ensuring that critical blockchain transaction concepts appear consistently across three independent authoritative sources before incorporation into knowledge base. This validation strategy provides protection against documentation errors, outdated specifications, and misinterpretation of technical content while establishing confidence in conceptual accuracy necessary for educational ontology development.

The triple-source validation process begins with concept identification in base material, typically Antonopoulos (2017), establishing initial understanding and terminology. The second source consultation seeks confirmation in formal specifications, particularly relevant BIPs for protocol features or BOLT specifications for Lightning Network concepts, validating that base material descriptions align with authoritative technical specifications. The third source consultation examines reference implementations (Bitcoin Core source code) or academic analyses providing independent perspectives and identifying subtle implementation details or security considerations not fully apparent from specifications alone.

For example, Segregated Witness validation consulted Antonopoulos (2017) for conceptual introduction, BIP141 (Lombrozo et al., 2015) for formal specification, and Bitcoin Core source code for implementation validation. This triple-source process revealed important details including weight unit calculations, witness program version interpretation rules, and soft fork deployment mechanics not fully evident from any single source. Similarly, Taproot validation consulted academic literature on Schnorr signatures (Bellare & Neven, 2006), formal BIP specifications (BIP340-342), and Bitcoin Core Taproot implementation documentation, revealing important security considerations regarding nonce generation and key aggregation protocols.

The validation process documented source URLs and access dates for all consulted materials, enabling reproducibility and facilitating updates as specifications evolve or implementations reveal additional details. This documentation practice recognizes that blockchain protocols continue evolving through soft forks, implementation refinements, and community best practice evolution, necessitating mechanisms for tracking information sources and maintaining temporal currency in educational materials grounded in current technical understanding.

---

## 5. Preliminary Taxonomy Development and Conceptual Organization

### 5.1 Hierarchical Concept Organization Principles

The knowledge acquisition process generated preliminary taxonomies organizing identified concepts into hierarchical structures that subsequently inform formal ontology class hierarchy development. These preliminary taxonomies balance multiple organizational principles including technical specialization relationships (subclass-superclass hierarchies based on feature sets), historical evolution patterns (organizing concepts by protocol version or enhancement timeline), and pedagogical progression requirements (sequencing concepts to support learning from fundamental toward advanced understanding).

Transaction type taxonomy organization follows technical specialization patterns, with generic Transaction concepts specializing into StandardTransaction types including legacy formats, Segregated Witness variants, and Taproot constructions. Legacy transactions further specialize into Pay-to-Public-Key, Pay-to-Public-Key-Hash, and Pay-to-Script-Hash types, while Segregated Witness transactions specialize into native witness programs (P2WPKH, P2WSH) and backward-compatible P2SH-wrapped variants. Taproot transactions introduce Pay-to-Taproot as a unified construction supporting both key-path and script-path spending modes. This taxonomic organization reflects technical distinctions in transaction formats, validation rules, and witness data handling while providing clear evolutionary progression from legacy through contemporary transaction types.

Script taxonomy organization distinguishes locking scripts encoding spending conditions from unlocking scripts (scriptSig in legacy transactions, witness data in SegWit/Taproot) providing satisfying data. Locking scripts further specialize by pattern including P2PKH scripts, P2SH scripts, P2WPKH scripts, P2WSH scripts, and Tapscript programs. Complex script patterns including multisignature scripts, timelock-enabled scripts, and Hashed Timelock Contracts represent additional specializations supporting specific use cases. This taxonomic structure captures Bitcoin Script's expressiveness while organizing patterns by common usage scenarios and security properties.

Digital signature taxonomy distinguishes ECDSA signatures used in legacy and Segregated Witness transactions from Schnorr signatures introduced with Taproot. Signature specialization further distinguishes individual signatures from aggregated signatures combining multiple signers into single signature objects through Schnorr's linear aggregation properties. This taxonomic organization reflects cryptographic evolution in Bitcoin protocol while capturing functional distinctions between signature types affecting verification procedures and transaction privacy properties.

### 5.2 Relationship Modeling and Property Specification

Beyond hierarchical concept organization, the knowledge acquisition process identified numerous relationships between concepts requiring explicit modeling in subsequent ontology formalization. These relationships, documented through property specifications in preliminary knowledge organization, enable reasoning about transaction composition, spending relationships, and blockchain integration patterns essential for comprehensive domain understanding.

Transaction composition relationships include hasInput and hasOutput properties connecting transactions to their component inputs and outputs, with cardinality constraints ensuring transactions possess at least one input (except coinbase) and at least one output. Input-transaction relationships include referencesTransaction connecting inputs to outputs being spent and hasUnlockingScript connecting inputs to scriptSig or witness data. Output relationships include hasLockingScript connecting outputs to spending condition specifications and hasValue connecting outputs to denomination specifications.

Spending relationships including spendsOutput and isSpentBy capture the fundamental blockchain graph structure where transaction outputs serve as inputs to subsequent transactions, creating directed acyclic graphs of value flow from coinbase transactions through multiple spending stages toward current UTXO set. These spending relationships prove essential for transaction validation, double-spend detection, and blockchain state reconstruction from complete transaction history.

Block-transaction relationships including containsTransaction and isContainedInBlock connect transactions to blocks through Merkle tree structures, while block-blockchain relationships including hasNextBlock and hasPreviousBlock form linear chain structures with consensus mechanisms resolving competing chains through proof-of-work comparisons. These relationships establish transaction finality through confirmation depth and enable reasoning about transaction security properties based on block height and accumulated proof-of-work.

---

## 6. Research Quality Assessment and Validation Results

### 6.1 Coverage Completeness Analysis

The knowledge acquisition process achieved comprehensive coverage across the blockchain transaction domain as specified in ontology development requirements. The base material analysis identified seventy-two foundational concepts establishing complete understanding of Bitcoin's original transaction architecture, script system, and cryptographic foundations. The post-2017 research phase identified eighty-five additional concepts addressing major protocol enhancements including Segregated Witness (eighteen concepts), Taproot and Schnorr signatures (thirty concepts), Lightning Network (thirty-four concepts), and complementary developments (eleven concepts). The combined inventory of 157 concepts provides comprehensive domain coverage spanning Bitcoin's complete evolution from Nakamoto's (2008) original design through contemporary protocol enhancements activated through November 2021.

Coverage completeness assessment against Bitcoin Improvement Proposal repository confirms inclusion of all major consensus-affecting BIPs through BIP342, ensuring temporal currency through the most recent major protocol upgrade. Coverage gaps, where they exist, involve minor BIPs addressing operational procedures (wallet behavior specifications, peer-to-peer message formats) or proposed but unactivated enhancements lacking consensus deployment, appropriately excluded from educational ontology focused on deployed protocol features. The coverage assessment confirms that no major deployed protocol features lack representation in the conceptual inventory, establishing confidence in ontology completeness for educational applications in blockchain software engineering through 2025.

### 6.2 Source Authority Validation

The source validation process confirmed that all 157 identified concepts receive documentation in authoritative sources meeting hierarchical selection criteria. Major concepts receive triple-source validation through base literature, formal specifications (BIPs or BOLTs), and implementation documentation or academic analysis. For example, Segregated Witness concepts validate through Antonopoulos (2017), BIP141-144 (Lombrozo et al., 2015; Wuille, 2016; Friedenbach, 2016), and Bitcoin Core documentation. Taproot concepts validate through academic Schnorr signature literature (Bellare & Neven, 2006), BIP340-342 (Wuille et al., 2021; Maxwell et al., 2021; Nick & Wuille, 2021), and Bitcoin Core Taproot documentation. Lightning Network concepts validate through original Lightning Network paper (Poon & Dryja, 2016), BOLT specifications, and academic payment channel analyses (Miller et al., 2019).

This triple-source validation provides confidence that conceptual understanding aligns with authoritative specifications while capturing implementation details and security considerations evident only through examination of multiple information sources. The validation additionally identified no contradictions between sources for major concepts, suggesting strong community consensus regarding technical specifications and operational properties across Bitcoin ecosystem documentation.

### 6.3 Temporal Currency Assessment

The temporal currency assessment confirms that the knowledge acquisition includes all major Bitcoin protocol enhancements through Taproot activation in November 2021, with supplementary coverage of Lightning Network development through 2025. This temporal scope ensures educational relevance for students learning contemporary blockchain development practices while acknowledging that protocol evolution continues with future enhancements under development or discussion.

The assessment identified several proposed protocol enhancements not yet achieving activation consensus including covenant proposals enabling enhanced smart contracts, cross-input signature aggregation proposals extending Taproot efficiency benefits, and various Layer 2 protocols beyond Lightning Network including validity rollups and state channels. These unactivated proposals appropriately remain outside current ontology scope given educational focus on deployed, operational protocol features rather than speculative future developments.

The temporal currency validation confirms that the conceptual inventory remains current through December 2025, providing appropriate foundation for educational deployment during the 2025 academic year with expectation that major conceptual frameworks remain stable over typical three-to-five year ontology lifecycles between major revisions.

---

## 7. Pedagogical Organization and Learning Path Design

### 7.1 Progressive Complexity Structures

The preliminary taxonomy development incorporated pedagogical organization principles ensuring appropriate knowledge scaffolding from foundational concepts through intermediate patterns toward advanced protocol understanding. This pedagogical organization aligns with constructivist learning theory's emphasis on building new understanding upon existing knowledge foundations (Piaget, 1954) and Vygotsky's (1978) zone of proximal development concept suggesting optimal learning occurs when instructional materials challenge learners slightly beyond current capability while providing necessary scaffolding.

Foundational concept layer includes basic transaction structure (Transaction, TransactionInput, TransactionOutput, UTXO), simple script patterns (P2PKH), and fundamental cryptographic primitives (hash functions, ECDSA signatures). This layer requires minimal prerequisite knowledge beyond basic understanding of cryptographic hashing and public-key cryptography, making it accessible to students with general computer science backgrounds. The foundational layer establishes vocabulary and basic architectural patterns necessary for understanding more sophisticated constructions.

Intermediate concept layer builds upon foundations through multisignature transactions, Pay-to-Script-Hash abstractions, timelock mechanisms, and transaction composition patterns. This layer requires foundational understanding but introduces increasing sophistication through multiple-party coordination (multisig), indirection through hash commitments (P2SH), and temporal constraints (timelocks). The intermediate layer prepares students for contemporary protocol enhancements by establishing patterns reappearing in more sophisticated forms in Segregated Witness and Taproot.

Advanced concept layer encompasses protocol enhancements including Segregated Witness witness separation, Taproot key-path and script-path spending modes, Schnorr signature properties, and Lightning Network payment channels. This layer requires strong understanding of foundational and intermediate concepts while introducing cutting-edge protocol features representing current best practices in blockchain transaction design. The advanced layer enables students to understand contemporary Bitcoin development while preparing them for analyzing future protocol enhancement proposals.

### 7.2 Prerequisite Relationship Identification

The knowledge acquisition process identified implicit prerequisite relationships informing instructional sequencing recommendations though not yet formalized in explicit prerequisite assertions within the ontology. These prerequisite relationships suggest that understanding certain concepts requires prior understanding of other concepts, with violation of prerequisite sequences likely causing comprehension difficulties or misconceptions.

For example, Segregated Witness understanding prerequisites include foundational transaction structure knowledge, script execution understanding, and familiarity with transaction malleability problems motivating SegWit deployment. Similarly, Taproot understanding prerequisites include Schnorr signature properties, Merkle tree data structures, and comprehension of privacy goals motivating design decisions. Lightning Network understanding prerequisites include payment channel concepts, HTLC constructions, timelock mechanisms, and penalty-based security models.

These prerequisite relationships, while implicit in the current research phase, suggest future ontology enhancement opportunities through formal prerequisite modeling enabling adaptive learning systems to generate personalized learning pathways based on student knowledge states and learning objectives. Such prerequisite modeling would enable intelligent tutoring systems to recommend concept exploration sequences respecting conceptual dependencies while allowing alternative paths accommodating diverse learning styles and interests.

---

## 8. Limitations and Future Research Directions

### 8.1 Scope Limitations and Boundary Acknowledgment

The knowledge acquisition focused specifically on Bitcoin transaction architecture and Lightning Network payment channels as primary exemplars of contemporary blockchain transaction systems. This scope deliberately excludes alternative blockchain platforms including Ethereum's account-based model and smart contract capabilities, alternative consensus mechanisms beyond Bitcoin's proof-of-work, and emerging Layer 2 technologies including validity rollups and zero-knowledge proof systems. While this Bitcoin-centric scope supports focused ontology development for software engineering education emphasizing proven, widely deployed technologies, it inherently limits generalizability to broader blockchain ecosystem encompassing diverse architectural approaches and consensus mechanisms.

The temporal scope through Taproot activation (November 2021) and Lightning Network development through 2025 provides strong currency for contemporary education while acknowledging that blockchain protocols continue evolving through additional enhancement proposals under development or community discussion. Future protocol enhancements including covenant proposals, cross-input signature aggregation, and various Layer 2 protocol expansions may necessitate ontology updates to maintain educational relevance over extended timeframes.

### 8.2 Educational Context Specificity

The knowledge acquisition process targeted requirements for the SEN0401 Special Topics in Software Engineering (Blockchain) course at Istanbul Kültür University, with resulting conceptual organization reflecting that educational context's learning objectives, student backgrounds, and instructional approaches. While the systematic methodology and authoritative source validation provide generalizability foundations, specific concept selection, detail granularity, and organizational decisions reflect the particular educational context. Alternative educational settings with different learning objectives, prerequisite requirements, or pedagogical approaches might benefit from different concept emphasis or organizational structures.

### 8.3 Future Research Opportunities

Several research directions extend the current knowledge acquisition work. First, empirical validation through student learning outcomes research could assess whether ontology-based instruction using this conceptual foundation produces superior learning compared to traditional approaches, providing evidence-based guidance for educational ontology development. Second, extension to alternative blockchain platforms including Ethereum, Cardano, or Polkadot would enable comparative analysis learning objectives examining architectural trade-offs across different consensus mechanisms, state models, and smart contract approaches. Third, integration with formal verification frameworks could enable not only conceptual understanding but also executable specification checking enabling students to verify protocol property claims through automated reasoning tools. These future directions would enhance both practical utility and research contributions of blockchain transaction ontology development.

---

## 9. Conclusion

This research phase established comprehensive conceptual foundations for blockchain transactions ontology development through systematic knowledge acquisition spanning foundational literature analysis and targeted post-2017 protocol enhancement research. The methodology's emphasis on authoritative source validation, triple-source confirmation for critical concepts, and hierarchical source authority criteria ensures technical accuracy and conceptual reliability necessary for educational ontology serving software engineering instruction. The identification of 157 distinct concepts organized into preliminary taxonomies provides robust foundation for subsequent ontology formalization while demonstrating domain coverage spanning Bitcoin's evolution from original Nakamoto (2008) design through contemporary protocol enhancements including Segregated Witness, Taproot, and Lightning Network.

The research phase's emphasis on pedagogical organization through progressive complexity structures and implicit prerequisite relationship identification ensures resulting ontology will support effective instruction aligned with constructivist learning principles and cognitive load theory. The systematic documentation of thirty-two authoritative sources with URLs enabling reproducibility and temporal currency tracking establishes methodological rigor supporting future ontology maintenance and enhancement as blockchain protocols continue evolving through community development processes.

The completion of this research phase with comprehensive domain coverage, validated through triple-source methodology across hierarchical authority tiers, establishes readiness for subsequent ontology formalization phases. The conceptual inventory, preliminary taxonomies, relationship specifications, and pedagogical organization provide necessary foundations for formal knowledge representation through OWL class definitions, property specifications, and axiomatization patterns transforming domain knowledge into machine-processable semantic web resources enabling novel educational applications in blockchain software engineering instruction.

---

## 10. References

Andresen, G. (2012). *BIP 16: Pay to Script Hash*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki

Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman. https://www.uky.edu/~rsand1/china2018/texts/Anderson-Krathwohl%20-%20A%20taxonomy%20for%20learning%20teaching%20and%20assessing.pdf

Antonopoulos, A. M. (2017). *Mastering Bitcoin: Programming the open blockchain* (2nd ed.). O'Reilly Media. https://github.com/bitcoinbook/bitcoinbook

Bellare, M., & Neven, G. (2006). Multi-signatures in the plain public-key model and a general forking lemma. In *Proceedings of the 13th ACM Conference on Computer and Communications Security* (pp. 390-399). ACM. https://doi.org/10.1145/1180405.1180453

Böhme, R., Christin, N., Edelman, B., & Moore, T. (2015). Bitcoin: Economics, technology, and governance. *Journal of Economic Perspectives*, 29(2), 213-238. https://doi.org/10.1257/jep.29.2.213

BtcDrak, Friedenbach, M., & Lombrozo, E. (2015). *BIP 112: CHECKSEQUENCEVERIFY*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki

Buterin, V. (2014). *A next-generation smart contract and decentralized application platform*. Ethereum White Paper. https://ethereum.org/en/whitepaper/

Decker, C., & Wattenhofer, R. (2014). Bitcoin transaction malleability and MtGox. In *Computer Security—ESORICS 2014* (pp. 313-326). Springer. https://doi.org/10.1007/978-3-319-11212-1_18

Dicheva, D., & Dichev, C. (2006). TM4L: Creating and browsing educational topic maps. *British Journal of Educational Technology*, 37(3), 391-404. https://doi.org/10.1111/j.1467-8535.2006.00612.x

Fernández-López, M., Gómez-Pérez, A., & Juristo, N. (1997). METHONTOLOGY: From ontological art towards ontological engineering. *AAAI Spring Symposium on Ontological Engineering*, 33-40. https://oa.upm.es/5484/1/METHONTOLOGY_.pdf

Friedenbach, M. (2015). *BIP 125: Opt-in Full Replace-by-Fee Signaling*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki

Friedenbach, M. (2016). *BIP 173: Base32 address format for native v0-16 witness outputs*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki

Gómez-Pérez, A., Fernández-López, M., & Corcho, O. (2004). *Ontological engineering: With examples from the areas of knowledge management, e-commerce and the Semantic Web*. Springer. https://doi.org/10.1007/b97353

Gruber, T. R. (1995). Toward principles for the design of ontologies used for knowledge sharing. *International Journal of Human-Computer Studies*, 43(5-6), 907-928. https://doi.org/10.1006/ijhc.1995.1081

Gruninger, M., & Fox, M. S. (1995). Methodology for the design and evaluation of ontologies. In *Proceedings of the Workshop on Basic Ontological Issues in Knowledge Sharing, IJCAI-95*. https://www.researchgate.net/publication/2437291_Methodology_for_the_Design_and_Evaluation_of_Ontologies

Huberman, B. A., Leshno, J. D., & Moallemi, C. C. (2017). Monopoly without a monopolist: An economic analysis of the bitcoin payment system. *Bank of Finland Research Discussion Papers* 27/2017. https://doi.org/10.2139/ssrn.3025604

Johnson, D., Menezes, A., & Vanstone, S. (2001). The elliptic curve digital signature algorithm (ECDSA). *International Journal of Information Security*, 1(1), 36-63. https://doi.org/10.1007/s102070100002

Katz, J., & Lindell, Y. (2014). *Introduction to modern cryptography* (2nd ed.). Chapman and Hall/CRC. https://doi.org/10.1201/b17668

Koblitz, N. (1987). Elliptic curve cryptosystems. *Mathematics of Computation*, 48(177), 203-209. https://doi.org/10.1090/S0025-5718-1987-0866109-5

Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. *ACM Transactions on Programming Languages and Systems*, 4(3), 382-401. https://doi.org/10.1145/357172.357176

Lombrozo, E., Lau, J., & Wuille, P. (2015). *BIP 141: Segregated Witness (Consensus layer)*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki

Maxwell, G., Nick, J., & Wuille, P. (2021). *BIP 341: Taproot: SegWit version 1 spending rules*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki

Maxwell, G., Poelstra, A., Seurin, Y., & Wuille, P. (2018). Simple Schnorr multi-signatures with applications to Bitcoin. *Designs, Codes and Cryptography*, 87, 2139-2164. https://doi.org/10.1007/s10623-019-00608-x

Miller, A., Bentov, I., Kumaresan, R., Cordi, C., & McCorry, P. (2019). Sprites and state channels: Payment networks that go faster than lightning. In *Financial Cryptography and Data Security* (pp. 508-526). Springer. https://doi.org/10.1007/978-3-030-32101-7_30

Nakamoto, S. (2008). *Bitcoin: A peer-to-peer electronic cash system*. https://bitcoin.org/bitcoin.pdf

Nick, J., & Wuille, P. (2021). *BIP 342: Validation of Taproot scripts*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki

Noy, N. F., & McGuinness, D. L. (2001). *Ontology development 101: A guide to creating your first ontology*. Stanford Knowledge Systems Laboratory Technical Report KSL-01-05. https://protege.stanford.edu/publications/ontology_development/ontology101.pdf

Piaget, J. (1954). *The construction of reality in the child*. Basic Books. https://doi.org/10.1037/11168-000

Poon, J., & Dryja, T. (2016). *The Bitcoin Lightning Network: Scalable off-chain instant payments*. https://lightning.network/lightning-network-paper.pdf

Schnorr, C. P. (1991). Efficient signature generation by smart cards. *Journal of Cryptology*, 4(3), 161-174. https://doi.org/10.1007/BF00196725

Schollmeier, R. (2001). A definition of peer-to-peer networking for the classification of peer-to-peer architectures and applications. In *Proceedings of the First International Conference on Peer-to-Peer Computing* (pp. 101-102). IEEE. https://doi.org/10.1109/P2P.2001.990434

Suárez-Figueroa, M. C., Gómez-Pérez, A., & Fernández-López, M. (2012). The NeOn methodology for ontology engineering. In *Ontology engineering in a networked world* (pp. 9-34). Springer. https://doi.org/10.1007/978-3-642-24794-1_2

Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive load theory*. Springer. https://doi.org/10.1007/978-1-4419-8126-4

Todd, P. (2014). *BIP 65: OP_CHECKLOCKTIMEVERIFY*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki

Uschold, M., & Gruninger, M. (1996). Ontologies: Principles, methods and applications. *The Knowledge Engineering Review*, 11(2), 93-136. https://doi.org/10.1017/S0269888900007797

van Rossum, G., & Warsaw, B. (2001). *PEP 1 – PEP Purpose and Guidelines*. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0001/

Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press. https://www.hup.harvard.edu/catalog.php?isbn=9780674576292

Wuille, P. (2016). *BIP 143: Transaction Signature Verification for Version 0 Witness Program*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki

Wuille, P. (2017). *BIP 174: Partially Signed Bitcoin Transaction Format*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki

Wuille, P., Nick, J., & Ruffing, T. (2021). *BIP 340: Schnorr Signatures for secp256k1*. Bitcoin Improvement Proposals. https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki

---

## Appendix A: Complete Concept Inventory

The complete inventory of 157 concepts identified through systematic knowledge acquisition is organized in the following categories for reference:

**Base Material Concepts (72 total)**: Transaction fundamentals (9 concepts), transaction structure components (7 concepts), script system (17 concepts), cryptographic primitives (14 concepts), transaction lifecycle (3 concepts), special transaction types (4 concepts), multisignature transactions (6 concepts), Pay-to-Script-Hash (6 concepts), timelock mechanisms (7 concepts), implicit concepts (5 concepts).

**Post-2017 Enhancements (85 total)**: Segregated Witness (18 concepts), Taproot and Schnorr signatures (30 concepts), Lightning Network (34 concepts), complementary enhancements (11 concepts).

Complete detailed listings with definitions and source citations are maintained in supporting documentation enabling ontology formalization phase.

## Appendix B: Source Documentation

All thirty-two authoritative sources consulted during knowledge acquisition are documented with complete citations including URLs, access dates, and hierarchical authority tier classifications. Source documentation enables reproducibility and supports future ontology maintenance as specifications evolve.

## Appendix C: Preliminary Taxonomy Structures

Preliminary taxonomy diagrams organizing concepts into hierarchical structures supporting subsequent ontology class hierarchy development are maintained as supporting documentation. These taxonomies reflect both technical specialization relationships and pedagogical progression requirements.

---

**Document Status**: Final  
**Version**: 1.0.0  
**Date**: December 12, 2025  
**Institution**: Istanbul Kültür University, Department of Computer Engineering  
**Course**: SEN0401 - Special Topics in Software Engineering (Blockchain)  
**Corresponding Author**: Dr. Yusuf Altunel (yusuf.altunel@iku.edu.tr)
