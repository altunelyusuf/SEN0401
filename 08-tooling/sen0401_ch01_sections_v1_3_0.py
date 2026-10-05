"""SEN0401 chapter 1, the renewal of version 1.3.0: the level-2 section prose, the worked examples added to leaf
concepts that had none, and the numeric claims the new prose states.

Why this module exists rather than a rewrite of the five text modules. An adversarial audit of the chapter 1 page
(version 9.28.0) found two content defects that are confined to particular concepts and leave the other prose
untouched, so the smallest honest change is a module that carries exactly the replacements:

  * Seventeen of the twenty-one level-2 sections had three paragraphs where the owner's standard is four to six, and
    the third paragraph of every level-2 section - including the four that did meet the count - was an inventory of
    the section's own children, which the breadcrumb row above the section already lists. SECTION_TAIL keeps the
    first two paragraphs of version 1.2.0 for each section, drops that inventory paragraph, and supplies three new
    paragraphs in its place, so every level-2 section reads as five paragraphs of substance.
  * Forty-eight of the ninety leaf concepts carried no executed example, and the Protocol concept's own prose
    promised an example that belonged to the HTTP concept instead. IO supplies an example for each leaf where a
    program genuinely shows the mechanism, and PARAS_REPLACE rewrites the one Protocol paragraph that described
    somebody else's example so that it describes Protocol's own.

Every expression in IO and in NUM is executed by the chapter builder before any ontology is written, under the
interpreter named in the ontology's resolution environment, and each one is restricted to the standard library and to
the files saved in 08-tooling/ch01-sources so that it also runs unchanged in the page's own Pyodide interpreter - no
pbkdf2_hmac and no RIPEMD-160, neither of which Pyodide provides.

Read by sen0401_ch01_corpus_v1_3_0.py.
"""
__version__ = "1.3.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch01_common_v1_2_0 import W, Y, E, H, K, prog as _prog, has as _has, js as _js

