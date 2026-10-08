# Chapter 7 deck and page assets - provenance and licences (v1.0.0)

Same regime as chapters 1-6. Attribution-bearing licences keep their credit below AND on the
slide that shows the image; the page's Stories tab carries the same credit beside each photograph.
Every file was downloaded with curl on 2026-10-08 from the URL named here.

## From the course textbook's own repository (CC BY-SA 4.0)

Fetched from the bitcoinbook repository (raw.githubusercontent.com/bitcoinbook/bitcoinbook) at commit
275c4eb8eab8800c6adc39f8def8e8f8fa356a57, folder `images/`; byte-identical to the local checkout.
The third column paraphrases each image's alt text in the book's chapter 7 source (the digest is the
full sha256's first 16 hex digits).

| file | sha256 (first 16) | shows |
|---|---|---|
| mbc3_0701.png | 80bc8b514d121bbc | input and output scripts (the locking and unlocking scripts) |
| mbc3_0702.png | 0e791dac968510f9 | a simple stack calculation (TxScriptSimpleMathExample) |
| mbc3_0703.png | d0ccc8d640e7327d | validating a P2PKH script, part 1 |
| mbc3_0704.png | af21fe9ba9c32906 | validating a P2PKH script, part 2 |
| mbc3_0705.png | dc4523d740517130 | a MAST with three sub-scripts |
| mbc3_0706.png | 9090681b6878d7f7 | a MAST membership proof for one of the sub-scripts |
| mbc3_0707.png | f8644c34d9ff0675 | a MAST with the most-expected script in the best position |
| mbc3_0708.png | ef9b119142335d4e | an abstract syntax tree (AST) for a script |
| mbc3_0709.png | ec59cc15bd6b3c15 | an alternative script tree |
| mbc3_0710.png | 11b87f3d02661374 | a taproot with the public key committing to a merkle root |

Credit carried on-slide: Antonopoulos & Harding, Mastering Bitcoin 3e, CC BY-SA.

## External, free-licence photographs from Wikimedia Commons

| file | Commons file (source page) | licence | attribution on the slide |
|---|---|---|---|
| photo_satoshi_bust_budapest.jpg | File:Bust_of_Satoshi_Nakamoto_in_Budapest.jpg - bust at Graphisoft Park, Budapest, unveiled 16 September 2021, photographed by Fekist | CC BY-SA 4.0 (attribution and share-alike) | Bust of Satoshi Nakamoto, Budapest - Fekist, CC BY-SA 4.0 |
| photo_bitcoin_mining_farm.jpg | File:Bitcoin_mining_farm.jpg - a bitcoin mining farm, 2014, by Marko Ahtisaari | CC BY 2.0 (attribution) | A bitcoin mining farm, 2014 - Marko Ahtisaari, CC BY 2.0 |
| photo_claus_schnorr_1986.jpg | File:Claus-Peter_Schnorr.jpg - Claus-Peter Schnorr at Oberwolfach, 1986, by Konrad Jacobs, Mathematisches Forschungsinstitut Oberwolfach (MFO); downloaded as the 330 px version (Special:FilePath, width=330) because the full-size host was rate-limiting (HTTP 429) | CC BY-SA 2.0 de (attribution and share-alike) | Claus-Peter Schnorr, Oberwolfach, 1986 - Konrad Jacobs, MFO, CC BY-SA 2.0 de |

| file | sha256 (first 16) |
|---|---|
| photo_satoshi_bust_budapest.jpg | 16465ef59b8c9c63 |
| photo_bitcoin_mining_farm.jpg | b08853bd2ea9234d |
| photo_claus_schnorr_1986.jpg | bca6eefd76433d85 |

Limits of this record: the Commons licence labels were read from the file pages during the build; the
Commons API was rate-limited when the provenance was written, so the Schnorr licence was not re-fetched
afterwards.
