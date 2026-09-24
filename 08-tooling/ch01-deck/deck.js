const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out.json')); const py = EX._python;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0401 Chapter 1 - Introduction to Bitcoin';
const C = { dark:'1B1F24', orange:'F7931A', ink:'1F2933', mute:'5B6B7B', card:'F4F2EE', code:'15191E', codeTxt:'E6EDF3', green:'7EE787', white:'FFFFFF', slate:'3A4250' };
const H='Cambria', B='Calibri', M='Courier New';
function chip(s,x,y){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:0.62,h:0.42,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.08});
  s.addText('\u20bf',{x,y,w:0.62,h:0.42,fontFace:B,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function title(s,t,sub){ chip(s,0.5,0.38); s.addText(t,{x:1.25,y:0.28,w:8.2,h:0.62,fontFace:H,fontSize:30,bold:true,color:C.dark,margin:0,valign:'middle',isTextBox:true});
  if(sub) s.addText(sub,{x:1.25,y:0.86,w:8.2,h:0.34,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true}); }
function light(){ const s=pres.addSlide(); s.background={color:C.white}; return s; } function dark(){ const s=pres.addSlide(); s.background={color:C.dark}; return s; }
function card(s,x,y,w,h,head,body,accent){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1});
  s.addText(head,{x:x+0.2,y:y+0.15,w:w-0.4,h:0.4,fontFace:H,fontSize:17,bold:true,color:accent||C.orange,margin:0,isTextBox:true});
  s.addText(body,{x:x+0.2,y:y+0.58,w:w-0.4,h:h-0.7,fontFace:B,fontSize:13,color:C.ink,margin:0,valign:'top',isTextBox:true}); }
function codeCard(s,rows,x,y,w,h,fs){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; rows.forEach(([c,r],i)=>{ const parts=c.split('; '); parts.forEach((p,j)=>{ runs.push({text:'>>> ',options:{color:C.orange,bold:true}}); runs.push({text:p,options:{color:C.codeTxt,breakLine:true}}); });
    runs.push({text:r,options:{color:C.green,breakLine:i<rows.length-1}}); });
  s.addText(runs,{x:x+0.2,y:y+0.12,w:w-0.4,h:h-0.24,fontFace:M,fontSize:fs||14,valign:'top',margin:0,paraSpaceAfter:2,isTextBox:true});
  s.addText('run under Python '+py,{x,y:y+h+0.04,w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
const note=(s,t)=>s.addNotes(t); const BK='Mastering Bitcoin, 3rd edition, chapter 1 (Antonopoulos and Harding, 2023)';

let s=dark();
[0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.1,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1}); if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.5,w:0.25,h:0,line:{color:C.orange,width:2}}); });
s.addText('\u20bf',{x:2.7,y:1.1,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 1: Introduction',{x:0.6,y:2.25,w:8.8,h:0.8,fontFace:H,fontSize:40,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Bitcoin as money, network and software \u2014 and how to start using it',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.orange,margin:0,isTextBox:true});
s.addText('SEN0401 Special Topics in Software Engineering: Block Chain \u00b7 Fall 2026 \u00b7 Yusuf Altunel, PhD \u00b7 \u0130stanbul K\u00fclt\u00fcr University',{x:0.6,y:4.55,w:8.8,h:0.45,fontFace:B,fontSize:12,color:'C9D1DA',margin:0,isTextBox:true});
note(s,BK+', free under CC BY-SA 4.0 from github.com/bitcoinbook/bitcoinbook (tag third_edition_print1). Every computed figure was executed under Python '+py+'; every claim beyond the book is in the chapter 1 research record, 03-materials/ch01/rdodi.');

s=light(); title(s,'bitcoin or Bitcoin?','The capital letter matters');
card(s,0.5,1.45,4.35,2.4,'bitcoin \u2014 the unit','Units of currency that store and transmit value among participants. There are no physical coins, not even individual digital coins: the coins are implied in transactions.',C.orange);
card(s,5.15,1.45,4.35,2.4,'Bitcoin \u2014 the system','A collection of concepts and technologies: a network, a protocol and open source software that runs on laptops and smartphones.',C.slate);
s.addText('Users control keys that prove ownership; with them they sign transactions that spend bitcoin to a new owner.',{x:0.5,y:4.2,w:9,h:0.6,fontFace:B,fontSize:14,color:C.ink,margin:0,isTextBox:true});
note(s,BK+': the unit is bitcoin with a small b, the system Bitcoin with a capital B.');