# ---------------------------------------------------------------------------------------------------------------------
# the three paragraphs that replace the closing inventory paragraph of every level-2 section
# ---------------------------------------------------------------------------------------------------------------------
SECTION_TAIL = {

 # ------------------------------------------------------------------ Money
 "Unit": [
  (E, "The vocabulary of this section is met before anything else in practice. A wallet that has just been installed "
      "shows a balance, and the balance is printed in one of the units fixed here; an exchange quotes a price as a pair "
      "of currencies, in which the first name is the unit being priced; a payment request carries an amount, and the "
      "amount is meaningless until the unit is known. The textbook follows the same convention in every chapter that "
      "comes after this one, writing the unit with a small letter and the system with a capital one, so a student who "
      "reads a later chapter and finds the word written one way rather than the other is being told which of the two is "
      "meant [AH]. The same convention is used in these course materials throughout."),
  (H, "The arithmetic of the section rests on one fact: the unit is divided into exactly one hundred million parts, and "
      "the smallest part, the satoshi, cannot be divided further by the protocol. Multiplying the cap of twenty-one "
      "million bitcoin by that divisor, the expression 21_000_000 * 10**8 gives 2100000000000000, so the whole supply "
      "that will ever exist is a little over two thousand one hundred million million satoshis - a number that fits "
      "comfortably in the sixty-four-bit whole-number type that the reference implementation uses for every amount it "
      "handles [BC]. Because the smallest unit is a whole number, every amount in the system is a whole number, and the "
      "decimal fractions a wallet displays are a presentation on top of integer arithmetic rather than the arithmetic "
      "itself. A conversion therefore belongs at the edge of a program, where a typed amount enters it, and nowhere "
      "else."),
  (K, "Two habits save a student from the most common errors of this section. The first is to write the unit down "
      "beside every figure, because a balance of one hundred thousand is a hundredth of a bitcoin when counted in "
      "satoshis and a hundred thousand bitcoin when counted in bitcoin, and nothing in the figure itself says which "
      "was meant. The second is to distrust any conversion that passes through an ordinary floating-point number: such "
      "numbers store a value in binary fractions and cannot hold a decimal amount exactly, so a sum that should be "
      "whole can come out a fraction of a satoshi away from it. In a classroom the error is invisible; in software "
      "that moves value it is a defect that only shows up on particular amounts, which is the worst way for a defect "
      "to show up."),
 ],

 "Supply": [
  (E, "The schedule is met wherever a figure about Bitcoin's quantity is quoted. A news report that says the reward "
      "has just been cut in half is reporting a halving; a chart of the circulating supply is drawing the running total "
      "of every subsidy paid so far; a claim that there will only ever be twenty-one million coins is quoting the "
      "limit this section computes, and quoting it slightly too generously, because the real total falls a little "
      "short of that round number. The rule itself is met in the source of the reference implementation, where one "
      "constant fixes the interval at 210,000 blocks and one function shifts the starting subsidy right once for every "
      "completed interval [BC]; the Bitcoin Wiki states the same schedule in words and gives the same total [BW]."),
  (H, "Three mechanisms produce the curve, and they operate in a fixed order. First, every block is allowed to create "
      "a quantity of new bitcoin, called the subsidy, which the miner of that block claims in its first transaction. "
      "Second, the allowance is halved at every completed interval of 210,000 blocks, which at one block every ten "
      "minutes is a little under four years: the expression round(210000 * 10 / (365.25 * 24 * 60), 2) gives 3.99 "
      "years. Third, the halving is a binary shift over a whole number of satoshis, so the allowance eventually shifts "
      "down to nothing rather than shrinking for ever, and the series ends. Adding every allowance of every block of "
      "every era therefore gives a finite total, and because each shift throws away any fraction below one satoshi, "
      "that total lands just under twenty-one million rather than exactly on it."),
  (K, "The schedule is often mistaken for a law of nature, and it is not. It is a rule in software that every "
      "participant enforces by rejecting a block that claims more than the rule allows, which means the limit holds "
      "for exactly as long as the participants keep running software that enforces it; the chapter makes the same "
      "point when it says that nobody can force you to accept bitcoins created beyond the expected issuance rate [AH]. "
      "A second confusion is between the subsidy and the miner's income. The subsidy is only the new bitcoin; the fees "
      "paid by the transactions in the block are added to it, so a miner's reward is larger than the subsidy and the "
      "two should never be quoted as the same figure."),
 ],

 "Price": [
  (E, "A price is met as a pair of names and a number, as in BTC/USD followed by a figure, and it is met in many "
      "places at once: on each exchange, in the display of a wallet that converts a balance into a local currency, in "
      "the rate a Bitcoin machine offers for cash, and in the figure a newspaper prints. None of these is the price, "
      "because there is no single market and therefore no single rate; each is a report of what some set of trades "
      "achieved over some period. The chapter meets the question practically, in Alice's purchase: before she can buy, "
      "she and her seller have to agree on a rate, and the rate they use is whatever a market they both trust was "
      "recently quoting [AH]."),
  (H, "A floating rate is produced by matching, not by announcement. Buyers post the most they will pay and sellers "
      "post the least they will accept; where the two overlap, a trade happens at a price between them, and the last "
      "such trade is what an exchange displays. Because trades differ in size as well as in price, combining several "
      "of them into one figure means weighting each price by the quantity that traded at it, which is what a "
      "volume-weighted average does: four bitcoin traded as three at one hundred and one at one hundred and four give "
      "an average of 101.0, whereas treating the two trades as equal would give 102.0. The weighted figure is the "
      "honest one, because it answers what the four bitcoin actually cost, and the unweighted one answers nothing in "
      "particular."),
  (K, "Three cautions belong here. A price is a value at a moment, so any figure quoted in teaching material is "
      "already out of date and should be read as an illustration of the arithmetic rather than as a fact about today. "
      "A price from a single market is a price in that market: a thin market can be moved by one large order, which is "
      "why a weighted average across markets is quoted instead. And a rate used to convert a balance into a local "
      "currency is not a promise that the balance can be sold at it, because selling a large quantity moves the price "
      "against the seller - the figure on the screen is the result of trades already made, not an offer for the next "
      "one."),
 ],

 "Issuance": [
  (E, "The contrast this section draws is met every time a payment crosses between the two systems. A bank transfer is "
      "settled by institutions that can delay it, reverse it or refuse it, and that are answerable for doing so; a "
      "bitcoin payment is settled by a rule that no institution applies and nobody can be asked to undo. The chapter "
      "meets the contrast at its sharpest in the section on acquiring bitcoin, where it explains that a seller of "
      "bitcoin who accepts a reversible payment carries a very high risk, which is why exchanges ask for identity and "
      "credit checks that can take days or weeks [AH]. The same contrast is met in the argument that mining "
      "decentralizes the currency-issuance and clearing functions of a central bank [AH]."),
  (H, "Where a central bank issues money by decision, Bitcoin issues it by a rule that anyone can evaluate. The "
      "decision route needs a body with a mandate, a process for taking the decision and a way of enforcing it; the "
      "rule route needs only that every participant computes the same allowance for the same block and refuses a block "
      "that exceeds it. Clearing is replaced in the same way: instead of an institution that holds both parties' "
      "accounts and moves a figure from one to the other, a block that includes the payment is accepted by everyone, "
      "and the payment is settled by that acceptance. Because the allowance shrinks to nothing after 6,930,000 blocks, "
      "the issuance side of the arrangement is temporary: at the pace of one block every ten minutes the last subsidy "
      "falls in the year 2140, after which the rule creates nothing and the fees paid by transactions are the whole of "
      "a miner's income."),
  (K, "Calling the currency deflationary needs care, because the word is used for two different things. In the "
      "monetary sense it describes a falling general level of prices, which is a property of an economy and not of a "
      "currency's issuance schedule; in the sense the chapter uses it describes an issuance that shrinks towards zero "
      "against a demand that may not, so that each unit is expected to buy more over time [AH]. The second sense is "
      "the one this section explains, and it is a statement about the schedule rather than a prediction about prices. "
      "It is also worth being exact about what is replaced: the chapter's claim is that mining takes over the "
      "issuance and clearing functions, not that it takes over supervision, consumer protection or monetary policy, "
      "none of which the system attempts."),
 ],

 # ------------------------------------------------------------------ Network
 "Consensus": [
  (E, "Consensus is met as the thing a student never sees working. A wallet that reports a payment as confirmed is "
      "reporting that the block containing it has been accepted by the network; an explorer that shows the same block "
      "identifier as every other explorer is showing that agreement held; a report that a chain was reorganised is a "
      "report of agreement being reached a second time on a different answer. It is met concretely in the ten-minute "
      "rhythm the chapter describes as a global lottery, and in the figure of six confirmations that the book's "
      "glossary gives as the point at which a payment is treated as settled [AH]."),
  (H, "The mechanism has two halves that must be held apart. The first half makes a block expensive: a miner must find "
      "a number which, placed in the block, makes the block's hash small enough, and because a hash cannot be aimed, "
      "the only method is to try. Each extra leading zero digit demanded of the hash multiplies the expected number of "
      "attempts by sixteen, so the expression [16**k for k in (1, 2, 3, 4)] gives [16, 256, 4096, 65536] - the cost of "
      "a block is set by a dial, and the dial is turned by the difficulty rule every 2016 blocks to hold the average "
      "interval at ten minutes. The second half makes agreement cheap: a participant does not negotiate, it simply "
      "prefers the chain with the most accumulated work, so two participants who have seen the same blocks reach the "
      "same answer without exchanging a single opinion."),
  (K, "The most common error here is to read a confirmation as a proof rather than as a cost. A confirmed payment is "
      "one whose reversal would require redoing the work of every block since it, which is expensive but not "
      "impossible, and the whitepaper itself states the residual probability rather than claiming certainty [NK]. The "
      "second error is to treat the Byzantine Generals' Problem as solved in the sense of the original paper. Lamport, "
      "Shostak and Pease prove agreement is attainable when more than two-thirds of the participants are loyal, or, "
      "with unforgeable written messages, for any number of them [LP]; Bitcoin's arrangement is a different one, in "
      "which the weight of a participant is the work it has done rather than its membership of a known group, and the "
      "guarantee it offers is economic rather than absolute."),
 ],

 "History": [
  (E, "The history is met in the artefacts it left behind, all of which can still be read. The paper of 2008 is a "
      "nine-page document that is still the shortest complete statement of the design [NK]. The software started in "
      "2009 is still being developed under the same name, so a student can read today the function that computes the "
      "block subsidy and find the same rule the paper describes [BC]. The first block of January 2009 is still the "
      "first block of the chain every node holds, and its identifier and timestamp can be fetched from any explorer "
      "[BS]. The withdrawal of the author in April 2011 is met in the absence of any authority to appeal to, which is "
      "the practical shape the chapter gives it [AH]."),
  (H, "Read as a sequence of steps, the history explains the design as a set of answers to failures that had already "
      "happened. Earlier digital currencies were centralized, so their operators could be sued or shut down and the "
      "currency died with the company; the answer was to remove the operator. The removal created a new problem, "
      "namely that without an operator nobody decides which of two conflicting histories is the real one; the answer "
      "to that was proof of work, a technique Back had published in 2002 to make electronic mail expensive to send in "
      "bulk, turned to the purpose of making a block expensive to produce [BK]. The remaining pieces - digital "
      "signatures to authorise a payment and a hash chain to order the record - were older still, so what the paper "
      "contributed was the arrangement rather than the parts."),
  (K, "Three claims about this history should be resisted. The first is that the author's identity matters to the "
      "system: the design can be read and checked without knowing who wrote it, and the chapter deliberately treats "
      "the name as an alias [AH]. The second is that the reference implementation is the protocol. It is one program "
      "that happens to define the rules in practice because the written specification is incomplete, which is a "
      "weakness of the arrangement rather than a feature of it. The third is that any figure printed in an older "
      "edition of the textbook is still current: the book's own glossary, for instance, still states a subsidy of 12.5 "
      "bitcoin a block, which was true at the time of writing and is two halvings out of date now [AH]."),
 ],

 "Standards": [
  (E, "These two practices are met whenever two programs by different authors have to agree about something the "
      "protocol itself does not fix. A recovery code written down from one wallet and typed into another works only "
      "because both authors implemented the same numbered proposal [B39]. A payment request scanned from a shop's "
      "screen is understood because both sides implemented the proposal that defines the format of such a request "
      "[B21]. An address in the newer format is accepted by a wallet that never heard of the shop's software because "
      "both follow the proposal that defines the encoding and its checksum. The licence is met in a different way: it "
      "is what allows a student to read the reference implementation's source at all."),
  (H, "A proposal is a document with a number, a status and an author, and the numbered series is the record of what "
      "has been suggested, what was accepted and what was rejected; the appendix of the textbook lists them with their "
      "numbers and statuses, so a claim about the rules can be traced to the document that states it [AH]. A status is "
      "part of the information: the payment-request proposal is recorded as closed with a successor proposed, which "
      "tells a reader that the format is in use but no longer the place to look for new work [B21]. The licence works "
      "by conditions rather than by permission: the Open Source Definition sets out ten conditions that a licence must "
      "meet before software may be called open source, among them that it must allow redistribution, must include "
      "source code and must permit derived works [OSI], and a licence either meets all of them or does not qualify."),
  (K, "A numbered proposal is not a law and not a decision. Anyone may write one; a number is assigned on submission, "
      "not on approval; and a proposal may sit for years at draft, be rejected, or be replaced, so citing a number "
      "without its status says much less than it appears to. Open source, likewise, is a statement about the licence "
      "and not about the quality, the security or the maintenance of the software: the definition's conditions concern "
      "what a recipient is allowed to do, and say nothing about whether anyone is reviewing the code. The two "
      "practices together explain how a system without an owner can change at all, which is a real achievement, but "
      "neither of them guarantees that a change is a good one."),
 ],

 # ------------------------------------------------------------------ Wallet
 "WalletPlatform": [
  (E, "The platform is met as the first question a newcomer actually faces, because it is the question the download "
      "page asks. Alice, in the chapter's story, installs a wallet on a mobile telephone, which is why her story "
      "features a camera, a QR code and a shop counter rather than a configuration file [AH]. A student who follows "
      "the same chapter on a desktop computer meets a different set of choices, among them whether to download the "
      "whole chain. Someone who signs in to an exchange's web page has chosen a web wallet without being asked, and "
      "someone handed a small sealed device at a meetup has met the fourth platform."),
  (H, "What separates the platforms is where the private key is kept and which other program can reach it. On a "
      "general-purpose computer or telephone the key is a file guarded by the operating system, so the wallet is as "
      "safe as that system and the other software on it; the convenience is that the same device also has the camera, "
      "the network and the screen. A web wallet keeps nothing locally, so its safety is the safety of a remote service "
      "and of the browser session that reaches it. A hardware signing device inverts the arrangement: the key never "
      "leaves the device, which has no general-purpose software on it and exposes only one operation, namely signing a "
      "transaction handed to it, so a compromised computer can ask for a signature but cannot take the key. That is "
      "also why such a device is useless alone and always works beside an ordinary wallet program that builds the "
      "transactions and talks to the network."),
  (K, "Two mistakes are easy here. The first is to read the list as a ranking, with hardware best and web worst: a "
      "hardware device protects a key superbly and protects nothing else, and for a person buying coffee with a small "
      "balance a mobile wallet is the better engineering choice. The second is to assume the platform decides the "
      "other two classifications. It does not: a desktop wallet may or may not run a full node, and a mobile wallet "
      "may hold its own keys or hand them to a service, so the platform, the node type and the control of keys have to "
      "be asked separately about any particular product. The chapter's own advice is to understand the differences "
      "before choosing, which is advice to ask three questions rather than one [AH]."),
 ],

 "NodeType": [
  (E, "The node type is met as a difference in what a wallet needs before it can tell the truth. A program that "
      "validates for itself has to fetch and check every block, which costs storage, bandwidth and hours of initial "
      "work, and it is met as the long first synchronisation that a newly installed full node performs. A lightweight "
      "client is met as a wallet that is usable within seconds of installation, because it asks remote servers for the "
      "few pieces of the chain that concern its own addresses. A third-party client is met as an application that "
      "shows a balance and a history with no chain data at all, because it is displaying what a service told it."),
  (H, "The three types are three answers to one question: which claims will this program check itself. A full node "
      "checks all of them, and it can do so because a block carries its own evidence - the identifier of a block is "
      "the hash of its own eighty-byte header, so recomputing that hash and comparing it is a complete check that the "
      "header is the one being claimed. A lightweight client checks a much smaller object: it keeps only the headers, "
      "and eighty bytes per block against the 2,325,617 bytes of block 840,000 is about 29,070 times less data, which "
      "is the whole reason the design exists [BS]. A third-party client checks nothing; it trusts the answer. Each "
      "step down the list buys speed and small size with trust, and the trust is specific - a server that answers "
      "about an address learns which addresses interest the asker, whatever else it does honestly."),
  (K, "Two points are regularly confused. First, lightweight does not mean insecure and full does not mean safe: a "
      "full node validates the chain but does nothing to protect the key on the same machine, and a careful "
      "lightweight wallet with a hardware signing device may protect money better than a full node on a shared "
      "computer. Second, the words peer and client describe roles rather than products. A full node is a peer because "
      "it both asks and answers; a lightweight client mostly asks; and a single program can act as a peer towards "
      "other nodes and as a server towards a wallet on the same machine. The chapter's own phrasing is about degrees of "
      "autonomy and about how a wallet interacts with the network, which is a description of behaviour and not of a "
      "brand [AH]."),
 ],

 "KeyControl": [
  (E, "The question is met at the moment a wallet is first opened, and usually without being asked out loud. A program "
      "that shows a list of words and insists they be written down has just handed over the keys, and with them the "
      "responsibility. A service that asks for an electronic-mail address and a password has kept the keys, and what "
      "the user receives is an account. The chapter meets the distinction in Alice's wallet, which produces a recovery "
      "code, and again in its warning that where you do not have control, your bitcoins are managed by a third party "
      "who ultimately controls your funds on your behalf [AH]."),
  (H, "The two arrangements differ in where the record of ownership lives. In a custodial arrangement the balance is a "
      "row in the custodian's own database, so the custodian can change it, freeze it, or lose it, and the customer's "
      "claim is a claim against the custodian rather than against the chain. In a noncustodial arrangement there is no "
      "such row: the balance is what anyone reading the public record computes for the addresses the key controls, so "
      "every reader gets the same figure and no single party can alter it. What the key holder owns is therefore not "
      "an entry in a ledger somebody keeps, but the ability to produce the one signature that moves those outputs, and "
      "the key itself is a number among 2 to the power 256, which written out in full has 78 decimal digits - large "
      "enough that holding it is the only way to control the money and guessing it is not a strategy."),
  (K, "Three warnings follow. The word wallet is used for both arrangements, often by the same company, so the "
      "question of who holds the keys has to be asked explicitly and answered before any money is moved. Control is "
      "not always all or nothing: some designs split a key or require several keys, which the course treats later, and "
      "a wallet may be noncustodial for spending while depending on a service for everything else. And control cuts "
      "both ways, which is the hardest part to teach: the arrangement that no institution can interfere with is also "
      "the arrangement in which no institution can help, so a key that is lost is money that is gone, and the chapter "
      "states the responsibility plainly alongside the benefit [AH]."),
 ],

 "Backup": [
  (E, "A backup is met twice: once when it is created, which is unavoidable, and once when it is used, which is "
      "usually unexpected. The creation is met at Alice's first start-up, where the wallet shows a sequence of ordinary "
      "words and asks for them to be recorded [AH]. The use is met when a telephone is lost, broken or replaced, and "
      "the same words typed into a different wallet program - possibly by a different author - reproduce the same keys "
      "and therefore the same money. It is also met, unhappily, on pages and in messages that ask for the words, which "
      "is the one request no legitimate program ever makes."),
  (H, "The recovery code works because the keys of a wallet are not independent secrets but are all derived, by a "
      "fixed procedure, from one secret; writing down that one secret therefore backs up every key the wallet will "
      "ever have, including the ones it has not generated yet. The words are a readable form of that secret: a "
      "standard fixes a list of 2048 words, so each word carries eleven bits, and a few extra bits of checksum are "
      "added so that a mistyped code is usually rejected rather than silently opening an empty wallet - which is why "
      "128 bits of entropy becomes twelve words and 256 bits becomes twenty-four [B39]. The words are then passed "
      "through a deliberately slow function before becoming a key, so that guessing a weak code costs an attacker real "
      "time [PK]."),
  (K, "Three things the code does not do deserve naming, because each has cost people money. It does not protect "
      "itself: anyone who reads the words controls the wallet, so a photograph of them in a cloud album is the wallet "
      "in a cloud album, and a file that merely encodes them is not protecting them at all, since any program on the "
      "machine can decode it. It does not carry the wallet's other data - the labels, the notes, the list of which "
      "address was given to whom - so a restored wallet has the money and none of the record of what it was for. And "
      "the checksum is not a guarantee: the standard itself states that about one mistyped code in 256 will pass the "
      "check anyway, so the words must be verified against the original rather than trusted because the wallet "
      "accepted them [B39]."),
 ],

 # ------------------------------------------------------------------ Usage
 "Address": [
  (E, "An address is met as a string to be copied, and as a square of black and white to be photographed. Alice meets "
      "it when she presses Receive and her wallet shows a new one; Joe meets the same address as a QR code on her "
      "screen, which his camera reads and his wallet turns back into text. A shop meets it as a payment request that "
      "carries an amount and a description beside it, so that the customer does not have to type either [B21]. A "
      "student meets it a third way, in a block explorer, where entering an address lists every payment ever made to "
      "it - which is the same fact seen from the side that matters for privacy [BS]."),
  (H, "An address is a short string with structure, and the structure is what lets a program reject a mistake before "
      "any money moves. In the newer format the string begins with a few characters naming the network, then a "
      "separator, then a data part written in an alphabet of thirty-two characters chosen so that no two of them are "
      "easily confused - the four characters 1, b, i and o are left out of it for exactly that reason - and it ends "
      "with six characters that are a checksum computed from everything before them. A wallet recomputes that "
      "checksum, and of the thirty-two characters that could stand in the last position only one makes the sum come "
      "out right, so a single mistyped character is caught. None of this involves asking anyone's permission: the "
      "address is derived from a key the wallet generated by itself, with no registration anywhere, which is why a new "
      "one costs nothing."),
  (K, "The cautions here are about information rather than about safety. Giving out an address is safe, and the "
      "chapter says so plainly: unlike a bank account number, nobody who learns one of your addresses can withdraw "
      "from your wallet, because you must initiate all spends [AH]. What is not safe is reusing one, because the "
      "public record then joins together everyone who paid it: two people given the same address can each see what the "
      "other sent, and so can anyone else. A second caution is that an address is not an identity and not a name - "
      "nothing in it says who controls it - so the privacy it offers is the privacy of an unlabelled number, which "
      "lasts exactly as long as nobody connects the number to a person. The third is mechanical: always let a program "
      "read an address, by copying or by camera, rather than typing it, because the checksum catches a typing mistake "
      "but a correctly typed wrong address is simply a payment to a stranger."),
 ],

 "Transfer": [
  (E, "A transfer is met as the few seconds between pressing Send and seeing a payment appear, and then as the wait "
      "that follows. The chapter's own story is the place it is met first: Joe enters an amount of 0.001 bitcoin, his "
      "wallet builds and signs a transaction, the transaction spreads across the network, and some minutes later a "
      "block includes it and Alice's wallet shows it as confirmed [AH]. It is met again in the fee a wallet proposes "
      "and lets the user raise or lower, in the number of confirmations an exchange demands before it credits a "
      "deposit, and in the newer arrangements that move value between two parties repeatedly without putting any of it "
      "on the chain [LN]."),
  (H, "A transfer is not a message that moves a balance; it is a signed document that consumes particular earlier "
      "outputs and creates new ones. The sum of what it consumes is at least the sum of what it creates, and the "
      "difference is the fee: consuming 110,000 satoshis to create an output of 100,000 leaves 10,000 satoshis for "
      "whichever miner includes the transaction, which is how inclusion is paid for without anyone being billed. "
      "Because the document is signed by the keys that control the outputs it consumes, no third party has to "
      "authorise it, and because it names its outputs explicitly there is no account whose balance could be read "
      "wrongly. Settlement then happens by inclusion: once the transaction is in a block, undoing it means replacing "
      "that block and every block after it, so each further block makes reversal more expensive, and six blocks is the "
      "point the book's glossary gives as the conventional threshold for treating a payment as settled [AH]."),
  (K, "Three expectations carried over from bank payments fail here. There is no reversal: a confirmed payment can "
      "only be answered by a second payment in the other direction, which the receiver has to agree to make, so the "
      "ledger grows and never shrinks. There is no pending state that can be cancelled by an institution; a "
      "transaction that is waiting is waiting to be chosen by a miner, and a fee too low to be attractive leaves it "
      "waiting indefinitely rather than failing cleanly. And an amount is irrevocably tied to the address typed into "
      "it, with no name on the other side to check against, which is why the chapter's practical advice is about "
      "reading the address and the amount carefully before signing rather than about recovering from a mistake "
      "afterwards."),
 ],

 "SemanticBridge": [
  (E, "The bridge is met wherever a system has to decide who may say something about whom. It is met in the "
      "identifiers of the web's identity standards, which look like an address with three parts separated by colons - "
      "a fixed prefix, the name of a method, and an identifier within that method - so that a reader can tell from the "
      "string itself how the identifier is to be resolved [DID]. It is met in the signed claims built on top of them, "
      "in which an issuer states something about a subject and a holder later shows that statement to a verifier [VC]. "
      "And it is met in this chapter's own subject, where control of an address is proved by a signature rather than "
      "granted by a registry."),
  (H, "What the two subjects share is a single substitution: a registry's permission is replaced by a proof. In the "
      "registry arrangement, a name belongs to whoever the register says it belongs to, so the register is the "
      "authority and also the single point of failure and of control. In the key arrangement, the name is bound to a "
      "key at the moment it is created, and anybody who can verify a signature can check the binding without asking "
      "anybody, which is exactly how an address works in this chapter. The consequences carry across as well: the "
      "holder of the key is the controller, the loss of the key is the loss of control, and there is no office that "
      "can restore it - so the recovery problem of the Wallet branch reappears, unchanged, in the identity layer of "
      "the web."),
  (K, "The bridge is a comparison and should not be read as an implementation. These identity standards are "
      "Recommendations of the World Wide Web Consortium and do not require a blockchain of any kind; several of their "
      "methods use one, several do not, and the standards are deliberately written so that the choice is a detail "
      "[DID]. Nor does a signed claim become true by being signed: a signature shows who made a statement and that it "
      "has not been altered, which is a question about provenance and not about accuracy. The useful transfer to this "
      "course is the architectural one - that the same choice between a register and a key recurs whenever "
      "identification is needed - and a student should be able to name that choice without asserting that one subject "
      "is built out of the other."),
 ],

 "Acquisition": [
  (E, "The four routes are met in four quite different places. A friend who already holds bitcoin is met at a local "
      "meetup, which the chapter names as a way of finding one [AH]. Earning is met in the shop or the freelance "
      "invoice, where bitcoin is accepted for something of value, and it is the only route that needs no counterparty "
      "willing to sell. A machine is met in a shopping centre or a corner shop, taking banknotes and sending bitcoin "
      "to a telephone shown to its camera. An exchange is met as a web page and an application connected to a bank "
      "account, and it is the route that asks for documents before it will do anything at all."),
  (H, "Underneath the four routes there is one mechanical difference that explains most of the rest: whether the "
      "payment given in exchange can be taken back. Cash and bitcoin cannot be reversed once handed over, so a direct "
      "sale between two people, or a machine taking banknotes, can complete in minutes. A card payment or a bank "
      "transfer can be reversed by the payer's institution for weeks afterwards, while the bitcoin sent in exchange "
      "cannot, so a seller accepting one of those is exposed for that whole period - which is why, as the chapter "
      "says, companies in this position demand identity and credit checks that can take days or weeks [AH]. The "
      "identity check is therefore not an arbitrary formality but the seller's answer to an asymmetry in "
      "reversibility, and the routes line up accordingly: the faster and more private a route is, the more of the risk "
      "the buyer and seller carry between themselves."),
  (K, "Two things are worth saying about the trade-offs. Convenience is paid for in information: the formal routes "
      "connect a verified identity to the addresses they pay out to, and that connection is permanent, because the "
      "public record never forgets, so the privacy consequences of this choice outlast the purchase itself. And a "
      "price quoted in one of these routes is not the market price: a machine or a direct seller charges a margin for "
      "immediacy, and the difference is the fee, whether or not it is called one. A newcomer should also know that the "
      "chapter's list is the set of routes that existed as it was written, and that which of them is legal, available "
      "or regulated depends entirely on the country the student is in - a fact the textbook cannot settle and this "
      "course does not advise on."),
 ],

 # ------------------------------------------------------------------ Nature
 "Characteristic": [
  (E, "The four properties are met as the first things a newcomer notices, usually in the form of a surprise. The "
      "absence of a coin to hold is met the moment someone asks where the bitcoin actually is and finds there is no "
      "object anywhere, only a record of transfers from which balances are computed. Borderlessness is met in a "
      "payment that arrives across a frontier without any step that mentions the frontier. Decentralisation is met in "
      "the absence of anyone to telephone. Robustness is met negatively, in the fact that the chain does not stop when "
      "a company fails or a country blocks a service, which is exactly what did happen to the earlier digital "
      "currencies the chapter's sidebar describes [AH]."),
  (H, "Each property is produced by a mechanism, and a student who can name the mechanism has understood the property "
      "rather than the slogan. Virtuality follows from the ledger being a list of transfers: a balance is derived by "
      "adding up what came in and subtracting what went out, so nothing has to exist as an object. Borderlessness "
      "follows from the network layer, which routes a transaction to whichever peers will relay it and has no field in "
      "which a country could be written. Decentralisation follows from the topology and from everyone enforcing the "
      "same rules: in the small network of seven nodes used in this chapter, only one node has the property that its "
      "failure cuts another node off, and real networks are far more densely connected, which is what makes the "
      "property hold in practice rather than in principle. Robustness follows from the cost of work: rewriting history "
      "means redoing every block since the point rewritten, and the cost rises with every block added."),
  (K, "These properties are frequently overstated, and the honest version of each is narrower. Virtual does not mean "
      "beyond reach: the keys live on real devices, and those devices can be stolen, broken or seized. Borderless "
      "describes the protocol and not the law - the network does not know where a user is, and the user's own "
      "jurisdiction very much does. Decentralized is a matter of degree rather than a yes or no, and it has to be "
      "asked separately about the network, the mining and the software development, which are decentralized to quite "
      "different extents. And robust means expensive to disturb, not impossible: the chapter's claim is about cost, "
      "and a property that rests on cost is only as strong as the cost is high."),
 ],

 "Architecture": [
  (E, "The four parts are met separately before they are met together. The network is met as a program that connects "
      "to a handful of peers it was not told about in advance and relays what it hears. The journal is met in a block "
      "explorer, where any transaction from the first block onwards can be looked up by anybody, with no account and "
      "no permission [BS]. The rules are met as a rejection: a transaction that spends an output twice, or a block "
      "that claims more new bitcoin than the schedule allows, is simply not accepted, and nothing had to be decided "
      "for that to happen. The consensus mechanism is met as the ten-minute rhythm in which the record advances [AH]."),
  (H, "The parts hold each other up, and the order of support is what makes the design work. The network moves "
      "messages but guarantees nothing about them, so any peer may lie. The rules mean that a lie is detectable, "
      "because every claim a message makes - a signature, an amount, a subsidy - can be checked by the recipient "
      "against rules it already has, so a dishonest peer costs its listeners nothing but a discarded message. The "
      "journal means that the checked history is the same object for everyone, and that an entry once accepted stays "
      "where it is, so the rules have something stable to be applied to. And the consensus mechanism settles the one "
      "question the other three cannot: which of two equally valid histories is the one to build on. Remove any one "
      "part and the system fails in a specific way, which is the useful way to learn the structure."),
  (K, "Two cautions apply to this section. The first is against treating the four parts as layers in the sense of a "
      "network protocol stack: they are not stacked in that way, and in a running node all four are at work on the "
      "same message at once, so the diagram in a student's head should be of parts that constrain each other rather "
      "than of a pile. The second is against reading a part of the chapter's architecture as an architecture of a "
      "product. The chapter is describing what the system consists of, not what a piece of software looks like "
      "inside; the reference implementation organises its own code quite differently, and the course's later chapters "
      "on building and running it are where that difference becomes visible [BC]."),
 ],
}

