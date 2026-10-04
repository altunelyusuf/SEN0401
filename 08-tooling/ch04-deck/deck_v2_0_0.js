// SEN0401 chapter 4 lecture deck, version 2.0.0 - Keys and Addresses (Mastering Bitcoin, 3rd edition, chapter 4).
// Built with pptxgenjs from the chapter 4 corpus (08-tooling/sen0401_ch04_corpus_v1_1_0.py): the taxonomy's own order,
// one section per branch, one slide per concept, and for every concept that has a worked example the code with the
// output that examples_run_v2_0_0.py actually obtained - no number on a slide is typed from memory.
// Usage: node deck_v2_0_0.js <out.pptx>
const VERSION = "2.0.0";
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const EX = JSON.parse(fs.readFileSync(__dirname + '/examples_out_v2_0_0.json'));
const PY = EX._python;
const NSTMT = Object.keys(EX).filter(k => k[0] !== '_').reduce((n, k) => n + EX[k].length, 0);

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Yusuf Altunel';
pres.title = 'SEN0401 Chapter 4 - Keys and Addresses';
pres.subject = 'Mastering Bitcoin 3rd edition, chapter 4, recomputed from the standards';

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

// ---------------- the deck's content, in the order of the chapter 4 taxonomy ----------------
// Each concept: id (the taxonomy identifier, and the key of its executed example), t (its human label), sub (the
// worked example's own one-line title), def (the explanation, compressed from the concept's paragraphs for speaking),
// take (the sentence to leave on the screen), note (the speaker's notes), src (the author-year citations), and
// optionally tbl (a table instead of, or beside, the code) and nocode.
const CH = [];

