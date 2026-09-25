const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out.json')); const py = EX._python;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0401 Chapter 2 - How Bitcoin Works';
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
const note=(s,t)=>s.addNotes(t); const BK='Mastering Bitcoin, 3rd edition, chapter 2 (Antonopoulos and Harding, 2023)';


let s=dark();
[0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.1,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1}); if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.5,w:0.25,h:0,line:{color:C.orange,width:2}}); });
s.addText('\u20bf',{x:2.7,y:1.1,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 2: How Bitcoin Works',{x:0.6,y:2.25,w:8.8,h:0.8,fontFace:H,fontSize:40,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('One payment, followed from Alice\u2019s wallet to the blockchain',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.orange,margin:0,isTextBox:true});
s.addText('SEN0401 Special Topics in Software Engineering: Block Chain \u00b7 Fall 2026 \u00b7 Yusuf Altunel, PhD \u00b7 \u0130stanbul K\u00fclt\u00fcr University',{x:0.6,y:4.55,w:8.8,h:0.45,fontFace:B,fontSize:12,color:'C9D1DA',margin:0,isTextBox:true});
note(s,BK+', free under CC BY-SA 4.0. Every computed figure was executed under Python '+py+'; claims beyond the book are in 03-materials/ch02/rdodi.');

s=light(); title(s,'Three parts, no trusted third party','Every user can verify every rule with their own software');
card(s,0.5,1.45,2.85,2.9,'Wallets','Users with wallets holding keys, which sign transactions.',C.slate);
card(s,3.575,1.45,2.85,2.9,'Transactions','Propagated across the network from wallet to wallet and on to miners.',C.orange);
card(s,6.65,1.45,2.85,2.9,'Miners','Produce, through competitive computation, the blockchain: the authoritative journal of all transactions.',C.slate);
note(s,BK+', sections How Bitcoin Works and Bitcoin Overview.');

s=light(); title(s,'Buying from an online store','Alice pays Bob\u2019s Store by scanning a QR code');
codeCard(s,EX.units,0.5,1.45,4.2,1.6,16);
card(s,5.0,1.45,4.5,2.9,'From bitcoin to satoshis','A bitcoin divides into 100,000,000 satoshis; a millibitcoin is a thousandth. Within seconds of Alice sending, Bob sees the payment on the register.',C.orange);
s.addText('Satoshis per bitcoin, and per millibitcoin',{x:0.5,y:3.35,w:4.2,h:0.4,fontFace:B,fontSize:12,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,BK+', section Buying from an Online Store.');

s=light(); title(s,'The payment request','What the store\u2019s QR code actually encodes');
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.5,y:1.45,w:9,h:1.05,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
s.addText('bitcoin:bc1qk2g6u8p4qm2s2lh3gts5cpt2mrv5skcuu7u3e4?amount=0.01577764&label=Bob%27s%20Store&message=Purchase%20at%20Bob%27s%20Store',{x:0.7,y:1.5,w:8.6,h:0.95,fontFace:M,fontSize:12.5,color:C.codeTxt,valign:'middle',margin:0,isTextBox:true});
[['Address','bc1qk2g6\u2026u7u3e4'],['Amount','0.01577764'],['Label','Bob\u2019s Store'],['Message','Purchase at Bob\u2019s Store']].forEach(([h,t],i)=>card(s,0.5+i*2.3,2.8,2.15,1.6,h,t,i%2?C.slate:C.orange));
s.addText('A URI format defined in BIP21: the wallet reads it, so Alice never types an address.',{x:0.5,y:4.6,w:9,h:0.4,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,BK+', section Buying from an Online Store: the invoice QR code encodes this URI, defined in BIP21. Highlighted in '+"the owner\u2019s course notes (CSE0469, after the 2nd edition)"+', which used the 2nd edition\u2019s older address format.');

s=light(); title(s,'A transaction is a ledger line','Inputs spend, outputs receive, and the difference is the fee');
codeCard(s,EX.fee,0.5,1.45,5.3,1.75,12);
card(s,6.1,1.45,3.4,2.9,'The implied fee','Inputs minus outputs, in satoshis. Nobody writes the fee down: the miner who includes the transaction collects the difference.',C.orange);
s.addText('Toy amounts in satoshis \u2014 not a real transaction',{x:0.5,y:3.5,w:5.3,h:0.4,fontFace:B,fontSize:12,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,BK+', section Transaction Inputs and Outputs. The amounts are an illustration; the computation was executed under Python '+py+'.');

s=light(); title(s,'Transaction chains and change','Every payment spends earlier outputs');
['Joe \u2192 Alice','Alice \u2192 Bob\u2019s Store','Bob \u2192 \u2026'].forEach((t,i)=>{ const x=0.5+i*3.1; s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:1.5,w:2.6,h:0.9,fill:{color:i===1?C.orange:C.card},line:{color:C.orange,width:1.5},rectRadius:0.1});
  s.addText(t,{x,y:1.5,w:2.6,h:0.9,fontFace:H,fontSize:16,bold:true,color:i===1?C.white:C.dark,align:'center',valign:'middle',margin:0,isTextBox:true}); if(i<2) s.addShape(pres.shapes.LINE,{x:x+2.6,y:1.95,w:0.5,h:0,line:{color:C.orange,width:2.5,endArrowType:'triangle'}}); });
codeCard(s,EX.change,0.5,2.9,3.2,1.1,17);
card(s,4.0,2.8,5.5,1.9,'Making change','Paying 5 bitcoins with a 20-bitcoin input sends 15 back as change, not counting the fee \u2014 usually to a new address, so outsiders cannot tell change from payment.',C.slate);
note(s,BK+', sections Transaction Chains and Making Change.');

s=light(); title(s,'Coin selection and common forms','Wallets choose inputs much as people choose cash');
card(s,0.5,1.45,2.85,3.0,'Coin selection','Many small inputs, or one large one? Always using the largest note leaves a pocket of change; wallets aim for a balance.',C.slate);
card(s,3.575,1.45,2.85,3.0,'Simple payment','The most common form: one input, two outputs \u2014 the payment and the change.',C.orange);
card(s,6.65,1.45,2.85,3.0,'Consolidation','Many inputs spent into one output, like exchanging a pile of coins for a single note.',C.slate);
note(s,BK+', sections Coin Selection and Common Transaction Forms.');

s=light(); title(s,'From wallet to network','Constructing and propagating a transaction');
[['1','Get inputs','The wallet finds unspent outputs it controls.'],['2','Create outputs','Payment, change, and the fee as the difference.'],['3','Transmit','Signed and sent to the network.'],['4','Propagate','Relayed node to node until miners hold it.']].forEach(([n,h,t],i)=>{ const x=0.5+i*2.3;
  s.addShape(pres.shapes.OVAL,{x,y:1.5,w:0.55,h:0.55,fill:{color:C.orange},line:{color:C.orange}}); s.addText(n,{x,y:1.5,w:0.55,h:0.55,fontFace:H,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(h,{x:x+0.65,y:1.5,w:1.55,h:0.55,fontFace:H,fontSize:15,bold:true,color:C.dark,valign:'middle',margin:0,isTextBox:true}); s.addText(t,{x,y:2.25,w:2.1,h:1.6,fontFace:B,fontSize:13,color:C.ink,valign:'top',margin:0,isTextBox:true}); });
note(s,BK+', sections Constructing a Transaction, Getting the Right Inputs, Creating the Outputs, Adding the Transaction to the Blockchain.');

s=light(); title(s,'Mining','Hard to produce, easy to check');
card(s,0.5,1.45,4.35,2.9,'Blocks','Transactions are bundled into blocks whose small header takes an enormous amount of computation to form correctly, and little to verify.',C.orange);
card(s,5.15,1.45,4.35,2.9,'Why miners stay honest','They earn only from blocks that follow every consensus rule. Mining also issues new bitcoin on a fixed, diminishing schedule.',C.slate);
note(s,BK+', section Bitcoin Mining.');

s=light(); title(s,'Confirmations, quantified','The whitepaper\u2019s own procedure, reproduced in Python');
codeCard(s,EX.wp,0.5,1.4,5.6,2.45,10);
const vals=JSON.parse(EX.table[0][1]); const tb=[[{text:'Confirmations',options:{bold:true,color:C.white,fill:{color:C.dark}}},{text:'Attacker succeeds (10% hash power)',options:{bold:true,color:C.white,fill:{color:C.dark}}}]];
[0,1,2,3,6,10].forEach(z=>tb.push([String(z),{text:String(vals[z]),options:{fontFace:M}}]));
s.addTable(tb,{x:6.4,y:1.4,w:3.1,colW:[1.1,2.0],fontFace:B,fontSize:11,color:C.ink,border:{type:'solid',pt:0.5,color:'D9D4CC'},rowH:0.33});
s.addText('Matches the table in Nakamoto (2008), section 11, to seven decimals.',{x:0.5,y:4.4,w:9,h:0.4,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Nakamoto (2008), section 11, Calculations: for q=0.1 the paper lists P=0.2045873 at z=1 and P=0.0002428 at z=6. The table on this slide was computed under Python '+py+'.');

s=light(); title(s,'Mining as a giant sudoku','An analogy for hard-to-solve, easy-to-check');
[['Hard to solve','Finding a solution takes enormous trial and error across the whole network.'],['Easy to verify','Anyone can check a finished puzzle quickly, however large it is.'],['Adjustable','Make the grid bigger or smaller and the puzzle gets harder or easier \u2014 like difficulty adjustment.'],['Resets','Each time someone wins, a new puzzle begins \u2014 about every 10 minutes.']].forEach(([h,t],i)=>card(s,0.5+i*2.3,1.45,2.15,3.0,h,t,i%2?C.slate:C.orange));
s.addText('An analogy, not the mechanism: mining really searches for a block header whose hash meets a target.',{x:0.5,y:4.6,w:9,h:0.4,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Analogy from '+"the owner\u2019s course notes (CSE0469, after the 2nd edition)"+'. The 3rd edition does not use it; its own description is on the Mining slide: a header that takes enormous computation to form and little to verify.');

s=light(); title(s,'Why six confirmations','Each block on top makes reversal harder');
card(s,0.5,1.45,4.35,2.9,'Stacking blocks','Each block mined on top is one more confirmation. To take back a payment with two confirmations, three blocks would have to be mined.',C.slate);
card(s,5.15,1.45,4.35,2.9,'Back to the genesis block','Every block links back to block number 0. By convention, more than six confirmations is considered very hard to change.',C.orange);
note(s,BK+', section Spending the Transaction.');

s=light(); title(s,'Must you always wait?','Ten minutes is an average, and six confirmations is a convention');
card(s,0.5,1.45,2.85,3.0,'Unconfirmed','Propagated, but not yet in a block. Blocks arrive every 10 minutes on average \u2014 not on a timetable.',C.slate);
card(s,3.575,1.45,2.85,3.0,'Small payments','A merchant may accept a cheap item unconfirmed: the double-spend risk is low, like a coffee shop taking small card payments without a signature.',C.orange);
card(s,6.65,1.45,2.85,3.0,'Large payments','Selling something expensive for bitcoin risks a double-spend, so the merchant waits for confirmations.',C.slate);
note(s,'Unconfirmed and 10 minutes on average: Mastering Bitcoin 3rd edition, chapter 1. Small versus large payments and the coffee-shop comparison: chapter 12, Mining and Consensus. The \u201c10 minutes misconception\u201d framing is from '+"the owner\u2019s course notes (CSE0469, after the 2nd edition)"+'.');

s=light(); title(s,'Looking it up: block explorers','Useful \u2014 and not private');
card(s,0.5,1.45,4.35,2.9,'What they do','Search by address, transaction, block number or block hash \u2014 Blockstream Explorer, Mempool.Space, BlockCypher.',C.slate);
card(s,5.15,1.45,4.35,2.9,'Privacy warning','The operator may link your searches to your IP address and browser. Looking up your own transactions can reveal what you own.',C.orange);
note(s,BK+', Block Explorer Privacy Warning in section Bitcoin Overview.');

s=light(); title(s,'Our theme: a chain of spends is provenance','W3C PROV-O fits the transaction chain');
[['Entity','an output',0.5],['Activity','a transaction',3.575],['Agent','the key holder',6.65]].forEach(([h,t,x],i)=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:1.5,w:2.85,h:1.2,fill:{color:i===1?C.orange:C.card},line:{color:C.orange,width:1.5},rectRadius:0.1});
  s.addText([{text:h,options:{bold:true,breakLine:true,fontSize:18}},{text:t,options:{fontSize:13}}],{x,y:1.5,w:2.85,h:1.2,fontFace:H,color:i===1?C.white:C.dark,align:'center',valign:'middle',margin:0,isTextBox:true}); });
s.addText('An output wasDerivedFrom earlier outputs, wasGeneratedBy a transaction, and the transaction wasAssociatedWith the signer \u2014 PROV-O\u2019s own terms.',{x:0.5,y:3.0,w:9,h:0.9,fontFace:B,fontSize:15,color:C.ink,margin:0,isTextBox:true});
s.addText('A project idea: publish a transaction chain as PROV-O RDF and query its history with SPARQL.',{x:0.5,y:4.3,w:9,h:0.45,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'PROV-O: The PROV Ontology, W3C Recommendation, 30 April 2013. The mapping is a teaching suggestion within the term theme.');

s=light(); title(s,'Try it: a blockchain you can break','Anders Brownworth\u2019s interactive demo');
card(s,0.5,1.45,9,1.6,'andersbrownworth.com/blockchain','Change one character in an earlier block and watch every later block\u2019s hash go invalid \u2014 the chain of hashes this chapter describes, made visible.',C.orange);
note(s,'Blockchain Demo by Anders Brownworth, linked from '+"the owner\u2019s course notes (CSE0469, after the 2nd edition)"+'; page verified reachable on 2026-09-25.');

s=light(); title(s,'Discussion','Assess what you got so far');
[['Noticeable issues','What stood out, and what surprised you?'],['Interesting details','What is the most interesting point? Is Bitcoin inspiring?'],['Unclarified issues','Which points need further explanation? Pick one critical issue and explain it.']].forEach(([h,t],i)=>card(s,0.5+i*3.05,1.45,2.85,2.9,h,t,i===1?C.orange:C.slate));
note(s,'Discussion prompts from '+"the owner\u2019s course notes (CSE0469, after the 2nd edition)"+', lightly edited.');

s=light(); title(s,'Check yourself','Answer before you open the interactive page');
['Where is the transaction fee written in a transaction?','Paying 5 from a 20 input, what is the change?','When does a transaction join the blockchain?','How likely is a 10% attacker to reverse six confirmations?','Which PROV-O term fits a Bitcoin transaction?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.orange},line:{color:C.orange}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: nowhere - it is inputs minus outputs; 15; when a miner includes it in a block that full nodes validate; about 0.0002428; an activity.');

s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter\u2019s research record');
const src=['Antonopoulos, A. M., Harding, D. A. (2023). Mastering Bitcoin, 3rd ed., ch. 2. O\u2019Reilly. CC BY-SA 4.0. github.com/bitcoinbook/bitcoinbook','Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System, section 11. bitcoin.org/bitcoin.pdf','Bitcoin Core (2026). Releases. bitcoincore.org/en/releases','W3C (2013). PROV-O: The PROV Ontology. W3C Recommendation. w3.org/TR/prov-o','Antonopoulos, A. M., Harding, D. A. (2023). Mastering Bitcoin, 3rd ed., ch. 12, Mining and Consensus','Altunel, Y. (2021). Course notes, chapter 2, after Mastering Bitcoin 2nd ed. \u2014 checked against the 3rd edition before use','Brownworth, A. Blockchain Demo. andersbrownworth.com/blockchain'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.3,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:5,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0; this deck is shared under the same licence.',{x:0.5,y:5.0,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch02/rdodi/sen0401_ch02_research_v1_0_0.ttl.');

s=dark(); s.addText('Next week: Chapter 3 \u2014 Bitcoin Core',{x:0.6,y:1.7,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 2 page, and change the attacker\u2019s hash power in its playground.',{x:0.6,y:2.65,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.orange,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D1DA',margin:0,isTextBox:true});
note(s,'Chapter 3 of the 3rd edition is Bitcoin Core.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