# ---------------------------------------------------------------------------------------------------------------------
# the one paragraph of a level-3 concept that described another concept's example
# ---------------------------------------------------------------------------------------------------------------------
PARAS_REPLACE = {
 ("Protocol", 3): (H,
  "A protocol fixes four things: who speaks first, which messages exist, how each message is laid out byte by byte, "
  "and what the receiver must do with each one. The layout is the part a program can be shown doing: every message of "
  "Bitcoin's own peer-to-peer protocol begins with four fixed bytes, called the magic value, that identify the network "
  "the message belongs to, so a node can tell at once whether a stream of bytes is even addressed to it. The worked "
  "example takes the four lines of the reference implementation's own source that set those bytes one at a time, "
  "copied from the file this chapter saved, and prints them as f9beb4d9 - the value that marks a message of the main "
  "Bitcoin network [BC]. A "
  "message whose first four bytes are different belongs to a different network, such as the test network, and is "
  "discarded without being parsed any further."),
}

# ---------------------------------------------------------------------------------------------------------------------
# the worked examples added to leaf concepts that had none: (example label, io expression, expected repr)
# ---------------------------------------------------------------------------------------------------------------------
_BECH32 = (
 "CH = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'\n"
 "GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]\n"
 "def polymod(values):\n"
 "    chk = 1\n"
 "    for v in values:\n"
 "        top = chk >> 25\n"
 "        chk = ((chk & 0x1ffffff) << 5) ^ v\n"
 "        for i in range(5):\n"
 "            if (top >> i) & 1: chk ^= GEN[i]\n"
 "    return chk\n"
 "def ok(addr):\n"
 "    hrp, data = addr.rsplit('1', 1)\n"
 "    expand = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]\n"
 "    return polymod(expand + [CH.index(c) for c in data]) == 1\n"
 "good = 'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'\n"
 "result = (ok(good), ok(good[:-1] + 'f'))")