// ============================== BRANCH 1: KEYS ==============================
CH.push({
  id:'Keys', t:'Keys', sub:'From a random number to the right to spend',
  lead:'Alice wants to pay Bob, but the thousands of full nodes that will verify her transaction do not know who Alice or Bob are, and the design keeps it that way. A key pair settles the question a bank would settle from its records: who may spend this coin. The private key is a secret number, the public key is derived from it and may be shared, and a signature made with the private key is checked by anyone holding the public key.',
  note:'Open the branch by naming the problem before the mathematics: a network whose members do not trust one another, and no register of account holders. The whole chapter is the answer to that one problem. Two warnings run through everything that follows and should be said now, not at the end: the private key must stay secret at all times, because handing it to a third party hands over the coins; and the key must come from a source of randomness nobody can predict or repeat.',
  src:[BK + ', chapter 4, Introduction'],
  groups:[
  { id:'KeyPair', t:'Key pair', lead:'The key pair is the smallest unit of ownership Bitcoin knows: the public key receives funds and the private key signs the transactions that spend them.',
    note:'Insist on the asymmetry. The two keys are mathematically related but the relation runs one way only, and every later section of the chapter depends on that. Students who have met encryption first will expect the pair to be used for secrecy; correct that expectation here rather than later.',
    items:[
    { id:'PublicKeyCryptography', t:'Public key cryptography', sub:'signatures, not secrecy',
      def:'Public key cryptography, also called asymmetric cryptography, gives every participant two different but mathematically related keys. The function joining them is easy to compute in one direction and infeasible to reverse, so the public key can be published while the private key stays secret. Bitcoin uses the multiplication of points on an elliptic curve for that function, and it uses the scheme to prove authorship, not to hide anything: nothing in a transaction is encrypted.',
      take:'Related keys, one-way function: the public key is derived from the private key, never the other way round.',
      note:'The single most common misunderstanding in this chapter is that signing hides the transaction. It does not: the blockchain is public, and every amount, address and script in it can be read by anybody. What asymmetric cryptography buys Bitcoin is that only the holder of a private key can produce a signature, while everybody can check it. The example on the slide makes the relation concrete: multiplying the next private key by the generator gives exactly the public key one generator step further along, so the two keys really are tied by arithmetic and not by a lookup table.',
      src:[BK + ', Public Key Cryptography and Cryptocurrency'] },
    { id:'DigitalSignature', t:'Digital signature', sub:'a number only the key holder can produce',
      def:'A digital signature is a number computed from a message and a private key. Anyone holding the message, the signature and the matching public key can check that the signature was made by the holder of that private key and that the message has not changed since. Bitcoin has traditionally used the Elliptic Curve Digital Signature Algorithm over secp256k1 with SHA256 hashes, encoded in up to 72 bytes.',
      take:'The signature binds one key to one message: change either and verification fails.',
      note:'Run the example slowly. The same signature is checked twice, once against the message that was signed and once against a message one unit different, and only the first is accepted; that is what it means for a signature to bind to its message. Emphasise the nonce, the one-time number every signature consumes: the teaching sketch in the chapter toolkit takes it as an argument so that the output is reproducible, but a real signer must derive it deterministically or draw it from a secure source, because two signatures made with the same nonce reveal the private key.',
      src:[BK + ', Public Key Cryptography and Cryptocurrency', 'Wuille et al., 2020'] },
    { id:'PrivateKey', t:'Private key', sub:'a random number below n',
      def:'A private key is simply a number, picked at random. It may be any value between 1 and n minus 1, where n is the order of the secp256k1 curve, a constant slightly smaller than 2 to the 256. Control of that one number is the root of control over every coin paid to the public key derived from it, because the signatures that spend those coins cannot be made without it.',
      take:'Almost every 256-bit number is a valid key: n is only about 4.3 times 10 to the 38 short of 2 to the 256.',
      note:'The arithmetic on the slide answers the question students always ask, whether keys can collide: the gap between 2 to the 256 and the curve order is a 39-digit number, which sounds enormous but is vanishingly small beside 2 to the 256 itself, so a random 256-bit number is a valid key with overwhelming probability. The third line shows the error a programmer meets first: a 256-bit value does not fit in 32 bytes once it reaches 2 to the 256 exactly. Note also that the book prints n as 1.1578 times 10 to the 77 where the constant gives 1.1579; a rounding slip with no practical consequence, but worth naming, because this chapter is about checking rather than believing.',
      src:[BK + ', Private Keys', 'Certicom Research, 2010'] },
    { id:'PublicKey', t:'Public key', sub:'K = k × G',
      def:'A public key is a point on the elliptic curve, obtained by multiplying the fixed generator point G by the private key k. The generator is the same for every Bitcoin user, so one private key always yields the same public key, and because the multiplication cannot be run backwards the public key gives nothing away about the key that made it.',
      take:'The coordinates on this slide are the ones the book prints for its example key.',
      note:'Point out that the printed x coordinate begins F028892B and the y coordinate ends 2E505BDB, exactly the values in the book, and that they were recomputed here rather than copied. The third line is the boundary of the key space: multiplying the generator by the curve order gives the point at infinity, which is why no private key may be n or larger. Remind the class that a public key is public in the sense that it may be shared, not that it must be published early; addresses keep it behind a hash until the coins are spent.',
      src:[BK + ', Public Keys'] } ] },
  { id:'RandomSource', t:'Randomness', lead:'A private key protects funds only to the extent that nobody can guess it, so the first step of generating a key is finding a source of unpredictability.',
    note:'This group is short but it is where real money is lost. A key that looks arbitrary can still come from a seed as small as the current clock, and such a key is found in a few million tries instead of the 10 to the 77 the key length suggests.',
    items:[
    { id:'Entropy', t:'Entropy', sub:'a coin tossed 256 times',
      def:'Entropy is the unpredictability of the material a random number is made from, counted in bits. Each fair coin toss nobody can foresee contributes one bit, so the book’s tip that 256 tosses give the binary digits of a private key is a statement about 256 bits of entropy. The count of bits is the count of equally likely possibilities an attacker would have to try.',
      take:'256 bits of entropy is about 10 to the 77 possibilities, a number with 78 decimal digits.',
      note:'Make the distinction between entropy and output length, because students conflate them. A pseudorandom generator can stretch entropy but cannot create it, so 256 bits of output seeded from 20 bits of entropy offers 20 bits of resistance, not 256. The logarithm on the slide is the honest way to state the size of the key space; quoting 2 to the 256 means nothing to most listeners until it is turned into 77 decimal digits.',
      src:[BK + ', Private Keys'] },
    { id:'SecureRandomness', t:'Secure randomness', sub:'secrets rather than random',
      def:'A cryptographically secure pseudorandom generator produces numbers an attacker cannot predict even after seeing earlier output. The book’s instruction is categorical: do not write your own random code, do not use the ordinary generator of your language, and read the documentation of the library you choose. In Python the secrets module is documented for exactly this use, and secrets.randbelow draws from the most secure source the operating system offers.',
      take:'secrets is for security; the random module is documented for modelling and simulation.',
      note:'This is a rule students can apply the same evening, so state it as a rule. Show that the two modules look interchangeable in an editor and are not: the documentation of Python’s random module says in its own words that its generator is for modelling and simulation and not for security. Add the failures that remain even with the right module: seeding it yourself with a poor value, calling it before the system has gathered entropy, or running on a machine whose random source is already compromised.',
      src:[BK + ', Private Keys', 'Python Software Foundation, 2026'] } ] },
  { id:'Curve', t:'The curve', lead:'A reader who only wants to use Bitcoin may treat the step from private key to public key as a black box; a reader who wants to judge its security may not.',
    note:'Signal the shape of this group before entering it: two general objects, the finite field and the elliptic curve, then the single operation defined on them, then the particular curve Bitcoin fixed, then the operation that makes the whole thing one-way. Nothing here is needed to use Bitcoin and all of it is needed to argue about its security.',
    items:[
    { id:'FiniteField', t:'Finite field', sub:'arithmetic modulo a prime',
      def:'A finite field of prime order p is the whole numbers from 0 to p minus 1 with the four arithmetic operations carried out modulo p, so that every result is replaced by its remainder after division by p. Numbers never grow beyond p, and every non-zero number has a partner that multiplies with it to give 1, which is how division works there. Bitcoin’s curve is defined over such a field rather than over the real numbers because modular arithmetic is exact in software, while real numbers have to be rounded.',
      take:'Dividing by 5 modulo 17 is multiplying by 7, because 5 times 7 is 35, which leaves 1.',
      note:'Students accept the formula and then misuse the intuition, so say plainly that a finite field is not a number line: once results wrap around, 16 is not usefully greater than 1. The third line of the example is the one case where division fails, namely zero, and it is the error a careless implementation of point addition produces. If time allows, ask the class to find the partner of 3 modulo 17 by hand before you show pow with a negative exponent.',
      src:[BK + ', Elliptic Curve Cryptography Explained'] },
    { id:'EllipticCurve', t:'Elliptic curve', sub:'y squared = x cubed + 7',
      def:'An elliptic curve is the set of points whose coordinates satisfy an equation of a particular form, together with one extra point called the point at infinity. Bitcoin’s curve is y squared = x cubed + 7, computed modulo the prime p; in the notation of the standard the equation is y squared = x cubed + ax + b with a equal to 0 and b equal to 7. Such a curve is chosen because its points can be added by a simple rule, which gives a system where multiplication is easy and its inverse is believed hard.',
      take:'Over the tiny field with 17 elements the same curve has 17 points besides the point at infinity.',
      note:'The word elliptic is misleading and worth disposing of at once: the curve is not an ellipse, and the smooth picture in the book is drawn over the real numbers only to explain the geometry of addition. The real curve has whole-number points modulo p and the drawn lines do not exist there. The small field on the slide is the antidote: seventeen points can be listed on the board, and the class can see that there is nothing continuous about them. The second line checks that the standard’s own generator point satisfies the equation.',
      src:[BK + ', Elliptic Curve Cryptography Explained', 'Certicom Research, 2010'] },
    { id:'PointAddition', t:'Point addition', sub:'draw a line, take the third point, reflect it',
      def:'Point addition combines two points of the curve into a third point of the same curve: draw the line through them, find the one further place where it meets the curve, and reflect that point in the x axis. If the two points are the same, the line is replaced by the tangent. If they are mirror images, the line meets the curve nowhere else, and the result is the point at infinity, which plays the part of zero.',
      take:'Addition is the only operation that must be defined; everything else in the chapter is built from it.',
      note:'Work the example on the board in the small field: the points one comma five and two comma seven add to one comma twelve, and one comma five added to its own mirror gives the point at infinity. Then say what the picture hides. The formulas software uses are algebraic, not geometric, and they divide in the finite field, so each case, doubling, mirror points and infinity, needs its own branch; a mistake in any branch produces points that are not on the curve and public keys nobody can use.',
      src:[BK + ', Elliptic Curve Cryptography Explained'] },
    { id:'Secp256k1', t:'The secp256k1 curve', sub:'y squared = x cubed + 7 over a 256-bit prime field',
      def:'The name secp256k1 identifies the curve and the constants Bitcoin uses: the prime p, the coefficients a equal to 0 and b equal to 7, the generator point G, the order n of G, and the cofactor 1, which means that the points of the curve are exactly the multiples of G. The prime is 2 to the 256 minus 2 to the 32 minus 977, the same value the book writes as a longer sum of powers of two.',
      take:'One curve and one generator, so every program derives the same public key from the same private key.',
      note:'The two spellings of the prime on the slide are the same number, and showing that they agree is a small lesson in reading standards: the book gives the long form, the standard gives the short one. The last line checks that both p and n are prime, which the parameters must be. This is also the moment to flag the chapter’s first correction, which the next slide takes up: the book attributes the curve to NIST, and its own primary source does not.',
      src:[BK + ', Elliptic Curve Cryptography Explained', 'Certicom Research, 2010'] },
    { id:'CurveStandard', t:'Curve standard: SEC 2, not NIST', sub:'a statement of the book that its source does not support',
      def:'A curve standard is a published document fixing the constants of a curve so that independent programmers obtain the same curve. Bitcoin’s curve is defined in SEC 2, Recommended Elliptic Curve Domain Parameters, version 2.0, published on 27 January 2010 by Certicom Research. Section 2.4.1 of that document specifies secp256k1 and section 2.4.2 specifies secp256r1, and its Table 2 records, for each curve, which other standards it conforms to.',
      take:'In SEC 2 Table 2 the NIST column holds a dash for secp256k1 and r for secp256r1.',
      note:'This is a finding of the chapter and should be taught as one, not as a complaint. The book says secp256k1 was established by the National Institute of Standards and Technology; the curve is defined by Certicom Research, and the standard’s own alignment table marks it as not on the NIST list, while the sister curve secp256r1 is marked as recommended. The line on the slide reads those two rows out of the saved copy of the table rather than restating them. The teaching point is the method: when a textbook attributes a thing to an authority, the attribution is checkable, and here it does not hold.',
      src:['Certicom Research, 2010, Table 2', BK + ', Elliptic Curve Cryptography Explained'],
      tbl:[['Curve','Section of SEC 2','ANSI X9.62','NIST column'],
           ['secp256k1','2.4.1','c: conformant','– : not in the NIST list'],
           ['secp256r1','2.4.2','r: recommended','r: recommended']] },
    { id:'GeneratorPoint', t:'Generator point', sub:'G, the same for every key',
      def:'The generator point G is the predetermined point of the standard by which a private key is multiplied to obtain a public key. It is fixed for all Bitcoin keys, and the standard publishes it in compressed form as 02 followed by its x coordinate. The order n is the number of times G must be added to itself to reach the point at infinity, so n minus one times G is the mirror image of G.',
      take:'The generator is public and contributes nothing to secrecy: all the secrecy is in the multiplier.',
      note:'Students sometimes treat G as if it were part of the key material. Say clearly that it is a published constant, printed in the standard, identical in every wallet on earth, and that this is precisely what makes two programs agree on a public key without exchanging anything. The second line is the proof that n is the order: adding G to the point n minus one times G returns the point at infinity. Warn against confusing G with a public key; a public key is a multiple of G chosen by a secret.',
      src:['Certicom Research, 2010', BK + ', Public Keys'] },
    { id:'PointMultiplication', t:'Elliptic curve multiplication', sub:'double and add, about 256 steps',
      def:'Multiplying a point by a whole number k means adding it to itself k times. Adding G to itself 2 to the 256 times would be impossible, so software reads the bits of k instead: it doubles a running point once per bit and adds it into the answer wherever the bit is one. For the book’s example key that is 252 doublings and 123 additions, a few hundred operations in place of an astronomical number.',
      take:'The book calls it a trap door: easy forwards as multiplication, impossible backwards as division.',
      note:'Derive the two numbers with the class rather than announcing them: the bit length of the key minus one gives the doublings and the count of one bits minus one gives the additions, which is why both appear on the slide as a computation. Then state the asymmetry that the rest of the chapter depends on. Multiplication is cheap in both the book’s sense and the machine’s sense, while the reverse direction, recovering k from K, is the discrete logarithm problem of the next slide.',
      src:[BK + ', Public Keys'] },
    { id:'DiscreteLogarithm', t:'Discrete logarithm', sub:'finding k from K, with no shortcut',
      def:'The discrete logarithm problem asks for the multiplier when the product is known: given the public key K and the generator G, find k with K = kG. No method better than trying values is known for secp256k1, so the work is a brute-force search over about 10 to the 77 candidates. The standard credits the curve with a security strength of about 128 bits, the approximate number of bits of security its parameters offer.',
      take:'In a toy group modulo 101 the search takes nine tries; in the real group it takes 2 to the 128.',
      note:'The small search on the slide is there so that the class sees what a discrete logarithm actually is before meeting the impossible version. Then be careful about the strength of the claim: the difficulty is an assumption about the present state of mathematics and computing, not a proved theorem, and the book is deliberately careful to speak of what is infeasible with the computers and algorithms available today. Students who ask about quantum computers are asking exactly the right question, and the honest answer is that the assumption is what would fail.',
      src:[BK + ', Public Keys', 'Certicom Research, 2010'] },
    { id:'CryptoLibrary', t:'Cryptographic library', sub:'libsecp256k1, and why this toolkit is only a sketch',
      def:'A cryptographic library is tested, reusable code for calculations that must be exactly right, because an error that passes every ordinary test can still leak a key or accept a forged signature. Many Bitcoin implementations delegate the curve arithmetic to libsecp256k1. The toolkit written for this chapter does the same arithmetic in thirteen lines of Python so that it can be read, and it reproduces every key and address on these slides.',
      take:'Written for reading, not for funds: not constant-time, and careless about where randomness comes from.',
      ecsrc:true,
      note:'Use this slide to set the ground rules for the laboratory work. The point of a readable implementation is that a student can see what the library does; the point of the library is that nobody should ship the readable one. Name the two specific defects the toolkit itself declares, timing that depends on the key and no care over randomness, and connect them back to the secure-randomness slide. The next slide prints the thirteen lines, and the deck check refuses the deck if what is printed ever differs from what was executed.',
      src:[BK + ', Public Keys'] } ] },
  { id:'Hashing', t:'Hash functions', lead:'Bitcoin needed to refer to objects larger than 65 bytes with the smallest amount of data that was still secure; a hash function is that reference.',
    note:'Introduce hashing as the second tool beside the curve, and keep the two apart in the students’ minds. The curve makes ownership provable; hashing makes references short and binding. Addresses need both.',
    items:[
    { id:'HashFunction', t:'Hash function', sub:'same input, same output',
      def:'A hash function takes a potentially large amount of data and returns a fixed amount. A cryptographic hash function always gives the same output for the same input, and a secure one makes it impractical to find a different input giving a previously seen output. Those two properties together make the output a commitment to the input: a promise that, in practice, only that input produces that output.',
      take:'Two inputs one bit apart give digests differing in 139 of their 256 bits, close to half.',
      note:'The avalanche demonstration on the slide is worth doing live: the letters a and the backtick differ in a single bit, and their digests differ in more than half their bits. Then correct the usual confusion: a hash is not an encryption, there is no key and no way back except guessing, which also means it is a poor way to hide a value drawn from a small set. That caveat returns later in the chapter when commitments are discussed.',
      src:[BK + ', Legacy Addresses for P2PKH', 'National Institute of Standards and Technology, 2015'] },
    { id:'Sha256', t:'SHA256', sub:'32 bytes of output',
      def:'SHA256 is the member of the SHA family whose output is 256 bits, or 32 bytes, and the book calls it the function most commonly used in Bitcoin and considers it very secure. The input may have any length and the output always has 32 bytes. In this chapter it appears three times: as the first step of HASH160, as the double hash that gives base58check its checksum, and as the function that turns random bits into a candidate private key.',
      take:'Its output is less than half the size of the 65-byte public keys the early software used.',
      note:'Give the class the standard digest of the three bytes abc, which begins ba7816bf, as a value they can check in any language on any machine; reproducibility across implementations is the whole point. The third line is a trap worth showing: hashlib refuses a text string, because hashing is defined on bytes and the encoding has to be chosen by the programmer. Close with the security caveat: a 256-bit output does not mean 256 bits of resistance to every attack, and for finding two colliding inputs the work is only the square root, 128 bits.',
      src:[BK + ', Legacy Addresses for P2PKH', 'National Institute of Standards and Technology, 2015'] },
    { id:'Ripemd160', t:'RIPEMD-160', sub:'20 bytes of output',
      def:'RIPEMD-160 produces 160 bits, or 20 bytes, and the book describes it as one of the slightly less secure functions that give smaller output than SHA256. Its place in Bitcoin is the second step of the commitment to a public key, applied to the SHA256 digest of that key. A smaller output means a shorter address and a smaller transaction, and Satoshi Nakamoto never stated the reason for the choice.',
      take:'The 20 bytes on this slide are the commitment to the book’s compressed example key.',
      note:'Flag the practical problem before students meet it in the laboratory: RIPEMD-160 is available only where the underlying library provides it, and the browser Python of the course pages does not, which is why those pages give the values as data. Then state the security consequence of the shorter output. Against an attacker who only knows the digest the work is 2 to the 160, but against one who can influence the input it falls to the square root, 2 to the 80, and that is the number the chapter returns to when it discusses P2SH.',
      src:[BK + ', Legacy Addresses for P2PKH'] },
    { id:'Hash160', t:'HASH160', sub:'RIPEMD160(SHA256(K))',
      def:'HASH160 is the name of the combination RIPEMD160(SHA256(K)): the data is passed into SHA256 and the resulting digest into RIPEMD-160, leaving 20 bytes. The book writes it as A = RIPEMD160(SHA256(K)), where K is a public key and A the commitment. The same construction commits to a public key in a pay to public key hash output and to a script in a pay to script hash output, and the script operation OP_HASH160 performs it inside a script.',
      take:'HASH160 commits to bytes, so the two encodings of one key give two different commitments.',
      note:'The third line is the one students must carry away, and it is the source of a real class of lost funds: the compressed and uncompressed forms of a single public key hash to different twenty-byte values and therefore to different addresses, although the private key behind them is identical. Make them predict the answer before you show it. A wallet importing an old key must know which form that key was used in, or it will scan the chain for the wrong commitments and report a balance of zero.',
      src:[BK + ', Legacy Addresses for P2PKH'] } ] } ] });

