const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0401 Chapter 4 - Keys and Addresses';
const C = { dark:'1B1F24', orange:'F7931A', ink:'1F2933', mute:'5B6B7B', card:'F4F2EE', code:'15191E', codeTxt:'E6EDF3', green:'7EE787', white:'FFFFFF', slate:'3A4250' };
const H='Cambria', B='Calibri', M='Courier New';
function chip(s,x,y){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:0.62,h:0.42,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.08});
  s.addText('₿',{x,y,w:0.62,h:0.42,fontFace:B,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function title(s,t,sub){ chip(s,0.5,0.38); s.addText(t,{x:1.25,y:0.28,w:8.2,h:0.62,fontFace:H,fontSize:28,bold:true,color:C.dark,margin:0,valign:'middle',isTextBox:true});
  if(sub) s.addText(sub,{x:1.25,y:0.86,w:8.2,h:0.34,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function light(){ const s=pres.addSlide(); s.background={color:C.white}; return s; } function dark(){ const s=pres.addSlide(); s.background={color:C.dark}; return s; }
function card(s,x,y,w,h,head,body,accent,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1});
  s.addText(head,{x:x+0.2,y:y+0.15,w:w-0.4,h:0.4,fontFace:H,fontSize:17,bold:true,color:accent||C.orange,margin:0,isTextBox:true});
  s.addText(body,{x:x+0.2,y:y+0.58,w:w-0.4,h:h-0.7,fontFace:B,fontSize:fs||13,color:C.ink,margin:0,valign:'top',isTextBox:true}); }
// rows: [statement, result]; an empty result prints nothing, as in a Python session after a statement
function codeCard(s,rows,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; rows.forEach(([c,r],i)=>{ const last=i===rows.length-1;
    runs.push({text:'>>> ',options:{color:C.orange,bold:true}}); runs.push({text:c,options:{color:C.codeTxt,breakLine:!(last&&r==='')}});
    if(r!=='') runs.push({text:r,options:{color:C.green,breakLine:!last}}); });
  s.addText(runs,{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||12,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  s.addText('run under Python '+py,{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
// plain monospaced text on a dark card (not Python: shell commands, logs, JSON)
function termCard(s,lines,x,y,w,h,fs,cap){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  s.addText(lines.map((t,i)=>({text:t,options:{color:t.startsWith('$ ')?C.orange:C.codeTxt,breakLine:i<lines.length-1}})),{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||11,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  if(cap) s.addText(cap,{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
function table(s,rows,x,y,w,colW,fs,rowH){ const tb=rows.map((r,i)=>r.map(t=>i===0?{text:t,options:{bold:true,color:C.white,fill:{color:C.dark}}}:{text:t}));
  s.addTable(tb,{x,y,w,colW,fontFace:B,fontSize:fs||12,color:C.ink,border:{type:'solid',pt:0.5,color:'D9D4CC'},rowH:rowH||0.4,valign:'middle'}); }
const foot=(s,t,y)=>s.addText(t,{x:0.5,y:y||4.75,w:9,h:0.4,fontFace:B,fontSize:12.5,italic:true,color:C.mute,margin:0,isTextBox:true});
const note=(s,t)=>s.addNotes(t); const BK='Mastering Bitcoin, 3rd edition, chapter 4 (Antonopoulos and Harding, 2023)';
const CORE='Bitcoin Core 31.1, downloaded, checked against its published checksums and run as an offline node with the book\u2019s public keys; the outputs are in 08-tooling/ch04-evidence.';


// 1
let s=dark();
[0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.1,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1}); if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.5,w:0.25,h:0,line:{color:C.orange,width:1.5}}); });
s.addText('₿',{x:2.7,y:1.1,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 4: Keys and Addresses',{x:0.6,y:2.25,w:8.8,h:0.8,fontFace:H,fontSize:38,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('From a random number to a string a payer can type — recomputed, and checked three ways',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:17,italic:true,color:C.orange,margin:0,isTextBox:true});
s.addText('SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',{x:0.6,y:4.55,w:8.8,h:0.45,fontFace:B,fontSize:12,color:'C9D1DA',margin:0,isTextBox:true});
note(s,BK+', free under CC BY-SA 4.0. Every number on these slides was computed under Python '+py+' by a toolkit written for this chapter (08-tooling/ch04-evidence), and checked against Bitcoin Core 31.1, the bech32 reference library the book runs, and the BIP350 test vectors. The toolkit is for reading, not for real funds.');

// 2
s=light(); title(s,'Paying Bob without naming him','The receiver is a key, not a person');
card(s,0.5,1.45,2.85,3.0,'Public key','Bob accepts bitcoins to a public key. Anyone can read it; it names no one.',C.slate);
card(s,3.575,1.45,2.85,3.0,'Signature','Alice proves she may spend her earlier output by signing with the private key behind her public key.',C.orange);
card(s,6.65,1.45,2.85,3.0,'Address','A short, typo-proof text that stands for the key, or for a script the key unlocks.',C.slate);
note(s,BK+', the introduction and Public Key Cryptography: the scheme of the original paper, in which a payment goes to a public key and is signed by the spender.');

// 3
s=light(); title(s,'Signatures, not secrecy','Why Bitcoin uses asymmetric cryptography');
card(s,0.5,1.45,4.35,2.9,'Not for hiding','Nothing about a transaction is encrypted. The blockchain is public.',C.slate);
card(s,5.15,1.45,4.35,2.9,'For proving','Only the private key’s owner can produce a signature; anyone with the public key and the transaction can check it. So everyone can verify every spend.',C.orange);
note(s,BK+', the sidebar Why Use Asymmetric Cryptography (Public/Private Keys)?');

// 4
s=light(); title(s,'A private key is a number','Picked at random, below n');
codeCard(s,EX.range,0.5,1.4,5.9,2.7,11.5);
card(s,6.65,1.4,2.85,2.7,'Use secrets','Python’s documentation: secrets is for security tokens and secrets; random is for simulation.',C.orange,12);
foot(s,'N is the order of the curve, about 1.1579 × 10⁷⁷. Never write your own random code for real keys.',4.45);
note(s,BK+', section Private Keys: any number between 0 and n − 1; use a cryptographically secure generator. Python 3.14.4 documentation, the secrets module. Executed under Python '+py+'; the value of k differs on every run and only the check 0 < k < n is shown.');

// 5
s=light(); title(s,'The curve: secp256k1','y² = x³ + 7 over a prime field');
codeCard(s,EX.curve,0.5,1.4,9,1.55,11);
card(s,0.5,3.25,4.35,1.5,'Example 4-1','The point the book gives lies on the curve: the difference is 0 modulo p.',C.slate,12);
card(s,5.15,3.25,4.35,1.5,'The prime','p = 2²⁵⁶ − 2³² − 977, which is the book’s longer sum of powers of two.',C.orange,12);
note(s,BK+', section Elliptic Curve Cryptography Explained, Example 4-1. P is defined in the chapter toolkit. Executed under Python '+py+'.');

// 6
s=light(); title(s,'A correction: who defined the curve','The book credits NIST; the standard does not');
table(s,[['Curve','ANSI X9.62','IEEE P1363','NIST'],['secp256k1','c: conformant','c: conformant','–: not in the NIST list'],['secp256r1','r: recommended','c: conformant','r: recommended']],0.5,1.5,9,[2.0,2.4,2.2,2.4],12,0.5);
card(s,0.5,3.2,9,1.5,'Where','SEC 2 (Standards for Efficient Cryptography, Certicom Research, 2010), Table 2. The book says secp256k1 was “established by” NIST. Bitcoin’s curve is a Koblitz curve defined in SEC 2, and the NIST column of SEC 2’s table marks secp256r1 as recommended and secp256k1 with a dash: not in that list.',C.orange,12);
note(s,'SEC 2 version 2.0, 27 January 2010, Table 2, rows secp256k1 and secp256r1, columns ANSI X9.62, IEEE P1363, IPSec and NIST: for secp256k1 the NIST column is a dash, for secp256r1 it is r. Book statement: chapter 4, Elliptic Curve Cryptography Explained. SEC 2’s legend: a dash denotes parameters nonconformant with the standard, c conformant, r explicitly recommended. Recorded as a finding.');

// 7
s=light(); title(s,'Public key = k × G','Double and add: about 256 steps');
const ecl=EX._snippets.ec.split('\n');
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.5,y:1.4,w:9,h:2.95,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
s.addText(ecl.map((t,i)=>({text:t,options:{color:C.codeTxt,breakLine:i<ecl.length-1}})),{x:0.7,y:1.5,w:8.6,h:2.75,fontFace:M,fontSize:11,valign:'top',margin:0,isTextBox:true});
foot(s,'ec_add is the chord-and-tangent rule; ec_mul adds a point to itself by doubling. G is the fixed generator point of secp256k1.',4.5);
note(s,BK+', section Public Keys. The two functions are the toolkit’s, shown exactly as they run; the check requires the slide to equal the source. Not constant-time and not for real funds; real software uses libsecp256k1.');

// 8
s=light(); title(s,'The book’s public key','k × G for k = 1E99…AEDD');
codeCard(s,EX.pubkey,0.5,1.4,9,2.35,10.5);
card(s,0.5,4.05,9,0.85,'Same as the book','x begins F028892B and y ends 2E505BDB. n × G is the point at infinity, so no key is n or more.',C.orange,12);
note(s,BK+', section Public Keys. The coordinates equal those printed. Executed under Python '+py+'.');

// 9
s=light(); title(s,'Compressed and uncompressed','One key, two spellings');
codeCard(s,EX.compress,0.5,1.4,9,2.1,10.5);
card(s,0.5,3.8,4.35,1.1,'02 or 03','The prefix records whether y is even or odd; x alone fixes y up to sign.',C.slate,12);
card(s,5.15,3.8,4.35,1.1,'04','The old form: x and y, 65 bytes.',C.orange,12);
note(s,BK+', section Compressed Public Keys. The compressed key equals the one printed (prefix 03, y odd). The y coordinate is recovered with one modular exponentiation because p is 3 modulo 4. Executed under Python '+py+'.');

// 10
s=light(); title(s,'A hash is a commitment','Publish the hash now, reveal the input later');
codeCard(s,EX.commit,0.5,1.4,9,2.05,10.5);
card(s,0.5,3.75,9,1.1,'Two keys, two hashes','The compressed and the uncompressed key of one private key hash to different 20-byte commitments, so they make different addresses.',C.orange,12);
note(s,BK+', section Legacy Addresses for P2PKH: the SHA-256 commitment to the answer to the Satoshi question, and HASH160 = RIPEMD-160(SHA-256(K)). Executed under Python '+py+'; RIPEMD-160 needs a Python built with an OpenSSL that provides it.');

// 11
s=light(); title(s,'The P2PKH address','Version 0x00, the commitment, base58check');
codeCard(s,EX.addr,0.5,1.4,9,1.6,11);
table(s,[['Public key','Bitcoin Core 31.1 says'],['compressed','1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'],['uncompressed','1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x']],0.5,3.3,9,[2.4,6.6],12,0.42);
note(s,CORE+' getdescriptorinfo and deriveaddresses on pkh(public key) gave the two addresses; validateaddress accepts them.');

// 12
s=light(); title(s,'Base58check','58 characters, a version byte, a checksum');
codeCard(s,EX.prefix,0.5,1.4,9,1.6,11);
card(s,0.5,3.3,4.35,1.5,'The alphabet','No 0, O, l, I: they look alike in many fonts. Plus and slash are dropped too.',C.slate,12);
card(s,5.15,3.3,4.35,1.5,'The checksum','The first four bytes of SHA-256 applied twice to the prefixed data, appended before encoding.',C.orange,12);
note(s,BK+', section Base58check Encoding and its table of version prefixes. The first characters were computed from the smallest and largest payloads of the right length: version 0x00 begins with 1, 0x05 with 3, 0xc4 with 2, and 0x80 with a suffix begins with K or L. Executed under Python '+py+'.');

// 13
s=light(); title(s,'Wallet import format','The same private key, two exports');
codeCard(s,EX.wif,0.5,1.4,9,2.2,10.5);
card(s,0.5,3.9,9,0.95,'Not a compressed key','The 01 suffix says: only derive compressed public keys from this key. That one byte moves the first character from 5 to K.',C.orange,12);
note(s,BK+', sections Private Key Formats and Compressed Private Keys: both strings equal the ones printed. Bitcoin Core 31.1 turns each of them into the matching address through the descriptors pkh(WIF): the uncompressed WIF gives 1424C2F4… and the compressed one 1J7mdg5r…. Executed under Python '+py+'.');

// 14
s=light(); title(s,'P2SH, and the collision numbers','A commitment to a script; numbers to refresh');
codeCard(s,EX.collide,0.5,1.4,5.3,2.0,11);
card(s,6.05,1.4,3.45,2.0,'The book, 2023','All miners: about 2⁸⁰ hashes an hour; 2¹²⁸ hashes would take about 32 billion years.',C.slate,12);
card(s,0.5,3.65,9,1.15,'Now','A third party’s hash-rate estimate is 9.5 × 10²⁰ hashes a second: 2.8 times the hourly figure, and about 11 billion years for 2¹²⁸ hashes. The conclusion stands; the numbers moved.',C.orange,12);
note(s,BK+', sections Legacy Pay to Script Hash (P2SH) and the sidebar P2SH Collision Attacks. Hash rate from the mempool.space API read on 2026-09-28 (a third party’s estimate). The P2SH example 3F6i6kwk… has a valid checksum and version byte 5. Executed under Python '+py+'.');

// 15
s=light(); title(s,'Bech32 addresses','HRP, 1, version, program, checksum');
codeCard(s,EX.bech,0.5,1.4,9,1.85,10);
card(s,0.5,3.55,4.35,1.3,'Parts','bc, the separator 1, then q for version 0 or p for 1, the witness program, and six checksum characters.',C.slate,12);
card(s,5.15,3.55,4.35,1.3,'Same four as the book','The toolkit, the book’s own library and, for the first three, Bitcoin Core’s validation all agree.',C.orange,12);
foot(s,'PROG_WPKH, PROG_WSH and PROG_TR are the three programs the book prints.',4.95);
note(s,BK+', section Bech32m: the four addresses and the reference library it runs (sipa/bech32). The toolkit and the library produce the same four strings; Bitcoin Core 31.1 validates all four and reports witness versions 0, 0, 1 and 16. Executed under Python '+py+'.');

// 16
s=light(); title(s,'Bech32 and bech32m','One constant apart');
codeCard(s,EX.ext,0.5,1.4,9,1.75,10.5);
card(s,0.5,3.45,4.35,1.4,'Why bech32m','With the old constant, adding or removing q before a final p kept the checksum valid. All six strings the book lists pass it.',C.slate,12);
card(s,5.15,3.45,4.35,1.4,'Bitcoin Core','Rejects all six: a version 1 witness must use a bech32m checksum.',C.orange,12);
note(s,BK+', section Problems with Bech32 Addresses and Bech32m. EXT is the intended string and the five extended ones the book prints. Core 31.1 answered “Version 1+ witness address must use Bech32m checksum” for each. Executed under Python '+py+'.');

// 17
s=light(); title(s,'Errors: detected, and located','The guarantees, tested');
table(s,[['Test on the book’s bc1q9d3x… address','Undetected'],['every one-character substitution','0'],['every two-character substitution','0'],['200,000 random three- or four-character substitutions','0'],['book’s typo example, in Bitcoin Core 31.1','errors located at 25 and 40']],0.5,1.5,9,[6.0,3.0],12.5,0.5);
foot(s,'That is a test, not a proof: the guarantee for up to four characters is a property of the code, which the tests do not replace.',4.3);
note(s,BK+', section Bech32 Addresses: any error affecting four characters or fewer is detected. The exhaustive and random tests are 08-tooling/ch04-evidence/sen0401_ch04_verify_v1_0_0.py; the typo example is the book’s bc1p9nh05… with two characters changed, whose positions Core reports as 25 and 40, the two letters the book underlines.');

// 18
s=light(); title(s,'Three independent checks','Written down, so you can rerun them');
table(s,[['Reference','What it checked','Result'],['The book’s bech32 library','the four addresses, 8 valid and 15 invalid BIP350 vectors','all agree'],['Bitcoin Core 31.1','public key to address, WIF to address, validation of every printed address','all agree'],['This chapter’s toolkit','key, addresses, WIF, checksums, vectors','all agree']],0.5,1.45,9,[2.6,4.6,1.8],12,0.6);
foot(s,'BIP173 and BIP350, which define bech32 and bech32m, are both marked Deployed in the BIPs repository.',4.3);
note(s,CORE+' The reference library and the BIP350 vectors were read on 2026-09-29 from github.com/sipa/bech32 and the BIPs repository.');

// 19
s=light(); title(s,'What a new wallet hands out','Bitcoin Core 31.1: four types');
table(s,[['Type','Looks like','Script'],['default','bc1q…','P2WPKH, witness v0'],['legacy','1…','P2PKH'],['p2sh-segwit','3…','P2SH wrapping P2WPKH'],['bech32','bc1q…','P2WPKH, witness v0'],['bech32m','bc1p…','taproot, witness v1']],0.5,1.45,9,[2.2,2.2,4.6],12,0.42);
foot(s,'The default is bech32; the book’s 1J7… address is the legacy type.',4.5);
note(s,CORE+' getnewaddress with each type on a throw-away wallet, getaddressinfo for the kind of script. The addresstype option’s help gives the default as bech32.');

// 20
s=light(); title(s,'Exporting one key','The notes’ commands, on 31.1');
termCard(s,['$ bitcoin-cli getnewaddress','bc1q…            # not 1J7… any more','$ bitcoin-cli dumpprivkey <address>','help: unknown command: dumpprivkey','$ bitcoin-cli importprivkey <WIF>','help: unknown command: importprivkey'],0.5,1.45,5.8,2.2,11,'run on 31.1');
card(s,6.5,1.45,3.0,2.2,'Still possible','A WIF key inside a descriptor: pkh(WIF) gives its address. Wallets are descriptor wallets.',C.orange,12);
foot(s,'BIP38 encrypts a key under a passphrase; the BIPs repository marks it Deployed with the comment “Unanimously Discourage for implementation”.',4.0);
note(s,CORE+' Bitcoin Core 30.0 release notes list dumpprivkey and importprivkey among the removed legacy wallet RPCs. The owner’s course notes, slides 31 and 32, run getnewaddress and dumpprivkey; slides 115 to 121 cover BIP38, which the 3rd edition’s chapter does not.');

// 21
s=light(); title(s,'Vanity addresses, recomputed','Each character multiplies the work by 58');
codeCard(s,EX.vanity,0.5,1.4,4.9,1.5,11);
table(s,[['Length','Book','Recomputed'],['4','1 minute','57 seconds'],['7','3–4 months','128 days'],['8','13–18 years','20 years'],['9','800 years','1,180 years'],['11','2.5 million years','4.0 million years']],5.6,1.4,3.9,[0.9,1.5,1.5],10.5,0.36);
foot(s,'At 100,000 keys a second, average time = half the frequency. The book’s frequencies are exact except 23 quintillion for eleven: 58¹¹ is 25 quintillion.',3.95);
note(s,BK+', section Vanity Addresses, the table of pattern frequency and average search time. Recomputed with average time = 58^n / 2 / 100,000 keys per second: the book’s times agree through seven characters and are about a third shorter from eight. Executed under Python '+py+'.');

// 22
s=light(); title(s,'Our theme: keys and identifiers','A key pair proves control without asking anyone');
[['Key pair','proves control by signing',0.5],['Address','names what a key controls',3.575],['DID','a URI for a subject and its keys',6.65]].forEach(([h,t,x],i)=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:1.5,w:2.85,h:1.2,fill:{color:i===1?C.orange:C.card},line:{color:i===1?C.orange:C.card},rectRadius:0.1});
  s.addText([{text:h,options:{bold:true,breakLine:true,fontSize:18}},{text:t,options:{fontSize:13}}],{x,y:1.5,w:2.85,h:1.2,fontFace:H,color:i===1?C.white:C.dark,align:'center',valign:'middle',margin:0,isTextBox:true}); });
s.addText('W3C’s Decentralized Identifiers are URIs that associate a subject with a DID document carrying cryptographic material such as verification methods; the controller can prove control without permission from any other party.',{x:0.5,y:3.0,w:9,h:1.0,fontFace:B,fontSize:15,color:C.ink,margin:0,valign:'top',isTextBox:true});
s.addText('A project idea: describe a Bitcoin address as a DID document and list what a verifier would check.',{x:0.5,y:4.3,w:9,h:0.45,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Decentralized Identifiers (DIDs) v1.0, W3C Recommendation, 19 July 2022, abstract. The project idea is a teaching suggestion within the term theme.');

// 23
s=light(); title(s,'Discussion','Assess what you got so far');
[['Trust','You reproduced a book’s numbers three ways. Which of the three would you trust least, and why?'],['Aged','Which statement or number in the chapter has aged, or was never right?'],['Your key','Would you export a single private key today? What would you use instead?']].forEach(([h,t],i)=>card(s,0.5+i*3.075,1.45,2.85,3.0,h,t,i%2?C.orange:C.slate));
note(s,'Discussion prompts written for this deck from its findings.');

// 24
s=light(); title(s,'Check yourself','Answer before you open the interactive page');
['Why does Bitcoin use asymmetric cryptography, if not to keep transactions secret?','Which standard defines secp256k1, and is it a NIST curve?','Why do one private key’s compressed and uncompressed public keys give different addresses?','What single change separates bech32 from bech32m, and what does it protect against?','The book’s 1J7… address: what type is it, and what does a 31.1 wallet give you by default?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.orange},line:{color:C.orange}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: so that anyone can verify a signature that only the key’s owner could make; SEC 2 by Certicom Research, and no; the two keys hash to different commitments; the checksum constant, 1 against 0x2bc830a3, which stops a q added or removed before a final p passing unnoticed; a legacy P2PKH address of the compressed key, and a bech32 P2WPKH address.');

// 25
s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter’s research record');
const src=['Antonopoulos, A. M., Harding, D. A. (2023). Mastering Bitcoin, 3rd ed., ch. 4. O’Reilly. CC BY-SA 4.0. github.com/bitcoinbook/bitcoinbook','Certicom Research (2010). SEC 2: Recommended Elliptic Curve Domain Parameters, version 2.0, Table 2. secg.org/sec2-v2.pdf','Wuille, P. (2020). BIP173, BIP350 and the bech32 reference code. github.com/bitcoin/bips, github.com/sipa/bech32','Bitcoin Core (2026). Release 31.1 run as an offline node; release notes 30.0. bitcoincore.org, github.com/bitcoin/bitcoin','Mempool Space (2026). Hash rate. mempool.space/api. A third party’s estimate.','W3C (2022). Decentralized Identifiers (DIDs) v1.0. w3.org/TR/did-core','Python Software Foundation (2026). secrets, Python 3.14.4 documentation','Altunel, Y. (2021). Course notes, chapter 4, after Mastering Bitcoin 2nd ed. — checked against the 3rd edition and 31.1 before use'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.4,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:5,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0; this deck is shared under the same licence.',{x:0.5,y:5.0,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch04/rdodi/sen0401_ch04_research_v1_0_0.ttl.');

// 26
s=dark(); s.addText('Next week: Chapter 5 — Wallets',{x:0.6,y:1.7,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 4 page, and edit its examples in the playground.',{x:0.6,y:2.65,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.orange,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D1DA',margin:0,isTextBox:true});
note(s,'Chapter 5 of the 3rd edition is Wallets.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