# The three examples below work on block data and on lines of the reference implementation's source. They cannot read
# a file, because the same program has to run in the reader's browser, where the repository is not present; so the few
# values each one needs are read out of the saved copy in 08-tooling/ch01-sources while this module is imported and
# written into the program as a literal. SRC below then re-reads the saved copy and checks that every literal is still
# the value the file carries, so an example cannot drift away from its source without the build stopping.
_SRCDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch01-sources")
def _saved(name, keys=None):
    import json
    d = json.load(open(os.path.join(_SRCDIR, name), encoding="utf-8"))
    return d if keys is None else {k: d[k] for k in keys}

_BLOCK0 = _saved("block0.json")
_B840 = _saved("block840000.json", ("height", "size"))
_MAGIC = "        pchMessageStart[0] = 0xf9;\n        pchMessageStart[1] = 0xbe;\n        pchMessageStart[2] = 0xb4;\n        pchMessageStart[3] = 0xd9;"
_HALVING_LINE = "        consensus.nSubsidyHalvingInterval = 210000;"
_OSD = ["Free Redistribution", "Source Code", "Derived Works", "Integrity of The Author", "No Discrimination Against Persons or Groups",
        "No Discrimination Against Fields of Endeavor", "Distribution of License", "License Must Not Be Specific to a Product",
        "License Must Not Restrict Other Software", "License Must Be Technology-Neutral"]