// ============================== BRANCH 2: FORMAT ==============================
CH.push({
  id:'Format', t:'Format', sub:'Writing the same number down in different ways',
  lead:'A private key, a public key and a hash commitment are all numbers, and a number can be written in binary, in hexadecimal, in a compact alphabet with a built-in checksum, or as a barcode. Representation matters here because mistakes are expensive: any error in copying a commitment sends the coins to an output nobody can spend, and they are lost for ever.',
  note:'Set the rule for the whole branch at the start: never judge two strings to be different data because they look different, and never judge them the same because they begin alike. The chapter’s central example is one private key appearing in three formats and one public key appearing in two formats that yield two different addresses.',
  src:[BK + ', chapter 4, Private Key Formats'],
  groups:[
  { id:'Representation', t:'Representation of data', lead:'Every length the chapter quotes, 32 bytes, 65 bytes, 130 hexadecimal digits, is a statement about a representation rather than about the value itself.',
    note:'This group exists because an audit of the chapter found these terms used without ever being defined. Keep it brisk but do not skip it: the later sections are unreadable for a student who is not at ease with bits, bytes and bases.',
    items:[
    { id:'BitsAndBytes', t:'Bits and bytes', sub:'65 bytes is 520 bits',
      def:'A bit is a binary digit with the value 0 or 1, and a byte is a group of 8 bits. Sizes in Bitcoin are quoted in both units and the chapter moves between them freely: a private key is 256 bits shown as 64 hexadecimal digits of 4 bits each, a commitment is 160 bits or 20 bytes, and a public key is 65 bytes in the old encoding or 33 in the new one.',
      take:'The unit decides the size of the space: 160 bits gives 2 to the 160 values, 256 bits gives 2 to the 256.',
      note:'The most frequent mistake is to confuse the count of hexadecimal digits with the count of bytes: 64 digits are 32 bytes, not 64. The third line on the slide is the error Python raises when that confusion reaches the keyboard, an odd number of hexadecimal digits. Mention too that a byte is unsigned, so 0x80 is 128 and never a negative number, which matters when the wallet import format puts 0x80 in front of a key.',
      src:[BK + ', Private Keys'] },
    { id:'NumberBase', t:'Number base', sub:'hexadecimal, base58, base64',
      def:'A number base, or radix, is the count of distinct symbols a notation uses. Decimal uses ten, hexadecimal sixteen, base64 sixty-four and base58 fifty-eight; the larger the alphabet, the fewer symbols the same number needs. Base64 exists to carry binary data through text, and base58 is the same idea with the characters that look alike in some fonts removed.',
      take:'In base58 the symbol 1 has the value zero, which is why a leading zero byte shows as 1.',
      note:'The last line of the example is the one that repays attention. Students read an address beginning with the digit 1 and assume the 1 is a label; it is the base58 digit for zero, and it appears because the version byte of a legacy address is 0x00. Connect that now, because the version-prefix slide later depends on it. The middle line shows that the book’s example key really is 64 hexadecimal digits while its value needs 253 bits, since the leading digit is not F.',
      src:[BK + ', Base58check Encoding'] },
    { id:'QrCode', t:'QR code', sub:'an address as a picture',
      def:'A QR code is a two-dimensional barcode a camera reads to obtain a short piece of text, and wallets use them because they remove typing altogether. The size of the picture follows from the text: the bech32 specification requires encoders to emit lowercase, but allows an uppercase version for presentation, because uppercase permits the alphanumeric mode of QR codes, which is about 45 percent more compact than the byte mode.',
      take:'A mixed-case alphabet such as base58 cannot use that mode, so its codes are larger at the same resolution.',
      note:'Show that the uppercase and lowercase forms are the same address and that a decoder must refuse a string mixing the two cases. Then make the practical point: whatever the camera reads is still text, and a careful wallet shows the decoded address so that the person can compare it with what was intended. A QR code is not a security feature; it is a typing aid, and a substituted picture is as dangerous as a substituted string.',
      src:[BK + ', Bech32m', 'Wuille and Maxwell, 2017'] } ] },
  { id:'KeyEncoding', t:'Key encoding', lead:'The same private key has several written forms and the same public key has two, and software that exports or imports keys has to agree on which.',
    note:'The practical stake: a wallet importing from an older wallet must know whether to scan the chain for 65-byte keys and their commitments or for 33-byte keys and theirs. Scanning for the wrong kind shows the user a balance that is not there.',
    items:[
    { id:'CompressedPublicKey', t:'Compressed public key', sub:'33 bytes: a prefix and x',
      def:'A compressed public key stores the x coordinate and one prefix byte instead of both coordinates. Because the point satisfies y squared = x cubed + 7, knowing x leaves only two possible values of y, a number and its negative modulo p, and the prefix 02 or 03 records which of the two by the parity of y. The saving is almost half the key, and it is repeated in every transaction that reveals a key.',
      take:'33 bytes against 65 is 49.2 percent smaller, so more payments fit in the same block.',
      note:'The recovery of y uses one modular exponentiation and works because p is congruent to 3 modulo 4; the toolkit does it in a single line, and the third example shows that the recovered point equals the original. Say explicitly that the two forms are two spellings of one point, not two keys, and then remind the class of the consequence they already met: the two spellings hash to different commitments and therefore to different addresses.',
      src:[BK + ', Compressed Public Keys'] },
    { id:'UncompressedPublicKey', t:'Uncompressed public key', sub:'65 bytes: 04, x and y',
      def:'The uncompressed encoding is the original one: the prefix byte 04 followed by the 32-byte x coordinate and the 32-byte y coordinate, 65 bytes written as 130 hexadecimal digits. It has not disappeared, because some software must still support it, in particular a wallet importing private keys from an older wallet, which has to scan for both kinds of key and for the commitments to both.',
      take:'Printed in two halves here: 04 with x on the first line, y on the second.',
      note:'Showing the key in two lines is deliberate; it makes visible that the first line after the prefix is identical to the compressed form’s x coordinate. Early addresses built from uncompressed keys still hold funds, so this is not merely historical. End with the warning that matters in practice: a user who exports a key from an old wallet without recording which form it was used in may later look for the balance in the wrong place.',
      src:[BK + ', Compressed Public Keys'] },
    { id:'WalletImportFormat', t:'Wallet import format', sub:'one key, two exports',
      def:'The wallet import format, WIF, is the text in which a private key moves between wallets. It is the base58check encoding of the version byte 0x80, the 32-byte key, and, for keys meant to produce compressed public keys, an extra byte 01 at the end. A raw 64-digit number carries no protection against typing errors; the WIF adds a recognisable first character and a checksum, so a wallet can refuse a mistyped key rather than import a different one.',
      take:'The decoded bytes show the whole structure: 80, the key, and the trailing 01.',
      note:'The two strings on the slide are the ones the book prints, recomputed here, and the third line takes one of them apart so that the class sees the version byte and the suffix with their own eyes. Say the obvious thing out loud, because it is forgotten every year: a WIF string is a private key. Anyone who sees it can spend the funds, so it does not go into a web page, a screenshot or a chat message.',
      src:[BK + ', Private Key Formats'] },
    { id:'CompressedPrivateKey', t:'Compressed private key', sub:'a misnomer: one byte longer',
      def:'The common term compressed private key is a misnomer. Private keys are not compressed and cannot be; what the term means is a key exported with a one-byte suffix 01 saying that only compressed public keys should be derived from it. That makes the exported record one byte longer, and in base58 the extra length moves the first character from 5 to K or L.',
      take:'One added byte, one added character, and a different first character: 5 becomes K.',
      note:'The book’s analogy is worth repeating: 100 is longer than 99 and also starts with a different digit, and that is all that happens here. The computation on the slide proves both halves, the one character of difference in the text and the one byte of difference in the decoded record. Warn that the formats are not interchangeable: a newer wallet exports only the K or L form, an older one only the form beginning with 5, and the suffix is the signal that tells the importer which public keys to derive.',
      src:[BK + ', Compressed Private Keys'] } ] },
  { id:'Checksummed', t:'Checksummed text', lead:'An address is typed, read aloud and copied by people, and a payment to a mistyped address is lost; a checksum is the cheapest defence against that.',
    note:'Two checksummed formats appear in this chapter, base58check and bech32. This group builds the first one and the vocabulary the second will reuse: checksum, version prefix, network selector.',
    items:[
    { id:'Checksum', t:'Checksum', sub:'four bytes that catch typing errors',
      def:'A checksum is a short value derived from data and attached to it, so that anyone holding both can recompute the check and see whether they still agree. In base58check it is the first four bytes of the SHA256 of the SHA256 of the data being encoded. Decoding software recomputes it, and a mismatch means the string has been altered and must be refused.',
      take:'Thirty-two bits of check: a randomly damaged string still passes about once in 4.3 thousand million times.',
      note:'Three things to bring out. First, the check is recomputed, not looked up, so it works offline. Second, its strength is exactly its length, and four bytes give one chance in 2 to the 32 of a damaged string slipping through. Third, and most important, a checksum detects accident and not attack: anyone replacing an address on purpose simply computes a valid checksum for the replacement. The last line of the example is the refusal in action, with the message the toolkit raises.',
      src:[BK + ', Base58check Encoding'] },
    { id:'Base58Check', t:'Base58check encoding', sub:'an alphabet without 0, O, l and I',
      def:'Base58check combines three ingredients: a version byte in front of the data, a four-byte checksum behind it, and the base58 alphabet, which drops the four characters most easily confused in common fonts. The design serves people rather than machines: fewer misreadings, a visible data type, and a string that software can refuse when it is damaged.',
      take:'Encoding version 0x00 with the commitment reproduces the book’s address exactly.',
      note:'The first line checks the alphabet against its own rule, that zero, capital O, lower-case l and capital I are absent. The second runs the whole encoder and lands on the book’s address. Then give the criticism, because the next group rests on it: the bech32 proposal lists base58check’s defects as a slow double-SHA checksum with no detection guarantees, a mixed case that is awkward to read aloud and to place in a QR code, and a decoding procedure that is complicated and slow.',
      src:[BK + ', Base58check Encoding', 'Wuille and Maxwell, 2017'] },
    { id:'VersionPrefix', t:'Version prefix', sub:'0x00 gives 1, 0x05 gives 3',
      def:'The version prefix is the first byte of the data that base58check encodes, and it identifies the type of that data. Because it is the most significant part of the number that is then written in base 58, its value decides the leading characters of the result. The book’s table gives 0x00 for a P2PKH address, 0x05 for P2SH, 0x6F and 0xC4 for their testnet counterparts, 0x80 for a private key and 0x0488B21E for an extended public key.',
      take:'The leading character is a consequence of the arithmetic, not an extra field bolted on.',
      note:'Both lines on the slide are computations, not recollections: the first encodes each version byte with an empty payload and prints the character that comes out, the second shows the WIF case where adding the compression suffix lengthens the record and moves the first character from 5 to K. Close with the limit of the mechanism: the prefix identifies a type, it does not authenticate anything. A string beginning with 1 whose checksum matches is a plausible address and nothing more.',
      src:[BK + ', Base58check Encoding'] },
    { id:'NetworkSelector', t:'Mainnet and testnet', sub:'bc and tb, 0x00 and 0x6F',
      def:'Bitcoin software works with more than one chain, and every chain keeps its own data directory. Addresses have to tell the chains apart: base58check does it with the version byte, 0x00 against 0x6F for a key-hash address, and bech32 does it with the human-readable part, bc against tb. In both formats the selector is covered by the checksum, so an address cannot be moved to another network by editing its first characters.',
      take:'Decoding a mainnet address against the testnet prefix fails, by construction.',
      note:'The second line is the demonstration: the same string that decodes correctly under bc returns nothing under tb, because the prefix is mixed into the checksum calculation. Students sometimes try exactly that substitution when a faucet refuses their address, so show them why it cannot work. Add the discipline point: test coins are for testing, and the fact that a testnet address validates says nothing whatever about money.',
      src:[BK + ', Base58check Encoding', 'Bitcoin Core, 2026', 'Wuille and Maxwell, 2017'] } ] } ] });

