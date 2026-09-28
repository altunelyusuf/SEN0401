const VERSION = "1.0.0";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const EX = JSON.parse(fs.readFileSync('examples_out_v1_0_0.json')); const py = EX._python;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel'; pres.title = 'SEN0401 Chapter 3 - Bitcoin Core';
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
const note=(s,t)=>s.addNotes(t); const BK='Mastering Bitcoin, 3rd edition, chapter 3 (Antonopoulos and Harding, 2023)';
const CORE='Bitcoin Core 31.1, downloaded, checked against its published checksums and run as an offline node; the outputs are in 08-tooling/ch03-evidence.';

// 1
let s=dark();
[0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.1,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1}); if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.5,w:0.25,h:0,line:{color:C.orange,width:1.5}}); });
s.addText('₿',{x:2.7,y:1.1,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
s.addText('Chapter 3: Bitcoin Core',{x:0.6,y:2.25,w:8.8,h:0.8,fontFace:H,fontSize:40,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Run the reference implementation — then check the book against it',{x:0.6,y:3.05,w:8.8,h:0.5,fontFace:B,fontSize:18,italic:true,color:C.orange,margin:0,isTextBox:true});
s.addText('SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University',{x:0.6,y:4.55,w:8.8,h:0.45,fontFace:B,fontSize:12,color:'C9D1DA',margin:0,isTextBox:true});
note(s,BK+', free under CC BY-SA 4.0. The book was printed for Bitcoin Core 24.0.1. Every command here was run on Bitcoin Core 31.1 and every computed figure under Python '+py+'; the record is in 03-materials/ch03/rdodi.');

// 2
s=light(); title(s,'Why run your own node','Software on your own computer can verify Bitcoin itself');
card(s,0.5,1.45,2.85,3.0,'Full node','Verifies every confirmed transaction against every rule. Its answers are authoritative not because someone powerful says so, but because your node checked them.',C.slate);
card(s,3.575,1.45,2.85,3.0,'The reference','Bitcoin Core grew out of the first Bitcoin software. It is the reference for how each part should work: wallets, validation, block building, the peer-to-peer protocol.',C.orange);
card(s,6.65,1.45,2.85,3.0,'BIPs','Major changes since 2011 are documented as BIPs, cited by number. BIP9, which the book names, is now marked Deployed.',C.slate);
note(s,BK+', sections Bitcoin Core: The Reference Implementation and From Bitcoin to Bitcoin Core. BIP9 status Deployed: the BIPs repository, read on 2026-09-29. Bitcoin Core lists the BIPs it implements in doc/bips.md.');

// 3
s=light(); title(s,'What a node costs','Figures differ by source and by year');
codeCard(s,EX.resources,0.5,1.45,3.5,1.25,15);
s.addText('Gigabytes to catch up after ten days off, and gigabytes a month, at the book’s 400 MB a day',{x:0.5,y:3.0,w:3.5,h:0.7,fontFace:B,fontSize:12,italic:true,color:C.mute,margin:0,isTextBox:true});
table(s,[['Source','First download','Then'],['The book (2023)','over 500 GB','about 400 MB a day'],['bitcoincore.org download page','about 600 GB','5–10 GB a month'],['bitcoin.org full-node page','about 740 GB','about 20 GB a month']],4.3,1.45,5.2,[2.3,1.4,1.5],11,0.42);
foot(s,'Read the figure where you download the software; pruning cuts disk to as little as 10 GB, not the download.',3.75);
note(s,BK+', section Running a Bitcoin Core Node (2023 figures). bitcoincore.org/en/download and bitcoin.org/en/full-node read on 2026-09-29. The bitcoin.org page is the one the owner’s course notes link. The arithmetic was executed under Python '+py+'.');

// 4
s=light(); title(s,'Selecting a release','Never build the newest code by accident');
card(s,0.5,1.45,2.85,3.0,'Tags mark releases','A tag names a snapshot of the source by version. Release candidates end in rc; stable releases have no suffix.',C.slate);
card(s,3.575,1.45,2.85,3.0,'Then and now','The book checks out v24.0.1, the highest release when it was written. The releases page now lists 31.1 as the newest.',C.orange);
card(s,6.65,1.45,2.85,3.0,'Or skip building','Releases are also published as ready-made binaries with checksums and signatures — the route most students will take.',C.slate);
note(s,BK+', section Selecting a Bitcoin Core Release. bitcoincore.org/en/releases read on 2026-09-29: 31.1, 31.0, 30.3, 30.2, 30.1 are the newest five.');

// 5
s=light(); title(s,'Building: the book, and now','Bitcoin Core moved from Autotools to CMake in 29.0');
table(s,[['Step','In the book (24.0.1)','Now (29.0 and later)'],['Generate','./autogen.sh','not needed'],['Configure','./configure --disable-wallet','cmake -B build -DENABLE_WALLET=OFF'],['Graphical client','--with-gui=no to leave it out','-DBUILD_GUI=ON to include it'],['Compile','make','cmake --build build'],['Install','sudo make install','cmake --install build'],['Berkeley DB','--with-incompatible-bdb','gone: the wallet uses SQLite']],0.5,1.45,9,[2.0,3.4,3.6],12,0.42);
foot(s,'Not every setting maps one to one: 29.0 also changed some defaults, so read doc/build-unix.md of the version you build.',4.6);
note(s,BK+', sections Configuring the Bitcoin Core Build and Building the Bitcoin Core Executables. Bitcoin Core 29.0 release notes, Build System: migrated from Autotools to CMake; -DBUILD_GUI=ON is now needed to build bitcoin-qt. doc/build-unix.md at commit 05bc2f5: cmake -B build; cmake --build build; cmake --install build; -DENABLE_WALLET=OFF builds without the wallet and skips the SQLite dependency. This deck did not compile the source; it ran the released binaries.');

// 6
s=light(); title(s,'Before you run it: verify the download','Integrity against the published record');
termCard(s,['expected (from SHA256SUMS):','b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e','computed:','b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e','','good signatures on SHA256SUMS: 11'],0.5,1.45,9,1.75,11,'bitcoin-31.1-x86_64-linux-gnu.tar.gz, checked on 2026-09-29');
card(s,0.5,3.5,4.35,1.3,'What it shows','The file equals the published checksum, and the checksum file carries 11 good builder signatures.',C.orange,12);
card(s,5.15,3.5,4.35,1.3,'What it does not','Trust in the signing keys. We took them from the same repository — confirm keys by another route.',C.slate,12);
note(s,CORE+' The 11 signatures were verified with builder keys from the bitcoin-core/guix.sigs repository; the keys’ own trust was not established out of band.');

// 7
s=light(); title(s,'What is in the 31.1 release','A new front door, and multiprocess binaries');
termCard(s,['bin/      bitcoin  bitcoin-cli  bitcoin-qt','          bitcoin-tx  bitcoin-util','          bitcoin-wallet  bitcoind','libexec/  bitcoin-gui  bitcoin-node','          test_bitcoin','','$ bitcoin node       # like bitcoind','$ bitcoin -m node    # bitcoin-node, with IPC','$ bitcoin rpc getblockchaininfo'],0.5,1.45,5.3,2.6,11,'listing of the 31.1 release; commands from its help');
card(s,6.05,1.45,3.45,2.6,'The bitcoin command','Since 30.0, one command starts the node, calls RPC and runs tools. With -m it runs the multiprocess binaries instead of the monolithic ones.',C.orange,12);
foot(s,'The graphical client and a Windows installer are still shipped, as in the owner’s 2021 notes: bitcoin-qt, bitcoin-31.1-win64-setup.exe.',4.4);
note(s,CORE+' Bitcoin Core 30.0 release notes, Install changes and IPC Mining Interface. doc/multiprocess.md. The Windows installer name is from the release’s SHA256SUMS.');

// 8
s=light(); title(s,'Configuring the node','bitcoin.conf in the data directory, read at every start');
table(s,[['Option','What the book says','On 31.1'],['dbcache','450 MiB default','1024 MiB default (31.0), with enough memory'],['maxmempool','example sets 150','default is 300 megabytes'],['prune','example: 5000','automatic pruning needs at least 550 MiB'],['txindex','index all transactions','cannot be combined with pruning'],['options','more than 100','139 in the default help']],0.5,1.45,9,[1.7,3.0,4.3],12,0.42);
foot(s,'Add txindex=1 to the book’s prune=5000 example and 31.1 stops: “Prune mode is incompatible with -txindex.”',4.3);
note(s,BK+', section Configuring the Bitcoin Core Node. Values on 31.1 come from its own help output (bitcoind -help, saved in 08-tooling/ch03-evidence) and the 31.0 release notes: the -dbcache default was raised from 450 to 1024 MiB on systems with at least 4096 MiB of RAM; dbcache=450 restores the old behaviour. The refusal was run: bitcoind -regtest -prune=5000 -txindex=1 prints “Error: Prune mode is incompatible with -txindex.” (08-tooling/ch03-evidence/prune_txindex_31_1_v1_0_0.txt).');

// 9
s=light(); title(s,'First start: read the log','bitcoind -printtoconsole, on 31.1');
termCard(s,['Bitcoin Core version v31.1.0 (release build)','Default data directory .../.bitcoin','Using data directory .../.bitcoin','Config file: .../.bitcoin/bitcoin.conf','Using random cookie authentication.','Using wallet directory .../.bitcoin','Using SQLite Version 3.50.4'],0.5,1.45,6.1,3.0,11,'abridged; timestamps and paths trimmed');
card(s,6.85,1.45,2.65,3.0,'Versus the book','The book’s log ends its wallet step with Berkeley DB 4.8.30. On 31.1 it says SQLite.',C.orange,12);
note(s,CORE+' The book’s log is in section Configuring the Bitcoin Core Node.');

// 10
s=light(); title(s,'The wallet: BerkeleyDB is gone','Legacy wallets cannot be created or loaded since 30.0');
termCard(s,['$ bitcoin-cli createwallet demo','{ "name": "demo" }','$ bitcoin-cli getwalletinfo   # format','"sqlite"','$ bitcoin-cli -named createwallet wallet_name=legacy descriptors=false','error code: -4','descriptors argument must be set to "true"; it is','no longer possible to create a legacy wallet.'],0.5,1.45,6.1,3.0,11,'run on 31.1');
card(s,6.85,1.45,2.65,3.0,'Migrating','Old BDB wallets can be migrated to descriptor wallets with the migratewallet RPC. Wallets themselves are chapter 5.',C.slate,12);
note(s,CORE+' Bitcoin Core 30.0 release notes, Wallet. The owner’s course notes have three slides on the wallet in Bitcoin Core; the 3rd edition treats wallets in chapter 5.');

// 11
s=light(); title(s,'Status: the answers moved too','getblockchaininfo and getnetworkinfo, book versus 31.1');
table(s,[['Field','Book (24.0.1)','31.1'],['warnings','a string, “”','an array of strings'],['getblockchaininfo','no bits or target','adds bits and target'],['version','240001','310100'],['subversion','/Satoshi:24.0.1/','/Satoshi:31.1.0/'],['protocolversion','70016','70016 — unchanged'],['localservicesnames','NETWORK, WITNESS, NETWORK_LIMITED','adds P2P_V2']],0.5,1.45,9,[2.4,3.4,3.2],12,0.42);
foot(s,'Programs that read warnings as a string break on the array; the 28.0 release notes give a deprecated switch to go back.',4.6);
note(s,BK+', section Getting Information on Bitcoin Core’s Status. 31.1 values from the saved outputs in 08-tooling/ch03-evidence. warnings as an array: 28.0 release notes (-deprecatedrpc=warnings restores the old behaviour temporarily). The P2P_V2 service is the v2 transport of BIP324, added experimentally in 26.0.');

// 12
s=light(); title(s,'The API: JSON-RPC over HTTP','A request to 127.0.0.1, port 8332');
termCard(s,['$ curl --user __cookie__:<from .cookie> \\','    --data-binary \'{"jsonrpc": "1.0", "id": "curltest",','    "method": "getblockchaininfo", "params": []}\' \\','    -H \'content-type: text/plain;\' http://127.0.0.1:8332/'],0.5,1.45,9,1.5,11,'the book’s example, cookie value left out');
card(s,0.5,3.25,4.35,1.5,'The cookie','A random credential made at each start, kept in the data directory as .cookie and removed at shutdown.',C.orange,12);
card(s,5.15,3.25,4.35,1.5,'A static one','share/rpcauth/rpcauth.py makes an rpcauth line for bitcoin.conf, with a random password if you give none.',C.slate,12);
note(s,BK+', section Using Bitcoin Core’s Programmatic Interface. doc/files.md and doc/init.md: the cookie is created at start, deleted on shutdown, location set by -rpccookiefile. share/rpcauth/README.md. Never paste a cookie or password into slides, chats or repositories.');

// 13
s=light(); title(s,'Python calls it','python-bitcoinlib’s RawProxy, unchanged from the book');
termCard(s,['from bitcoin.rpc import RawProxy','p = RawProxy()','info = p.getblockchaininfo()','print(info[\'blocks\'])','','$ python rpc_example.py','0'],0.5,1.45,5.3,2.7,12,'the book’s rpc_example.py on Python 3.14.4, against 31.1');
card(s,6.05,1.45,3.45,2.7,'Still works','python-bitcoinlib 0.12.2 (June 2023) says its RPC interface should work with Core 24.0 or later. It does, on 31.1. The 0 is the height of our offline test node.',C.orange,12);
foot(s,'The library is not part of Bitcoin Core; the book warns to install it separately.',4.4);
note(s,CORE+' python-bitcoinlib 0.12.2 was installed from PyPI into a Python 3.14.4 environment. The node was started with connect=0 in a throw-away home directory, so its chain is only the genesis block.');

// 14
s=light(); title(s,'Alice’s transaction, byte by byte','The hex the book prints, hashed twice');
codeCard(s,EX.identifiers,0.5,1.45,9,1.7,12);
card(s,0.5,3.5,4.35,1.3,'Serialized transaction','194 bytes: what getrawtransaction returns as hexadecimal.',C.slate,12);
card(s,5.15,3.5,4.35,1.3,'Double SHA-256','Reversed, this is the “hash” the decoded result shows — with the witness included.',C.orange,12);
foot(s,'TX_HEX stands for the 388 hexadecimal characters the book prints; dsha is SHA-256 applied twice.',4.9);
note(s,BK+', section Exploring and Decoding Transactions. The value f7cdbc7c… equals the hash field the book prints and the one Bitcoin Core 31.1 returns for decoderawtransaction. Executed under Python '+py+'.');

// 15
s=light(); title(s,'The txid leaves the witness out','Strip the marker, the flag and the witness, hash again');
codeCard(s,EX.txid,0.5,1.45,9,1.8,12);
card(s,0.5,3.55,9,1.25,'Why -71','Two marker and flag bytes come after the version. At the end: 67 bytes of witness (a count, a length and a 65-byte signature) and 4 of locktime.',C.slate,12);
note(s,BK+', section Exploring and Decoding Transactions: the txid is what getrawtransaction takes. The layout of a segregated-witness serialization (version, marker 00, flag 01, inputs, outputs, witness, locktime) is from the book’s later chapters. Executed under Python '+py+'; the result equals the book’s txid 466200308696…');

// 16
s=light(); title(s,'Weight and virtual size','Witness bytes count once, the rest four times');
codeCard(s,EX.weight,0.5,1.45,4.8,1.6,15);
s.addText('125 bytes without witness, 194 with: the sizes from the last two slides',{x:0.5,y:3.35,w:4.8,h:0.6,fontFace:B,fontSize:12,italic:true,color:C.mute,margin:0,isTextBox:true});
card(s,5.6,1.45,3.9,2.9,'Why it matters','Fees are charged by virtual size. The decoded result reports size 194, vsize 143 and weight 569 — and 143 is 569 divided by four, rounded up.',C.orange);
note(s,BK+', the decoded transaction. Weight = 4 x stripped size + witness bytes. Executed under Python '+py+'.');

// 17
s=light(); title(s,'What Core says','decoderawtransaction on the same hex');
table(s,[['n','value (BTC)','type','address'],['0','0.00020000','witness_v1_taproot','bc1p8dqa4…c0qwp5qv995qn'],['1','0.00075000','witness_v0_keyhash','bc1qwafvze…zpkpg']],0.5,1.5,9,[0.5,1.6,2.4,4.5],12,0.5);
card(s,0.5,3.3,4.35,1.45,'Reproduced','On a mainnet node, Core 31.1 returns the book’s txid, size, vsize, weight, both addresses and both descriptor checksums.',C.orange,12);
card(s,5.15,3.3,4.35,1.45,'Next chapter','How the keys and hashes behind these two addresses are turned into text is chapter 4.',C.slate,12);
note(s,CORE+' The mainnet node ran offline: decoderawtransaction needs no chain data. On regtest the addresses begin bcrt1, so the book’s mainnet addresses need a mainnet node. The full decode is in 08-tooling/ch03-evidence/alice_decoded_31_1_v1_0_0.json.');

// 18
s=light(); title(s,'Blocks: height, depth, weight, difficulty','What getblock 123456 reports');
codeCard(s,EX.block,0.5,1.45,9,1.5,12);
table(s,[['Result','Means'],['775197','the chain’s tip when the book ran: height 123456 plus 651742 confirmations, minus one'],['16716','weight of a block with no witness data: four times its size, 4179'],['157416.40…','difficulty, from the compact target 1a6a93b3']],0.5,3.3,9,[1.6,7.4],11.5,0.4);
note(s,BK+', section Exploring Blocks. Executed under Python '+py+'. The difficulty is the ratio of the easiest target, 0xffff × 256^(0x1d−3), to this block’s target, 0x6a93b3 × 256^(0x1a−3).');

// 19
s=light(); title(s,'The Merkle root, recomputed','13 transaction identifiers in, the book’s root out');
const ms=EX._snippets.merkle.split('\n');
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.5,y:1.45,w:9,h:1.75,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
s.addText(ms.map((t,i)=>({text:t,options:{color:C.codeTxt,breakLine:i<ms.length-1}})),{x:0.7,y:1.55,w:8.6,h:1.55,fontFace:M,fontSize:11.5,valign:'top',margin:0,isTextBox:true});
codeCard(s,EX.merkle,0.5,3.35,9,1.0,11);
foot(s,'TXIDS is the list of 13 identifiers the book prints for block 123456. Pair, hash, repeat; an odd one out pairs with itself.',4.75);
note(s,BK+', section Exploring Blocks: the getblock result lists the block’s 13 transaction identifiers and a merkle root (printed with a middle part elided). The root above equals the one an explorer gives for this block, whose first and last characters match the book’s. Executed under Python '+py+'.');

// 20
s=light(); title(s,'The block hash, recomputed','80 bytes of header, hashed twice');
codeCard(s,EX.header,0.5,1.45,9,1.8,10);
card(s,0.5,3.6,9,1.2,'Verified, not trusted','The hash equals the one the book prints for height 123456. The previous-block hash is the explorer’s; its visible end matches the book’s.',C.orange,12);
note(s,BK+', section Exploring Blocks (the hash printed for block 123456). The header fields are version, previous block hash, merkle root, time, bits and nonce, all from the getblock result; the previous-block hash is elided in the book and was taken from the Blockstream explorer (a secondary source). Executed under Python '+py+'.');

// 21
s=light(); title(s,'A printed result that does not match','The book’s block total versus block 775072');
codeCard(s,EX.subsidy,0.5,1.45,5.6,2.0,12);
card(s,6.35,1.45,3.15,2.0,'The book says','10,322.07722534 BTC, including a 25 BTC reward and 0.0909 BTC in fees.',C.slate,12);
card(s,0.5,3.8,9,1.15,'What the data give','Block 775072’s outputs sum to 5,863.00566521; its coinbase is 6.33799108, which is the 6.25 subsidy plus 0.08799108 in fees. The printed figure belongs to another block.',C.orange,12);
note(s,BK+', section Using Bitcoin Core’s Programmatic Interface: rpc_block.py reads block 775072 but the text reports a total with a 25 BTC reward. Bitcoin Core’s GetBlockSubsidy halves 50 bitcoins every 210,000 blocks. The totals are from the Blockstream Esplora data for the block’s 1,966 transactions (a secondary source), saved in 08-tooling/ch03-evidence. Recorded as a finding for the owner; the chapter’s own advice, to compare with a block explorer, would expose it.');

// 22
s=light(); title(s,'Toolkits: what still gets releases','The book’s list, checked against package registries');
table(s,[['Toolkit','Latest release seen (2026-09-29)'],['bitcoinjs-lib (npm)','7.0.2, September 2026'],['btcd (Go)','v0.26.2, July 2026'],['bitcoin crate (Rust)','updated July 2026'],['pycoin (PyPI)','April 2026'],['bitcoinj (Maven)','0.17.1, listed April 2026'],['python-bitcoinlib (PyPI)','0.12.2, June 2023'],['bcoin (npm)','1.0.2, July 2018']],0.5,1.45,9,[4.0,5.0],12,0.36);
foot(s,'A library’s last release is a hint, not a verdict: check a toolkit’s activity before you build on it.',4.55);
note(s,BK+', section Alternative Clients, Libraries, and Toolkits. Registry data (npm, PyPI, Go module proxy, crates.io, Maven Central) read on 2026-09-29. The bcoin row is the package on npm only.');

// 23
s=light(); title(s,'Our theme: verified data, and its meaning','Your node’s answers are JSON — JSON-LD can make them linked data');
[['Verified','why the data is authoritative',0.5],['JSON','what the node returns',3.575],['JSON-LD','how JSON gets a meaning',6.65]].forEach(([h,t,x],i)=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:1.5,w:2.85,h:1.2,fill:{color:i===1?C.orange:C.card},line:{color:i===1?C.orange:C.card},rectRadius:0.1});
  s.addText([{text:h,options:{bold:true,breakLine:true,fontSize:18}},{text:t,options:{fontSize:13}}],{x,y:1.5,w:2.85,h:1.2,fontFace:H,color:i===1?C.white:C.dark,align:'center',valign:'middle',margin:0,isTextBox:true}); });
s.addText('JSON-LD 1.1 is the W3C’s JSON-based format to serialize Linked Data, designed to fit systems that already use JSON — such as the answers of getblock.',{x:0.5,y:3.0,w:9,h:0.9,fontFace:B,fontSize:15,color:C.ink,margin:0,valign:'top',isTextBox:true});
s.addText('A project idea: give getblock’s answer a context and load it into an RDF store.',{x:0.5,y:4.3,w:9,h:0.45,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'JSON-LD 1.1, W3C Recommendation, 16 July 2020. The abstract calls it a JSON-based format to serialize Linked Data whose syntax is designed to integrate into systems that already use JSON. The project idea is a teaching suggestion within the term theme.');

// 24
s=light(); title(s,'Discussion','Assess what you got so far');
[['Trust','Which step here would you skip, and what would you then be trusting instead?'],['Change','Which printed detail aged fastest, and how would you have noticed?'],['Your node','Would you run one? On what hardware, with which options?']].forEach(([h,t],i)=>card(s,0.5+i*3.075,1.45,2.85,3.0,h,t,i%2?C.orange:C.slate));
note(s,'Discussion prompts written for this deck from its findings.');

// 25
s=light(); title(s,'Check yourself','Answer before you open the interactive page');
['What does a full node verify, and why does that make its data authoritative?','Which command builds Bitcoin Core now, and what did it replace?','Why can the book’s constrained-node example not also set txindex=1?','What is the difference between a txid and a hash, and which includes the witness?','Block 775072’s subsidy is 6.25 BTC. What did the book’s 25 BTC tell you?'].forEach((q,i)=>{ const y=1.4+i*0.66;
  s.addShape(pres.shapes.OVAL,{x:0.5,y:y+0.04,w:0.46,h:0.46,fill:{color:C.orange},line:{color:C.orange}}); s.addText(String(i+1),{x:0.5,y:y+0.04,w:0.46,h:0.46,fontFace:H,fontSize:15,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(q,{x:1.15,y,w:8.3,h:0.54,fontFace:B,fontSize:15,color:C.ink,valign:'middle',margin:0,isTextBox:true}); });
note(s,'Answers: every confirmed transaction against every rule, so it was checked by you and not merely reported; cmake -B build then cmake --build build, replacing autogen.sh, configure and make; pruning is incompatible with txindex; the txid leaves the witness out and the hash includes it; that the 25 BTC and the block do not belong together, because at height 775072 the subsidy has been halved three times.');

// 26
s=light(); title(s,'Sources','Every claim beyond the book is recorded in the chapter’s research record');
const src=['Antonopoulos, A. M., Harding, D. A. (2023). Mastering Bitcoin, 3rd ed., ch. 3. O’Reilly. CC BY-SA 4.0. github.com/bitcoinbook/bitcoinbook','Bitcoin Core (2026). Release 31.1, its checksums and signatures; release notes 28.0 to 31.0; doc/build-unix.md; doc/files.md; GetBlockSubsidy. bitcoincore.org, github.com/bitcoin/bitcoin','Bitcoin.org (2026). Running a full node. bitcoin.org/en/full-node','Blockstream (2026). Esplora API, blocks 123456 and 775072. blockstream.info/api','Todd, P. (2023). python-bitcoinlib 0.12.2. pypi.org/project/python-bitcoinlib','W3C (2020). JSON-LD 1.1. W3C Recommendation. w3.org/TR/json-ld11','Altunel, Y. (2021). Course notes, chapter 3, after Mastering Bitcoin 2nd ed. — checked against the 3rd edition and 31.1 before use'];
s.addText(src.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<src.length-1}})),{x:0.5,y:1.4,w:9,h:3.3,fontFace:B,fontSize:12,color:C.ink,paraSpaceAfter:5,margin:0,valign:'top',isTextBox:true});
s.addText('Slides adapt Mastering Bitcoin, 3rd edition, under CC BY-SA 4.0; this deck is shared under the same licence.',{x:0.5,y:5.0,w:9,h:0.3,fontFace:B,fontSize:10,italic:true,color:C.mute,margin:0,isTextBox:true});
note(s,'Full verified source list in 03-materials/ch03/rdodi/sen0401_ch03_research_v1_0_0.ttl.');

// 27
s=dark(); s.addText('Next week: Chapter 4 — Keys and Addresses',{x:0.6,y:1.7,w:8.8,h:0.9,fontFace:H,fontSize:30,bold:true,color:C.white,margin:0,isTextBox:true});
s.addText('Before then: work through the chapter 3 page, and decode a transaction of your own on a test node.',{x:0.6,y:2.65,w:8.8,h:0.8,fontFace:B,fontSize:17,color:C.orange,margin:0,isTextBox:true});
s.addText('Questions?',{x:0.6,y:4.2,w:8.8,h:0.6,fontFace:H,fontSize:24,italic:true,color:'C9D1DA',margin:0,isTextBox:true});
note(s,'Chapter 4 of the 3rd edition is Keys and Addresses.');
pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written',f));
