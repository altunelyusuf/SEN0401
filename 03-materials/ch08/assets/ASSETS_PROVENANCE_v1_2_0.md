# Chapter 8 page assets - provenance and licences (v1.2.0, addition to v1.0.0 and v1.1.0)

The chapter 8 interactive page (page 9.42, template 9.45.0) embeds these files, all of which the course made or already holds:

| item | on the page? | licence | why |
|---|---|---|---|
| sen0401_ch08_lib-1.0.0-py3-none-any.whl (SHA-256 recorded in 08-tooling/ch08-page/pywheels_v1_0_0.json and checked when the page is made) | yes, as hex in the page data, unpacked into the browser's Python at start | the course's own licence (CC BY 4.0, Yusuf Altunel) | it holds three modules copied unchanged from 08-tooling: sen0401_ch07_script_lib_v1_0_0.py, sen0401_ch08_sig_lib_v1_0_0.py, sen0401_ch08_claims_v1_0_0.py; standard library only (hashlib, hmac, struct); written by the course |
| ch08_schnorr.png, ch08_android.png, ch08_bitcoinlogo.png | yes, downscaled, as the pictures of the three stories | as recorded in ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (CC BY-SA 2.0 de, CC BY 3.0, public domain); every picture carries its credit on the page | the stories' own pictures; two are stand-ins and say so |
| the book's chapter 8 ontology (3e/01-ontologies/mastering_bitcoin_3e_ch08_v1_1_1.ttl at the pinned commit) | yes, as the page's "book" passages | the book's licence, CC BY-SA 4.0, as the course's register records | the page's agents search it |
| Bitcoin Core 31.1.0, libsecp256k1, the BIPs, the fetched sources | no | not redistributed | the 34 examples that read their saved copies or the record of Core's run are shown as recorded, not run |

**Open question for the owner:** the licence under which the deck's and the page's pictures of people and logos may be shown in a course that is published openly is recorded per picture (above); the Bitcoin logo and the Android robot are stand-ins, not the event pictured.

The page runs in the reader's browser under Pyodide 0.28.2 (CPython 3.13.2); the research ran Python 3.14.6. 45 of the chapter's 79 worked examples run in the browser and equal the recorded result; 34 read a saved file a browser does not have and are shown with their recorded output.