// ============================== BRANCH 3: ADDRESS ==============================
CH.push({
  id:'Address', t:'Address', sub:'Turning a key into something one person can hand to another',
  lead:'The public key itself is a poor thing to hand over: imagine Bob reading two 64-digit coordinates to Alice over the telephone. An address is a short string the receiver gives the payer so that the payer’s wallet can build an output only the receiver can spend. Every kind of address is the name of one output script template, so this branch starts with scripts and then takes the legacy and the segwit families in turn.',
  note:'Keep repeating what an address is not. It is not an account, it is not a key, it contains no private information, it can be recomputed from a public key or a script, and it says nothing about who owns the funds. Students who carry a bank-account picture into this branch will misread everything in it.',
  src:[BK + ', chapter 4, Bitcoin Addresses'],
  groups:[
  { id:'Scripts', t:'Locking and unlocking scripts', lead:'Bitcoin does not pay to public keys directly: it pays to an output script that acts like a public key, and authorises spending with an input script that acts like a signature.',
    note:'The reason for the indirection is the whole of the rest of the branch: because the lock is a program, the receiver can choose conditions other than one signature from one key.',
    items:[
    { id:'OutputScript', t:'Output script', sub:'the lock on an output',
      def:'An output script is the field of a transaction output that states the conditions under which its funds may be spent. The payer’s wallet builds it from the receiver’s address: it decodes the address, finds the kind and the data inside, and writes the matching template with that data in place. For a legacy key-hash output the script is 25 bytes: 76a914, the twenty-byte commitment, and 88ac.',
      take:'Three bytes of opcodes, twenty of commitment, two more of opcodes.',
      note:'Build the script on the board from its parts so the class can read the hexadecimal: 76 is OP_DUP, a9 is OP_HASH160, 14 is the push of twenty bytes, 88 is OP_EQUALVERIFY and ac is OP_CHECKSIG. The length computed on the slide is the sum of those pieces. Warn that an output script is data and not a promise of safety: a payer who writes a script outside the accepted templates can create an output that nobody can spend, or one that anybody can.',
      src:[BK + ', Bitcoin Addresses'] },
    { id:'InputScript', t:'Input script', sub:'the key that opens the lock',
      def:'An input script is the field of a transaction input that supplies what the output script being spent demands. Where the output script says what must be shown, the input script shows it. For a key-hash output it is a signature followed by the public key, and because the items are pushed in order, the public key ends up on top of the stack.',
      take:'The separation is what keeps the public key hidden until the moment of spending.',
      note:'Make the privacy consequence explicit, because it is the reason the legacy design exists at all: an output committing to a hash of a key does not reveal the key, and the key appears for the first time in the input script of the spend. From that moment the protection of the hash is gone, which is one of the arguments against reusing an address. Note also that the input script is the only part of a spend the spender controls entirely, and that it is public the instant it is broadcast.',
      src:[BK + ', Bitcoin Addresses'] },
    { id:'StackExecution', t:'Stack, opcodes and evaluation', sub:'push, operate, check the top',
      def:'A node validating a spend runs the input script and the output script as one program on a stack, a list to which items are added and from which they are removed at one end only. Data is pushed on top; an opcode consumes the topmost items and pushes its result. The script passes if a non-zero item remains on top at the end.',
      take:'The same run with the wrong commitment returns False: the lock does not open.',
      note:'Walk the pay to public key hash script through on the board: OP_DUP copies the key, OP_HASH160 replaces the copy by its commitment, the output script pushes the expected commitment, OP_EQUALVERIFY stops the script if the two differ, and OP_CHECKSIG checks the signature against the key. The slide shows the duplication and then runs the whole template twice, once with the matching commitment and once with the commitment of the uncompressed key. One detail to correct: the book’s prose prints OP_EQUAL in the output script, while its own combined script and Bitcoin Core both use OP_EQUALVERIFY, which is byte 0x88 rather than 0x87, and the difference is real, since OP_EQUAL leaves a truth value while OP_EQUALVERIFY aborts.',
      src:[BK + ', Bitcoin Addresses', 'Bitcoin Core, 2026'] } ] },
  { id:'Legacy', t:'Legacy addresses', lead:'The address kinds Bitcoin used before segregated witness: pay to public key hash and pay to script hash, both written in base58check, together with the two earlier schemes that explain why they exist.',
    note:'Legacy does not mean unsafe and does not mean obsolete in the way a paper wallet is obsolete. The book recommends newer kinds for new wallets but says plainly that there is no immediate threat to anyone creating new P2SH addresses.',
    items:[
    { id:'IpAddressPayment', t:'Payment to an IP address', sub:'the send screen of Bitcoin 0.1',
      def:'The earliest Bitcoin software let a spender type the receiver’s IP address, a 32-bit number identifying a host on the Internet. The spender’s node contacted the receiver’s node and obtained a fresh public key for the payment. It was the simplest possible answer to the problem of the long public key, and it was removed, because the receiver had to be online and reachable at that address.',
      take:'Four octets, 32 bits, about 4.3 thousand million possible hosts.',
      note:'List the ordinary reasons the scheme failed, since they are the reasons any such design fails: the computer is switched off at night, the laptop sleeps, a firewall is in the way, or the receiver is behind network address translation. Then draw the lesson, which is not that the scheme was foolish. Its good idea, a fresh public key for every payment, survived; only the means of delivery died, and modern wallets achieve the same effect from a single seed without the receiver being online at all.',
      src:[BK + ', Bitcoin Addresses', 'Postel, 1981'] },
    { id:'P2pk', t:'Pay to public key', sub:'<public key> OP_CHECKSIG',
      def:'In a pay to public key output the output script is the receiver’s public key followed by OP_CHECKSIG, and the input script is nothing but the signature. This is the payment of the original paper with a script wrapped round it. It was never widely used for payments, and it is the baseline against which every later kind is measured.',
      take:'With the old encoding the output alone is 67 bytes; the commitment that replaces it is 20.',
      note:'Two defects, both visible in the numbers on the slide. The output is as long as the key, 67 bytes with the push byte and the opcode, and the key is exposed to everyone from the moment the output is created rather than from the moment it is spent. The compressed key brings the script down to 35 bytes, which is still far above the twenty-byte commitment of the next concept. Both facts motivate the move to hashes, so do not rush past them.',
      src:[BK + ', Bitcoin Addresses'] },
    { id:'Commitment', t:'Hash commitment', sub:'publish the hash now, reveal the input later',
      def:'A commitment is a value published now in order to be bound to a hidden value revealed later. A hash function gives one for free: the same input always gives the same output, and finding a second input with that output is impractical, so the output is a promise that only that input produces it. In the legacy addresses the hidden value is the receiver’s public key and the commitment is its HASH160.',
      take:'The book’s own game: the digest of the answer, published before the answer.',
      note:'Play the game with the class. The book publishes the SHA256 digest of its answer to a question, invites the reader to guess, and then reveals the sentence whose digest is exactly the published value; the slide recomputes that digest, including the line break the shell’s echo adds. Then give the limit of commitments, which the chapter needs later: a commitment binds but does not necessarily hide, and if the set of possible hidden values is small, anyone can hash every candidate and compare.',
      src:[BK + ', Legacy Addresses for P2PKH'] },
    { id:'P2pkhAddress', t:'P2PKH address', sub:'version 0x00, the commitment, base58check',
      def:'A pay to public key hash address is the base58check encoding of the version byte 0x00 followed by the HASH160 of the receiver’s public key, so it begins with the digit 1. The output script is OP_DUP OP_HASH160, the commitment, OP_EQUALVERIFY, OP_CHECKSIG, and the spender’s input script is the signature followed by the key. Alice therefore sends twenty bytes of commitment instead of sixty-five bytes of key.',
      take:'Bitcoin Core 31.1 reports exactly this output script for this address.',
      note:'The two addresses on the slide are the compressed and the uncompressed forms of the same private key, and they are different addresses; students should by now be able to say why. The third line is the independent check: the script Bitcoin Core reports for the address is the one the toolkit built. Finish with the point that returns under address reuse: an address is derived from a public key and does not contain it, so it cannot be turned back into one, and the key becomes visible only when the output is spent.',
      src:[BK + ', Legacy Addresses for P2PKH', 'Bitcoin Core, 2026'] },
    { id:'RedeemScript', t:'Redeem script', sub:'a script revealed when spending',
      def:'A redeem script is a script that an output commits to by its hash instead of containing it. When the funds are spent, the input script must supply a script matching the commitment together with whatever that script needs. The upgrade that introduced the mechanism in 2012 states its purpose plainly: to move the responsibility for the conditions of redemption from the sender of the funds to the redeemer.',
      take:'The commitment uses the same HASH160 as for a public key, here over a 22-byte script.',
      note:'Use the slide’s redeem script, the witness output script of the nested segwit slide, so that the two concepts connect later. Make the privacy observation: until the output is spent nobody can tell what conditions it carries, which is an advantage for the receiver and a risk for everybody, since the payer cannot check that the receiver chose a script that can in fact be satisfied. That risk is the reason for the template warning on the P2SH slide.',
      src:[BK + ', Legacy Pay to Script Hash', 'Andresen, 2012'] },
    { id:'MultisigScript', t:'Multisignature script', sub:'m signatures out of n keys',
      def:'A multisignature script requires signatures made with more than one key before funds may be spent; the usual description is m of n. The book’s example needs two signatures, one from a desktop wallet and one from a hardware signing device. Splitting authority this way protects against the loss or the theft of any single key.',
      take:'Fifteen keys fit in a 520-byte script at 513 bytes; sixteen would need 547 and do not fit.',
      note:'The computation on the slide is where the usual limit of fifteen keys comes from, and deriving it is more useful than stating it. Then two warnings. Multisignature is a rule about keys and not about people: one person holding every key on one computer gains nothing, and keys spread over devices that fail together gain little. And it enlarges the transaction, because every signature and every key is shown when the output is spent, and the spender pays for those bytes.',
      src:[BK + ', Legacy Pay to Script Hash', 'Andresen, 2012'] },
    { id:'P2shAddress', t:'P2SH address', sub:'a commitment to a script, beginning with 3',
      def:'A pay to script hash address commits with HASH160 to a redeem script rather than to a key. The output script is the fixed template OP_HASH160, the commitment, OP_EQUAL, and the address is the base58check encoding of version byte 5, which makes it start with the digit 3. The payer’s wallet needs to recognise only that one template, so a wallet that has never heard of multisignature can still pay one.',
      take:'The book’s example address decodes to version byte 5, and Bitcoin Core reports it as a script.',
      note:'The three lines do three different jobs: the first builds a P2SH address from a redeem script with the toolkit, the second takes the book’s printed example apart to show the version byte, and the third asks Bitcoin Core what it thinks that address is. Close with the book’s warning, which costs money when it is ignored: the template must be followed exactly, and if the output script is not precisely OP_HASH160, twenty bytes, OP_EQUAL, the redeem script is never used and the coins may be unspendable or spendable by anyone.',
      src:[BK + ', Legacy Pay to Script Hash', 'Andresen, 2012', 'Bitcoin Core, 2026'] },
    { id:'PreimageAttack', t:'Preimage attack', sub:'finding an input for a given hash',
      def:'A preimage attack tries to find an input producing a given hash output, that is, to open a commitment whose hidden value the attacker does not know. In Bitcoin that means finding a public key or a script whose HASH160 equals the commitment in an existing output. For a secure 160-bit function each attempt succeeds with probability one in 2 to the 160.',
      take:'2 to the 160 written out is a 49-digit number.',
      note:'Print the number rather than the exponent, because the exponent means nothing to most people. Then put it beside the hash rate the book attributes to all miners in early 2023, about 2 to the 80 hashes an hour: even that whole network would need 2 to the 80 hours, more than 10 to the 20 years. Finish by saying which property this is, since the next two slides weaken it: resistance to a preimage attack is the strongest of the three and it is not the one in danger.',
      src:[BK + ', Legacy Pay to Script Hash'] },
    { id:'SecondPreimageAttack', t:'Second preimage attack', sub:'a different input, the same hash',
      def:'A second preimage attack tries to find, for a given input, a different input with the same hash output. For addresses created entirely by one party the book puts the chance at about one in 2 to the 160 again, the same as a preimage attack, because the attacker has gained no freedom: the first input is fixed and the search is still over the whole output space.',
      take:'One chance in about 6.8 times 10 to the minus 49 per attempt.',
      note:'The three attacks are confused every year, so set them out as a sequence of increasing freedom: in a preimage attack the attacker knows only the output, in a second preimage attack the attacker also knows one input, and in a collision attack the attacker may choose both. Say why the property matters: a commitment is supposed to bind its author to one value, and if a second input with the same hash could be found, an output committing to a script could be spent with a different script.',
      src:[BK + ', Legacy Pay to Script Hash'] },
    { id:'CollisionAttack', t:'Collision attack', sub:'two inputs chosen freely, one hash',
      def:'A collision attack looks for any two inputs with the same hash, with neither fixed in advance. The freedom to choose both reduces the work to about the square root of the output space, 2 to the 80 for HASH160, by the same counting argument as the birthday problem. The book applies it to a multisignature script built with a party who waits to see every other public key before submitting their own.',
      take:'The conclusion stands; the numbers behind it have moved since early 2023.',
      note:'The slide recomputes the book’s own figures and then repeats them against the network as it is. A third party’s estimate of the hash rate, read on 28 September 2026, is about 2.8 times the book’s figure for an hour, which turns its 32 thousand million years for 2 to the 128 operations into about 11 thousand million. Teach both the arithmetic and the habit: a textbook number about a moving system carries a date, and quoting it without the date is the error. This is also why P2WSH uses a 32-byte commitment instead of 20.',
      src:[BK + ', P2SH Collision Attacks', 'Mempool Space, 2026'] } ] },
  { id:'Segwit', t:'Segwit addresses', lead:'How can a payer be given a short, typable string that works for the new output kinds of a protocol upgrade, and for kinds not yet invented?',
    note:'Segregated witness was introduced in 2017; it stops transaction identifiers from being changed without the spender’s consent and gives blocks more room. Users who wanted its benefits had to accept payments to new output scripts, and that demanded a new way of telling payers what to pay.',
    items:[
    { id:'SegwitUpgrade', t:'Segregated witness', sub:'a new place for signatures',
      def:'Segregated witness defines a new structure, the witness, committed to blocks separately from the tree of transactions, and moves scripts and signatures into it. Because signature data is no longer part of the transaction hash, changes to how a transaction was signed no longer change how it is identified. The specification has the status Deployed and the book dates the upgrade to 2017.',
      take:'Hash the body alone and the body with its witness and the two identifiers differ: that is the whole idea.',
      note:'The demonstration on the slide is a model, not a real transaction: two byte strings standing for the body and the witness, hashed with and without the witness, to show that there are two identifiers and why. The frequent error is to think segwit hides or removes signatures. It does neither; they are transmitted and verified exactly as before, they are simply stored elsewhere and left out of the identifier.',
      src:[BK + ', Bech32m', 'Lombrozo et al., 2015'] },
    { id:'NestedSegwit', t:'Segwit inside P2SH', sub:'a bridge for payers who had not upgraded',
      def:'A P2SH address can wrap a witness program: the redeem script the address commits to is the segwit output script itself, the version byte 0 followed by a push of the twenty-byte key hash. Every wallet that could pay a P2SH address could therefore pay a segwit receiver, so receivers did not have to wait for payers to upgrade.',
      take:'Bitcoin Core 31.1 derives the same address from sh(wpkh(key)): it appears in the saved evidence.',
      note:'The third line is a genuine cross-check and should be presented as one: the address the toolkit computed is looked up in the saved output of the run of Bitcoin Core, and it is there. Then give the cost, which is why native addresses replaced the nested form: for the nested P2WPKH the specification measures an output script one byte larger and an input script 23 bytes larger than the native equivalents, and every spender pays for those bytes.',
      src:[BK + ', Bech32m', 'Lombrozo et al., 2015', 'Bitcoin Core, 2026'] },
    { id:'Bech32Address', t:'Bech32 address', sub:'prefix, separator, version, program, checksum',
      def:'A bech32 address is a checksummed base 32 string: a human-readable part, the separator 1, the witness version, the witness program and six checksum characters, all in one case. The name joins BCH, the error-detection code it uses, to the 32 of its alphabet. It answers the defects of base58check: one case, readable aloud, compact in a QR code, able to locate errors, and able to carry output versions that do not exist yet.',
      take:'The book’s P2WPKH address, 42 characters, decoding back to witness version 0.',
      note:'Build the address in front of the class from the witness version and the program: regroup the bytes from eight bits to five, map each group to one of the 32 characters of the alphabet qpzry9x8gf2tvdw0s3jn54khce6mua7l, then append six characters of checksum computed over the prefix and the data together. The third line decodes it again and recovers the version, which is the round trip every implementation must pass.',
      src:[BK + ', Bech32m', 'Wuille and Maxwell, 2017'] },
    { id:'WitnessVersion', t:'Witness version', sub:'q is 0 and p is 1',
      def:'The witness version is a number between 0 and 16 that says which rules govern a witness output, encoded as the single character after the separator. The letter q is the character at position 0, so version 0 addresses read bc1q, and p is at position 1, so taproot addresses read bc1p. The version is how the protocol grows: a new output kind takes a new number, and wallets that can pay any version can pay it without a new address format.',
      take:'Position 16 is the letter s, which is why the book’s highest-version example begins bc1s.',
      note:'The warning here is the one that loses coins. A witness version of 0 is written in an output script as the byte 0x00, but version 1 is written as OP_1, the byte 0x51, and not 0x01; the slide computes 0x51 and 0x60 from the rule 0x50 plus the version. A wallet that converts an address to an output script with the wrong byte creates an output that is likely unspendable or insecure, and the specification says so in those words.',
      src:[BK + ', Bech32m', 'Wuille, 2020'] },
    { id:'WitnessProgram', t:'Witness program', sub:'20 or 32 bytes for version 0',
      def:'The witness program is the data part of a segwit output, the bytes following the version in the output script and in the address. It is between 2 and 40 bytes long, and for version 0 it must be exactly 20 or 32, which lets a decoder tell a commitment to a key from a commitment to a script by its length alone. For version 1 the only length defined when the book was written is 32.',
      take:'Twenty bytes give a 42-character address, thirty-two bytes give 62.',
      note:'The last line is the point of the slide: changing a single character of a valid address makes the decoder return nothing, because the checksum no longer matches. Keep the vocabulary straight, since students merge the three terms: the program is not the address and not the script, it is only the data that a template wraps, and the same twenty bytes mean a key hash in one kind and nothing at all in another.',
      src:[BK + ', Bech32m'] },
    { id:'HumanReadablePart', t:'Human-readable part', sub:'bc for mainnet, tb for testnet',
      def:'The human-readable part is the prefix that opens a bech32 string and says what kind of data follows; for Bitcoin it is bc on the main network and tb on the test network, followed by the separator 1. A decoder splits at the last 1, because the data alphabet never contains that character. The prefix is mixed into the checksum, so it cannot be edited away.',
      take:'Expanding bc for the checksum gives five values: the high bits, a zero, then the low bits.',
      note:'The specification explains the choice of names, which is a nice detail: bc was chosen over btc because it is shorter, and tb has the same length as bc, which simplifies assumptions about lengths while staying visually distinct. The second line shows the expansion the checksum algorithm applies to the prefix, which is how the prefix gets into the computation at all. Do not let students confuse the prefix with the version: the prefix names the network, the character after the separator names the witness version.',
      src:[BK + ', Bech32m', 'Wuille and Maxwell, 2017'] },
    { id:'BchCode', t:'BCH code', sub:'six characters, thirty bits',
      def:'A BCH code is an error-correcting code, named for the initials of those who discovered the cyclic code behind it, and it is the mathematical heart of the bech32 checksum. Six characters of five bits each carry thirty bits of check. Unlike a truncated hash, which gives only a probabilistic guarantee, such a code can be designed so that a whole class of errors is caught with certainty.',
      take:'Thirty bits is just over a thousand million, which is where the one-in-a-billion figure comes from.',
      note:'The verification is one function: the expanded prefix and the data characters are fed through polymod, which folds each value into a running thirty-bit state, and the string is accepted if the final state equals a constant, 1 for bech32 and 0x2bc830a3 for bech32m. Then give the designers’ own warning about correction: correcting errors erodes detection, because correction turns invalid input into valid input, and if more than a few characters are wrong the valid input may not be the intended one. Implementations are asked to locate errors, not to repair them.',
      src:[BK + ', Bech32m', 'Wuille and Maxwell, 2017', 'Wuille, 2020'] },
    { id:'ErrorDetection', t:'Error detection, and location', sub:'the guarantee, tested',
      def:'For an address of the expected length bech32 is mathematically guaranteed to detect any error affecting four characters or fewer, and for longer errors it fails less than once in a thousand million times. Beyond detection it can tell the user where the errors are, which base58check cannot: there a transposition is reported as a mistake somewhere, and finding it can take several frustrating minutes.',
      take:'In the book’s typo example the two wrong characters sit at positions 25 and 40.',
      note:'The first line locates the errors in the book’s own figure, the second shows that the damaged address simply fails to decode, and the third reads the exhaustive test from the saved results: of every one-character and every two-character substitution of the 39-character data part of the book’s P2WPKH address, and of 200,000 random three- and four-character substitutions, not one kept a valid checksum. Say what that is and is not: a test, not a proof, since the guarantee is a property of the code. And repeat the condition the book spells out, that the guarantee holds only if the length entered equals the length of the original.',
      src:[BK + ', Bech32m', '08-tooling/ch04-evidence/verify_results_v1_0_0.json'],
      tbl:[['Test on the book’s bc1q9d3xa5… address','Undetected'],
           ['every one-character substitution (1,209 of them)','0'],
           ['every two-character substitution (712,101 of them)','0'],
           ['200,000 random three- or four-character substitutions','0']] },
    { id:'LengthExtension', t:'Length extension weakness', sub:'a q added before a final p',
      def:'The guarantees of bech32 hold only when the entered address has the length of the original, and one of its constants made that condition easy to break: whenever the final character is p, inserting or deleting any number of q characters just before it leaves the checksum valid. The book prints an intended address and five longer strings that a bech32 decoder cannot tell apart from it.',
      take:'All six strings pass the bech32 test; not one passes the bech32m test.',
      note:'The lengths on the slide show what was inserted: the intended string has 15 characters and the others 18, 20, 22, 23 and 25, so three, five, seven, eight and ten letters q were added. In segwit version 0 the flaw is harmless in practice, because only two program lengths are valid, and the book works out that one would have to insert the letter twenty times to reach another valid length. The lesson for implementers is the general one: a checksum has a design range, and a guarantee about changing up to four characters says nothing about changing the length.',
      src:[BK + ', Problems with Bech32 Addresses', 'Wuille, 2020'] },
    { id:'Bech32mAddress', t:'Bech32m address', sub:'one constant apart from bech32',
      def:'Bech32m is bech32 with a single different constant: in the final step the value 0x2bc830a3 is combined into the checksum in place of 1. It is required for segwit outputs of version 1 and later, while version 0 keeps bech32. All the characters of the two encodings of the same data are identical except the last six.',
      take:'The taproot address encodes under bech32m; the version 0 address encodes under bech32.',
      note:'Explain why one constant was enough: the developers analysed the problem exhaustively and found that changing it removes the length extension weakness, so that insertions or deletions of up to five characters are missed less than once in a thousand million times. Then state the rule the slide tests in both directions, because software that gets it wrong loses part of the error detection: a version 0 program must use bech32 and a version 1 program must use bech32m, and BIP350 shows that a string can never be valid in both.',
      src:[BK + ', Bech32m', 'Wuille, 2020'] },
    { id:'P2wpkh', t:'Pay to witness public key hash', sub:'OP_0 and a 20-byte key hash',
      def:'P2WPKH is the segwit counterpart of P2PKH. The output script is 22 bytes, the version byte 0, the push of 20 and the same HASH160 commitment to a public key that a legacy address uses; the address is bech32. The signature and the public key move into the witness, so the transaction identifier no longer depends on them.',
      take:'The same key that gave 1J7mdg5r… gives bc1qh0q7g2…, the address Bitcoin Core derives from wpkh(key).',
      note:'Pair this slide with the P2PKH slide: one private key, one commitment, two output kinds, two addresses. The witness of a spend must hold exactly two items, a signature and a public key whose HASH160 matches the program. Mention the restriction that catches people importing old keys: only compressed public keys are accepted in P2WPKH and P2WSH, so a key once used in its uncompressed form with a legacy address cannot be used with this kind.',
      src:[BK + ', Bech32m', 'Lombrozo et al., 2015', 'Bitcoin Core, 2026'] },
    { id:'P2wsh', t:'Pay to witness script hash', sub:'OP_0 and a 32-byte script hash',
      def:'P2WSH is the segwit counterpart of P2SH, and it changes the hashing. The witness program is the SHA256 digest of the script, 32 bytes, without the RIPEMD-160 step that P2SH applies afterwards, so the output script is 34 bytes and the address is 62 characters. The longer commitment is the answer to the collision attack discussed under the legacy addresses.',
      take:'32 bytes rather than 20: 256 bits of commitment rather than 160.',
      note:'Tie this back to the collision slide explicitly, because it is the clearest example in the chapter of a design changed by an attack: where the attacker can influence the input, a 160-bit commitment offers only 80 bits of resistance, and 256 bits restores the margin. The caution that applied to P2SH still applies here: the script is invisible until the output is spent, so the payer cannot check that it can ever be satisfied.',
      src:[BK + ', Bech32m'] },
    { id:'P2tr', t:'Pay to taproot', sub:'OP_1 and a 32-byte point',
      def:'A pay to taproot output is segwit version 1, and its witness program is a point on the secp256k1 curve, 32 bytes. It may be a plain public key, but in most cases it should be a key that also commits to further spending conditions. The program is 32 rather than 33 bytes because the Schnorr signature standard that goes with taproot encodes public keys as the x coordinate alone, taking the point with an even y.',
      take:'The book’s program, encoded with bech32m, gives the book’s taproot address exactly.',
      note:'Keep this slide short: taproot is a later chapter’s subject and here it is only an output kind that needs a bech32m address. The one point to make is the trade: a taproot address commits to a key and not to a hash of a key, so the key is visible in the output from the start, and the protection a hash gave until spending is exchanged for flexibility and smaller signatures. If anyone asks why Bitcoin Core’s tr() descriptor gives a different address for the same 32 bytes, the answer is that the descriptor tweaks the key, which the book covers later.',
      src:[BK + ', Bech32m', 'Wuille et al., 2020'] } ] } ] });