s=light(); title(s,'From a paper to a running network','History, and what has changed since the book');
const tl=[['2008','Nakamoto\u2019s paper: A Peer-to-Peer Electronic Cash System'],['2009','The network starts from a reference implementation'],['Apr 2011','Nakamoto withdraws from public view'],['Dec 2023','3rd edition of the book published'],['20 Apr 2024','Halving at block 840000: subsidy 3.125'],['Today','Bitcoin Core 31.1 is the newest release']];
s.addShape(pres.shapes.LINE,{x:0.7,y:2.55,w:8.6,h:0,line:{color:C.orange,width:3}});
tl.forEach(([d,t],i)=>{ const x=0.55+i*1.5; s.addShape(pres.shapes.OVAL,{x:x+0.45,y:2.4,w:0.3,h:0.3,fill:{color:i<3?C.slate:C.orange},line:{color:C.white,width:2}});
  s.addText(d,{x,y:1.75,w:1.4,h:0.5,fontFace:H,fontSize:15,bold:true,color:C.dark,align:'center',margin:0,isTextBox:true});
  s.addText(t,{x,y:2.9,w:1.4,h:1.3,fontFace:B,fontSize:11.5,color:C.ink,align:'center',valign:'top',margin:0,isTextBox:true}); });
s.addText('Grey: in the book. Orange: after it, or its publication.',{x:0.5,y:4.6,w:9,h:0.35,fontFace:B,fontSize:11,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'2008 and 2009 and April 2011: '+BK+'. Halving at block 840000 on 2024-04-20 to 3.125: Bitcoin Wiki, Controlled supply. Bitcoin Core 31.1: bitcoincore.org/en/releases, read 2026-09-25.');

s=light(); title(s,'Proof of work and consensus','Agreeing without an authority: the key innovation');
card(s,0.5,1.45,2.85,2.9,'Consensus','A decentralized network must agree on which transactions happened \u2014 with no trusted party to ask.',C.slate);
card(s,3.575,1.45,2.85,2.9,'Proof of work','A global lottery every 10 minutes on average. Winning is costly; checking the win is cheap.',C.orange);
card(s,6.65,1.45,2.85,2.9,'Double-spend solved','Spending one unit twice was digital money\u2019s weakness, handled before only by a central clearinghouse.',C.slate);
s.addText('Its ancestor: Hashcash (Back, 2002), proposed to throttle abuse by making each request cost computation.',{x:0.5,y:4.55,w:9,h:0.45,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,BK+'. Hashcash: Back, A. (2002), Hashcash - A Denial of Service Counter-Measure.');

s=light(); title(s,'Try it: a toy proof of work','Find a number whose SHA-256 hash starts with four zeros');
codeCard(s,EX.pow,0.5,1.45,9,1.85,13);
card(s,0.5,3.65,9,1.2,'A toy, not the real thing','Bitcoin\u2019s difficulty is astronomically higher and adjusts so a block is found every 10 minutes on average. The principle is the same: hard to find, instant to verify.',C.orange);
note(s,'The search and its result were executed under Python '+py+'. The interactive page has a playground where students change the data and the number of zeros.');

s=light(); title(s,'Just below 21 million','The supply is a schedule, not a decision');
const eras=JSON.parse(EX.eras[0][1].replace(/'/g,'"'));
s.addChart(pres.charts.BAR,[{name:'Block subsidy (bitcoin)',labels:['Era 0','Era 1','Era 2','Era 3','Era 4','Era 5'],values:eras}],{x:0.5,y:1.35,w:5.2,h:3.4,barDir:'col',chartColors:[C.orange],showValue:true,dataLabelPosition:'outEnd',dataLabelFontSize:10,dataLabelFormatCode:'0.#####',showTitle:true,title:'Block subsidy by era',titleFontSize:13,catAxisLabelFontSize:10,valAxisHidden:true,valGridLine:{style:'none'}});
codeCard(s,EX.supply,6.0,1.45,3.5,2.3,11);
s.addText('Every 210000 blocks the subsidy halves; the sum converges just below 21 million, as the book says.',{x:6.0,y:4.1,w:3.5,h:0.9,fontFace:B,fontSize:12,color:C.ink,margin:0,isTextBox:true});
note(s,'Chart values and both results computed under Python '+py+'. Each era is 210000 blocks; era 4 began at block 840000 on 2024-04-20 (Bitcoin Wiki, Controlled supply).');

s=light(); title(s,'Choosing a wallet: by platform','The book names types, not brands \u2014 wallets change too fast');
card(s,0.5,1.45,2.85,3.0,'Desktop','The first type of Bitcoin wallet, created as a reference implementation. Autonomy and control, on operating systems that are often poorly secured.',C.slate);
card(s,3.575,1.45,2.85,3.0,'Mobile','The most common type of Bitcoin wallet, on iOS and Android: always with you.',C.orange);
card(s,6.65,1.45,2.85,3.0,'Web','Used through a browser: convenient, and it places trust in whoever runs the service.',C.slate);
note(s,BK+', section Types of Bitcoin wallets.');

s=light(); title(s,'Choosing a wallet: by how much it checks','Full node versus lightweight');
const tbl=[[{text:'',options:{fill:{color:C.dark}}},{text:'Validates history itself?',options:{bold:true,color:C.white,fill:{color:C.dark}}},{text:'Trusts',options:{bold:true,color:C.white,fill:{color:C.dark}}}],
 [{text:'Full node',options:{bold:true}},'Yes \u2014 the entire history of transactions','Nobody else for the ledger'],
 [{text:'Lightweight client',options:{bold:true}},'No','Other nodes for validation'],
 [{text:'Third-party API client',options:{bold:true}},'No','A third party\u2019s servers']];
s.addTable(tbl,{x:0.5,y:1.5,w:9,colW:[2.4,3.6,3.0],fontFace:B,fontSize:15,color:C.ink,border:{type:'solid',pt:0.5,color:'D9D4CC'},rowH:0.55});
note(s,BK+', section Full node versus Lightweight.');

s=light(); title(s,'Who controls the keys?','The question that decides who really owns the bitcoin');
card(s,0.5,1.45,4.35,2.9,'Noncustodial','Only you hold the keys. Only you can spend \u2014 and only you can lose access. The book\u2019s example, Alice, chooses this.',C.orange);
card(s,5.15,1.45,4.35,2.9,'Custodial','Someone else holds the keys for you. Convenient, but the bitcoin is theirs to move.',C.slate);
note(s,BK+', section Who controls the keys.');

s=light(); title(s,'Recovery codes','A list of words that can rebuild the whole wallet');
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.5,y:1.45,w:4.6,h:2.9,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
s.addText('media  suspect  effort  dish\nalbum  shaft  price  junk\npizza  situate  oyster  rib',{x:0.7,y:1.6,w:4.2,h:2.1,fontFace:M,fontSize:17,color:C.codeTxt,valign:'middle',margin:0,isTextBox:true});
s.addText('Sample from the book \u2014 never use a published code',{x:0.7,y:3.8,w:4.2,h:0.4,fontFace:B,fontSize:11,italic:true,color:C.orange,margin:0,isTextBox:true});
card(s,5.4,1.45,4.1,2.9,'What it is','Words chosen randomly by the wallet and used as the basis for its keys. Wallets commonly follow BIP 39, whose initial entropy is 128 to 256 bits. Whoever has the words has the bitcoin.',C.orange);
note(s,BK+', section Recovery Codes, sample table. BIP 39 (Palatinus, Rusnak, Voisine and Bowe, 2013): allowed initial entropy 128-256 bits.');

s=light(); title(s,'Bitcoin addresses','Numbers derived from your key \u2014 registered nowhere');
card(s,0.5,1.45,2.85,2.9,'Derived','Generated by the wallet from its private key, without any service or registration.',C.slate);
card(s,3.575,1.45,2.85,2.9,'Safe to share','Anyone with your address can pay you; nobody can withdraw with it. You initiate every spend.',C.orange);
card(s,6.65,1.45,2.85,2.9,'New each time','Reusing an address lets payers see each other\u2019s payments. A new invoice and address per payment protects privacy.',C.slate);
note(s,BK+', section Bitcoin Addresses.');

s=light(); title(s,'Receiving, pricing, sending','Alice\u2019s first bitcoin');
[['1','Receive','The wallet shows an address or invoice, often as a QR code.'],['2','Agree a price','A floating exchange rate set by markets; pricing services average them.'],['3','Send','The wallet signs a transaction that spends to the recipient\u2019s address.']].forEach(([n,h,t],i)=>{ const x=0.5+i*3.05;
  s.addShape(pres.shapes.OVAL,{x,y:1.5,w:0.6,h:0.6,fill:{color:C.orange},line:{color:C.orange}}); s.addText(n,{x,y:1.5,w:0.6,h:0.6,fontFace:H,fontSize:20,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(h,{x:x+0.75,y:1.52,w:2.1,h:0.55,fontFace:H,fontSize:18,bold:true,color:C.dark,valign:'middle',margin:0,isTextBox:true});
  s.addText(t,{x,y:2.3,w:2.8,h:1.6,fontFace:B,fontSize:14,color:C.ink,valign:'top',margin:0,isTextBox:true}); if(i<2) s.addShape(pres.shapes.LINE,{x:x+2.85,y:1.8,w:0.2,h:0,line:{color:C.orange,width:2}}); });
note(s,BK+', sections Receiving Bitcoin, Finding the Current Price of Bitcoin, Sending and Receiving Bitcoin.');

s=light(); title(s,'Our theme: semantic technologies','The chapter\u2019s key idea, applied to identity');
card(s,0.5,1.45,4.35,2.9,'From the book','Control belongs to whoever holds the keys. No central registry issues addresses or approves spends.',C.slate);
card(s,5.15,1.45,4.35,2.9,'W3C standards','Decentralized Identifiers (Recommendation, 2022) apply the same principle to identity; Verifiable Credentials 2.0 (Recommendation, 2025) build signed claims on it.',C.orange);
s.addText('A project idea for this term: model keys, identities and credentials as an ontology, and reason over them.',{x:0.5,y:4.55,w:9,h:0.45,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'W3C Decentralized Identifiers (DIDs) v1.0, Recommendation 9 July 2022; Verifiable Credentials Data Model v2.0, Recommendation 5 May 2025. The project idea is a suggestion within the term theme, not a requirement.');

s=light(); title(s,'Check yourself','Answer before you look at the interactive page');
['What problem does proof of work solve without a central clearinghouse?','Why does the total supply stay just below 21 million?','What was the block subsidy after the halving in April 2024?','In a noncustodial wallet, who can spend the bitcoin?','Why should you use a new address for each payment?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.orange},line:{color:C.orange}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: the double-spend; the subsidy halves every 210000 blocks so the sum converges at 20999999.9769; 3.125 bitcoin; only the user; to keep payers from seeing each other\u2019s payments.');

s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter\u2019s research record');
const src=['Antonopoulos, A. M., Harding, D. A. (2023). Mastering Bitcoin, 3rd ed., ch. 1. O\u2019Reilly. CC BY-SA 4.0. github.com/bitcoinbook/bitcoinbook','Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. bitcoin.org/bitcoin.pdf','Back, A. (2002). Hashcash - A Denial of Service Counter-Measure. hashcash.org','Bitcoin Wiki (2026). Controlled supply. en.bitcoin.it/wiki/Controlled_supply','Bitcoin Core (2026). Releases. bitcoincore.org/en/releases','Palatinus, M. et al. (2013). BIP 39 \u2013 Mnemonic code for generating deterministic keys','W3C (2022). Decentralized Identifiers v1.0; W3C (2025). Verifiable Credentials Data Model v2.0'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.5,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:5,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0; this deck is shared under the same licence.',{x:0.5,y:5.0,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch01/rdodi/sen0401_ch01_research_v1_0_0.ttl.');

s=dark();
s.addText('Next week: Chapter 2 \u2014 Overview',{x:0.6,y:1.7,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 1 interactive page, and mine a block in its playground.',{x:0.6,y:2.65,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.orange,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D1DA',margin:0,isTextBox:true});
note(s,'Chapter 2 of the 3rd edition is Overview.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
