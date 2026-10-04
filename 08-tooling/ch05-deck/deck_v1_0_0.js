// SEN0401 chapter 5 lecture deck, version 1.0.0 - Wallet Recovery (Mastering Bitcoin, 3rd edition, chapter 5).
// Built with pptxgenjs from the chapter 5 corpus (08-tooling/sen0401_ch05_corpus_v1_0_0.py): the taxonomy's own order,
// one section per branch, one slide per concept, and for every concept that has a worked example the code with the
// output that examples_run_v2_0_0.py actually obtained - no number on a slide is typed from memory.
// Usage: node deck_v1_0_0.js <out.pptx>
const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync(__dirname + '/examples_out_v1_0_0.json'));
const PY = EX._python;
const NSTMT = Object.keys(EX).filter(k => k[0] !== '_').reduce((n, k) => n + EX[k].length, 0);

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel';
pres.title = 'SEN0401 Chapter 5 - Wallet Recovery';
pres.subject = 'Mastering Bitcoin 3rd edition, chapter 5, recomputed from the standards and checked against Bitcoin Core 31.1';

const C = { dark:'1B1F24', orange:'F7931A', ink:'1F2933', mute:'5B6B7B', card:'F4F2EE', code:'15191E',
            codeTxt:'E6EDF3', green:'7EE787', white:'FFFFFF', slate:'3A4250', line:'D9D4CC', pale:'FBF9F6' };
const H = 'Cambria', B = 'Calibri', M = 'Courier New';
const BK = 'Antonopoulos and Harding, 2023';
const COURSE = 'SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University';

let nContent = 0, nCode = 0;

function chip(s, x, y) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y, w:0.62, h:0.42, fill:{color:C.orange}, line:{color:C.orange}, rectRadius:0.08});
  s.addText('₿', {x, y, w:0.62, h:0.42, fontFace:B, fontSize:18, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
}
function light() { const s = pres.addSlide(); s.background = {color:C.white}; return s; }
function dark() { const s = pres.addSlide(); s.background = {color:C.dark}; return s; }
function title(s, t, sub) {
  chip(s, 0.5, 0.38);
  s.addText(t, {x:1.25, y:0.28, w:8.25, h:0.62, fontFace:H, fontSize:t.length > 46 ? 22 : 26, bold:true, color:C.dark, margin:0, valign:'middle', isTextBox:true});
  if (sub) s.addText(sub, {x:1.25, y:0.88, w:8.25, h:0.32, fontFace:B, fontSize:12.5, italic:true, color:C.mute, margin:0, isTextBox:true});
}
function card(s, x, y, w, h, head, body, accent, fs) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y, w, h, fill:{color:C.card}, line:{color:C.card}, rectRadius:0.1});
  s.addText(head, {x:x+0.22, y:y+0.13, w:w-0.44, h:0.36, fontFace:H, fontSize:15, bold:true, color:accent || C.orange, margin:0, isTextBox:true});
  s.addText(body, {x:x+0.22, y:y+0.5, w:w-0.44, h:h-0.62, fontFace:B, fontSize:fs || 13.5, color:C.ink, margin:0, valign:'top', lineSpacingMultiple:1.02, isTextBox:true});
}
// rows: [statement, printed answer]; an empty answer prints nothing, as in a Python session after a statement
function codeCard(s, rows, x, y, w) {
  let lines = 0, widest = 0;
  rows.forEach(([c, r]) => { lines += (r === '' ? 1 : 2); widest = Math.max(widest, c.length + 4, r.length); });
  let fs = widest <= 62 ? 12.5 : widest <= 72 ? 11.5 : widest <= 82 ? 10.5 : widest <= 90 ? 9.8 : 9.2;
  while (fs > 8.5 && 0.26 + lines * fs * 0.0175 > CODEMAX) fs -= 0.3;   // then shrink until every line fits the box
  const h = Math.min(CODEMAX, 0.26 + lines * fs * 0.0175);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y, w, h, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.1});
  const runs = [];
  rows.forEach(([c, r], i) => {
    const last = i === rows.length - 1;
    runs.push({text:'>>> ', options:{color:C.orange, bold:true}});
    runs.push({text:c, options:{color:C.codeTxt, breakLine:!(last && r === '')}});
    if (r !== '') runs.push({text:r, options:{color:C.green, breakLine:!last}});
  });
  s.addText(runs, {x:x+0.18, y:y+0.1, w:w-0.36, h:h-0.2, fontFace:M, fontSize:fs, valign:'top', margin:0, paraSpaceAfter:0, isTextBox:true});
  nCode += rows.length;
  return y + h;
}
function table(s, rows, x, y, w, colW, fs, rowH) {
  const tb = rows.map((r, i) => r.map(t => i === 0 ? {text:t, options:{bold:true, color:C.white, fill:{color:C.dark}}} : {text:t}));
  s.addTable(tb, {x, y, w, colW, fontFace:B, fontSize:fs || 12, color:C.ink, border:{type:'solid', pt:0.5, color:C.line}, rowH:rowH || 0.34, valign:'middle'});
}
function sourceLine(s, src) {
  if (!src) return;
  s.addText('Sources: ' + src.join('; '), {x:0.5, y:5.26, w:9, h:0.24, fontFace:B, fontSize:9, italic:true, color:C.mute, margin:0, isTextBox:true});
}
function pyCaption(s, y) {
  s.addText('executed under Python ' + PY + ' · examples_out_v' + VERSION.replace(/\./g, '_') + '.json',
    {x:0.5, y:y, w:9, h:0.22, fontFace:B, fontSize:9, italic:true, color:C.mute, align:'right', margin:0, isTextBox:true});
}
// one connected tree: a parent box on the left, its children in a column, one elbow line each
function tree(s, parent, children, x, y, w, h, colour) {
  const px = x, pw = 2.5, ph = Math.min(0.9, h);
  const py = y + (h - ph) / 2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x:px, y:py, w:pw, h:ph, fill:{color:colour || C.orange}, line:{color:colour || C.orange}, rectRadius:0.08});
  s.addText(parent, {x:px+0.08, y:py, w:pw-0.16, h:ph, fontFace:H, fontSize:13.5, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
  const cols = children.length > 7 ? 2 : 1;
  const per = Math.ceil(children.length / cols);
  const cw = (w - pw - 0.55) / cols - (cols > 1 ? 0.12 : 0);
  const ch = Math.min(0.46, (h - 0.04 * (per - 1)) / per);
  const spine = px + pw + 0.22;
  s.addShape(pres.shapes.LINE, {x:px+pw, y:py+ph/2, w:0.22, h:0, line:{color:C.mute, width:1}});
  s.addShape(pres.shapes.LINE, {x:spine, y:y, w:0, h:h, line:{color:C.mute, width:1}});
  children.forEach((t, i) => {
    const col = Math.floor(i / per), row = i % per;
    const cy = y + row * (ch + 0.04);
    const cx = spine + 0.3 + col * (cw + 0.24);
    if (col === 0) s.addShape(pres.shapes.LINE, {x:spine, y:cy+ch/2, w:0.3, h:0, line:{color:C.mute, width:1}});
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x:cx, y:cy, w:cw, h:ch, fill:{color:C.pale}, line:{color:C.line, width:1}, rectRadius:0.06});
    s.addText(t, {x:cx+0.06, y:cy, w:cw-0.12, h:ch, fontFace:B, fontSize:t.length > 34 ? 9.5 : t.length > 26 ? 10.5 : 11.5, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true});
  });
}

// ---------------- the deck's content, in the order of the chapter 5 taxonomy ----------------
// Each concept: id (the taxonomy identifier, and the key of its executed example), t (its human label), sub (the
// worked example's own one-line title), def (the explanation, compressed from the concept's paragraphs for speaking),
// take (the sentence to leave on the screen), note (the speaker's notes), src (the author-year citations), and
// optionally tbl (a table instead of, or beside, the code) and nocode.
const CH = [];

// ============================== BRANCH 1: WALLET KEYS ==============================
CH.push({
  id:'WalletKeys', t:'Wallet keys', sub:'What a wallet really contains, and where its keys come from',
  lead:'The chapter opens by correcting a belief borrowed from cash. A wallet database holds only keys; the coins are outputs recorded on the blockchain, and a person owns an output only as long as she can prove control of the key that guards it. A lost leather wallet takes its banknotes with it; a lost wallet database never contained any bitcoins at all.',
  note:'Say at the start that the word wallet is used for three different things in this chapter: the database of keys, the application that reads and writes it, and the hardware device that signs. Every sentence about wallets should be read with the question of which of the three is meant. The second half of the branch is the history that the rest of the chapter depends on: independent keys, then a seed, then a tree of keys derived from that seed.',
  src:[BK + ', chapter 5, Wallet Technology Overview'],
  groups:[
  { id:'WalletContents', t:'Wallet contents', lead:'What is inside a Bitcoin wallet and what is not: a database of keys, sometimes only the public ones, and a signer that may live somewhere else entirely.',
    note:'Security and convenience pull in opposite directions throughout this group. An application on a phone or a web server is exposed to theft and mistakes; a device that keeps the private keys offline is safer and clumsier. Every arrangement in the rest of the chapter is a point between those two.',
    items:[
    { id:'WalletDatabase', t:'Wallet database', sub:'a file of keys, not of coins',
      def:'A wallet database is the stored collection of keys, and the notes about them, that a wallet application reads and writes. The book prefers that name over Bitcoin wallet so that the data can be told apart from the programs. The database contains only keys; the bitcoins those keys control are outputs recorded on the blockchain, where everybody can see them and nobody but the key holder can move them.',
      take:'The fresh Bitcoin Core wallet made for this chapter holds eight descriptors and no coins at all.',
      note:'The evidence on the slide is a real wallet created offline for this chapter: eight descriptors, four script kinds, and a declared range of a thousand indices each, eight thousand prepared scripts in total. Nothing in that file is money. Correct the shorthand that causes the trouble: the sentence "the wallet holds the coins" hides the real situation, and the same hidden assumption leads people to protect the application, which can be reinstalled, while neglecting the database or the seed, which cannot.',
      src:[BK + ', Wallet Technology Overview', 'Bitcoin Core, 2026'] },
    { id:'PublicKeyOnlyWallet', t:'Wallet with public keys only', sub:'receiving without the power to spend',
      def:'Not every wallet database holds what a spending transaction needs. Some contain only public keys, and others only some of the private keys required to authorise a spend. An application working with such a database can see the payments made to its public keys and show them to the user, but it cannot produce the signatures that spending demands.',
      take:'From the chapter’s own extended public key, a receiving address, derived with no private key in sight.',
      note:'Run the example as the merchant’s web server would: take the account’s extended public key, derive the first key of the receiving branch, and turn it into an address. The last line shows what is actually stored, a compressed public key beginning with the byte 2. Then give the caution the standard gives: such a database is not worthless to an attacker, because anyone holding an extended public key can derive every address below it and read the whole history of payments they received.',
      src:[BK + ', Wallet Technology Overview', 'Wuille, 2012'] },
    { id:'ExternalSigning', t:'External signing', sub:'the application builds, the device signs',
      def:'External signing means that the program preparing a transaction is not the one that signs it. The wallet application, which knows only public data, assembles an unsigned transaction; a hardware signing device, or another participant in a multisignature arrangement, holds the private key and returns the signature. The reason is the difference in exposure: a phone or a laptop installs software of uncertain origin, while a device built only to sign is a much smaller target.',
      take:'The frontend can check the signature with the public key alone; it never sees the private one.',
      note:'The example separates the two roles deliberately: the device holds the key and makes the signature, the frontend holds only the public key and verifies. That verification is the same operation a node performs. Then name the limit: external signing protects the keys and not the user’s judgement. A signer can only sign what it is shown, so the transaction the device displays must be read by the person, because a compromised application may have built one that pays somebody else.',
      src:[BK + ', Wallet Technology Overview'] } ] },
  { id:'KeyGenerationMethods', t:'Key generation methods', lead:'The way a wallet produces its keys decides what the user has to back up: every key separately, or one seed once.',
    note:'This group is the history of the whole chapter in five steps. Each step removes a backup problem and introduces a new question, and the last of them, the tree, is what the second half of the chapter is about.',
    items:[
    { id:'IndependentKeyGeneration', t:'Independent key generation', sub:'every key backed up on its own',
      def:'In independent key generation a wallet creates each key separately from fresh random data, with no connection between them, and the database is simply the collection. All the early Bitcoin wallets worked this way. The weakness is the backup: the user had to save the database again every time a new key was generated and handed out, which could be as often as every new payment.',
      take:'A thousand keys of 32 bytes are 32,000 bytes of backup, and every further key adds 32 more.',
      note:'The arithmetic is trivial and the consequence is not: a backup that goes stale on every payment is a backup people stop making. That is the behaviour the chapter blames for a generation of lost coins. Add the point that matters when someone inherits an old wallet file: independent keys cannot be regenerated from any recovery code, so the only backup is a copy of the database itself, and the first question to ask of an old file is whether its keys came from a seed.',
      src:[BK + ', Wallet Technology Overview'] },
    { id:'Seed', t:'Seed', sub:'one random value behind everything',
      def:'A seed is the starting value of a deterministic wallet: a large random number, usually 128 to 256 bits, from which every key is computed by a repeatable procedure. Recording the seed and the name of the algorithm therefore backs up every key the wallet will ever derive. The hierarchical standard accepts 128 to 512 bits and advises 256.',
      take:'The chapter’s own example seed is 64 hexadecimal digits, which is 256 bits; a BIP39 seed is 512.',
      note:'Keep the two numbers on the slide apart, because students merge them: the chapter’s hashed-seed example is 256 bits, while the seed that BIP39 actually produces is 512 bits, the full output of one HMAC-SHA512 block. Then give the warning the chapter gives when it contrasts recovery codes with brainwallets: a seed is only as good as its randomness, humans are very poor sources of it, and the seed must be created by the wallet rather than chosen by the user.',
      src:[BK + ', Wallet Technology Overview', 'Wuille, 2012'] },
    { id:'DeterministicKeyGeneration', t:'Deterministic key generation', sub:'the seed hashed with a counter',
      def:'Deterministic key generation computes keys from the seed by a fixed rule instead of drawing a new random number each time. The book demonstrates it with a hash function: hashing the text of the seed together with 0, 1 and 2 gives three seemingly random values, and the same seed always gives the same three. A cryptographic hash function is repeatable, changes unpredictably when its input changes, and cannot be run backwards, which is exactly what the rule needs.',
      take:'The three derived values begin 50b18e0b, a965dbcd and 19580c97, as the book prints them.',
      note:'Note the detail that trips people up when they try the book’s command: the text hashed includes the line break that the shell’s echo adds, which is why the example builds the bytes explicitly. Then say what is wrong with this scheme as a wallet: it produces one sequence of keys and it cannot derive public keys separately from private ones, which is the flexibility the next concepts add.',
      src:[BK + ', Wallet Technology Overview'] },
    { id:'KeyTweak', t:'Key tweak', sub:'adding the same value to both sides',
      def:'A key tweak is a number added to a key to produce a related key. Because a public key is the private key multiplied by the generator point, adding t times the generator to a public key gives exactly the public key of the private key increased by t. The same tweak therefore moves both halves of a pair in step, and whoever knows only the public key can compute the child public key.',
      take:'Adding the generator 123 times to the public key of 5 gives the public key of 128.',
      note:'This one line of arithmetic is the whole reason an online shop can hand out fresh addresses without holding a key that can spend. Work it through on the board with the small numbers on the slide before the class meets the real derivation. Then give the caution: a tweak is only as private as the rule that produces it. If tweaks are public, anyone with the parent public key can compute every child, and anyone who learns a child private key can subtract the tweak and recover the parent.',
      src:[BK + ', Wallet Technology Overview'] },
    { id:'HdKeyGeneration', t:'Hierarchical deterministic generation', sub:'a tree of keys under one seed',
      def:'Hierarchical deterministic generation, standardised as BIP32, derives a tree from one seed: any key may be the parent of a sequence of children, any child may be a parent in turn, and there is no limit on the depth. Public keys can be derived without the private ones. Every modern wallet the book’s authors know of uses it by default.',
      take:'Each key has 2 to the 31 normal children and 2 to the 31 hardened ones: about four billion in all.',
      note:'Explain why a tree rather than a list: a single chain of keys can only be shared all or nothing, while an owner usually wants to share some public keys and no private ones. Then flag the cost that the fifth branch of this chapter is entirely about: a tree is enormous, nothing marks which parts of it a wallet used, and a recovery therefore needs to know the paths as well as the seed.',
      src:[BK + ', Wallet Technology Overview', 'Wuille, 2012'] } ] } ] });