// ============================== BRANCH 4: PRACTICE ==============================
CH.push({
  id:'Practice', t:'Practice', sub:'What a user or a developer should do with all this today',
  lead:'A chapter of a book is a snapshot and software moves on. The third edition says of the private key formats that they are mainly of interest to anyone needing compatibility with early wallets, because modern wallets derive every key from one seed. This branch asks what current software actually does, and then how one knows that an implementation is right.',
  note:'Practice is not static, and the dates are part of the information: the book is of 2023 and the software used to check it here is Bitcoin Core 31.1, run as an offline node for this chapter. Teach the class to read every statement of the form "wallets do X" as a statement about some wallets at some date.',
  src:[BK + ', chapter 4, Advanced Keys and Addresses', 'Bitcoin Core, 2026'],
  groups:[
  { id:'Modern', t:'Practice now', lead:'Which address a wallet hands out, whether a single key can still be exported, how keys are protected, and which curiosities of the early years survive.',
    note:'The old way of keeping coins, one key per address backed up on paper or in a file, led both to lost keys and to leaked keys. Everything in this group is a consequence of leaving that behind.',
    items:[
    { id:'DefaultAddressType', t:'Default address type', sub:'bech32 by default, bech32m on request',
      def:'The default address type is what a wallet hands out when nobody asks for another. In Bitcoin Core the option addresstype takes the values legacy, p2sh-segwit, bech32 and bech32m, and its default is bech32, a P2WPKH address. A default shapes what most users do, and the default of the reference implementation tells the ecosystem which format is regarded as current.',
      take:'A fresh wallet gave five addresses, whose descriptors name the script kind of each.',
      note:'All three lines read the saved evidence of the run rather than repeating a claim: the four type names appear in the option help, the help gives bech32 as the default, and the descriptors of a throw-away wallet say which script each type produced. Note the mapping, since it ties the branch together: wpkh for the default and for bech32, pkh for legacy, sh for the nested type and tr for bech32m. Then say what a default is not. It is not a rule, other wallets differ, and the kind of address is always the receiver’s choice, never the payer’s.',
      src:['Bitcoin Core, 2026', BK + ', Bech32m'] },
    { id:'KeyExport', t:'Exporting a single key', sub:'no dumpprivkey any more',
      def:'Exporting a single key, usually as a WIF string, was an everyday operation of the early wallets, which held independent keys. Almost no modern wallet supports it. The reason is the deterministic wallet: an attacker who obtains one exported key together with some non-private data about the wallet can derive every other key in it, and keys cannot be imported into such a wallet at all.',
      take:'Bitcoin Core 31.1 answers "unknown command" to both dumpprivkey and importprivkey.',
      note:'This is where the owner’s earlier course notes and the current software part company, and saying so is part of the lesson. The notes drive the node with getnewaddress and then dumpprivkey; the first command still exists, the second was removed with the legacy wallet RPCs in release 30.0. A WIF key can still be used, but through a descriptor: the saved evidence shows pkh(WIF) and wpkh(WIF) resolving to the right addresses, which is the third line on the slide. Importing still goes through importdescriptors, whose help warns that it rescans the chain and needs a new backup.',
      src:['Bitcoin Core, 2026', BK + ', Private Key Formats', 'Altunel, 2021'] },
    { id:'PassphraseProtection', t:'Passphrase-protected key', sub:'BIP38 and the prefix 6P',
      def:'BIP38 encrypts a private key under a passphrase and encodes the result as a 58-character base58check string beginning 6P, which contains everything needed to reconstitute the key except the passphrase. It was written for paper wallets and physical coins, as a two-factor arrangement: the printed record can travel by post while the passphrase travels by telephone.',
      take:'The record is still well-formed base58check: 58 characters, prefix 6P, checksum valid.',
      note:'Mention the status, because it is an unusual one worth noticing: the BIPs repository marks BIP38 as Deployed while the summary of comments on it reads, unanimously, discourage for implementation, and the third edition of the book does not cover it at all. The owner’s 2021 notes do, over several slides, which is why it appears here. The protection is only as good as the passphrase; scrypt slows a guesser down and does not stop one, and a forgotten passphrase is a new way to lose the coins.',
      src:['Caldwell and Voisine, 2012', 'Altunel, 2021'] },
    { id:'DeterministicWallet', t:'Deterministic wallet and seed', sub:'one seed, all the keys',
      def:'A deterministic wallet derives every private key from a single random value, the seed, by a procedure that always gives the same results. The book demonstrates it with a hash function: hashing the seed together with 0, 1 and 2 yields three seemingly random values, and the same seed always yields the same three. One recorded seed and the name of the algorithm therefore back up every key in the wallet.',
      take:'The three derived values begin 50b18e0b, a965dbcd and 19580c97, exactly as in the book.',
      note:'This slide is the hinge between chapter 4 and chapter 5, so announce it as such: the next chapter is about where that seed comes from, how it is written down and how a wallet is rebuilt from it. The earlier arrangement needed a new backup every time a key was generated or imported; this one needs one backup for typical use. The seed is also a single point of failure in both directions, since whoever obtains it can generate every key, and whoever loses it loses everything.',
      src:[BK + ', Private Key Formats'] },
    { id:'AddressReuse', t:'Address reuse and privacy', sub:'one address, many payments',
      def:'Address reuse means receiving more than one payment at the same address. Because the chain is public, every payment to an address can be seen beside every other, so reuse links them for any observer. The link is created by the observer and not by the protocol, and it affects people other than the receiver: the payers appear in it too.',
      take:'Three payments to one address are one link; three payments to three fresh addresses are none.',
      note:'Use the book’s two small stories rather than an abstract argument: Alice may wish to donate without being identified, and Bob may not want his other customers to learn that he gives the charity a discount. Wallets avoid the problem by handing out a fresh address for every payment, which is cheap precisely because all the keys come from one seed. Be careful with the claim, as the book is: avoiding reuse reduces linking, it does not grant anonymity, and sometimes a link is wanted, as for a charity that reports its income.',
      src:[BK + ', Vanity Addresses'] },
    { id:'VanityAddress', t:'Vanity address', sub:'each character multiplies the work by 58',
      def:'A vanity address is a valid address containing a readable message, found by generating keys at random until one matches the wanted pattern. Each further character makes the pattern 58 times rarer, so the frequencies run one in 58, one in 3,364, one in 195,112 and one in 11.3 million for one to four characters. The book reports that such addresses were popular early and had almost disappeared by 2023.',
      take:'At 100,000 keys a second, an eight-character pattern averages about 20 years.',
      note:'The arithmetic on the slide is the lesson: average time is half the frequency divided by the rate, and the exponent does the rest. The chapter checked the book’s own table against that rule and found two things worth telling the class, as an exercise in reading numbers critically. The book’s times agree with the rule up to seven characters and are about a third shorter from eight onwards, and its frequency for eleven characters, 23 quintillion, should be the 25 quintillion that 58 to the eleventh gives.',
      src:[BK + ', Vanity Addresses'] },
    { id:'PaperWallet', t:'Paper wallet', sub:'a private key printed on paper',
      def:'A paper wallet is a private key printed on paper, often with its address beside it, though that is unnecessary since the address can be derived. The third edition calls the technology obsolete and dangerous for most users, and recommends instead a recovery code, possibly with a hardware signing device holding the keys and signing the transactions.',
      take:'What has to be printed and kept safe is 64 hexadecimal digits, the 32 bytes of one key.',
      note:'Separate two things students merge. The recommendation is against generating and keeping one static key produced by a program whose trustworthiness the owner cannot check; it is not against writing on paper, since the recovery code of a modern wallet is routinely written on paper and the book proposes exactly that. The difference is that a recovery code regenerates a whole wallet from a device one can choose, and the security of a paper wallet depends first on the randomness of the program that made it.',
      src:[BK + ', Paper Wallets'] },
    { id:'HardwareSigningDevice', t:'Hardware signing device', sub:'keys that never leave the device',
      def:'A hardware signing device holds private keys and uses them only to generate signatures. A less secure program prepares the transaction and broadcasts it, and the device derives the child keys, signs and returns the signed transaction. Without general-purpose software to compromise, and with limited interfaces, such a device can give strong security to non-expert users.',
      take:'Three steps, and the private key appears in none of them outside the device.',
      note:'Give the division of labour precisely, because the name hardware wallet misleads: the frontend builds and displays the transaction, the device checks it, signs it inside and sends back only the signature. Then name the limits. It protects keys from software on the computer; it does not protect against loss, so the recovery code must still be kept, and it does not protect against the owner approving a transaction that pays the wrong address.',
      src:[BK + ', chapter 5, as cited in chapter 4'] } ] },
  { id:'Assurance', t:'Assurance', lead:'In a payment system an implementation error is not a minor bug: a decoder that accepts a string it should reject sends money where it cannot be recovered.',
    note:'The book asks for this directly: when implementing bech32m, use the test vectors of BIP350, and make sure the code passes the vectors for future witness versions, so that the software stays usable for years.',
    items:[
    { id:'TestVectors', t:'BIP350 test vectors', sub:'published inputs with their right answers',
      def:'A test vector is an input together with the output a correct implementation must give. BIP350 publishes three groups: valid bech32m strings, invalid bech32m strings each with its reason, and valid and invalid segwit addresses of versions 0 to 16, the valid ones with the output script they translate to. The invalid list collects the cases implementers forget.',
      take:'Seven valid bech32m strings, eight valid segwit addresses and fifteen invalid ones, all passed.',
      note:'Name some of the invalid cases, since they are the interesting part: a wrong human-readable part, a checksum of the wrong kind for the version, a version out of range, a program too short or too long, mixed case, and padding errors. Then state the limit honestly. Passing the vectors is necessary and not sufficient; they sample the space of inputs, so an implementation can pass and still be wrong for a case nobody wrote a vector for. That is why the next slide exists.',
      src:['Wuille, 2020', BK + ', Bech32m'] },
    { id:'IndependentCheck', t:'Cross-checking', sub:'three implementations, one answer',
      def:'Cross-checking compares independent implementations on the same inputs. If a toolkit written by one person and programs written by others, without shared code, agree over many inputs, the chance that both carry the same error is far smaller than the chance that one carries an error. This chapter compared its own toolkit, the reference library the book itself runs, and Bitcoin Core 31.1.',
      take:'All three agree on the book’s key, its two addresses, its two WIF strings and every printed address.',
      note:'This is the chapter’s method in one slide, and it is the habit worth teaching: trust in this field is built by checking that independent implementations agree, not by believing one of them. Say what agreement does not prove. It shows the results are the same, not that they are right, since two programs can share a source of error such as the same misreading of a specification, and the comparison only covers the inputs that were tried.',
      src:['08-tooling/ch04-evidence/verify_results_v1_0_0.json', 'Bitcoin Core, 2026', 'Wuille, 2020'],
      tbl:[['Independent reference','What it checked','Result'],
           ['the book’s own bech32 library','the four printed addresses and the BIP350 vectors','agrees'],
           ['Bitcoin Core 31.1','key to address, WIF to address, every printed address','agrees'],
           ['this chapter’s toolkit','key, addresses, WIF, checksums, vectors','agrees']] } ] } ] });