_HEADER = (
 "import hashlib, struct\n"
 "b = %r\n"
 "header = (struct.pack('<i', b['version'])\n"
 "          + bytes.fromhex(b['previousblockhash'] or '00' * 32)[::-1]\n"
 "          + bytes.fromhex(b['merkle_root'])[::-1]\n"
 "          + struct.pack('<III', b['timestamp'], b['bits'], b['nonce']))\n"
 "digest = hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1].hex()\n"
 "result = (len(header), digest == b['id'], digest[:12])") % (_BLOCK0,)

_GRAPH = (
 "links = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B', 'F'], 'E': ['C', 'F'],\n"
 "         'F': ['D', 'E', 'G'], 'G': ['F']}\n"
 "def reach(start, down):\n"
 "    seen, todo = set(), [start]\n"
 "    while todo:\n"
 "        x = todo.pop()\n"
 "        if x in seen or x == down: continue\n"
 "        seen.add(x); todo += [y for y in links[x] if y != down]\n"
 "    return len(seen)\n"
 "alive = {d: reach(next(n for n in links if n != d), d) for d in links}\n"
 "result = sorted(d for d, k in alive.items() if k < len(links) - 1)")

IO = {
 "BitcoinUnit": ("the same amount in bitcoin, millibitcoin and satoshis",
   "(lambda d: (str(d), str(d * 1000), int(d * 10**8)))(__import__('decimal').Decimal('0.001'))",
   "('0.001', '1.000', 100000)"),
 "BitcoinAddress": ("the checksum of the address, and of the same address with one character changed",
   _prog(_BECH32), "(True, False)"),
 "FullNode": ("the identifier of block 0, recomputed from the block's own header",
   _prog(_HEADER), "(80, True, '000000000019')"),
 "LightweightClient": ("eighty bytes of header against the whole of block 840000",
   _prog("b = %r\nresult = (80, b['size'], round(b['size'] / 80))" % (_B840,)),
   "(80, 2325617, 29070)"),
 "ThirdPartyApiClient": ("what a client knows when it only has the service's answer",
   _prog("answer = %r\nresult = (answer['height'], answer['tx_count'], len(answer))" % (_BLOCK0,)),
   "(0, 1, 13)"),
 "ByzantineGeneralsProblem": ("how many generals are needed to tolerate one, two and three traitors",
   "[(m, 3 * m + 1) for m in (1, 2, 3)]", "[(1, 4), (2, 7), (3, 10)]"),
 "ReferenceImplementation": ("the halving interval, taken from the line of the reference implementation that sets it",
   _prog("import re\nline = %r\nresult = int(re.search(r'nSubsidyHalvingInterval = (\\d+);', line).group(1))" % (_HALVING_LINE,)),
   "210000"),
 "OpenSourceSoftware": ("the conditions a licence must meet, numbered",
   _prog("conditions = %r\nresult = (len(conditions), conditions[0], conditions[-1])" % (_OSD,)),
   "(10, 'Free Redistribution', 'License Must Be Technology-Neutral')"),
 "HardwareSigningDevice": ("a signature from a device that never gives up its key",
   _prog("n, e, d = 3233, 17, 2753\n"
         "class Device:\n"
         "    def __init__(self, key): self._key = key\n"
         "    def sign(self, m): return pow(m, self._key, n)\n"
         "dev = Device(d)\n"
         "sig = dev.sign(65)\n"
         "result = (sig, pow(sig, e, n) == 65, [m for m in dir(dev) if not m.startswith('_')])"),
   "(588, True, ['sign'])"),
 "CustodialWallet": ("a balance the custodian can rewrite",
   _prog("db = {'alice': 100_000}\ndb['alice'] = 0\nresult = db"), "{'alice': 0}"),
 "NoncustodialWallet": ("the same balance computed by three readers of the public record",
   _prog("journal = [('Joe', 'Alice', 100_000), ('Alice', 'Eve', 30_000)]\n"
         "def balance(who, j): return sum(a for f, t, a in j if t == who) - sum(a for f, t, a in j if f == who)\n"
         "readers = [balance('Alice', list(journal)) for _ in range(3)]\n"
         "result = (readers, len(set(readers)) == 1)"),
   "([70000, 70000, 70000], True)"),
 "WalletMetadata": ("what a recovery code gives back, and what it does not",
   _prog("backup = {'words': 'nephew dog crane clever quantum crazy purse traffic repeat fruit old clutch'.split()}\n"
         "restored = {'words': backup['words'], 'labels': backup.get('labels', {})}\n"
         "result = (len(restored['words']), restored['labels'])"),
   "(12, {})"),
 "AddressReuse": ("what two people who were given the same address can see",
   _prog("journal = [('Joe', 'addr1', 100_000), ('Bob', 'addr1', 40_000), ('Carol', 'addr2', 7_000)]\n"
         "reused = [a for a in sorted({x[1] for x in journal}) if sum(1 for x in journal if x[1] == a) > 1]\n"
         "leaked = [(s, m) for s, a, m in journal if a in reused]\n"
         "result = (reused, leaked)"),
   "(['addr1'], [('Joe', 100000), ('Bob', 40000)])"),
 "Privacy": ("how many payments each address reveals",
   _prog("journal = [('Joe', 'addr1', 100_000), ('Bob', 'addr1', 40_000), ('Carol', 'addr2', 7_000)]\n"
         "seen = {}\n"
         "for sender, addr, amount in journal: seen.setdefault(addr, []).append((sender, amount))\n"
         "result = {a: len(v) for a, v in seen.items()}"),
   "{'addr1': 2, 'addr2': 1}"),
 "Irreversibility": ("a refund is a second entry, not the removal of the first",
   _prog("ledger = []\n"
         "def pay(f, t, a): ledger.append((f, t, a))\n"
         "pay('Joe', 'Alice', 100_000)\n"
         "pay('Alice', 'Joe', 100_000)\n"
         "net = sum(a for f, t, a in ledger if t == 'Alice') - sum(a for f, t, a in ledger if f == 'Alice')\n"
         "result = (len(ledger), net)"),
   "(2, 0)"),
 "ElectronicPayment": ("a payment that can be taken out of the record altogether",
   _prog("rows = [('Joe', 'Alice', 100_000)]\nrows.remove(('Joe', 'Alice', 100_000))\nresult = (rows, len(rows))"),
   "([], 0)"),
 "DecentralizedIdentity": ("the three parts of a decentralized identifier",
   "'did:example:123456789abcdefghi'.split(':')", "['did', 'example', '123456789abcdefghi']"),
 "VerifiableCredential": ("a signed claim, and the same claim after one character is added",
   _prog("n, e, d = 3233, 17, 2753\n"
         "def digest(claim): return sum(claim.encode()) % n\n"
         "claim = 'Alice passed SEN0401'\n"
         "sig = pow(digest(claim), d, n)\n"
         "result = (sig, pow(sig, e, n) == digest(claim), pow(sig, e, n) == digest(claim + '!'))"),
   "(94, True, False)"),
 "CurrencyExchange": ("the one trade that two bids and two asks produce",
   _prog("bids = [(60_100, 2), (60_000, 5)]\n"
         "asks = [(60_050, 3), (60_200, 4)]\n"
         "result = [(min(b, a), min(bq, aq)) for b, bq in bids for a, aq in asks if b >= a]"),
   "[(60050, 2)]"),
 "Protocol": ("the four bytes that mark a message of the main network",
   _prog("import re\nsrc = %r\n"
         "byts = [int(m, 16) for m in re.findall(r'pchMessageStart\\[\\d\\] = 0x([0-9a-f]{2});', src)]\n"
         "result = (bytes(byts).hex(), len(byts))" % (_MAGIC,)),
   "('f9beb4d9', 4)"),
 "Internet": ("how many addresses one small block of the internet holds",
   "__import__('ipaddress').ip_network('203.0.113.0/24').num_addresses", "256"),
 "DistributedSystem": ("two participants that receive in different orders and still agree",
   _prog("arrivals_a = ['tx1', 'tx2', 'tx3']\narrivals_b = ['tx2', 'tx1', 'tx3']\n"
         "result = (arrivals_a != arrivals_b, set(arrivals_a) == set(arrivals_b))"),
   "(True, True)"),
 "Malware": ("a secret that was only encoded, read back by any program on the machine",
   "__import__('base64').b64decode('bmVwaGV3IGRvZyBjcmFuZQ==').decode()", "'nephew dog crane'"),
 "Phishing": ("two domain names that look alike and are not the same name",
   "('bitcoin.org' == 'bitco\\u0131n.org', hex(ord('i')), hex(ord('\\u0131')))", "(False, '0x69', '0x131')"),
 "Decentralized": ("the only node of this chapter's small network whose loss cuts another node off",
   _prog(_GRAPH), "['F']"),
 "PublicJournal": ("every entry of the journal that names Alice, found by anybody who reads it",
   _prog("journal = [('Joe', 'Alice', 100_000), ('Alice', 'Eve', 30_000), ('Joe', 'Eve', 5_000)]\n"
         "result = [(f, t, a) for f, t, a in journal if 'Alice' in (f, t)]"),
   "[('Joe', 'Alice', 100000), ('Alice', 'Eve', 30000)]"),
 "Robust": ("how many hashes an extra demanded zero digit costs",
   "[16**k for k in (1, 2, 3, 4)]", "[16, 256, 4096, 65536]"),
}

