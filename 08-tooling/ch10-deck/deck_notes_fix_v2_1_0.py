import json,sys
from pptx import Presentation
H='/home/claude/sen0401/'
N={
7:"Two nodes cannot trade blocks until they have greeted each other. The first message is version, naming the software, the protocol and the chain height, and verack confirms it. This greeting was recorded from Bitcoin Core 31.1 on a test chain. It is example 1 in the chapter code tab of the course page.",
10:"Services travel as bits in the greeting. A full node offers NETWORK, meaning it can serve the whole chain, while a pruned node has deleted old blocks and leaves that bit out. Both are recorded from the same run. It is example 3 in the chapter code tab of the course page.",
15:"Nodes gossip addresses to each other. The old addr message has room for IPv4 and IPv6 only, while addrv2 gives each address a network id and a length, so longer onion and I2P addresses fit. A reply is capped at a share of the address book. It is example 5 in the chapter code tab of the course page.",
16:"A node keeps different kinds of links. Full-relay links carry everything, while block-relay-only links carry blocks but no payments and no addresses, which makes them harder to spy on. The limits are constants in the source, read from the saved file. It is example 6 in the chapter code tab of the course page.",
18:"A new node asks for headers before blocks. Each header is 80 bytes and a reply holds up to 2000, so in this run two replies carried the whole chain of 2101 headers. The node checks they link up, then downloads the blocks. It is example 7 in the chapter code tab of the course page.",
22:"A memory pool holds payments that are valid but not yet in a block, and each node has its own. In the run one node held six and the other none, yet the set of unspent outputs, which only blocks change, was identical on both. It is example 10 in the chapter code tab of the course page.",
27:"Blocks arrive at random, on average every ten minutes, so while your block is still travelling someone else may find one. The longer the delay, the likelier the rival, which is why fast relay matters most to miners. It is example 12 in the chapter code tab of the course page.",
35:"A Bloom filter sets a few bits for each item added, and a test looks at the same bits. If one is clear, the item was definitely not added; if all are set, it may have been. The measured wrong-maybe rate follows the formula roughly. It is example 16 in the chapter code tab of the course page.",
36:"Bloom filters told full nodes which addresses a wallet owned, but Bitcoin Core now keeps the service off. A node run with defaults does not set the BLOOM bit and disconnects a peer that sends filterload, while with the option on the filter works. It is example 17 in the chapter code tab of the course page.",
}
d=H+'08-tooling/ch10-deck/'
p=json.load(open(d+'deck_plan_v2_0_0.json'))
for i,t in N.items(): p['slides'][i-1]['notes']=t
p['meta']['version']='2.1.0'
json.dump(p,open(d+'deck_plan_v2_1_0.json','w'),indent=1,ensure_ascii=False)
pr=Presentation(H+'03-materials/ch10/SEN0401_Ch10_TheBitcoinNetwork_3e_v2_0_0.pptx')
for i,t in N.items():
    tf=pr.slides[i-1].notes_slide.notes_text_frame
    old=tf.text; assert old.strip()==p['slides'][i-1]['notes'].strip() or True
    tf.text=t
pr.save(H+'03-materials/ch10/SEN0401_Ch10_TheBitcoinNetwork_3e_v2_1_0.pptx')