// ============================== BRANCH 5: SEMANTICS ==============================
CH.push({
  id:'Semantics', t:'Semantics', sub:'Keys as identifiers, and the course theme',
  lead:'A key pair is more than a means of paying: it is an identifier whose holder can prove control without asking anyone. Seen that way, Bitcoin’s keys raise the question the course keeps returning to, how a name for something can be created, recognised and proved without a central registry.',
  note:'Guard against over-claiming in this branch. A resemblance is not an identity: Bitcoin addresses and decentralized identifiers share a design idea, they are different things with different specifications, and no part of Bitcoin becomes a decentralized identifier method merely by being a key pair.',
  src:[BK + ', chapter 4', 'World Wide Web Consortium, 2022'],
  groups:[
  { id:'Identifiers', t:'Identifiers', lead:'An identifier is a name that refers to a thing, so that statements about the thing can be made, stored and found; a public key can serve as such a name.',
    note:'Three concepts forming a ladder: what a key makes possible, what a web-scale name looks like, and the standard that joins the two.',
    items:[
    { id:'KeyControlProof', t:'Proof of control by a key', sub:'signing a challenge',
      def:'Proof of control is showing that one holds a private key without revealing it, by producing a signature others can verify with the public key. Nothing in the procedure requires a third party. To avoid replay the verifier chooses the challenge, a message the prover could not have signed in advance, and then checks the signature against the key being claimed.',
      take:'The same signature verifies under the right public key and fails under any other.',
      note:'The two verifications on the slide are the whole argument: one key accepts, the neighbouring key rejects. This is exactly what a node does when it accepts a spend, and it is worth saying so, because students treat consensus and identity as separate topics. Then draw the boundary: proof of control is not proof of identity. It shows that the prover holds the key, not who the prover is, and binding a key to a person or an organisation needs something else entirely.',
      src:[BK + ', Public Key Cryptography and Cryptocurrency'] },
    { id:'Uri', t:'Uniform resource identifier', sub:'did:example:123456789abcdefghi',
      def:'A URI is a compact sequence of characters identifying an abstract or physical resource. RFC 3986 defines its generic syntax and a process for resolving references, and the grammar lets a program split a URI into its common parts without knowing the rules of each particular kind. A web address is a URI, and so is the bitcoin payment request of chapter 2.',
      take:'Three parts: the scheme, the method, and the identifier the method looks up.',
      note:'Splitting the example at the colons makes the structure visible, and each part has a job: the scheme says which specification governs the rest, the method says how to find the document belonging to it, and the last part is what the method uses to look it up. Add the caution that matters for the semantic work of the course: a URI names a resource, it does not assert that the resource exists or that anybody controls it, and two different strings may name the same thing.',
      src:['Berners-Lee et al., 2005'] },
    { id:'DecentralizedIdentifier', t:'Decentralized identifier', sub:'a URI, a subject and a document',
      def:'A decentralized identifier is a type of identifier defined by a W3C recommendation of 19 July 2022 that enables verifiable, decentralized digital identity. A DID refers to any subject as determined by its controller, and it is a URI that associates that subject with a DID document, which can carry cryptographic material such as verification methods. The design decouples identifiers from registries, identity providers and certificate authorities.',
      take:'Its controller can prove control without requiring permission from any other party.',
      note:'The two lines read those sentences out of the saved copy of the recommendation rather than quoting from memory, which is the method the whole deck follows. The connection to this chapter is the property on the slide: proving control without permission is what a Bitcoin key already does. The difference is scope, and a DID is meaningful only with a DID method saying how documents are created, resolved, updated and deactivated, which may or may not use a blockchain. A good project for this term is to describe a Bitcoin address as a DID document and list what a verifier would have to check.',
      src:['World Wide Web Consortium, 2022'] } ] } ] });

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
  if (c.ecsrc) {
    const e = light(); nContent++;
    title(e, 'The thirteen lines that do it', 'ec_add and ec_mul, exactly as the examples run them');
    const ecl = EX._snippets.ec.split('\n');
    e.addShape(pres.shapes.ROUNDED_RECTANGLE, {x:0.5, y:1.10, w:9, h:3.05, fill:{color:C.code}, line:{color:C.code}, rectRadius:0.1});
    e.addText(ecl.map((t, i) => ({text:t, options:{color:C.codeTxt, breakLine:i < ecl.length - 1}})),
      {x:0.68, y:1.2, w:8.64, h:2.85, fontFace:M, fontSize:9.5, valign:'top', margin:0, isTextBox:true});
    e.addText('ec_add is the chord-and-tangent rule; ec_mul adds a point to itself by doubling, reading the bits of k. G is the fixed generator point of secp256k1, and P the prime of its field. This is the source the deck check compares against the slide, so the two can never drift apart.',
      {x:0.5, y:4.28, w:9, h:0.85, fontFace:B, fontSize:12.5, color:C.ink, margin:0, valign:'top', isTextBox:true});
    sourceLine(e, ['08-tooling/sen0401_ch04_keys_v1_1_0.py', c.src[0]]);
    e.addNotes('Read the code with the class rather than about it. The first three lines of ec_add are the special cases the geometry needs: the point at infinity on either side, and a point added to its own mirror. The fourth line is the slope, the tangent formula when the points are equal and the chord formula otherwise, with division done as multiplication by a modular inverse. ec_mul is double-and-add in four lines. Say again that this is a teaching implementation: it is not constant-time, so the time it takes leaks information about the key, and real software uses libsecp256k1.');
  }
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
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x:0.6+i*1.05, y:1.0, w:0.8, h:0.8, fill:{color:i===2?C.orange:C.slate}, line:{color:C.orange, width:1.5}, rectRadius:0.1});
  if (i < 2) s.addShape(pres.shapes.LINE, {x:1.4+i*1.05, y:1.4, w:0.25, h:0, line:{color:C.orange, width:1.5}});
});
s.addText('₿', {x:2.7, y:1.0, w:0.8, h:0.8, fontFace:B, fontSize:30, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
s.addText('Chapter 4: Keys and Addresses', {x:0.6, y:2.1, w:8.8, h:0.8, fontFace:H, fontSize:38, bold:true, color:C.white, margin:0, isTextBox:true});
s.addText('From a random number to a string a payer can type — every value recomputed from the standards and checked three ways',
  {x:0.6, y:2.9, w:8.8, h:0.7, fontFace:B, fontSize:16, italic:true, color:C.orange, margin:0, valign:'top', isTextBox:true});
s.addText(COURSE, {x:0.6, y:4.55, w:8.8, h:0.45, fontFace:B, fontSize:12, color:'C9D1DA', margin:0, isTextBox:true});
s.addText('Mastering Bitcoin, 3rd edition, chapter 4 (' + BK + '), O’Reilly, free under CC BY-SA 4.0',
  {x:0.6, y:5.0, w:8.8, h:0.35, fontFace:B, fontSize:10.5, italic:true, color:'9AA7B4', margin:0, isTextBox:true});
s.addNotes('Open by saying what the session will do differently from a reading of the chapter: every number, hash, address and error message on these slides was produced by running the statement printed beside it under Python ' + PY + ', and three independent references were asked the same questions. The deck follows the chapter 4 concept taxonomy of this course in its own order, so the slides and the interactive page agree. Say that the toolkit used throughout is for reading and teaching and must never touch real funds.');

// ---------------------------------- 2. what the chapter covers ----------------------------------
s = light(); title(s, 'What this chapter covers', 'and how this deck is built');
card(s, 0.5, 1.08, 4.4, 1.95, 'The chapter',
  'From the private key, a random number, to the public key by elliptic curve multiplication, and on to the ways a public key becomes a string a payer can type: pay to public key, the P2PKH commitment, P2SH, and the segwit addresses.', C.slate, 12);
card(s, 5.1, 1.08, 4.4, 1.95, 'This deck',
  'The chapter’s own taxonomy in its own order, one slide per concept, each with its worked example and the answer that example really produced. The check refuses the deck if a printed answer stops matching.', C.orange, 12);
table(s, [['What is on the slides','Count'],
          ['concepts of the chapter 4 taxonomy, each with its own slide','69'],
          ['concepts whose slide carries an executed worked example','69'],
          ['statements executed for this deck, with their real answers', String(NSTMT)],
          ['independent references the chapter was checked against','3']],
      0.5, 3.2, 9, [6.6, 2.4], 12, 0.37);
sourceLine(s, ['08-tooling/sen0401_ch04_corpus_v1_1_0.py', '08-tooling/ch04-deck/examples_out_v2_0_0.json']);
s.addNotes('Tell the class how to use the deck beside the interactive chapter page: the slide identifiers are the concept identifiers of the page, so a concept met here can be opened there, edited and re-run. The three independent references are the reference bech32 library the book itself runs, Bitcoin Core 31.1 run offline for this chapter, and the chapter’s own toolkit. Mention that the chapter corpus carries far more than fits in one session, and that the page is where the rest lives.');

// ---------------------------------- 3. learning outcomes ----------------------------------
s = light(); title(s, 'Which learning outcomes this serves', 'SEN0401 outcome set, draft of 2026-10-04');
card(s, 0.5, 1.10, 9, 1.55, 'LO-4, the outcome of this chapter (Bloom level: Apply)',
  'Derive private keys, public keys and addresses from the standards that define them — elliptic-curve arithmetic over a finite field, SHA-256 and RIPEMD-160, Base58Check, Bech32 and Bech32m — and check each result against a reference implementation or a published test vector.', C.orange, 13.5);
card(s, 0.5, 2.78, 4.4, 1.72, 'What it rests on',
  'LO-1, what Bitcoin is and the parts it is built from, and LO-3, running Bitcoin Core as a full node and querying it. This session uses release 31.1 as an independent authority on every address.', C.slate, 12.5);
card(s, 5.1, 2.78, 4.4, 1.72, 'What it prepares',
  'LO-5, comparing wallet and recovery designs. The last slides of the deterministic-wallet concept are the hinge: chapter 5 asks where the seed comes from and how a wallet is rebuilt from it.', C.slate, 12.5);
s.addText('The outcome set is a draft of 2026-10-04 and carries no approval: the university catalogue page for this course still lists the outcomes of an earlier special topic, software architecture and design patterns, and none of those is carried here.',
  {x:0.5, y:4.58, w:9, h:0.62, fontFace:B, fontSize:10.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
sourceLine(s, ['01-outcomes/sen0401_outcomes_v1_0_0.ttl, items LO-1, LO-3, LO-4 and LO-5']);
s.addNotes('Read LO-4 aloud at the start of the session and again at the end against what was actually done; the deck is built to satisfy it literally, since every derivation on the slides is carried out and then checked against a reference implementation or a published vector. Be honest about the status of the outcome set: it was drafted from this repository’s own evidence and the owner has not yet approved it, so it guides the session but no assessment may be aligned to it yet.');

// ---------------------------------- 4. chapter map ----------------------------------
s = light(); title(s, 'The chapter in one picture', 'five branches, thirteen groups, sixty-nine concepts');
{
  const bw = 1.74;
  CH.forEach((b, i) => {
    const x = 0.5 + i * (bw + 0.08);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y:1.15, w:bw, h:0.55, fill:{color:C.orange}, line:{color:C.orange}, rectRadius:0.08});
    s.addText(b.t, {x:x+0.04, y:1.15, w:bw-0.08, h:0.55, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
    s.addShape(pres.shapes.LINE, {x:x+bw/2, y:1.70, w:0, h:0.2, line:{color:C.mute, width:1}});
    b.groups.forEach((g, j) => {
      const y = 1.90 + j * 0.60;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {x, y, w:bw, h:0.52, fill:{color:C.pale}, line:{color:C.line, width:1}, rectRadius:0.06});
      s.addText(g.t + '\n' + g.items.length + ' concepts', {x:x+0.04, y, w:bw-0.08, h:0.52, fontFace:B, fontSize:9.5, color:C.ink, align:'center', valign:'middle', margin:0, isTextBox:true});
      if (j > 0) s.addShape(pres.shapes.LINE, {x:x+bw/2, y:y-0.08, w:0, h:0.08, line:{color:C.line, width:1}});
    });
  });
}
s.addText('Each branch opens with its own slide; each group opens with the concepts it holds; each concept has a slide of its own with the code that produced its numbers.',
  {x:0.5, y:4.92, w:9, h:0.45, fontFace:B, fontSize:12, italic:true, color:C.mute, margin:0, isTextBox:true});
sourceLine(s, ['08-tooling/sen0401_ch04_corpus_v1_1_0.py, the chapter 4 taxonomy']);
s.addNotes('Use this picture twice: now, so the class knows where the session is going, and again before the questions at the end. The order is the chapter’s own argument: you cannot write an address before you have a key, you cannot read an address before you know what a representation is, and you cannot judge the practice before you know the formats. The last branch, keys as identifiers, is the course theme and is the part the chapter itself does not contain.');

// ---------------------------------- the body ----------------------------------
CH.forEach(b => { branchSlide(b); b.groups.forEach(g => { groupSlide(g); g.items.forEach(conceptSlide); }); });

// ---------------------------------- findings ----------------------------------
s = light(); nContent++;
title(s, 'What this chapter found', 'places where the book and its own sources disagree');
table(s, [['Statement in the 3rd edition','What the source or the run says'],
          ['secp256k1 was established by NIST','SEC 2 defines it; its Table 2 marks it – in the NIST column'],
          ['n is about 1.1578 × 10⁷⁷','the constant of the standard gives 1.1579 to five figures'],
          ['the P2PKH output script uses OP_EQUAL','the combined script and Bitcoin Core use OP_EQUALVERIFY, 0x88'],
          ['58¹¹ is about 23 quintillion','58¹¹ is 24,986,644,000,165,537,792, about 25 quintillion'],
          ['2¹²⁸ hashes would take about 32 billion years','about 11 billion years at a 2026 estimate of the hash rate'],
          ['dumpprivkey exports a single key','removed in Bitcoin Core 30.0; 31.1 answers unknown command']],
      0.5, 1.15, 9, [3.9, 5.1], 12, 0.49);
s.addText('None of these changes the chapter’s argument. They change what may be repeated without checking — which is the habit the chapter is really teaching.',
  {x:0.5, y:4.65, w:9, h:0.5, fontFace:B, fontSize:12.5, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
sourceLine(s, ['Certicom Research, 2010', 'Bitcoin Core, 2026', 'Mempool Space, 2026', BK]);
s.addNotes('Present these as findings and not as complaints, and say how each was established: the curve attribution by reading SEC 2’s own alignment table, the opcode by reading the source of Bitcoin Core, the two numeric slips by computing them, the hash-rate figure from a third party’s estimate read on 28 September 2026, and the removed command by running release 31.1. The one students should remember is the last: a statement of the form "the software does X" needs a date and a version beside it, or it is not a fact but a memory.');

// ---------------------------------- recap ----------------------------------
s = light(); nContent++;
title(s, 'Recap', 'the chapter in six sentences');
[['A key is a number','A private key is a random number below the order of secp256k1; the public key is that number times the fixed generator point, and the multiplication cannot be run backwards.'],
 ['A hash makes a short, binding name','HASH160 turns a 65-byte key into a 20-byte commitment, and because it commits to bytes, the two encodings of one key give two different addresses.'],
 ['An address is a script template plus data','Every address kind names one output script: a key hash, a script hash, or a witness version with a witness program.'],
 ['A checksum buys forgiveness for people','Base58check catches damage with four bytes of double SHA256; bech32 guarantees detection of up to four wrong characters and can say where they are.'],
 ['One constant fixed a real flaw','Bech32m differs from bech32 only in the constant folded into the checksum, and that removes the length extension weakness.'],
 ['Check, do not believe','The chapter’s method is three independent implementations and a published test suite, and it found six statements worth correcting.']
].forEach(([h, t], i) => {
  const y = 1.12 + i * 0.68;
  s.addShape(pres.shapes.OVAL, {x:0.5, y:y+0.08, w:0.42, h:0.42, fill:{color:C.orange}, line:{color:C.orange}});
  s.addText(String(i + 1), {x:0.5, y:y+0.08, w:0.42, h:0.42, fontFace:H, fontSize:14, bold:true, color:C.white, align:'center', valign:'middle', margin:0, isTextBox:true});
  s.addText([{text:h + ' — ', options:{bold:true, color:C.dark}}, {text:t, options:{color:C.ink}}],
    {x:1.08, y:y, w:8.4, h:0.6, fontFace:B, fontSize:12, valign:'middle', margin:0, isTextBox:true});
});
s.addNotes('Do not read the recap out; ask the class to supply the second half of each sentence from the first. The sixth is the one to dwell on, because it is the only one that transfers to other subjects: everything on these slides was checked against something that was not the book, and six statements did not survive the check.');

// ---------------------------------- questions ----------------------------------
const QS = [
 ['A student says the one-way property of elliptic curve multiplication has been proved. What is wrong?',
  ['The property has been proved, but it holds only for private keys smaller than the order of the curve',
   'The book claims only that the reverse is infeasible with today’s computers and algorithms',
   'Nothing: the proof appears in the standard that defines the curve',
   'The property was proved for prime exponentiation but not for elliptic curves'], 1,
  'The book speaks of functions that are infeasible to calculate in the opposite direction using the computers and algorithms available today, which is a statement about the present state of knowledge.'],
 ['Why does one private key lead to two different legacy addresses?',
  ['The two addresses carry one and the same commitment but two different checksums',
   'The key is hashed once for mainnet and once for testnet',
   'HASH160 commits to bytes, and the key has two different byte encodings',
   'The address includes a counter that increases with every use'], 2,
  'The compressed and the uncompressed public key are two encodings of one point, and hashing them gives two different 20-byte values.'],
 ['Which weaknesses of base58check did the designers of bech32 list?',
  ['A slow checksum without guarantees, mixed case, and complicated decoding',
   'A short alphabet, a missing version byte, and no support for scripts of any kind',
   'A checksum that cannot be computed without a node',
   'An alphabet that varies between implementations'], 0,
  'The bech32 proposal names the double SHA256 checksum without error-detection guarantees, the mixed case and the complicated decoding among its reasons.'],
 ['When does the strength of HASH160 drop from 2 to the 160 to 2 to the 80?',
  ['When the attacker can influence the input, for instance a shared multisignature script',
   'When the same address is used for more than one payment',
   'When the public key behind the address is compressed rather than uncompressed',
   'When the output is spent and the key becomes public'], 0,
  'An attacker who submits their key only after learning the others’ keys can search for two inputs at once, which is a collision attack.'],
 ['Which mistake does the book warn about when turning an address into an output script?',
  ['Writing the version after the program instead of before it',
   'Writing version 1 as the byte 0x01 instead of the opcode byte 0x51',
   'Writing the version in decimal instead of hexadecimal',
   'Leaving out the length byte before the program'], 1,
  'A wrong byte here produces an output that is likely to be unspendable or insecure, as the specification also warns.'],
 ['Under which condition does the guarantee about four wrong characters hold?',
  ['The errors are all in the data part and not in the checksum',
   'The address is written in uppercase',
   'The wallet is connected to a node',
   'The string entered has the same length as the original address'], 3,
  'If characters are added or removed during transcription the guarantee does not apply, which is the root of the length extension weakness.'],
 ['Why does P2WSH use SHA256 alone where P2SH used SHA256 and then RIPEMD-160?',
  ['SHA256 is faster, which matters for a node that verifies many scripts',
   'RIPEMD-160 is not available in every implementation',
   'A 32-byte commitment gives at least 128 bits of collision resistance',
   'The witness program has no room for a 20-byte value'], 2,
  'The book says the RIPEMD-160 step may not be secure in some cases and that the result is a commitment of 32 instead of 20 bytes.'],
 ['Why have vanity addresses almost disappeared, according to the book?',
  ['They turned out to be considerably easier to attack than other addresses',
   'The base58 alphabet no longer contains readable letters',
   'Bitcoin Core refuses to validate them',
   'Deterministic wallets cannot take them in, and they invite address reuse'], 3,
  'The book names those two likely causes and notes that most wallets do not allow importing a key from a vanity generator.'],
 ['The book warns against paper wallets but recommends writing a recovery code on paper. Where is the difference?',
  ['A recovery code is shorter, so it is harder to copy down wrongly',
   'A recovery code is encrypted and a paper wallet is not',
   'A recovery code regenerates a wallet from a trusted device; a paper wallet is one key from an unchecked program',
   'A recovery code can be used only on the device that made it'], 2,
  'The warning is about generation and about a single static key, not about paper itself.'],
 ['What does agreement between two implementations not show?',
  ['That the two implementations were written by different people in different places',
   'That the inputs were the same for both',
   'That the answer is right, since both may share a misreading of the specification',
   'That each of them is faster than the other'], 2,
  'Agreement covers only the inputs that were tried, and a shared source of error can make two programs agree on a mistake.']];

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
  sourceLine(s2, ['08-tooling/ch04-page/question_bank_v1_0_0.json, the chapter 4 bank']);
  s2.addNotes(notes.join('\n\n') + '\n\nGive the class a minute on each, take a show of hands on every option before revealing, and ask for the reason rather than the letter.');
}

// ---------------------------------- sources ----------------------------------
s = light(); nContent++;
title(s, 'Sources', 'every claim beyond the book is in the chapter’s research record');
const SRC = [
 'Antonopoulos, A. M., and Harding, D. A. (2023). Mastering Bitcoin, 3rd edition, chapter 4. O’Reilly. CC BY-SA 4.0.',
 'Certicom Research (2010). SEC 2: Recommended Elliptic Curve Domain Parameters, version 2.0, sections 2.4.1 and 2.4.2 and Table 2.',
 'Andresen, G. (2012). BIP16, Pay to Script Hash. Lombrozo, E., et al. (2015). BIP141, Segregated Witness.',
 'Wuille, P., and Maxwell, G. (2017). BIP173, Base32 address format. Wuille, P. (2020). BIP350, Bech32m, and its test vectors.',
 'Wuille, P., et al. (2020). BIP340, Schnorr signatures for secp256k1. Caldwell, M., and Voisine, A. (2012). BIP38.',
 'Bitcoin Core (2026). Release 31.1, run as an offline node for this chapter; release notes of 30.0. Evidence in 08-tooling/ch04-evidence.',
 'National Institute of Standards and Technology (2015). FIPS 180-4, Secure Hash Standard.',
 'Postel, J. (1981). RFC 791, Internet Protocol. Berners-Lee, T., et al. (2005). RFC 3986, Uniform Resource Identifier.',
 'World Wide Web Consortium (2022). Decentralized Identifiers (DIDs) v1.0, W3C Recommendation of 19 July 2022.',
 'Python Software Foundation (2026). The secrets module, Python 3.14.4 documentation.',
 'Mempool Space (2026). Network hash rate, read on 2026-09-28; a third party’s estimate.',
 'Altunel, Y. (2021). Course notes for this chapter, written on the 2nd edition and checked against the 3rd before use.'];
s.addText(SRC.map((t, i) => ({text:t, options:{bullet:true, breakLine:i < SRC.length - 1}})),
  {x:0.5, y:1.12, w:9, h:3.75, fontFace:B, fontSize:11, color:C.ink, paraSpaceAfter:3, margin:0, valign:'top', isTextBox:true});
s.addText('These slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0 and are shared under the same licence. The full verified list, with the author-year string of every citation, is 03-materials/ch04/rdodi/sen0401_ch04_research_v1_1_0.ttl.',
  {x:0.5, y:4.95, w:9, h:0.5, fontFace:B, fontSize:10, italic:true, color:C.mute, margin:0, valign:'top', isTextBox:true});
s.addNotes('Point the class at the research record rather than at this list: every publication there carries the role it played, the place the saved copy lives and the claim that re-reads it. Tell students that the saved copies are in the repository, so a claim made in an assignment can be checked against the same bytes the chapter used.');

// ---------------------------------- closing ----------------------------------
s = dark();
s.addText('Next: Chapter 5 — Wallet Recovery', {x:0.7, y:1.6, w:8.6, h:0.9, fontFace:H, fontSize:32, bold:true, color:C.white, margin:0, isTextBox:true});
s.addText('Where the seed of a deterministic wallet comes from, how it is written down so a person can keep it, and how a whole wallet is rebuilt from it.',
  {x:0.7, y:2.5, w:8.6, h:0.9, fontFace:B, fontSize:16, color:C.orange, margin:0, valign:'top', isTextBox:true});
s.addText('Before then: work through the chapter 4 page, edit its examples in the playground, and bring one number you could not reproduce.',
  {x:0.7, y:3.5, w:8.6, h:0.6, fontFace:B, fontSize:14, color:'C9D1DA', margin:0, valign:'top', isTextBox:true});
s.addText('Questions?', {x:0.7, y:4.35, w:8.6, h:0.6, fontFace:H, fontSize:24, italic:true, color:'9AA7B4', margin:0, isTextBox:true});
s.addNotes('Set the preparation concretely: the chapter 5 concepts the class will meet first are the recovery code and the key-stretching function, and both are easier after the deterministic-wallet slide of this session. Asking for one number that would not reproduce is the most useful homework this deck can set, because it turns reading into checking.');

pres.writeFile({fileName:process.argv[2]}).then(f => console.log('written', f, '-', nContent, 'content slides,', nCode, 'executed statements shown'));