// ============================== BRANCH 2: RECOVERY CODES ==============================
CH.push({
  id:'RecoveryCodes', t:'Recovery codes', sub:'The written form of a seed, and the choices behind it',
  lead:'A recovery code is the short written form of a wallet’s seed: a sequence of words, or in one case a string of letters and digits, from which every key can be computed again. It is the one thing a user is asked to keep, and keeping it is the whole of the backup. If the database is lost, every key can be regenerated from the code; if someone else obtains the code, they can regenerate the same keys and take everything.',
  note:'Clear away two confusions before the detail begins. A recovery code is not a password: it is not chosen by the user, it is generated from randomness by the wallet, and it cannot be changed without moving the money, except in the one scheme that enciphers its own seed. And it is not a brainwallet, which is the next group’s subject. The first group compares the schemes; the second collects the decisions that choosing a scheme does not settle.',
  src:[BK + ', chapter 5, Seeds and Recovery Codes'],
  groups:[
  { id:'CodeSchemes', t:'Recovery code schemes', lead:'The five schemes the chapter lists as in wide use, and the sixth it adds in a note: they differ in what the words encode, whether a version travels with them, and whether one code is enough.',
    note:'A student who learns only BIP39 will misread the others. Keep four questions in view through the group: does the code encode the seed or a ciphertext, does it carry a version number, does its checksum cover the passphrase, and is one code enough or must several be collected.',
    items:[
    { id:'Bip39Code', t:'BIP39 recovery code', sub:'12 to 24 words for 128 to 256 bits',
      def:'A BIP39 code is a word sequence encoding a random number together with a short checksum, from which a 512-bit seed is derived. The wallet generates random bytes, appends a checksum, and reads the result in groups of eleven bits, each group an index into a list of 2,048 words. People transcribe words far better than hexadecimal, and the standard’s own motivation is that such a sentence can be written on paper or spoken over the telephone.',
      take:'The chapter’s 128 bits of entropy encode and decode to exactly the twelve words it prints.',
      note:'The round trip on the slide is the point: entropy to words and back, with the checksum confirming. Run it both ways with the class. Then list the shortcomings the standard itself names, because they are the reason the other five schemes exist: the seed depends on the word list, since the words rather than the entropy are hashed, so a translated code gives a different wallet; the conversion is one-way; the checksum is short, missing about one random error in 256 and correcting none; and there is no versioning.',
      src:[BK + ', Seeds and Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'ElectrumV2Code', t:'Electrum version 2 code', sub:'a version number inside the phrase',
      def:'Electrum’s scheme from version 2.0 derives both the master key and a version number from a keyed hash of the normalised phrase, so it needs no fixed global word list and can tell an old code from a new one. The phrase is reduced to single spaces with diacritics removed and hashed with HMAC-SHA512 under the key "Seed version"; the leading digits of that hash are the version.',
      take:'The chapter’s BIP39 words hash to c7d284c2…, which is neither Electrum version.',
      note:'The computation on the slide is the honest demonstration of the mechanism: the book’s own twelve words are a perfectly good BIP39 code and carry neither of Electrum’s registered prefixes, 01 for standard and 100 for segwit, which is exactly how Electrum tells the schemes apart and why it refuses to generate BIP39 codes at all. Give the cost the Electrum document itself states: imposing a prefix does not reduce the entropy of the seed, but it does let an attacker reject a wrong candidate before paying for the key stretching.',
      src:[BK + ', Seeds and Recovery Codes', 'Electrum Technologies, 2026'] },
    { id:'AezeedCode', t:'Aezeed cipher seed', sub:'19 bytes of plaintext, enciphered',
      def:'Aezeed, the recovery code of the lnd wallet, does not encode the seed directly: it enciphers a plaintext of one byte of internal version, two bytes of timestamp and sixteen bytes of entropy under a key stretched from the user’s passphrase with scrypt, using an authenticated cipher with a 64-bit checksum, and encodes the result as 24 words. It therefore carries two version numbers and a wallet birthday, and the passphrase can be changed without moving any funds.',
      take:'Version, salt, ciphertext and tag come to 33 bytes, which is exactly 24 words of eleven bits.',
      note:'The second computation is worth doing with the class because it shows why the code is 24 words rather than some other number: 33 bytes are 264 bits, and 264 divided by 11 is 24. Then bring out the trade-off that the deniability slide will return to. Because Aezeed authenticates the passphrase and reports an error for a wrong one, it gains error detection and loses plausible deniability, and it becomes possible to prove that a passphrase has been revealed.',
      src:[BK + ', Seeds and Recovery Codes', 'Lightning Labs, 2026a'] },
    { id:'MuunCode', t:'Muun recovery code', sub:'a key to a printed kit, not a seed',
      def:'The Muun code is the odd one in the list: it is not words, and it is not the seed. The wallet requires several signatures to spend, so one seed could never restore it; instead the user is given a document containing the private keys in encrypted form, and the code is what decrypts them. The two objects are useless apart, and the recovery tool needs no cooperation from the company.',
      take:'Muun’s own tool states that the process requires no collaboration from Muun to work.',
      note:'Both lines on the slide are read out of the saved copy of Muun’s own document rather than quoted from memory, which is the method this deck follows everywhere. Make the structural point, since it generalises: a wallet whose spending needs several keys cannot be restored from one seed, because the other participants’ public keys are not derivable from it. Then the weakness the shape implies: two objects must both survive, and keeping the kit and the code in one place defeats the separation entirely.',
      src:[BK + ', Seeds and Recovery Codes', 'Muun, 2026'] },
    { id:'Slip39Code', t:'SLIP39 share set', sub:'several codes, a threshold of them needed',
      def:'SLIP39 distributes one seed over several word codes with a threshold: five codes may be made of which any three recover the seed, while any two reveal nothing about it. The mathematics is polynomial interpolation over a finite field: a polynomial of degree below the threshold is built, each holder receives one point of it, and any threshold-many points determine it exactly.',
      take:'Three of the five shares recover the secret; two of them do not.',
      note:'The demonstration on the slide is a toy over a prime field rather than SLIP39’s own field of 256 elements, so that the arithmetic can be read; say so, and say why the shape is nevertheless right. The standard’s motivation is worth quoting: redundant backups raise the risk that a holder absconds with something valuable and liquid, and secret sharing distributes custody so that loss survives one or a few compromised parties. The risk is moved rather than removed: too low a threshold eases theft, too high eases loss.',
      src:[BK + ', Seeds and Recovery Codes', 'Rusnak et al., 2017'] },
    { id:'Codex32Code', t:'codex32 recovery code', sub:'a checksum a person can verify by hand',
      def:'codex32 writes a master seed in the bech32 alphabet with an error-correcting checksum designed to be verified with printed instructions, scissors and a pen, and it can split the seed into up to 31 shares with a threshold between 2 and 9. It is a draft proposal rather than a settled standard, written for a user who does not want to trust a computing device at all.',
      take:'The standard’s own 48-character example passes its checksum and yields its 16-byte payload.',
      note:'The three lines verify the proposal’s own published example end to end: its length, its checksum, and the seed bytes inside it. Use its comparison with BIP39 as the summary of why such proposals keep appearing: BIP39 has no error-correcting ability, cannot sensibly be extended to secret sharing, has no versioning or metadata, and makes interoperability harder through choices such as SHA-512 and eleven-bit words. Treat codex32 as one more point on a trade-off curve, not as a recommendation.',
      src:[BK + ', Seeds and Recovery Codes', 'Olsson Curr et al., 2023'] } ] },
  { id:'CodeTradeoffs', t:'Choices behind a recovery code', lead:'Whether to add a passphrase, whether deniability is a feature or a trap, why an invented phrase is not a code, how far memory can be trusted, and what a code is worth to someone prepared to use force.',
    note:'These are the decisions a user actually makes, and they cannot all be made well at once. The chapter’s own sidebar says that users and developers disagree about which approach is better, some strongly favouring deniability and others the error detection that helps novices and people under duress.',
    items:[
    { id:'RecoveryPassphrase', t:'Recovery code passphrase', sub:'a different wallet for every passphrase',
      def:'A passphrase is an extra secret the user supplies that enters the derivation of the seed; in BIP39 it is appended to the constant salt of the stretching function. Four of the schemes allow one. It creates a second factor, something memorised beside something written, and it allows a duress wallet: a chosen passphrase leading to a small balance that distracts an attacker from the real one.',
      take:'The same twelve words give 5b56c417… with no passphrase and 3b5df16d… with the chapter’s.',
      note:'The two seeds on the slide are the chapter’s own two tables, recomputed. Emphasise that neither is more correct than the other: the words are the password and the passphrase only changes the salt, so both are valid derivations. Then state the two failures the chapter states twice: if the owner is incapacitated or dead and nobody else knows the passphrase, the funds are gone for ever; and if the passphrase is kept beside the code, there is no second factor at all.',
      src:[BK + ', Recovery Code Passphrases', 'Palatinus et al., 2013'] },
    { id:'PlausibleDeniability', t:'Plausible deniability', sub:'every passphrase looks valid',
      def:'Plausible deniability is the property that any passphrase at all produces a working tree of keys, so a person who hands over a code, with or without a passphrase, cannot be shown to have withheld the one that holds the money. BIP39 claims the property in those words. It exists only because nothing checks the passphrase, which is why it cannot be had together with error detection.',
      take:'Three different passphrases, three different valid 64-byte seeds, and no way to tell which is meant.',
      note:'The positive case is real: a thief who takes a code but not the passphrase sees a valid tree, and an owner who sent a little money to the passphrase-free tree learns that the code has been compromised. Give the danger just as plainly, because the chapter does: a person coerced into revealing a code that does not hold the expected amount may simply go on being coerced, and designing for deniability means there is no way to prove that everything has been revealed. Deniability is a defence against a thief who has left, not against one still present.',
      src:[BK + ', Recovery Code Passphrases', 'Palatinus et al., 2013'] },
    { id:'Brainwallet', t:'Brainwallet', sub:'a phrase the user invented',
      def:'A brainwallet is a wallet whose seed comes from a phrase the user thought up. The chapter raises the term only to separate it from a recovery code: a code is created randomly by the wallet and shown to the user, where a brainwallet is chosen by the user, and that single difference decides whether the keys can be guessed, because humans are very poor sources of randomness.',
      take:'Twelve words drawn from a list of 2,048 carry 132 bits: 128 of entropy and 4 of checksum.',
      note:'The arithmetic on the slide measures what the wallet’s randomness buys, and the second line shows the same number reached the other way, from the standard’s two formulas. Ask the class how many bits they think a memorable invented sentence carries; the honest answer is usually under forty. End with the distinction the term invites people to blur: memorising a code the wallet generated keeps the randomness and risks only forgetting, while inventing a phrase destroys the randomness before anything else can go wrong.',
      src:[BK + ', Seeds and Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'Memorization', t:'Memorising a recovery code', sub:'words instead of hexadecimal',
      def:'Memorising a code means keeping it only in one’s head. The ability is a side effect of the encoding rather than a recommended practice: twelve to twenty-four ordinary words are within reach of rote learning where 32 hexadecimal digits are not, and the word list was designed to help, with unique four-letter prefixes and similar pairs avoided.',
      take:'Thirty-two hexadecimal characters against twelve words, none longer than seven letters.',
      note:'There is one situation in which memory is genuinely valuable and the chapter names it: a person who cannot carry physical belongings across a border without their being seized or inspected. For everyone else it is an edge case. Give the three failure modes the chapter gives, because they are the argument for writing the code down as well: a forgotten code with a lost database means the coins are gone; memory cannot be inherited; and a person believed to have memorised a code may be coerced.',
      src:[BK + ', Seeds and Recovery Codes'] },
    { id:'PhysicalCoercion', t:'Coercion and physical risk', sub:'a published record of attacks',
      def:'Coercion is the risk that someone obtains a code by threatening its holder rather than by breaking anything. The chapter cites a public record kept by Jameson Lopp documenting over a hundred physical attacks on suspected owners of bitcoin and other digital assets, including at least three deaths and numerous cases of torture, hostage-taking or threats to a family.',
      take:'The list says of itself that it is not comprehensive: many attacks are not publicly reported.',
      note:'This belongs in a technical chapter because it follows from a technical fact: payments are irreversible and a key cannot be frozen or reissued, so a code is a bearer instrument and whoever can state it can spend. The defences are organisational: a duress wallet with a small balance, a code distributed with SLIP39 or codex32 so that no one person can produce the whole secret, and, most effective of the three, not being believed to hold a code at all. Say clearly that the published figures are a lower bound on reported cases, not a measurement of anybody’s risk.',
      src:[BK + ', Seeds and Recovery Codes', 'Lopp, 2026'] },
    { id:'WalletBirthday', t:'Wallet birthday', sub:'a creation date inside the code',
      def:'A wallet birthday is the date the database was created, stored inside the recovery code itself, so that a restoration can scan the chain from that date instead of from the beginning. It is metadata rather than cryptography: nothing is protected by it, and a restoration is simply made cheaper. Aezeed spends two bytes on it, counted in days since Bitcoin’s genesis block.',
      take:'Two bytes of days from 2009 reach the year 2188, which is the limit Aezeed states.',
      note:'The arithmetic shows why two bytes are enough and the second line reads Aezeed’s own phrase for the unit out of its saved document. Without a birthday a restoration must assume the worst and examine the whole chain, which for a lightweight client means either a great deal of downloading or asking a server questions that reveal which addresses matter. Note the cost too: a birthday narrows the window in which a wallet’s transactions can be looked for, so it tells a reader of the code roughly when its owner started.',
      src:[BK + ', Seeds and Recovery Codes', 'Lightning Labs, 2026a'] } ] } ] });

// ============================== BRANCH 3: THE BIP39 STACK ==============================
CH.push({
  id:'Bip39Stack', t:'The BIP39 stack', sub:'Nine steps from random bytes to a 512-bit seed',
  lead:'Here the chapter stops surveying and works through one stack in detail: BIP39 recovery codes, BIP32 hierarchical derivation and BIP44-style implicit paths, all of them in place since 2014 or earlier. BIP39 itself is nine numbered steps in two halves: steps one to six make the code, steps seven to nine turn the code into a seed. Everything in this branch can be carried out by hand or in a few lines of Python.',
  note:'One point of order saves confusion later: the standard calls the words a mnemonic and the chapter calls them a recovery code; they are the same thing, and this course uses the chapter’s term except when quoting. The three tables the chapter prints are the targets of this branch, and every one of them is recomputed on the slides that follow.',
  src:[BK + ', chapter 5, Recovery Codes', 'Palatinus et al., 2013'],
  groups:[
  { id:'CodeGeneration', t:'Generating a recovery code', lead:'Six steps: random entropy, a checksum taken from its hash, the two joined, cut into groups of eleven bits, each group mapped to one of 2,048 words.',
    note:'The order of the steps is not arbitrary and following it answers the questions that otherwise look like magic: why 2,048 words rather than a thousand, why 12 words and not 13, and why a single mistyped word is usually caught.',
    items:[
    { id:'Entropy', t:'Entropy', sub:'128 random bits in sixteen bytes',
      def:'Entropy here is the amount of unpredictability in a value, counted in bits: 128 bits of entropy means an attacker could only find the value by searching among 2 to the 128 equally likely possibilities. It is the random input of the whole process and the only secret in it. The standard requires a multiple of 32 bits, between 128 and 256, and notes that more entropy improves security and lengthens the sentence.',
      take:'The chapter’s sixteen bytes are 128 bits, about 3.4 times 10 to the 38 possibilities.',
      note:'Entropy cannot be added later, and no amount of hashing creates it: a function can stretch what is already there, which is what the whole stack does. Name the misconception the chapter’s own sidebar disposes of, because students assume the opposite: there is no apparent benefit in more than 128 bits, since the security strength of a Bitcoin public key is 128 bits; the one secondary benefit arises when an attacker sees part of a code, and the chapter does not recommend relying on it.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'Bip39Checksum', t:'BIP39 checksum', sub:'the first bits of a SHA-256 hash',
      def:'The checksum is the first entropy-length-over-32 bits of the SHA-256 hash of the entropy, appended to it. For 128 bits of entropy that is four bits, which brings the total to 132, a multiple of eleven. Without it, any twelve words from the list would be a valid code and a single wrong word would silently open a different, empty wallet.',
      take:'The chapter’s entropy hashes to a first byte whose leading four bits are 0111.',
      note:'Compute the four bits with the class from the first byte of the digest; it is the kind of step students believe only once they have done it. Then be candid as the standard is: this checksum is weak because it is short. About one random error in 256 passes it, and it can give no assistance at all in correcting an error, which is one of the complaints that codex32 and the other schemes answer.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'WordList', t:'Word list', sub:'2,048 words, eleven bits each',
      def:'The word list is the dictionary the bits are read against. The number is a round binary one rather than a round decimal one: 2 to the eleventh is 2,048, so one word carries exactly eleven bits and nothing is wasted. The standard’s criteria are that the first four letters identify a word unambiguously, that similar pairs such as build and built are avoided, and that the list is sorted so that implementations can search it.',
      take:'Positions 96, 1929 and 459 hold army, van and defense: the chapter’s first three words.',
      note:'The three lookups on the slide are the bridge to the next concept, which computes those same three numbers from the entropy. The last line checks that the shipped list really is sorted. Then give the best-known weakness: because the words rather than the entropy are hashed to make the seed, translating a code to another list necessarily produces a completely different seed, which is why the standard strongly discourages non-English lists.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'BitSegment', t:'Eleven-bit segment', sub:'where the words come from',
      def:'An eleven-bit segment is one group of the bit string that becomes one word. The entropy with its checksum appended is cut into such groups, and each group’s value, a number from 0 to 2,047, indexes the list. Eleven does not divide eight, so a segment generally straddles two bytes, which is why an implementation works on a bit string rather than on bytes.',
      take:'The first three segments are 96, 1929 and 459, and those are army, van and defense.',
      note:'This is the slide on which a recovery code stops being a sentence and becomes a number written in base 2,048, with a few check digits at the end. Make that statement explicitly. Then warn against the trap it invites: the segments do not correspond to fixed parts of the entropy in any way that would let one word be corrected on its own, because they cross byte boundaries and the last segment mixes entropy with checksum.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'CodeLength', t:'Code length', sub:'the chapter’s table, recomputed',
      def:'The length of a code is not a free choice: the checksum is a thirty-second of the entropy, and the number of words is the total divided by eleven. Because the entropy is always a multiple of 32, the division comes out whole. Twelve words therefore mean 128 bits of entropy and twenty-four words mean 256.',
      take:'All five rows of the chapter’s table follow from its two formulas, exactly.',
      note:'Derive one row with the class and then show the whole table computed in a single line. The useful thing a student takes away is that the number of words is a statement about entropy, so a 24-word code is not twice as safe as a 12-word one in any way that matters. The chapter’s sidebar says why: extended private keys hold at most 512 bits, slightly fewer than 2 to the 256 private keys exist, and the security strength of a public key is 128 bits.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] },
    { id:'TextNormalization', t:'Text normalisation', sub:'one character, two code points',
      def:'Normalisation rewrites text in one agreed form before it is used as data, because the same visible characters can be stored in more than one way. BIP39 requires compatibility decomposition, NFKD, in UTF-8, for both the words and the passphrase. Without the rule, two wallets could disagree about a code that looks identical on both screens, since the seed comes from hashing the text.',
      take:'The single character e-acute becomes two code points after normalisation, e then a combining accent.',
      note:'Show the bytes as well as the lengths, because that is what is hashed. Then name the failure mode, which is nastier than most: a wrong normalisation produces a perfectly valid-looking seed for an empty wallet, exactly like a mistyped passphrase, and the checksum cannot help because it is computed over the entropy and not over the text.',
      src:[BK + ', Recovery Codes', 'Palatinus et al., 2013'] } ] },
  { id:'SeedDerivation', t:'From the code to the seed', lead:'The last three steps: the words are the password, the constant mnemonic plus any passphrase is the salt, and 2,048 rounds of HMAC-SHA512 give the 512-bit seed.',
    note:'This is where a passphrase can be added and where the one-way step happens. The output is not the entropy that went in; it is 512 bits derived from it, which is why an arbitrary BIP32 seed cannot be written as a BIP39 code.',
    items:[
    { id:'KeyStretchingFunction', t:'Key-stretching function', sub:'deliberately slow, on purpose',
      def:'A key-stretching function turns a secret into a key and is made deliberately expensive to compute, so that every guess an attacker makes costs more. The word stretching refers to the cost rather than the length: the output could be produced far more cheaply and is not. BIP39 uses 2,048 rounds, which multiplies an attacker’s work by 2,048 and the honest user’s by the same.',
      take:'2,048 rounds is about 11 bits of extra work: useful beside 64 bits, irrelevant beside 128.',
      note:'The chapter is unusually precise about what stretching does and does not buy, and the class should hear all of it: the rounds make brute-forcing a code slightly harder in software and barely affect special-purpose hardware; for an attacker who must guess a whole code the 128-bit minimum is already more than sufficient; and the real benefit appears only where an attacker has learned part of a code. That is why the parameters are low: every restoration pays the cost too.',
      src:[BK + ', From Recovery Code to Seed'] },
    { id:'Pbkdf2', t:'PBKDF2', sub:'the book’s first seed, recomputed',
      def:'PBKDF2 is the standard password-based key derivation function of PKCS #5, and BIP39 fixes all four of its inputs: the sentence is the password, the string mnemonic followed by the passphrase is the salt, the iteration count is 2,048, HMAC-SHA512 is the underlying function, and the derived key is 64 bytes. Naming a standard function rather than inventing one is what makes a code portable between wallets.',
      take:'The chapter’s twelve words give a seed beginning 5b56c417303faa3f, exactly as printed.',
      note:'Point out that this reproduction needs nothing but Python’s standard library, which is the practical meaning of portability. The third line is the error every implementer meets first: the password must be bytes, and the encoding is the programmer’s choice, which is why normalisation had to be settled on the previous slide. Add the other order-of-arguments trap: the words are the password and the salted constant is the salt, and swapping them yields a valid-looking but wrong seed that no checksum will catch.',
      src:[BK + ', From Recovery Code to Seed', 'Moriarty et al., 2017', 'Palatinus et al., 2013'] },
    { id:'Salt', t:'Salt', sub:'the constant mnemonic, plus any passphrase',
      def:'A salt is the second, non-secret input of a key derivation function. Classically it makes precomputed tables useless, because a given password yields a different key under every salt. BIP39 gives it a second job: the salt is the string mnemonic followed by the optional passphrase, so the passphrase enters the derivation here and nowhere else.',
      take:'Same words, two salts, two seeds: the chapter’s two tables side by side.',
      note:'Note what BIP39 gives up. A classical salt is random and stored beside the derived key, so two users with the same password get different keys; BIP39’s salt is a fixed constant whenever no passphrase is used, so every wallet in the world shares it, and the protection against precomputation comes from the 128 bits of entropy in the words rather than from the salt. Because the salt enters the first link of the chain, changing one character of it changes the whole output.',
      src:[BK + ', From Recovery Code to Seed', 'Moriarty et al., 2017'] },
    { id:'RootSeed', t:'Root seed', sub:'512 bits, that is 64 bytes',
      def:'The root seed is the single number that stands for a whole wallet, and the input of the next branch. BIP39 produces one of 512 bits; BIP32 accepts 128 to 512. Every key in the wallet is derived from it, which is what makes it possible to re-create a wallet of thousands of keys in any compatible software by transferring only the code the seed came from.',
      take:'Sixty-four bytes, and nothing else in the wallet is random.',
      note:'Keep the seed and the code apart in the students’ minds, because the difference decides which software can do what: the code is an encoding of the entropy, the seed is the stretched result, and the mapping is one-way, so a wallet that imports a seed directly can never show the user words for it. One sentence of the next branch belongs here as a bridge: the seed is given to HMAC-SHA512 under a fixed key, and the two halves of the result become the master private key and the master chain code.',
      src:[BK + ', From Recovery Code to Seed', 'Wuille, 2012'] },
    { id:'Bip39Passphrase', t:'Optional passphrase in BIP39', sub:'the book’s second seed, recomputed',
      def:'The optional passphrase is appended to the constant salt, so the same words give a different 512-bit seed for every passphrase. There is essentially no wrong passphrase: all of them are valid and all lead to different seeds, forming a set so large that no one could brute-force or stumble upon one that is in use.',
      take:'One character short of the chapter’s passphrase gives an entirely different, perfectly valid seed.',
      note:'The second line is the slide’s whole lesson, so set it up: ask the class to predict what happens if the passphrase is mistyped by one character. The answer is not an error message but another valid wallet, empty. Repeat the three risks where the mechanism is visible: a forgotten passphrase is an unrecoverable loss because nothing in the code hints that one exists; a passphrase stored with the code is no second factor; and no checksum anywhere covers it.',
      src:[BK + ', From Recovery Code to Seed', 'Palatinus et al., 2013'] },
    { id:'SecurityStrength', t:'Security strength', sub:'512, 256 and 128 bits',
      def:'Security strength is the work an attacker needs, in bits. The chapter’s sidebar gives three numbers: an extended private key holds 512 bits, a private key 256, and the elliptic curve offers about 128, because the best known attack on the discrete logarithm problem costs about the square root of the group size. More than 128 bits of entropy therefore protects a key that can be attacked with 2 to the 128 work.',
      take:'About 3.4 times 10 to the 38 operations: that is what 128 bits of strength means.',
      note:'Turn the exponent into a decimal figure, as the slide does, because the exponent persuades nobody. Give the one genuine benefit of more entropy that the sidebar names, and the caution that goes with it: if a fixed fraction of a code is seen, half of a 128-bit code is plausibly brute-forcible while half of a 256-bit code is not, but the chapter does not recommend relying on that and prefers keeping codes safe or distributing them. Finish by saying what these numbers do not cover: coercion and data loss, which are the rest of the chapter.',
      src:[BK + ', From Recovery Code to Seed', 'Wuille, 2012'] } ] } ] });

// ============================== BRANCH 4: HIERARCHICAL DETERMINISTIC WALLET ==============================
CH.push({
  id:'HdWallet', t:'Hierarchical deterministic wallet', sub:'One seed, one keyed hash, and a tree without end',
  lead:'An HD wallet is one whose keys form a tree, every node computed from the seed by the rule of BIP32. A single seed is a good backup only if everything else can be recomputed from it, and this is the rule by which it is recomputed. The branch takes the tree in four steps: the master keys, the function that makes a child, the extended key that a wallet actually passes around, and the notation that says which key is meant.',
  note:'One warning covers the whole branch and the next one answers it: the tree is enormous, with about four billion first-level keys each having four billion children, and nothing marks which parts a wallet used. Recovering from data loss therefore needs more than the recovery code and the algorithms; it needs to know which paths were used.',

  src:[BK + ', chapter 5, Hierarchical Deterministic Wallets', 'Wuille, 2012'],
  groups:[
  { id:'MasterKeys', t:'Master keys from the seed', lead:'One call of HMAC-SHA512 under the fixed key "Bitcoin seed" turns the seed into the root of the tree: the left half is the master private key, the right half the master chain code.',
    note:'Everything below the root is derived, so if these two are right the whole tree is right, and if either is wrong nothing below it is recoverable. The examples use BIP32’s own first test vector so that students can check them against the standard.',
    items:[
    { id:'HmacSha512', t:'HMAC-SHA512', sub:'a keyed hash, split in half',
      def:'HMAC is a way of using an ordinary hash function with a key, so that the output depends on both; with SHA-512 the output is 64 bytes. BIP32 always divides that output into two halves of 32 bytes, using the left as key material and the right as a chain code. A keyed hash is needed because a plain hash would not keep the tree private: mixing in a second secret value makes derivation depend on more than the key itself.',
      take:'The test vector’s seed hashes to 64 bytes beginning e8f32e723decf405.',
      note:'Two confusions arise here and both are worth stating before they happen. The chain code is the key of the HMAC and the key material is part of the message, which is the reverse of what the names suggest, and swapping them yields a plausible but incompatible wallet. The third line is the error that enforces the first point in practice: the key must be bytes. Say that this same function appears three times in the chapter, for the master keys, for a normal child and for a hardened child.',
      src:[BK + ', Creating an HD Wallet from the Seed', 'Krawczyk et al., 1997', 'Wuille, 2012'] },
    { id:'MasterPrivateKey', t:'Master private key', sub:'the left half, read as a number',
      def:'The master private key, written m, is the left 32 bytes of that hash read as a 256-bit number. It is the root of the tree and the one key from which every other can be reached, so its loss or leak is total: knowing an extended private key allows reconstruction of every descendant key, private and public. BIP32 rejects the seed if the number is zero or not below the curve order, which happens with vanishing probability.',
      take:'BIP32’s first test vector gives the master key e8f32e72…436b35, and it lies in range.',
      note:'Have the class compare the printed value with the standard’s published vector; agreeing with a document nobody in the room wrote is the point of test vectors. Keep the seed and this key apart: the seed can be shorter and is what a recovery code encodes, while the master key is derived from it and cannot be turned back into it. Mention where the key is met in practice, as the string beginning xprv and as the letter m at the head of every path.',
      src:[BK + ', Creating an HD Wallet from the Seed', 'Wuille, 2012'] },
    { id:'MasterChainCode', t:'Master chain code', sub:'the right half, 256 bits of extra entropy',
      def:'The master chain code is the second half of the same hash, 32 bytes that travel beside the key and take part in deriving its children. Both private and public keys are extended with it, and it is identical for the two halves of one pair. Without it, knowing an index and a child key would be enough to derive other children; with it, a child key alone cannot find its siblings.',
      take:'The test vector’s chain code, 873dff81…d37d508, is 256 bits beside a 256-bit key.',
      note:'The chain code is the part users forget, and forgetting it is fatal in two directions: a key without its chain code can derive nothing, and a chain code that leaks beside a child private key can expose the rest of a branch. Say plainly that it is secret even though it is not a key. BIP32’s own implications section is the authority: leaking a private key means access to coins, leaking a public key can mean loss of privacy, and extended keys need more care because they stand for a whole subtree.',
      src:[BK + ', Creating an HD Wallet from the Seed', 'Wuille, 2012'] } ] },
  { id:'ChildDerivation', t:'Deriving child keys', lead:'One function, differing only in what is fed to it, generates the whole tree from a key, a chain code and an index.',
    note:'This group is the mathematical centre of the chapter. Everything that makes an HD wallet useful follows from how its three variants relate: handing a server an extended public key, keeping private keys on a device that never sees the internet, restoring a whole wallet from one code.',
    items:[
    { id:'ChildKeyDerivation', t:'Child key derivation', sub:'512 bits split into two halves',
      def:'A child is derived by hashing the parent key, the parent chain code and a 32-bit index with HMAC-SHA512 and splitting the result: the right half becomes the child chain code, and the left half, read as a number, is added to the parent private key modulo the curve order to give the child private key. The uniformity is the point: one function, correct once, is correct everywhere in the tree.',
      take:'Each step produces a 32-byte chain code and a key that is a sum taken modulo n.',
      note:'Every slash in a path such as m/84h/0h/0h/0/0 is one call of this function; say so, because it makes paths concrete. The left half is not used directly as the key, which students assume: it is added to the parent key. Note the validity rule and the honest statement of its rarity: if the left half is at least the curve order, or the child key is zero, the index is skipped, and the probability is below one in 2 to the 127.',
      src:[BK + ', Child Private Key Derivation', 'Wuille, 2012'] },
    { id:'ChainCode', t:'Chain code', sub:'256 bits beside every key',
      def:'A chain code is the 32 bytes that travel with a key and take part in deriving its children. The root’s chain code comes from the seed; every other is the right half of its parent’s derivation hash, so each node of the tree has its own. It introduces deterministic random data so that knowing an index and a child key is not enough to derive other children.',
      take:'A child’s chain code differs from its parent’s, which is what separates the branches.',
      note:'The demonstration is small but worth running: derive one child and show that the chain code has changed. This is what separates an HD wallet from a bare sequence of hashes, and it is why a key handed to someone without its chain code can derive nothing at all. Repeat the care the standard asks for: a chain code is secret although it is not a key, because it corresponds to an entire subtree.',
      src:[BK + ', Extended Keys', 'Wuille, 2012'] },
    { id:'IndexNumber', t:'Index number', sub:'two ranges in 32 bits',
      def:'The index is the 32-bit number that says which child is wanted, and its range decides the kind of derivation. Indices from 0 to 2 to the 31 minus 1 are used only for normal derivation; indices from 2 to the 31 upwards only for hardened derivation, and those are written with an apostrophe or an h. The index is serialised as four bytes and appended to the key material before hashing.',
      take:'The three boundary values: 2147483647, 2147483648 and 4294967295.',
      note:'The split makes a security property visible in a path: a reader can tell from an index alone whether the parent’s private key was needed, and therefore whether the branch above can be shared as an extended public key. Correct the chapter’s own slip while the numbers are on the screen: it says each parent key can have 2,147,483,647 children and gives 2 to the 31 as the value, but 2 to the 31 is 2147483648, and BIP32 counts 2 to the 31 normal children with indices 0 to 2 to the 31 minus 1.',
      src:[BK + ', Using Derived Child Keys', 'Wuille, 2012'] },
    { id:'PrivateChildDerivation', t:'Private child key derivation', sub:'the left half added to the parent key',
      def:'For a normal child, the compressed parent public key and the four bytes of the index go into the hash, so the parent private key is needed only to compute that public key. The child private key is the left half of the hash plus the parent private key, taken modulo the curve order; the right half is the child’s chain code. This is the function a signing device runs, and it is cheap enough for a small device to run many times.',
      take:'The first normal child of BIP32’s test vector master key, computed as arithmetic.',
      note:'A wallet that knows a path and holds the master key with its chain code can reproduce every private key it ever used, which is the whole promise of a seed backup; say it here, where the mechanism is on the screen. Then correct a slip the careful reader will find: the chapter writes that a parent private or public key is combined, with the parenthesis uncompressed key, while BIP32 serialises the parent public key in compressed form, the 33 bytes beginning 02 or 03.',
      src:[BK + ', Child Private Key Derivation', 'Wuille, 2012'] },
    { id:'HardenedDerivation', t:'Hardened child key derivation', sub:'the private key into the hash instead',
      def:'Hardened derivation feeds the parent private key, padded with a leading zero byte to the length of a compressed public key, into the hash in place of the parent public key. That breaks the relationship between the parent public key and the child chain code, so a leaked child private key can no longer be combined with the parent chain code to recover anything above it.',
      take:'The first hardened child of the test vector master key: edb2e14f…, nothing like the normal child.',
      note:'Give the risk it answers, which is the chapter’s clearest security argument: an extended public key contains the chain code, so a child private key that leaks can be used with it to derive all the other child private keys, and together with the parent chain code to deduce the parent private key. Hardening is not a stronger kind of key and it does not protect the child; it protects everything above. Hence the practice: the level-1 children of the master keys are always derived hardened.',
      src:[BK + ', Hardened Child Key Derivation', 'Wuille, 2012'] },
    { id:'PublicChildDerivation', t:'Public child key derivation', sub:'a child address with no private key',
      def:'A child public key can be derived from a parent public key and chain code alone, because adding a value to a public key gives the public key of the sum. BIP32 defines the function only for non-hardened indices. This is the reason the standard exists in the form it has: a web shop can let its server generate a fresh address for every order without giving the server anything that can spend.',
      take:'The public derivation and the private one agree; asking for a hardened child refuses.',
      note:'The third line proves the identity that everything rests on, and the fourth shows the refusal with the message the library raises. Both are worth pausing on. Then give the cost the whole group has been circling: an extended public key lets its holder compute every address of a branch, so it must be treated more carefully than an ordinary public key, both for privacy and because of the leak that a non-hardened child private key makes possible.',
      src:[BK + ', Public Child Key Derivation', 'Wuille, 2012'] },
    { id:'ChildKeyIndependence', t:'Using a derived child key', sub:'what it can and cannot do alone',
      def:'A child key taken out of the tree behaves exactly like a randomly generated key: it makes a public key, an address and signatures. It cannot find its parent, cannot find its siblings, and without its own chain code cannot derive grandchildren. A child private key, its public key and its address are indistinguishable from keys created at random, so nothing outside the wallet reveals that they belong to a sequence.',
      take:'The one exception: with the parent extended public key, a normal child private key gives the parent away.',
      note:'Build the slide around that exception, because it is the practical reason hardened derivation exists and the fourth line demonstrates it: the parent private key is recovered by subtraction. Then add the limit of indistinguishability: a single key looks random, but the chain of a wallet’s addresses can often be linked on the blockchain by how outputs are spent, so one key’s anonymity is not privacy for the wallet.',
      src:[BK + ', Using Derived Child Keys', 'Wuille, 2012'] } ] },
  { id:'ExtendedKeys', t:'Extended keys', lead:'The object a wallet actually passes around: a key together with its chain code, the root of a branch rather than a single key.',
    note:'An extended private key can create a complete branch; an extended public key can create only a branch of public keys. That difference is what users most often misjudge when they paste one of these strings somewhere.',
    items:[
    { id:'ExtendedKey', t:'Extended key', sub:'78 bytes before encoding',
      def:'An extended key is a key together with its chain code, stored as the two concatenated. Neither half derives anything alone, because the chain code is the key of the HMAC and the key is part of its message. The serialised form adds five fields: four version bytes, a depth, the parent fingerprint and the child number, giving 78 bytes before the checksum.',
      take:'4 + 1 + 4 + 4 + 32 + 33 is 78, and the chapter’s own xpub decodes to exactly that.',
      note:'The arithmetic and the decode on the slide say the same thing twice, once from the layout and once from a real string. Two cautions. The chapter’s phrase, that extended keys are stored simply as the concatenation of the key and the chain code, describes the pair and not the serialised string, which carries five more fields and a checksum. And an extended key is not a wallet: it says nothing about which script types or paths were used, which is the gap descriptors fill in the next branch.',
      src:[BK + ', Extended Keys', 'Wuille, 2012'] },
    { id:'ExtendedPrivateKey', t:'Extended private key', sub:'the chapter’s xprv, decoded',
      def:'An extended private key is the extended key whose key half is private: it derives every descendant, private and public, and is written with the prefix xprv. It is the most dangerous object in a wallet after the seed, and the most useful: it is what a signing device holds, what a cold backup contains, and what BIP32 says must be shared when two systems both need to spend.',
      take:'Version 0488ade4, depth 1, and 33 bytes of key data beginning with the pad byte 0.',
      note:'The decode is done with base58 arithmetic and a double SHA-256 and nothing else, so the class can see that the checksum holds and read the fields out one by one. Make the pad byte explicit: a private key is 32 bytes and the field is 33, so BIP32 prescribes a leading zero, which is how software tells the two kinds of extended key apart inside the structure. Then the warning: an extended private key is not protected by being long or unfamiliar, and anyone who copies the string has the subtree.',
      src:[BK + ', Extended Keys', 'Wuille, 2012'] },
    { id:'ExtendedPublicKey', t:'Extended public key', sub:'111 characters of base58check',
      def:'An extended public key is a public key with its chain code: it derives all the normal public keys of its branch and none of the private ones, and is written with the prefix xpub. It is the object that makes the standard worth having, and its two classic uses are a web server that creates a fresh address per order and a watching wallet that sees a balance it cannot spend.',
      take:'Always 111 characters, version 0488b21e, key data beginning 02 or 03.',
      note:'The fixed length is a useful sanity check for students pasting keys about, so point it out. Then insist on the protection it still needs: it cannot spend, but it reveals every address of its branch, so leaking it is a privacy failure, and BIP32 adds the sharper risk that a non-hardened child private key leaked beside it gives up the parent. The chapter states the practical version: a leaked child private key with a parent chain code reveals all the children and even the parent private key.',
      src:[BK + ', Extended Keys', 'Wuille, 2012'] },
    { id:'ExtendedKeyEncoding', t:'Extended key encoding', sub:'why they begin xprv and xpub',
      def:'Extended keys are written in base58check so that they can be copied between wallets, with four version bytes chosen so that the result begins xprv or xpub on mainnet and tprv or tpub on testnet. The checksum catches typing errors before any derivation is attempted, and the version prefix tells reader and software which kind of object they have, which matters because the two kinds are otherwise the same shape.',
      take:'A truncated string fails the checksum before anything else is tried.',
      note:'The refusal on the last line is the feature, not a bug; let the class see the message. Then raise the confusion that the prefixes have caused in practice: BIP49 and BIP84 define alternative version bytes producing ypub and zpub for their script types, while BIP43 argues against the whole practice and recommends always using the original bytes, because one scheme may generate nodes for several currencies or for something that is not a currency at all.',
      src:[BK + ', Extended Keys', 'Wuille, 2012', 'Palatinus and Rusnak, 2014a'] },
    { id:'KeyFingerprint', t:'Key fingerprint', sub:'the first 32 bits of an identifier',
      def:'A key fingerprint is the first four bytes of the identifier of an extended key, where the identifier is the HASH160 of the serialised public key, ignoring the chain code. It exists so that software can match a child with its parent quickly, and because it comes from a public key alone, a wallet holding only an xpub can state the origin of the keys it derives.',
      take:'The test vector master key has the fingerprint 3442193e: eight hexadecimal digits, 32 bits.',
      note:'The fingerprint reappears in the next branch as the first field of a descriptor’s key origin, so flag the connection now. Then give BIP32’s own warning, which has two parts: four bytes are not an identity, software must be willing to deal with collisions, and the full 160-bit identifier could be used internally where it matters.',
      src:['Wuille, 2012', 'Wuille and Chow, 2021'] } ] },
  { id:'TreeNavigation', t:'Navigating the tree', lead:'A path names one key by the route from the root: slashes between levels, m for private and M for public, an apostrophe or h for a hardened step.',
    note:'Without a convention the tree is unmanageable and wallets cannot be moved between implementations, because the possibilities for internal organisation are endless. The levels below are the ones a user meets by name.',
    items:[
    { id:'KeyPath', t:'Key path', sub:'m/84h/0h/0h/0/2 as five indices',
      def:'A key path is the name of one key, written as the route from the root. Reading it is mechanical: start at the root and apply the derivation function once per element, choosing the hardened variant where the element carries an apostrophe or an h. The ancestry can be read the other way too: m/x/y/z is the z-th child of m/x/y, which is the y-th child of m/x.',
      take:'Five elements become the indices 2147483732, 2147483648, 2147483648, 0 and 2.',
      note:'Convert the path with the class before showing the computation; the hardened numbers are just 2 to the 31 plus 84, 0 and 0, which the second line makes plain. Three details trip readers up and all three are worth saying: the capital M means only that the key named is public and not that there is a second tree; the apostrophe and the letter h mean the same thing; and a path is part of a backup, because a recovery code gives the seed and says nothing about which branches were used.',
      src:[BK + ', HD Wallet Key Identifier (Path)', 'Wuille, 2012'] },
    { id:'Bip43Purpose', t:'Purpose level', sub:'44 hardened is 0x8000002c',
      def:'BIP43 reserves the first hardened level of the tree as a purpose number saying which scheme the rest of the tree follows, and recommends that each scheme use its own BIP number. The level exists because BIP32 alone leaves implementers too many degrees of freedom, so that two wallets can both claim to be BIP32 compatible while producing different logical structures.',
      take:'The four purposes this chapter meets: 44, 49, 84 and 86, each hardened.',
      note:'Show how the hexadecimal value is built, because students meet these numbers in logs and descriptors rather than as decimals. Two points are easy to miss. The purpose level is hardened, so nothing above it can be shared as an extended public key and the purpose cannot be read off a shared xpub. And the branch m/0 hardened was already taken by BIP32’s own default account before the proposal existed.',
      src:[BK + ', Navigating the HD Wallet Tree Structure', 'Palatinus and Rusnak, 2014a'] },
    { id:'Bip44Structure', t:'BIP44 structure', sub:'five predefined levels',
      def:'BIP44 fixes five levels under purpose 44 hardened: purpose, coin type, account, change and address index. The first three are hardened and the last two are not, which is the division worth learning by heart, because it is what allows an account’s extended public key to be exported to a machine that must not be able to spend.',
      take:'Hardened, hardened, hardened, normal, normal: the shape of every standard path.',
      note:'Derive the pattern from the indices rather than asserting it, as the third line does. Then give the discovery rules that come with the standard, because they decide what a restoration actually finds: software should not create an account while the previous one has no transaction history, and on restoring it should derive the first account, scan its external chain within the gap limit of twenty addresses, and continue only while transactions are found.',
      src:[BK + ', Navigating the HD Wallet Tree Structure', 'Palatinus and Rusnak, 2014b'] },
    { id:'AccountBranch', t:'Account branch', sub:'the third level, hardened',
      def:'The account level splits a wallet into independent subaccounts that never mix coins, for accounting or organisational reasons: donations, savings, common expenses. It is hardened, and that is the design decision that makes it safe to export, because the account’s extended public key cannot be used to work back to the master key even if a private key below it leaks.',
      take:'The second account of a BIP44 wallet is m/44h/0h/1h, index 1 above the hardened boundary.',
      note:'The word account here means a branch of a key tree and nothing more: there is no balance held anywhere, and nobody outside can tell that two addresses belong to one account. Add the discovery rule that bites here, because people do meet it: software is told not to create an account unless the previous one has history, so a wallet restored from a code stops looking after the first account with no transactions, and an account created out of order can be missed.',
      src:[BK + ', Navigating the HD Wallet Tree Structure', 'Palatinus and Rusnak, 2014b', 'Wuille, 2012'] },
    { id:'ChangeBranch', t:'Change branch', sub:'0 for receiving, 1 for change',
      def:'The fourth level has only two values: 0 for the external chain, whose addresses are handed out, and 1 for the internal chain, which receives change. Both use normal derivation, which is what makes an account’s extended public key useful, since a server given it can derive both branches and recognise change as well as receipts.',
      take:'M/44h/0h/3h/1/14 is the fifteenth change address of the fourth account.',
      note:'Read the path aloud and have the class name each element; by this slide they should be able to. Two cautions. Change addresses belong to the same wallet, so a tool scanning only branch 0 will under-report a balance, and one handing out addresses from branch 1 leaks which outputs are change. BIP44 notes the asymmetry that follows for scanning: only external chains need be scanned, because internal chains receive only coins coming from the associated external chain.',
      src:[BK + ', Navigating the HD Wallet Tree Structure', 'Palatinus and Rusnak, 2014b', 'Wuille, 2012'] },
    { id:'AddressIndex', t:'Address index', sub:'the level a wallet advances',
      def:'The address index is the last level of a BIP44 path, counted from zero with normal derivation, and it is the level a wallet advances each time it needs a new address. Because the derivation is normal, the whole sequence can be produced from the account’s extended public key, which is what a web store does.',
      take:'Bitcoin Core prepares a thousand scripts in advance, which it calls the keypool.',
      note:'This level is where privacy is won or lost: a unique address per order improves privacy and gives each order an identifier to track. The second line reads the keypool default out of the node’s own option help, and it answers the question students ask next, namely how a wallet knows how far ahead to prepare. Finish with the two-sided consequence: nobody can tell from an address that it is the third of an account, and neither can a restored wallet tell how far its owner had gone.',
      src:[BK + ', Navigating the HD Wallet Tree Structure', 'Bitcoin Core, 2026'] } ] } ] });

// ============================== BRANCH 5: BACKING UP DERIVATION PATHS ==============================
CH.push({
  id:'PathBackup', t:'Backing up derivation paths', sub:'The part of a backup a recovery code does not contain',
  lead:'In a BIP32 tree there are about four billion first-level keys, each with four billion children, so no wallet can generate even a small fraction of the possible keys. Recovering from data loss therefore needs more than the code, the seed algorithm and the derivation algorithm: it needs to know which paths the wallet used. This is the gap through which money is actually lost, when a perfectly good code is entered into software that looks in a different part of the tree.',
  note:'There are two answers and the chapter prefers neither absolutely. Implicit paths are convenient and inflexible; explicit paths are flexible and demand more of the user. Wallets for single-signature scripts have long used the first, wallets for multiple signatures increasingly use the second, and applications that do both usually conform to the implicit standards and also provide descriptors.',
  src:[BK + ', chapter 5, Backing Up Key Derivation Paths'],
  groups:[
  { id:'PathConventions', t:'Implicit and explicit paths', lead:'Either the path is fixed by a standard that every implementation knows, or it is written down beside the recovery code.',
    note:'The four standard paths in this group are one per script type, and the last concept, multisignature, is the case the chapter uses to show why implicit paths cannot be enough.',
    items:[
    { id:'ImplicitPath', t:'Implicit path', sub:'the path a wallet assumes',
      def:'An implicit path is one fixed by a standard, so that nothing has to be recorded. Whenever a new kind of address appears, a proposal defines the path for it, and a wallet implementing that proposal uses those keys both when first started and after a restoration. The advantage is that a user keeps only the words; the disadvantage is that a restoring wallet must derive and scan every path it supports.',
      take:'Four purposes, four script types: 44 for P2PKH, 49 for nested segwit, 84 for native, 86 for taproot.',
      note:'Give the three consequences the chapter lists, because each is a real failure students may meet. A code without a version number cannot warn its owner when a new wallet version drops support for an older path; the same happens in reverse when a code is entered into older software that does not know newer paths; and codes that do carry version information, Electrum version 2 and Aezeed, can detect the mismatch and say so. That is the strongest practical argument for versioned codes in the whole chapter.',
      src:[BK + ', Backing Up Key Derivation Paths'] },
    { id:'ExplicitPath', t:'Explicit path', sub:'the path written down with the code',
      def:'An explicit path is derivation information backed up beside the recovery code, saying exactly which keys go with which scripts. In practice it is written as an output script descriptor. The gains are exactness: no need to support outdated scripts, no compatibility problems in either direction, and room for extra information such as other participants’ public keys.',
      take:'One real descriptor already carries the script type, the master fingerprint, the path and the branch.',
      note:'The three lines take apart the descriptor Bitcoin Core 31.1 produced for this chapter, so the class sees that nothing has to be guessed. Give the cost the chapter states: explicit paths require the user to back up more, and although that extra information usually cannot compromise security, it can reduce privacy and does need some protection, since an extended public key in a descriptor reveals every address of its branch.',
      src:[BK + ', Backing Up Key Derivation Paths', 'Wuille and Chow, 2021', 'Bitcoin Core, 2026'] },
    { id:'StandardPath44', t:'BIP44 path for legacy scripts', sub:'m/44h/0h/0h',
      def:'The BIP44 account path is the oldest of the standard implicit paths and the one the chapter’s table gives for legacy pay-to-public-key-hash addresses, the ones beginning with the digit 1. A wallet that supports only BIP44 will find only those addresses, which is exactly what makes a path a part of a backup.',
      take:'The fresh Bitcoin Core wallet’s first descriptor is pkh with the origin 6d8c4b8f/44h/0h/0h.',
      note:'The second line reads the real descriptor out of the saved wallet, so the path on the slide is not a claim but an observation. Make the layering point that BIP380 complains about and descriptors remove: the script type is not part of the path arithmetic at all, since the same keys could make any kind of address, and it is the standard alone that says this path’s keys belong in pay-to-public-key-hash scripts. Note also that the chapter’s table prints coin type 1 for BIP49 because that standard’s vectors are on testnet.',
      src:[BK + ', Backing Up Key Derivation Paths', 'Palatinus and Rusnak, 2014b', 'Bitcoin Core, 2026'] },
    { id:'StandardPath49', t:'BIP49 path for nested segwit', sub:'49 hardened is 0x80000031',
      def:'BIP49 gives segwit keys wrapped in a script hash their own account path, using BIP44’s structure with a different purpose value. Its reasoning is the clearest statement of why implicit paths need discipline: the alternatives it rejected would have put legacy and segwit addresses in one account, so that an incompatible wallet might show the account and miss some outputs, where this scheme fails visibly instead, showing the account or nothing.',
      take:'The same wallet’s nested descriptor wraps wpkh inside sh under the 49h account.',
      note:'The failure mode is the lesson: better that a wallet finds nothing than that it finds part of a balance, because a user checking a balance cannot tell a partial answer from a complete one. Note that the standard also defines alternative version bytes, giving ypub and yprv, and that the chapter’s table row uses coin type 1 because BIP49’s own vectors are on testnet, so a reader working on mainnet should use m/49h/0h/0h.',
      src:[BK + ', Backing Up Key Derivation Paths', 'Weigl, 2016', 'Bitcoin Core, 2026'] },
    { id:'StandardPath84', t:'BIP84 path for native segwit', sub:'the test vector, recomputed end to end',
      def:'BIP84 gives native segwit keys their own account path, and it is the path most wallets use today. Its addresses are the bech32 strings beginning bc1q, and they are cheaper to spend than the nested form, which is why that form was transitional. The derivation is the familiar one: PBKDF2 to the seed, HMAC-SHA512 to the master key, three hardened steps to the account, two normal steps to the address key.',
      take:'The standard’s own first address, recomputed here and derived independently by Bitcoin Core 31.1.',
      note:'This is the chapter’s fullest end-to-end check and it deserves time: from twelve words to an address, through every mechanism the branch has built, and then compared character by character with what the node produced from the same descriptor. The agreement is the point of the whole session. Mention the prefixes once more: BIP84 defines zpub and zprv, while the descriptor Core emits uses an ordinary xpub with an explicit path, which is what BIP43 and BIP380 prefer.',
      src:['Rusnak, 2017', 'Bitcoin Core, 2026', BK + ', Backing Up Key Derivation Paths'] },
    { id:'StandardPath86', t:'BIP86 path for single-key taproot', sub:'one tweak more than the others',
      def:'BIP86 gives single-key taproot outputs their own account path and adds one step to the pattern: the derived key becomes the internal key, and the output key is the internal key plus a tagged hash of it times the generator point, so that the output commits to an unspendable script path rather than to none. The address is written in bech32m.',
      take:'From the same twelve words, the taproot address of the standard’s first key.',
      note:'Explain why the standard exists at all, in its own candid words: there are now solutions that remove the need for fixed derivation paths per script type, but many software wallets and hardware signers still use seed backups that carry no derivation or script information, so a common scheme makes such outputs likely to be recovered. Note what the course’s browser pages cannot do here, since students will try: the point addition and the bech32m checksum need the machinery of chapter 4.',
      src:['Chow, 2021', BK + ', Backing Up Key Derivation Paths'] },
    { id:'Multisignature', t:'Multisignature', sub:'why implicit paths are not enough',
      def:'Multisignature means spending needs signatures from more than one key: a two-of-three arrangement lists three potential signers of whom at least two must sign. In this chapter it is the argument against implicit paths. Alice needs only Bob’s or Carol’s signature to spend, but she needs both of their public keys to find their joint funds on the blockchain, so each of the three must back up all three public keys.',
      take:'Three ways to meet a two-of-three condition, and no seed that can reproduce the arrangement.',
      note:'The mechanism that matters here is not the script but the information each participant must keep: a seed derives that participant’s own keys and nothing else, so which keys, how many signatures and in what order is non-deterministic information no recovery code can reproduce. Keep two distinctions clear: the threshold and the number of keys are different numbers, and earlier editions of the book wrote m-of-n where this one writes t-of-k.',
      src:[BK + ', Backing Up Key Derivation Paths', BK + ', chapter 7, Multisignature'] } ] },
  { id:'Descriptors', t:'Output script descriptors', lead:'The notation in which explicit paths are written: one line that names the script type, the keys, where each key came from and the branch below it.',
    note:'Bitcoin Core’s wallets are descriptor wallets, so every example in this course that comes from a real node is a descriptor. The standard’s motivation is exactly this branch’s problem: a backup of keys alone cannot say which output scripts and addresses to produce.',
    items:[
    { id:'OutputScript', t:'Output script', sub:'what a descriptor describes',
      def:'An output script is the program in a transaction output that states the condition for spending it, and it is the thing a descriptor describes. One key can appear in several kinds of script, each giving a different address, which is why the standards of this branch assign a different path to each: the key itself does not say which script it belongs in.',
      take:'A native segwit output script is 22 bytes: a zero, a push of twenty, and the key hash.',
      note:'Build the 22 bytes from the key derived two slides earlier so the class sees the chain from words to script. Then make the argument BIP380 makes: wallets traditionally stored keys and later mutated them into scripts, but given only private keys a restored wallet cannot know which kinds of script and address to produce, which has caused real incompatibilities. Keep the three senses of the word script apart: the output script, the input script and the witness.',
      src:['Wuille and Chow, 2021', 'Rusnak, 2017'] },
    { id:'OutputScriptDescriptor', t:'Output script descriptor', sub:'a function, its origin and its keys',
      def:'A descriptor is an expression describing a set of output scripts: a script type written as a function, and key expressions as its arguments. A key expression is optional key origin information in brackets, then the key, which may be a hexadecimal public key, a WIF key or an extended key, then zero or more path elements and optionally a final wildcard. Functions may nest, as in sh(wpkh(...)).',
      take:'One real descriptor: the function wpkh, the origin 73c5da0a/84h/0h/0h, and the branch /0/*.',
      note:'Take the real descriptor apart on the board in those three pieces; everything in this branch is contained in them. A descriptor records the script type, the keys, the origin of each key and the paths below it, so a wallet given one guesses nothing while a wallet given only a seed guesses everything. Two things a descriptor is not: it is not secret by default, since one with an extended public key gives its holder every address of the branch, and it is not a private backup, since it holds no secret unless an xprv is put in it.',
      src:[BK + ', Output Script Descriptors', 'Wuille and Chow, 2021', 'Bitcoin Core, 2026'] },
    { id:'DescriptorChecksum', t:'Descriptor checksum', sub:'eight characters after a hash sign',
      def:'A descriptor carries an eight-character error-detecting checksum after a hash sign, computed over the whole expression with a linear code in the bech32 alphabet. A descriptor is a long string a person may have to type, and one wrong character would point a wallet at the wrong keys; the checksum turns that silent failure into a refusal.',
      take:'The standard’s smallest example and this chapter’s real descriptor both reproduce their checksums.',
      note:'Both lines are reproductions of published values, the standard’s own raw(deadbeef) example and the checksum Bitcoin Core appended to the BIP84 descriptor for this chapter. Then give the limit: the checksum protects the descriptor and not the keys, so a descriptor with a valid checksum may still name the wrong account, and a descriptor whose extended key is wrong will usually fail that key’s own base58check instead.',
      src:['Wuille and Chow, 2021', 'Bitcoin Core, 2026'] },
    { id:'KeyOrigin', t:'Key origin', sub:'a fingerprint and the path above the key',
      def:'The key origin is the bracketed part at the start of a key expression: eight hexadecimal characters for the fingerprint of the key where derivation starts, then the path from it to the key that follows. It is what lets a public descriptor be matched with a private key held elsewhere, because a signing device can compare the fingerprint with its own master key and derive exactly the key named.',
      take:'Fingerprint 73c5da0a and the three hardened steps 84, 0, 0 of the account above the key.',
      note:'The origin is metadata: it takes no part in deriving anything below the key, and the path it records has already been applied. That is why the brackets usually hold the hardened part down to the account and the part after the key is the normal branch and index. Note the writing convention the chapter recommends and Core follows: h rather than an apostrophe, because an apostrophe has a special meaning in a shell.',
      src:['Wuille and Chow, 2021', BK + ', Output Script Descriptors', 'Bitcoin Core, 2026'] },
    { id:'MultipathDescriptor', t:'Multipath descriptor', sub:'one descriptor, two branches',
      def:'A multipath descriptor writes one derivation step as a tuple in angle brackets, so that a single descriptor stands for the receive and the change descriptor of a wallet. The expansion is purely textual and its order is fixed: the first value gives the first descriptor. Wallets almost always need two descriptors differing in one digit, which is why the notation exists.',
      take:'The tuple 0 and 1 expands to the receive descriptor and the change descriptor, in that order.',
      note:'The evidence makes the need concrete: the fresh Bitcoin Core wallet has eight descriptors that are four pairs, each pair sharing an account key and differing only in the branch, with one of each pair marked internal. Two points of care: the notation is a convenience and not a new capability, since the two descriptors can always be given separately; and the tuple is a path element, not a wildcard, so a multipath descriptor with a final star describes two infinite families of scripts.',
      src:['Chow, 2022', 'Bitcoin Core, 2026'] },
    { id:'Miniscript', t:'Miniscript', sub:'conditions a descriptor can carry',
      def:'Miniscript is a structured language for a subset of Bitcoin scripts, written so that spending conditions can be analysed, composed and signed for; a descriptor can contain a miniscript expression. Raw Bitcoin script is hard to reason about: finding the cheapest script for a set of conditions, composing two scripts, or deciding what a script permits are all non-trivial, and that is what the language is for.',
      take:'Core’s documentation shows a policy decaying from four-of-four to one-of-four over time.',
      note:'Use that example, which the second and third lines confirm are present in the saved documentation: four keys and three time locks, starting as four-of-four and decaying to three-of-four, two-of-four and finally one-of-four at successive halving heights, written as a threshold expression inside a witness-script descriptor with multipath keys. Take two points only, since the subject is beyond this chapter: the explicit approach scales to conditions no implicit path could express, and one line of text can then record a whole arrangement, which is why wallets are moving to descriptors.',
      src:['Wuille et al., 2023', 'Bitcoin Core, 2026', BK + ', Output Script Descriptors'] } ] } ] });

// ============================== BRANCH 6: BACKING UP DATA THAT IS NOT KEYS ==============================
CH.push({
  id:'NonkeyBackup', t:'Backing up data that is not keys', sub:'A restored wallet with the right balance can still be useless',
  lead:'Deterministic derivation solves the backup of keys, but most wallet databases store more than keys: the labels and notes a user wrote about every payment. Those are not deterministic and cannot be restored from a recovery code. The chapter asks the reader to imagine a bank statement from a year ago with every date and amount and a blank description field; that is what a seed-only restoration leaves.',
  note:'The branch’s conclusion is a warning about habits rather than about software: users and wallet applications need to do more than back up a recovery code. The chapter also observes that a number of widely used applications make recovery codes easy and provide no way at all to back up or restore label data.',
  src:[BK + ', chapter 5, Backing Up Non-key Data'],
  groups:[
  { id:'WalletNotes', t:'Labels and notes', lead:'The information a user adds by hand: a name on an address so a payment can be recognised, a note on a transaction so its purpose is remembered.',
    note:'This information is private in a way the keys are not: labels stay in the wallet and are never shared with the network, which protects privacy and keeps personal data off the blockchain. That is also why a leaked label file is so damaging.',
    items:[
    { id:'AddressLabel', t:'Address label', sub:'a name on an address when it is created',
      def:'An address label is a name a user gives to one of their own addresses, so that payments arriving there can be told apart. In the chapter’s example Bob labels the address he generates when he sends Alice an invoice. The label is a note about the wallet’s own address, not about the payer, and nothing about it leaves the wallet: mechanically it is a row in the local database keyed by the address.',
      take:'The address is derived from the seed and the label is not: a restoration reproduces one and loses the other.',
      note:'That asymmetry is the whole branch in one sentence, so make the class say it back. Labels are what make a fresh address per payment practical, as the web store slides will show: without a note recording which address belonged to which order, the per-order identifier would be useless. Then give BIP329’s own caution, which the third line reads from the saved proposal: the data is privacy-sensitive, encryption in transit is highly recommended, encryption at rest should be considered, and unencrypted exports should be deleted as soon as possible.',
      src:[BK + ', Backing Up Non-key Data', 'Raw, 2022'] },
    { id:'TransactionLabel', t:'Transaction label', sub:'the user’s own record of what the money did',
      def:'A transaction label is a note on a payment made or received. The blockchain holds amounts and times and has no field for a description; the only metadata a receiver chooses for a typical payment are the amount and the address. So the label exists nowhere but in the user’s own database, and a seed-only restoration shows a list of approximate times and amounts.',
      take:'The chapter’s own two rows: 0.00100 received and 0.00075 paid, leaving 0.00025.',
      note:'Work the arithmetic as the chapter prints it and then correct the picture, because this is a good place for it: a real wallet works in satoshis, the integer unit of chapter 2, precisely to avoid the rounding that decimal fractions invite, and the rounding on this slide is only there to match the chapter’s table. Mention that BIP329 has a record type for transactions keyed by the transaction identifier, and that labels have become mandatory when spending in several wallets.',
      src:[BK + ', Backing Up Non-key Data', 'Raw, 2022'] },
    { id:'LabelExportFormat', t:'Label export format', sub:'one record as a line of JSON',
      def:'BIP329 proposes a line-based JSON format for exporting labels, so that they can be moved between applications instead of locking a user into one. An export is a UTF-8 file with one JSON object per line, each carrying a type and a reference, with the label and a few other properties optional. The line-based form means a file can be split, streamed or added to, and one malformed line cannot invalidate the whole import.',
      take:'One record: a type, a reference and a label, on a single line.',
      note:'The motivation is lock-in, and the standard says so plainly: moving funds between wallets is well defined by BIP39, BIP32 and BIP44, while there has been no standard way to transfer the labels a user applied. Give the three limits: the proposal is a draft and informational, so support varies; it defines no private key types, deliberately; and the data is privacy-sensitive, which is why it recommends encryption in transit and at rest.',
      src:[BK + ', Backing Up Non-key Data', 'Raw, 2022'] } ] },
  { id:'OtherProtocolData', t:'Other data a wallet keeps', lead:'Protocols built on top of Bitcoin add state that no seed can reproduce, and the consequences of losing it are worse than losing a label.',
    note:'The chapter is blunt about the stakes: if the node a wallet connects to realises that data has been lost, it may be able to steal bitcoins, and if both parties lose their databases with no adequate backup, both lose funds.',
    items:[
    { id:'LightningNetwork', t:'Lightning Network', sub:'funds in a channel, not in an output you alone control',
      def:'The Lightning Network is a protocol of payment channels on top of Bitcoin: funds sit in an output that two parties control jointly, and the parties sign successive versions of a settlement dividing the balance, only the last of which is meant to be published. A node’s money is therefore in two pools: on-chain funds it can spend with no auxiliary data, and off-chain funds inside a channel.',
      take:'The lnd recovery document is in exactly those two halves: on-chain recovery and off-chain recovery.',
      note:'Take only the recovery consequence from this slide, since the protocol belongs to a later chapter: a Lightning-capable wallet’s backup problem is strictly harder than a Bitcoin wallet’s, because part of its state changes with every payment and cannot be recomputed from any seed. The chapter’s conclusion applies here with full force, and the next slide is the protocol’s own partial answer.',
      src:[BK + ', Backing Up Non-key Data', BK + ', chapter 14', 'Lightning Labs, 2026b'] },
    { id:'StaticChannelBackup', t:'Static channel backup', sub:'taken once, when the channel opens',
      def:'A static channel backup records what is needed to recover a channel’s settled funds. The word static means it is taken once, when the channel is created, and remains good until the channel closes. The alternative, copying the channel database periodically, is dangerous because one never knows whether the copy holds the latest state; the static backup aims instead at a simple, safe recovery of settled funds after partial or complete data loss.',
      take:'The file is encrypted under a key derived from the user’s seed, so it cannot be used in isolation.',
      note:'That encryption is the link back to the rest of this chapter and forward to the next two slides, so point it out: the key comes from the seed the user already has, which protects the privacy of the channels in the backup and stops a stranger importing somebody else’s channels. Then quote the limit rather than softening it: the chapter says the method cannot guarantee results.',
      src:[BK + ', Backing Up Non-key Data', 'Lightning Labs, 2026b'] },
    { id:'Encryption', t:'Encryption', sub:'a note hidden and recovered with a derived key',
      def:'Encryption turns readable data into a form only a key holder can read back. A wallet can therefore store a backup where anyone can see it, as long as the key stays secret. The example shows the shape at its simplest: a key is derived from the seed by hashing, the note is combined with it by exclusive-or, and combining the result with the same key again returns the original text.',
      take:'The same operation twice: unreadable bytes, then the note again.',
      note:'Say clearly that the demonstration is a one-time pad shown for its shape only; real schemes use a block cipher or an authenticated cipher, as Aezeed does with aez and SLIP39 does with a Feistel network. What the example does show correctly is the structure that matters: the key comes from the seed by a one-way function, so it never has to be stored, and decryption is the same operation run again, so nothing else must be remembered. A pad reused on two messages is broken, which is why the key here is derived with a purpose string.',
      src:[BK + ', Backing Up Non-key Data', 'Lightning Labs, 2026a', 'Rusnak et al., 2017'] },
    { id:'EncryptedWalletBackup', t:'Encrypted wallet backup', sub:'everything, under a key from the seed',
      def:'An encrypted wallet backup is the chapter’s one solution for backing up everything at once: a few applications frequently and automatically create complete encrypted copies of their wallet database, under a key derived from their seed. The copy therefore holds the keys, the labels and whatever protocol data the wallet keeps, and the user restores it by entering the recovery code, regenerating the key and decrypting.',
      take:'The backup key derived from the chapter’s own seed: the same value, two ways.',
      note:'The two lines derive the same key from the real seed and from the printed prefix, which is a small lesson in reproducibility as well as a demonstration. The chapter’s argument for storing such a backup anywhere is that Bitcoin keys must be unguessable and modern encryption is strong, so nobody can open it but someone who can generate the seed, which makes untrusted cloud hosting or even random network peers acceptable. The limit to emphasise: this concentrates everything on the seed, so a leak now exposes the whole transaction history and the labels as well as the money.',
      src:[BK + ', Backing Up Non-key Data'] } ] } ] });

// ============================== BRANCH 7: DEPLOYING KEYS IN PRACTICE ==============================
CH.push({
  id:'WalletDeployment', t:'Deploying keys in practice', sub:'The chapter’s worked example: a shop, a server and a device',
  lead:'The chapter follows a merchant from a hobby page with one address to a shop that derives a fresh address for every order from an extended public key on the server, with the private keys on a device in a drawer. Everything the chapter has built — the tree, the extended public key, the hardened step above it, the standard path — exists so that a person can take payments without putting the power to spend on an exposed computer.',
  note:'Two of this branch’s lessons are organisational rather than technical. The safety of the arrangement comes from the hardened step above the shared key, not from the secrecy of the extended public key, which must still be protected for privacy. And the limit that bites in production is not cryptographic at all: it is the gap limit.',
  src:[BK + ', chapter 5, Using an Extended Public Key on a Web Store'],
  groups:[
  { id:'WebStore', t:'An extended key on a web store', lead:'One address for every order, derived on a machine that holds nothing able to spend.',
    note:'The story has stages worth retelling: a single address works for a few orders a week while weakening everyone’s privacy; then the shop succeeds, several orders of the same amount arrive together, and matching payments to orders becomes impossible.',
    items:[
    { id:'XpubDeployment', t:'Extended public key deployment', sub:'the watching half on the exposed machine',
      def:'Deploying an extended public key means installing the public half of a branch on a machine that must receive but not spend. The server derives a new address for every order and holds no private key that could be stolen; on another, safer machine the extended private key derives the matching private keys and spends. Without this, the only alternative was to generate thousands of addresses elsewhere and preload them.',
      take:'From one extended public key, the first addresses of the receiving branch, derived on the server.',
      note:'The computation is the deployment: an account xpub, a branch, an index, an address, with no secret anywhere in the calculation. Then give the two risks the sources name. Someone who breaks into the server can at most see all incoming payments, which is already a serious privacy loss, since the extended public key reveals every address of the branch; and the structure itself carries meaning, with one branch for payments received and another for change.',
      src:[BK + ', Using an Extended Public Key on a Web Store', 'Wuille, 2012'] },
    { id:'GapLimit', t:'Gap limit', sub:'how far a wallet keeps looking',
      def:'The gap limit is the number of unused addresses in a row a wallet tolerates before it stops looking for payments. A wallet cannot derive and scan four billion keys, so it generates a few at a time and extends as they are used. A gap arises in ordinary use when a key is handed to someone who then does not pay, and that is harmless as long as later keys were already generated.',
      take:'With a gap of 20, a payment at index 25 is never found; with a gap of 30 it is.',
      note:'The two scans on the slide are the same data under two limits, and the difference is money. Exceeding the limit loses funds in the most confusing possible way: the coins are on the chain, the keys are derivable, and the wallet shows nothing. Give the three choices a wallet has when its limit is reached, each with a cost: refuse further requests, generate beyond the limit and risk a restoration missing later payments, or hand out addresses already distributed and lose privacy. Production systems dodge it with very large gap limits and by rate-limiting invoices.',
      src:[BK + ', Using an Extended Public Key on a Web Store'] },
    { id:'PaymentProcessor', t:'Payment processor', sub:'where the bookkeeping actually happens',
      def:'A payment processor is the software that turns an extended public key into a working shop: it derives the next address, shows it to the customer, watches the chain for a payment of the right amount to that address, marks the invoice paid and keeps the association. A self-hosted one lets a merchant accept bitcoins with the extended public key as its only key material.',
      take:'BTCPay Server describes itself as free, open-source and self-hosted, with no fees or intermediaries.',
      note:'Both lines read the project’s own description from the saved copy rather than repeating a claim. Make the point about what this course is endorsing: the chapter names one product as an example and we should not read that as a recommendation; what matters is the property, self-hosted and holding no private key, because that is what bounds the damage a compromise can do to diverting future payments.',
      src:[BK + ', Using an Extended Public Key on a Web Store', 'BTCPay Server contributors, 2026'] } ] },
  { id:'OfflineKeys', t:'Keys kept offline', lead:'The other half of every arrangement in the chapter: where the private keys are when they are not in use.',
    note:'Here the chapter’s reasoning about which key is where becomes a decision about physical objects. A seed on paper, a device in a drawer, a code memorised: each is a different balance between the risk of loss and the risk of theft.',
    items:[
    { id:'ColdStorage', t:'Cold storage', sub:'keys that never touch a connected computer',
      def:'Cold storage is keeping keys where no connected computer can read them, created and stored in a secure offline environment. It works because receiving and spending are asymmetric: receiving needs only public information, which can live on an exposed machine, while spending needs the private key and happens rarely. Spending then means carrying an unsigned transaction to the offline side and a signature back.',
      take:'The two halves of one extended key: a public key byte on one side, a pad byte and a secret on the other.',
      note:'The comparison on the slide is exact and worth drawing out: the same chain code appears in both the xpub and the xprv, which is why the public side can derive the whole branch, while the key fields differ, 33 bytes beginning 02 or 03 against a zero pad and 32 secret bytes. Then say which way cold storage moves the risk: an offline key cannot be stolen over a network and cannot be recovered if the paper burns, so the recovery code, not the device, is the backup.',
      src:[BK + ', Using an Extended Public Key on a Web Store', 'Wuille, 2012'] },
    { id:'HardwareSigningDevice', t:'Hardware signing device', sub:'signs, and never exports',
      def:'A hardware signing device is a small purpose-built computer that holds private keys and signs with them. The frontend builds and displays the transaction; the device derives the child key, signs inside and returns the signature. Out of it come public keys, extended public keys and signatures; into it go transactions to sign and the derivation information needed to find the right key, which is why descriptors carry a key origin.',
      take:'The signature verifies for the transaction that was signed and for no other.',
      note:'The last line is the user-facing property: a signature is bound to one transaction, so a device that shows what it is signing gives the owner a real check. Three cautions. The name hardware wallet invites the belief that the coins are in the device, which the first branch corrected. The device protects keys from software on the computer and not from loss, so the recovery code must still be kept. And most such devices will never export private keys at all, which is why an extended public key is what the merchant copies out.',
      src:[BK + ', Wallet Technology Overview', 'Wuille and Chow, 2021'] },
    { id:'WrittenBackup', t:'Written backup', sub:'twelve words instead of thirty-two digits',
      def:'A written backup is the recovery code recorded on a physical medium. The chapter recommends it even for schemes designed for easy memorisation, because memory fails, cannot be inherited, and can be the reason a person is coerced. What is written is the code and, where one exists, a note that a passphrase exists, though not the passphrase itself in the same place.',
      take:'The same 128 bits: thirty-two hexadecimal characters, or twelve English words.',
      note:'The two encodings on the slide are the chapter’s own comparison, and the second line confirms that both really carry 128 bits. Name paper’s own risks rather than pretending it is a solution: it burns, it fades, it can be photographed, and a code in a drawer is a bearer instrument anyone in the house can carry away. The chapter’s answer is not to choose between paper and memory but to plan, and for an explicit-path wallet the descriptor should be written down too.',
      src:[BK + ', Seeds and Recovery Codes', 'Altunel, 2021'] } ] } ] });

// ============================== BRANCH 8: FOUNDATIONS ==============================
CH.push({
  id:'Foundations', t:'Foundations the chapter relies on', sub:'The four ideas the rest of the chapter assumes',
  lead:'This branch exists for a reason of method rather than of subject: a teaching text should not use a word it has not explained, and an audit of this chapter’s explanations found four terms used as though they were self-evident. The hash function underlies every derivation here; SHA-256 and SHA-512 fix the sizes of everything; the digital signature is what the keys exist to produce; and secret sharing is the mathematics behind two of the recovery schemes.',
  note:'Warn about the level of treatment. These are summaries sufficient for this chapter and no more: the design of hash functions, the security proofs of signature schemes and the algebra of secret sharing are each a subject of their own, and the book’s later chapters go further.',
  src:[BK + ', chapter 5, and the standards it cites'],
  groups:[
  { id:'CryptographicPrimitives', t:'Cryptographic primitives', lead:'The properties of these four operations are the reasons the chapter’s claims are true.',
    note:'Tie each claim to its primitive: that a child key cannot find its parent is a property of the hash function; that a checksum detects but cannot correct is a property of SHA-256 used as a compressor; that a server can safely hold an xpub is a property of the key pair; and that three of five codes recover a seed is a property of polynomial interpolation.',
    items:[
    { id:'HashFunction', t:'Hash function', sub:'the same input, the same output; a changed input, anything',
      def:'A hash function maps an input of any length to an output of fixed length. It always gives the same output for the same input, and if the input changes even slightly the output changes unpredictably, so that nobody can foresee the new value even knowing the new input. It cannot be run backwards.',
      take:'Three letters give ba7816bf; one letter different gives something unrelated; the first repeats exactly.',
      note:'Run the three lines in that order, because together they are the definition: repeatability, avalanche, repeatability again. Each property does a job in this chapter: repeatability is what makes a seed a backup, unpredictability is what makes derived keys unguessable, and the one-way direction is what makes a child key useless for finding its parent. Add the two limits: a hash is not encryption, nothing can be recovered from the output, and a hash is not a signature and proves nothing about who produced the data.',
      src:[BK + ', Wallet Technology Overview', 'Palatinus et al., 2013'] },
    { id:'ShaAlgorithm', t:'SHA-256 and SHA-512', sub:'32 bytes and 64 bytes',
      def:'SHA-256 and SHA-512 are two members of the second family of secure hash algorithms, with outputs of 256 and 512 bits. Which is used where fixes the sizes everything in this chapter is built around, and a reader who notices that stops finding the numbers arbitrary.',
      take:'64 bytes from one HMAC-SHA512, split in half: a 256-bit key and a 256-bit chain code.',
      note:'Trace the sizes out loud: a BIP39 seed is 512 bits because HMAC-SHA512 produces 64 bytes in one block; a BIP32 derivation yields a 256-bit key and a 256-bit chain code because those 64 bytes are split in half; an extended key’s 78 bytes include 32 of chain code and 33 of key data. SHA-256 appears in the BIP39 checksum, in base58check’s double hash and in BIP86’s tagged hash; SHA-512 in BIP32 and in PBKDF2. Note that the browser pages of this course provide SHA-2 and SHA-3 but not RIPEMD-160.',
      src:['Palatinus et al., 2013', 'Wuille, 2012', 'Python Software Foundation, 2026'] },
    { id:'DigitalSignature', t:'Digital signature', sub:'what a signing device returns',
      def:'A digital signature is the proof that the holder of a private key authorised a particular message. In Bitcoin the message is a transaction and the key is the one controlling the output being spent. The chapter assumes this throughout, beginning with its first sentence about wallet databases, which holds that simple databases contain both the public keys that receive bitcoins and the private keys that create the signatures authorising spending.',
      take:'A key derived from a recovery code signs, and its public key verifies.',
      note:'Close the loop from the start of the session: the key signing here was derived from twelve words through PBKDF2, HMAC-SHA512 and five derivation steps, and nothing else was needed. Note that the signer in the chapter toolkit takes its nonce as an argument so that the demonstration reproduces, and that a real signer must derive it deterministically or draw it from a secure source. The signature scheme itself belongs to the book’s chapters 7 and 8.',
      src:[BK + ', Wallet Technology Overview'] },
    { id:'SecretSharing', t:'Secret sharing', sub:'three of five, and two of five',
      def:'Secret sharing splits a secret into shares so that a chosen number of them recovers it and any fewer reveal nothing. The construction is polynomial: a polynomial whose constant term is the secret and whose degree is below the threshold is built, and each holder is given one point of it; any threshold-many points determine the polynomial, and therefore the secret, exactly.',
      take:'Any three of the five shares return the secret; any two return a wrong number, not a partial one.',
      note:'The last line is the property students find surprising and it is the one that matters: two shares do not give a blurry version of the secret, they give a value with no relation to it. Say that this demonstration is over a prime field for readability while SLIP39 works in a field of 256 elements, and that codex32 uses the same idea in the bech32 alphabet. The risk does not vanish: a threshold too low eases theft, too high eases loss.',
      src:['Rusnak et al., 2017', 'Olsson Curr et al., 2023'] } ] },
  { id:'RecoveryPractice', t:'Recovery as a practice', lead:'The chapter closes by saying that it is up to the reader to use the systems available and to test the backups regularly.',
    note:'These last two concepts are about behaviour rather than mechanism, and they are the ones most likely to decide whether a student keeps their coins.',
    items:[
    { id:'DataLoss', t:'Data loss', sub:'what the node itself offers',
      def:'Data loss is the ordinary failure the whole chapter is written against: a disk dies, a phone is lost, a file is overwritten. A recovery code answers it for the keys and not for anything else, and the software itself offers two mechanisms worth knowing: a command that copies the wallet file safely while the node runs, and a pool of keys prepared in advance so that a backup stays useful for a while after it is taken.',
      take:'Bitcoin Core copies the wallet file safely and prepares a thousand scripts ahead by default.',
      note:'Both lines are read out of the node’s own help text. The keypool is the subtle one, so explain the connection: the warning in that help says that smaller sizes increase the risk of losing funds when restoring from an old backup if none of the original pool’s addresses remain, which is the same gap-limit problem seen from the wallet’s side rather than the scanner’s. The lesson for students is that a backup has an expiry date unless the wallet is deterministic.',
      src:['Bitcoin Core, 2026', BK + ', chapter 5'] },
    { id:'BackupTesting', t:'Testing a backup', sub:'the only way to know it works',
      def:'Testing a backup means carrying out the restoration before it is needed: entering the code into a fresh wallet, checking that the expected addresses appear, and confirming that the derivation is the one the original used. The chapter closes the whole subject on this point, saying it is up to the reader to use the systems available and to test the backups regularly.',
      take:'The same words give the same seed every time; one wrong word fails the checksum at once.',
      note:'The three lines are the test in miniature: determinism, a valid code, and the refusal of a code with one word changed. Make the limits of each explicit, because students over-read them. The checksum catches most single-word errors and misses about one random error in 256; it says nothing about whether the derivation path is the one the original wallet used, and nothing at all about a passphrase, which has no checksum anywhere. That is why a real test restores and compares addresses rather than merely accepting the words.',
      src:[BK + ', chapter 5', 'Palatinus et al., 2013'] } ] } ] });

// ---------------------------------- rendering ----------------------------------
const DEFY = 1.08, DEFH = 1.88, TAKEY = 3.02, CODEY = 3.40, CAPY = 5.00, CODEMAX = 1.56;
function defFont(t) { return t.length > 480 ? 12 : t.length > 400 ? 12.5 : 13.5; }

function conceptSlide(c) {
  const s = light(); nContent++;
  title(s, c.t, c.sub);
  card(s, 0.5, DEFY, 9, DEFH, 'What it is', c.def, C.slate, defFont(c.def));
  if (c.take) s.addText('▸ ' + c.take, {x:0.5, y:TAKEY, w:9, h:0.34, fontFace:B, fontSize:12, bold:true, color:C.orange, margin:0, valign:'middle', isTextBox:true});
  const rows = EX[c.id];
  if (!rows) throw new Error('no executed example for concept ' + c.id);
  codeCard(s, rows, 0.5, CODEY, 9);
  pyCaption(s, CAPY);
  sourceLine(s, c.src);
  s.addNotes(c.note + '\n\nSources: ' + c.src.join('; ') + '. Every value on this slide was produced by running the statements shown, under Python ' + PY + '; the deck check re-runs them against the finished slides.');
  if (c.tbl) {
    const t2 = light(); nContent++;
    title(t2, c.t, 'the evidence behind the slide before this one');
    const n = c.tbl.length, cols = c.tbl[0].length;
    const colW = cols === 2 ? [6.2, 2.8] : cols === 3 ? [2.9, 4.3, 1.8] : [2.0, 2.3, 2.3, 2.4];
    const rowH = Math.min(0.6, 2.7 / (n - 1));
    table(t2, c.tbl, 0.5, 1.25, 9, colW, 12.5, rowH);
    const cy = 1.25 + rowH * n + 0.25;
    card(t2, 0.5, cy, 9, Math.max(0.85, 5.18 - cy), 'Why this table is here', c.take, C.orange, 13);
    sourceLine(t2, c.src);
    t2.addNotes(c.note);
  }
}

function groupSlide(g) {
  const s = light(); nContent++;
  title(s, g.t, 'what this part of the chapter contains');
  card(s, 0.5, 1.08, 9, 1.85, 'In one sentence', g.lead, C.orange, 13.5);
  tree(s, g.t, g.items.map(i => i.t), 0.5, 3.02, 9, 2.28, C.slate);
  s.addNotes(g.note);
}

function branchSlide(b) {
  const s = dark(); nContent++;
  s.addShape(pres.shapes.RECTANGLE, {x:0, y:0, w:0.22, h:5.63, fill:{color:C.orange}, line:{color:C.orange}});
  s.addText(b.t, {x:0.7, y:0.5, w:8.8, h:0.7, fontFace:H, fontSize:34, bold:true, color:C.white, margin:0, isTextBox:true});
  s.addText(b.sub, {x:0.7, y:1.2, w:8.8, h:0.4, fontFace:B, fontSize:15, italic:true, color:C.orange, margin:0, isTextBox:true});
  s.addText(b.lead, {x:0.7, y:1.75, w:8.8, h:1.65, fontFace:B, fontSize:14, color:'D7DEE6', margin:0, valign:'top', isTextBox:true});
  const names = b.groups.map(g => g.t + ' (' + g.items.length + ')');
  names.forEach((t, i) => {
    const w = 8.8 / names.length - 0.14, x = 0.7 + i * (w + 0.14);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y:3.65, w, h:0.78, fill:{color:C.slate}, line:{color:C.orange, width:1}, rectRadius:0.08});
    s.addText(t, {x:x+0.06, y:3.65, w:w-0.12, h:0.78, fontFace:B, fontSize:t.length > 24 ? 10.5 : 12, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
  });
  s.addText('Sources: ' + b.src.join('; '), {x:0.7, y:4.72, w:8.8, h:0.24, fontFace:B, fontSize:9.5, italic:true, color:'9AA7B4', margin:0, isTextBox:true});
  s.addNotes(b.note);
}


// ---------------------------------- 1. title ----------------------------------
let s = dark();
[0, 1, 2].forEach(i => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x:0.6+i*1.05, y:1.0, w:0.8, h:0.8, fill:{color:i===0?C.orange:C.slate}, line:{color:C.orange, width:1.5}, rectRadius:0.1});
  if (i < 2) s.addShape(pres.shapes.LINE, {x:1.4+i*1.05, y:1.4, w:0.25, h:0, line:{color:C.orange, width:1.5}});
});
s.addText('₿', {x:0.6, y:1.0, w:0.8, h:0.8, fontFace:B, fontSize:30, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
s.addText('Chapter 5: Wallet Recovery', {x:0.6, y:2.1, w:8.8, h:0.8, fontFace:H, fontSize:38, bold:true, color:C.white, margin:0, isTextBox:true});
s.addText('From twelve words to a tree of keys — and back again, with every value recomputed from the standards',
  {x:0.6, y:2.9, w:8.8, h:0.7, fontFace:B, fontSize:16, italic:true, color:C.orange, margin:0, valign:'top', isTextBox:true});
s.addText(COURSE, {x:0.6, y:4.55, w:8.8, h:0.45, fontFace:B, fontSize:12, color:'C9D1DA', margin:0, isTextBox:true});
s.addText('Mastering Bitcoin, 3rd edition, chapter 5 (' + BK + '), O’Reilly, free under CC BY-SA 4.0',
  {x:0.6, y:5.0, w:8.8, h:0.35, fontFace:B, fontSize:10.5, italic:true, color:'9AA7B4', margin:0, isTextBox:true});
s.addNotes('Open by saying what the session will do: take the chapter’s own twelve words and carry them all the way to an address that Bitcoin Core 31.1 derives independently from the same descriptor, stopping at every mechanism on the way. Every number, hash, key and address on these slides was produced by running the statement printed beside it under Python ' + PY + '. Say that the chapter 5 library used throughout is written for reading and is checked against the BIP32 and BIP380 test vectors and against a real node, and that it must never be used with real funds.');

// ---------------------------------- 2. what the chapter covers ----------------------------------
s = light(); title(s, 'What this chapter covers', 'and how this deck is built');
card(s, 0.5, 1.08, 4.4, 1.95, 'The chapter',
  'What a wallet really contains, where its keys come from, how a seed is written down as a recovery code, how one seed becomes a tree of keys, which parts of a backup the code does not contain, and how the keys are deployed in practice.', C.slate, 12);
card(s, 5.1, 1.08, 4.4, 1.95, 'This deck',
  'The chapter’s own concept taxonomy in its own order, one slide per concept, each with its worked example and the answer that example really produced. The check refuses the deck if a printed answer stops matching.', C.orange, 12);
table(s, [['What is on the slides','Count'],
          ['concepts of the chapter 5 taxonomy, each with its own slide','85'],
          ['concepts whose slide carries an executed worked example','85'],
          ['statements executed for this deck, with their real answers', String(NSTMT)],
          ['the chapter’s own tables and test vectors reproduced here','7']],
      0.5, 3.2, 9, [6.6, 2.4], 12, 0.37);
sourceLine(s, ['08-tooling/sen0401_ch05_corpus_v1_0_0.py', '08-tooling/ch05-deck/examples_out_v1_0_0.json']);
s.addNotes('The seven reproductions worth naming at the start, so the class knows what to expect: the chapter’s entropy and its twelve words, its seed without a passphrase, its seed with one, its table of code lengths, BIP32’s first test vector down to a hardened child, the chapter’s own xprv and xpub decoded, and BIP84’s first address checked against Bitcoin Core 31.1. Mention that the chapter corpus carries more than fits in one session and that the interactive page is where the rest lives.');

// ---------------------------------- 3. learning outcomes ----------------------------------
s = light(); title(s, 'Which learning outcomes this serves', 'SEN0401 outcome set, draft of 2026-10-04');
card(s, 0.5, 1.08, 9, 1.55, 'LO-5, the outcome of this chapter (Bloom level: Evaluate)',
  'Compare wallet and recovery designs — deterministic derivation, recovery codes, key stretching and salts, secret sharing, output descriptors, multisignature — and judge what each costs and protects when a key or a backup is lost or stolen.', C.orange, 13.5);
card(s, 0.5, 2.78, 4.4, 1.72, 'What it rests on',
  'LO-4, deriving keys and addresses from the standards. The elliptic-curve arithmetic, the hash functions and the address encodings of chapter 4 are used here without being re-explained.', C.slate, 12);
card(s, 5.1, 2.78, 4.4, 1.72, 'What it asks for beyond that',
  'Judgement. The level is Evaluate, not Apply: most of this chapter is a comparison of designs whose costs fall on different people at different times.', C.slate, 12);
s.addText('The outcome set is a draft of 2026-10-04 and carries no approval: the university catalogue page for this course still lists the outcomes of an earlier special topic, software architecture and design patterns, and none of those is carried here.',
  {x:0.5, y:4.58, w:9, h:0.62, fontFace:B, fontSize:10.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
sourceLine(s, ['01-outcomes/sen0401_outcomes_v1_0_0.ttl, items LO-4 and LO-5']);
s.addNotes('Read LO-5 aloud and point out the verb: judge. Most of the questions in this chapter have no single right answer, because a passphrase, a threshold or a gap limit trades one risk against another, and the deck is built so that each trade is stated with both sides. Be honest about the status of the outcome set: it was drafted from this repository’s own evidence, the owner has not approved it, and no assessment may be aligned to it yet.');

// ---------------------------------- 4. chapter map ----------------------------------
s = light(); title(s, 'The chapter in one picture', 'eight branches, eighteen groups, eighty-five concepts');
{
  const bw = 1.07;
  CH.forEach((b, i) => {
    const x = 0.5 + i * (bw + 0.07);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y:1.15, w:bw, h:0.72, fill:{color:C.orange}, line:{color:C.orange}, rectRadius:0.08});
    s.addText(b.t, {x:x+0.03, y:1.15, w:bw-0.06, h:0.72, fontFace:H, fontSize:9, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
    s.addShape(pres.shapes.LINE, {x:x+bw/2, y:1.87, w:0, h:0.17, line:{color:C.mute, width:1}});
    b.groups.forEach((g, j) => {
      const y = 2.04 + j * 0.60;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y, w:bw, h:0.52, fill:{color:C.pale}, line:{color:C.line, width:1}, rectRadius:0.06});
      s.addText(g.t + '\n' + g.items.length, {x:x+0.03, y, w:bw-0.06, h:0.52, fontFace:B, fontSize:7.5, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true});
      if (j > 0) s.addShape(pres.shapes.LINE, {x:x+bw/2, y:y-0.08, w:0, h:0.08, line:{color:C.line, width:1}});
    });
  });
}
s.addText('Each branch opens with its own slide; each group opens with the concepts it holds; each concept has a slide of its own with the code that produced its numbers. The number under a group is how many concepts it contains.',
  {x:0.5, y:4.92, w:9, h:0.45, fontFace:B, fontSize:11.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
sourceLine(s, ['08-tooling/sen0401_ch05_corpus_v1_0_0.py, the chapter 5 taxonomy']);
s.addNotes('Use the picture to set the shape of the session. The first three branches answer what a wallet holds and how a seed is written down; the middle three build the tree and then admit what the tree does not record; the last two are practice and the foundations the chapter assumed. Point at the fifth branch and say that it is where money is actually lost, so that the class knows why the long middle section matters.');

// ---------------------------------- the body ----------------------------------
CH.forEach(b => { branchSlide(b); b.groups.forEach(g => { groupSlide(g); g.items.forEach(conceptSlide); }); });

// ---------------------------------- what the chapter reproduces ----------------------------------
s = light(); nContent++;
title(s, 'What this session reproduced', 'the chapter’s own tables and the standards’ own vectors');
table(s, [['Printed in the chapter or the standard','Recomputed here'],
          ['128 bits of entropy → twelve words, and back again','agrees, checksum valid'],
          ['the same words → a seed beginning 5b56c417303faa3f','agrees'],
          ['the same words with a passphrase → 3b5df16df2157104','agrees'],
          ['the table of entropy, checksum and word count, five rows','agrees in every row'],
          ['BIP32 test vector 1: master key, chain code, first hardened child','agrees'],
          ['the chapter’s xprv and xpub, decoded field by field','checksums valid'],
          ['BIP84 test vector → bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu','agrees with Bitcoin Core 31.1']],
      0.5, 1.15, 9, [5.9, 3.1], 12, 0.44);
s.addText('Nothing here was copied from the book. Each line was computed from the chapter’s own inputs with the standard library, and the last was also derived independently by a node that had never seen this code.',
  {x:0.5, y:4.62, w:9, h:0.52, fontFace:B, fontSize:12.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
sourceLine(s, [BK, 'Palatinus et al., 2013', 'Wuille, 2012', 'Rusnak, 2017', 'Bitcoin Core, 2026']);
s.addNotes('Use this slide to make the method explicit before the recap. Three kinds of agreement appear in it, and they are worth different amounts: agreement with the book shows that the book is right and that we read it correctly; agreement with a standard’s published test vector shows that the implementation is right; and agreement with an independent program that shares no code with ours is the strongest of the three. The last row has all three at once.');

// ---------------------------------- recap ----------------------------------
s = light(); nContent++;
title(s, 'Recap', 'the chapter in six sentences');
[['A wallet holds keys, not coins','The database is a collection of keys and notes; the coins are outputs on the blockchain, and ownership is the ability to prove control of a key.'],
 ['A recovery code is a written seed','Words encode entropy with a short checksum; a stretching function turns them into 512 bits, and any passphrase at all produces a different valid wallet.'],
 ['One seed becomes a tree','HMAC-SHA512 makes the master key and chain code; the same function with a key, a chain code and an index makes every child, and hardening protects what is above.'],
 ['A public branch can live in the open','An extended public key derives every normal child public key and no private one, which is how a shop takes payments on a machine that cannot spend.'],
 ['The code is not the whole backup','The tree does not say which paths were used, and labels and protocol data are not derived from anything: implicit paths or descriptors answer the first, separate backups the second.'],
 ['Every choice is a trade','A passphrase, a threshold, a gap limit, deniability against error detection: each protects against one loss and makes another more likely.']
].forEach(([h, t], i) => {
  const y = 1.12 + i * 0.68;
  s.addShape(pres.shapes.OVAL, {x:0.5, y:y+0.08, w:0.42, h:0.42, fill:{color:C.orange}, line:{color:C.orange}});
  s.addText(String(i + 1), {x:0.5, y:y+0.08, w:0.42, h:0.42, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
  s.addText([{text:h + ' — ', options:{bold:true, color:C.dark}}, {text:t, options:{color:C.ink}}],
    {x:1.08, y:y, w:8.4, h:0.6, fontFace:B, fontSize:11.5, valign:'middle', margin:0, isTextBox:true});
});
s.addNotes('Do not read the recap out; ask the class to supply the second half of each sentence from the first. The sixth is the one to dwell on, because it is what the Evaluate level of the outcome asks for: every mechanism in this chapter moves a risk rather than removing it, and naming who carries the new risk, and when, is the skill the chapter is teaching.');

// ---------------------------------- questions ----------------------------------
const QS = [
 ['Which shortcoming does BIP39 itself list that a version number would have removed?',
  ['The code is too long to write down',
   'The checksum covers the passphrase and so cannot be checked',
   'The word list changes with every release',
   'Software cannot tell which derivation a code belongs to, so it may show an empty wallet'], 3,
  'The standard lists the absence of a versioning scheme; Electrum version 2 and Aezeed add one.'],
 ['BIP39 calls its checksum short. What is the consequence the standard states?',
  ['About one random error in 256 is missed and no correction is possible',
   'The checksum cannot be computed without the passphrase',
   'Codes of 24 words have no checksum at all',
   'Two different codes always share a checksum'], 0,
  'The standard lists the modest odds of catching random errors among BIP39’s shortcomings.'],
 ['Why is plausible deniability dangerous as well as useful?',
  ['Because nothing can prove that everything has been revealed, so coercion may continue',
   'Because the second wallet is easier to brute force',
   'Because a duress wallet cannot hold any funds',
   'Because the passphrase becomes part of the checksum, so an attacker can tell the wallets apart'], 0,
  'The chapter states both sides: a thief who leaves may be detected, while an attacker who stays has no reason to stop.'],
 ['Against which attacker does BIP39’s key stretching help least?',
  ['An attacker who has seen half of the code',
   'An attacker guessing a whole 128-bit code',
   'An attacker with the user’s passphrase',
   'An attacker with special-purpose hardware'], 3,
  'The chapter says special-purpose hardware is not significantly affected by the 2,048 rounds.'],
 ['Why is public child derivation defined only for normal children?',
  ['Because hardened children have no chain code',
   'Because hardened children are not on the curve',
   'Because a hardened child’s hash needs the parent private key',
   'Because the index would overflow 32 bits'], 2,
  'BIP32’s public derivation function returns failure for an index of 2 to the 31 or more.'],
 ['A merchant gives an auditor the account’s extended public key. What has the auditor gained?',
  ['The power to spend from the account',
   'Sight of the receiving addresses only, since change hangs from another branch',
   'Nothing, since the key is public',
   'Sight of every payment of that account, in and out, and no power to spend'], 3,
  'BIP32 lists audits among its use cases for exactly this sharing; the change branch is also a normal child.'],
 ['What is the disadvantage of implicit paths?',
  ['A wallet must derive and scan every path it supports, which is wasteful and may still miss funds',
   'They require extra information beside the code, which may reduce privacy',
   'They cannot be used with a passphrase',
   'They only work for multisignature wallets'], 0,
  'The chapter calls their inflexibility the disadvantage, with the version-number problem as its sharpest form.'],
 ['Why can a two-of-three participant not restore the arrangement from their own seed alone?',
  ['Because they need the other two public keys to recognise the joint funds',
   'Because their own key is not derived from their seed',
   'Because the funds are held by the other two',
   'Because the threshold is stored on the blockchain'], 0,
  'The chapter’s Alice, Bob and Carol example is the reason implicit paths are not enough.'],
 ['Which of the three choices for a wallet at its gap limit keeps privacy but risks a restoration?',
  ['Refusing further requests',
   'Handing out keys it has already given away',
   'Generating keys beyond the limit',
   'Lowering the limit'], 2,
  'Other software with the same extended public key will not see payments received after the extended gap.'],
 ['What does a static channel backup let a user recover?',
  ['The funds fully settled in the channel, not those in payments still in flight',
   'Every payment the channel ever routed',
   'The channel itself, which the protocol reopens automatically after a recovery',
   'Nothing without the other party’s backup'], 0,
  'The backup is made when the channel is created, so it cannot describe later payments.']];

for (let i = 0; i < QS.length; i += 2) {
  const s2 = light(); nContent++;
  title(s2, 'Check yourself', 'questions ' + (i + 1) + ' and ' + (i + 2) + ' of ' + QS.length + ', from the chapter’s own question bank');
  const notes = [];
  [0, 1].forEach(j => {
    const q = QS[i + j]; if (!q) return;
    const y0 = 1.12 + j * 2.1;
    s2.addShape(pres.shapes.OVAL, {x:0.5, y:y0, w:0.42, h:0.42, fill:{color:C.orange}, line:{color:C.orange}});
    s2.addText(String(i + j + 1), {x:0.5, y:y0, w:0.42, h:0.42, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
    s2.addText(q[0], {x:1.08, y:y0-0.04, w:8.4, h:0.5, fontFace:B, fontSize:13.5, bold:true, color:C.dark, valign:'middle', margin:0, isTextBox:true});
    s2.addText(q[1].map((o, n) => ({text:'(' + 'abcd'[n] + ')  ' + o, options:{breakLine:n < q[1].length - 1}})),
      {x:1.08, y:y0+0.5, w:8.4, h:1.45, fontFace:B, fontSize:11.5, color:C.ink, valign:'top', margin:0, paraSpaceAfter:2, isTextBox:true});
    notes.push('Question ' + (i + j + 1) + ': the answer is (' + 'abcd'[q[2]] + '). ' + q[3]);
  });
  sourceLine(s2, ['08-tooling/ch05-page/question_bank_v1_0_0.json, the chapter 5 bank']);
  s2.addNotes(notes.join('\n\n') + '\n\nGive the class a minute on each, take a show of hands on every option before revealing, and ask for the reason rather than the letter.');
}

// ---------------------------------- sources ----------------------------------
s = light(); nContent++;
title(s, 'Sources', 'every claim beyond the book is in the chapter’s research record');
const SRC = [
 'Antonopoulos, A. M., and Harding, D. A. (2023). Mastering Bitcoin, 3rd edition, chapter 5, with the glossary and chapters 7 and 14. O’Reilly. CC BY-SA 4.0.',
 'Wuille, P. (2012). BIP32, Hierarchical Deterministic Wallets. Palatinus, M., et al. (2013). BIP39, Mnemonic code, and its English word list.',
 'Palatinus, M., and Rusnak, P. (2014). BIP43, Purpose field, and BIP44, Multi-account hierarchy. Weigl, D. (2016). BIP49. Rusnak, P. (2017). BIP84. Chow, A. (2021). BIP86.',
 'Wuille, P., and Chow, A. (2021). BIP380 to BIP386, Output script descriptors. Chow, A. (2022). BIP389, Multipath key expressions. Wuille, P., et al. (2023). BIP379, Miniscript.',
 'Raw, C. (2022). BIP329, Wallet label export format. Olsson Curr, L., et al. (2023). BIP93, codex32.',
 'Rusnak, P., et al. (2017). SLIP-0039, Shamir secret sharing for mnemonic codes. Rusnak, P., and Palatinus, M. (2014). SLIP-0044, Registered coin types.',
 'Electrum Technologies (2026). The Seed Version System. Lightning Labs (2026). The aezeed cipher seed, and Recovering Funds From lnd.',
 'Muun (2026). Recovery tool. BTCPay Server contributors (2026). BTCPay Server. Lopp, J. (2026). Known Physical Bitcoin Attacks.',
 'Krawczyk, H., et al. (1997). RFC 2104, HMAC. Moriarty, K., et al. (2017). RFC 8018, PKCS #5 and PBKDF2. Percival, C., and Josefsson, S. (2016). RFC 7914, scrypt.',
 'Bitcoin Core (2026). Release 31.1, run as an offline node for this chapter, and the wallet sources and documentation at commit 05bc2f5. Evidence in 08-tooling/ch05-evidence.',
 'Trezor (2026). The BIP39 test vectors of python-mnemonic. Python Software Foundation (2026). The hashlib module, Python 3.14.4.',
 'Altunel, Y. (2021). Course notes for this chapter, written on the 2nd edition and checked against the 3rd before use.'];
s.addText(SRC.map((t, i) => ({text:t, options:{bullet:true, breakLine:i < SRC.length - 1}})),
  {x:0.5, y:1.12, w:9, h:3.75, fontFace:B, fontSize:10.5, color:C.ink, paraSpaceAfter:3, margin:0, valign:'top', isTextBox:true});
s.addText('These slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0 and are shared under the same licence. The full verified list, with the author-year string of every citation, is 03-materials/ch05/rdodi/sen0401_ch05_research_v1_0_0.ttl.',
  {x:0.5, y:4.95, w:9, h:0.5, fontFace:B, fontSize:10, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
s.addNotes('Point the class at the research record rather than at this list: every publication there carries the role it played, the place the saved copy lives and the claim that re-reads it. Every file named here was saved into the repository and compared with its upstream copy on 2 October 2026, so a claim made in an assignment can be checked against the same bytes the chapter used.');

// ---------------------------------- closing ----------------------------------
s = dark();
s.addText('Next: Chapter 6 — Transactions', {x:0.7, y:1.6, w:8.6, h:0.9, fontFace:H, fontSize:32, bold:true, color:C.white, margin:0, isTextBox:true});
s.addText('The keys of chapters 4 and 5 exist to authorise spending. Chapter 6 takes the transaction apart: inputs, outputs, scripts and fees.',
  {x:0.7, y:2.5, w:8.6, h:0.9, fontFace:B, fontSize:16, color:C.orange, margin:0, valign:'top', isTextBox:true});
s.addText('Before then: work through the chapter 5 page, restore the chapter’s twelve words in the playground, and bring one derivation you could not reproduce.',
  {x:0.7, y:3.5, w:8.6, h:0.6, fontFace:B, fontSize:14, color:'C9D1DA', margin:0, valign:'top', isTextBox:true});
s.addText('Questions?', {x:0.7, y:4.35, w:8.6, h:0.6, fontFace:H, fontSize:24, italic:true, color:'9AA7B4', margin:0, isTextBox:true});
s.addNotes('Set the preparation concretely: restoring the chapter’s own words and reaching the BIP84 address is a complete exercise that uses every mechanism of the session, and anyone who cannot reach it has found a real gap in their understanding rather than a typing mistake. Remind the class once more that none of this code is for real funds.');

pres.writeFile({fileName:process.argv[2]}).then(f => console.log('written', f, '-', nContent, 'content slides,', nCode, 'executed statements shown'));