# ---------------------------------------------------------------------------------------------------------------------
# the numbers the new section prose states, each executed by the chapter builder
# ---------------------------------------------------------------------------------------------------------------------
NUM = [
 ("21_000_000 * 10**8", "2100000000000000"),                                    # Unit: satoshis in the whole supply
 ("round(210000 * 10 / (365.25 * 24 * 60), 2)", "3.99"),                        # Supply: years in one halving interval
 ("[16**k for k in (1, 2, 3, 4)]", "[16, 256, 4096, 65536]"),                   # Consensus, Robust: the cost of a zero
 ("round(2325617 / 80)", "29070"),                                              # NodeType: headers against whole blocks
 ("len('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee')", "42"),                   # Address: the length of an address
 ("'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'[-6:]", "'c6aaee'"),             # Address: the checksum characters
 ("sorted(set('0123456789abcdefghijklmnopqrstuvwxyz') - set('qpzry9x8gf2tvdw0s3jn54khce6mua7l'))",
  "['1', 'b', 'i', 'o']"),                                                      # Address: the four excluded characters
 ("110_000 - 100_000", "10000"),                                                # Transfer: the fee of the example
 ("2048 .bit_length() - 1", "11"),                                              # Backup: bits carried by one word
 ("[(ent, (ent + ent // 32) // 11) for ent in (128, 256)]", "[(128, 12), (256, 24)]"),   # Backup: words for 128, 256 bits
 ("len(str(2**256))", "78"),                                                    # KeyControl: digits in a private key
 ("33 * 210000", "6930000"),                                                    # Issuance: blocks until the last subsidy
 ("2016 * 10 // (60 * 24)", "14"),                                              # Consensus: days in one retarget period
]

# ---------------------------------------------------------------------------------------------------------------------
# the values the examples carry as literals, re-read from the saved copies of the sources so they cannot drift
# ---------------------------------------------------------------------------------------------------------------------
SRC = [
 _has("core_chainparams.cpp", *[l.strip() for l in _MAGIC.splitlines()]),       # Protocol: the four magic bytes
 _has("core_chainparams.cpp", _HALVING_LINE.strip()),                           # ReferenceImplementation: the interval
 _has("osd.txt", *_OSD),                                                        # OpenSourceSoftware: the ten conditions
 _has("did.txt", "did:example:123456789abcdefghi"),                             # DecentralizedIdentity: the identifier
 _has("ch04_keys.adoc", "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee"),          # BitcoinAddress: the address itself
]
# the block data the two node examples carry: the saved files are read here, by the builder, and compared field by field
BLOCKS = [
 ("%s == %r" % (_js("block0.json"), _BLOCK0), "True"),
 ("{k: %s[k] for k in ('height', 'size')} == %r" % (_js("block840000.json"), _B840), "True"),
]
