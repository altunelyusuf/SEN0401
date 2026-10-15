# Chapter 12 assets - provenance and licences (v1.0.0)

Every file was downloaded on 2026-10-15 with curl from Wikimedia Commons (upload.wikimedia.org original, 960 px rendition) or, for the fork-in-the-road photograph, from Flickr; Wikimedia rate-limited the host for hours during the work (HTTP 429 with a Retry-After of 600 s), so two pictures were fetched by a background loop that retried every 650 s. The author, licence and date were read from the Openverse index of Commons and Flickr (api.openverse.org) or from the file's EXIF on the same day. CC BY and CC BY-SA files keep their credit below and wherever the picture is shown.

| file | page | author | licence | date | used in story |
|---|---|---|---|---|---|
| photo_adam_back.jpg | https://commons.wikimedia.org/w/index.php?curid=139613004 (File:Adam Back 2014) | Joi Ito | CC BY 2.0 | 2014 | HashcashBeforeBitcoin (the inventor of Hashcash, the proof of work that Nakamoto cites) |
| photo_fork_in_the_road.jpg | https://www.flickr.com/photos/31246066@N04/5279568656 | Ian Sane | CC BY 2.0 | not stated on the page | ChainSplitOfMarch2013 (a fork in a road, an illustration of the split, not of the event) |
| photo_asic_miner.jpg | https://commons.wikimedia.org/w/index.php?curid=92021894 (File:Antminer ASIC Miner.jpeg) | Steve Rainwater from Irving, US | CC BY-SA 2.0 | 2017-09-14 (EXIF) | HalvingBlockWithRecordFees (an Antminer S9, a machine of the kind that mines blocks; not the machine that mined block 840,000) |
| photo_taproot_profile.jpg | https://commons.wikimedia.org/wiki/File:Starr-070404-6562-Leucaena_leucocephala-taproot_profile_in_roadcut-Keomoku_Rd-Lanai_(24258711924).jpg | Forest and Kim Starr | CC BY 3.0 | 2007-04-04 | TaprootThroughSpeedyTrial (the taproot of a tree in a road cut, a pun on the name, not an illustration of the soft fork) |

The only picture that shows a living person is the portrait of Adam Back (CC BY 2.0). No picture is a photograph of the event it stands next to.
