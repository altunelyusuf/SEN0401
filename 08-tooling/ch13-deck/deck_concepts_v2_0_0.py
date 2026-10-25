"""The key concepts of chapter 13 for the deck 2.0.0 (Bitcoin Security): the 25 distinct primary-source concepts of the chapter research (03-materials/ch13/rdodi/sen0401_ch13_research_v1_0_2.ttl,
de-duplicated by normalised label as the deck standard check does), each with the part of the chapter it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line
meaning and analogy of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept, its meaning, then 'Think of ...'. The parts and groups are those of the chapter
corpus (sen0401_ch13_corpus_v1_0_2.py). NEW file; nothing earlier is edited."""
__version__ = "2.0.0"

# level 1: divider subtitle (carries the meaning and the analogy of the part)
L1 = {
    "SecurityModel": "A node trusts only what it can check itself, like a cashier who tests every note.",
    "ProtectingKeys": "Keys are kept where thieves cannot reach, like cash in a safe and not in a pocket.",
    "KeepingAccess": "Access survives loss through a backup, like a spare key in a drawer.",
    "SharingControl": "Control is shared among keys or pieces, like a vault that needs two keyholders.",
    "CustodyHistory": "Handing coins to someone else is trust, like leaving cash with a stranger.",
    "Survivability": "Funds should outlive their owner, like a will with a waiting period.",
}

# level 2: (pill, meaning, analogy)   pill at most 4 words and one line wide
L2 = {
    "TransactionsPublishable": ("Payment secrecy", "A signed payment can be published because it never contains the key.", "a cheque that shows the signature but never the pen"),
    "TransportEncryption": ("Encrypted peers", "Nodes talk in an encrypted language by default; old nodes fall back.", "two people who switch to a private language"),
    "RootOfTrust": ("Root of trust", "One typed-in block is the start of all checking.", "the founder at the top of a family tree"),
    "VerifyingTheSoftware": ("Software checks", "A hash proves the download is the listed file; a signature says who listed it.", "a seal on a medicine box"),
    "ColdStorage": ("Cold storage", "Keys stay on a machine that is never online; only the signed file travels.", "a manager who signs cheques in another building"),
    "WalletEncryption": ("Wallet lock", "A passphrase locks the keys but not the balance.", "a locked drawer in a shop window"),
    "SigningDevices": ("Signing devices", "A small device holds the keys and signs, and waits longer after each wrong PIN.", "a safe that empties itself after too many tries"),
    "PaperAndMemory": ("Paper, memory", "Paper wallets are obsolete; a secret made of a few words is quickly guessed.", "a password written on a sticky note"),
    "SeedWords": ("Seed words", "Twelve words and a checksum stand for all the keys of a wallet.", "a recipe card from which the same dish is cooked again"),
    "WalletBackups": ("Wallet backups", "A backup restores only what it knew when it was made.", "a spare key cut before the locksmith adds new locks"),
    "Multisig": ("Several keys", "Two of three keys must sign, so one lost or stolen key is not fatal.", "a safe deposit box that needs two keyholders"),
    "SharingASecret": ("Shared secret", "A secret is cut into shares; enough of them rebuild it, fewer reveal nothing.", "a map torn in three: two pieces show the spot"),
    "ExchangeFailures": ("Exchange failures", "When an exchange holds the keys, customers hold only a claim on it.", "leaving your cash with a shopkeeper who may close"),
    "PhysicalCoins": ("Physical coins", "A coin can hide a key under a seal that shows if it was opened.", "a tamper seal on a medicine bottle"),
    "Heirs": ("Heirs", "A timelock lets an heir spend only after a set wait.", "a will that takes effect after a waiting period"),
    "Limits": ("Limits of the runs", "Some safeguards could not be run here; the deck says which.", "a test drive that never left the car park"),
}

# key concepts: label of the research -> (branch, meaning, analogy)
K3 = {
    "Bitcoin Security": ("SecurityModel", "Keeping coins safe by keeping the keys safe, and by checking what you run.", "locking your front door and also checking who made the lock"),
    "Security Principles": ("SecurityModel", "Rules such as trusting as little as possible and checking what you can.", "the habits of a cashier who tests every note"),
    "Developing Bitcoin Systems Securely": ("SecurityModel", "Builders must assume attackers read the code and copy the data.", "building a shop on the assumption that burglars know the plan"),
    "The Root of Trust": ("SecurityModel", "The book's name for the one thing a system must simply believe.", "the founder at the top of a family tree"),
    "root of trust": ("SecurityModel", "Everything checked later is checked against this starting point.", "the zero mark on a ruler"),
    "decentralization": ("SecurityModel", "No single party can change or stop the system.", "a town square with no single owner"),
    "decentralized consensus": ("SecurityModel", "Thousands of nodes check the same rules and so agree on one history.", "a class where every pupil marks the same sum"),
    "genesis block": ("SecurityModel", "The first block, whose hash is typed into the software.", "the first page of a ledger, signed in advance"),
    "User Security Best Practices": ("ProtectingKeys", "The book's advice for people who hold keys.", "the safety rules printed on a ladder"),
    "best practices": ("ProtectingKeys", "Habits that experience shows to work, such as offline keys and tested backups.", "washing your hands before cooking"),
    "Physical Bitcoin Storage": ("ProtectingKeys", "Keeping the secret on paper, metal or a device that can be locked away.", "keeping a spare key in a bank box"),
    "Hardware Signing Devices": ("ProtectingKeys", "Small devices that hold the keys and sign inside.", "a safe that makes you wait longer after each wrong code"),
    "cold storage": ("ProtectingKeys", "Keys on a machine that is never connected to the network.", "cash in a safe at home, not in your pocket"),
    "paper backup": ("ProtectingKeys", "The seed written on paper; fine for a copy, poor for daily use.", "a recipe card kept in the kitchen drawer"),
    "Ensuring Your Access": ("KeepingAccess", "Planning so that you can still reach your coins after a loss.", "keeping a copy of your house key with a neighbour"),
    "backing up": ("KeepingAccess", "Saving what a wallet needs, and doing it again after changes.", "photocopying a document after each new page"),
    "recovery codes": ("KeepingAccess", "A short secret that rebuilds the keys, such as the seed words.", "the reset code printed in a new phone's box"),
    "seed": ("KeepingAccess", "The number from which every key of a wallet is derived.", "a single seed that grows into a whole orchard"),
    "Diversifying Risk": ("SharingControl", "Not putting all trust in one key, one place or one person.", "not keeping all your eggs in one basket"),
    "risk diversification": ("SharingControl", "Spreading loss and theft over several keys so that no single failure is fatal.", "splitting savings across several banks"),
    "Multisig and Governance": ("SharingControl", "Several keyholders, such as partners, agree before coins move.", "a board of directors that must vote before a payment"),
    "multisignature addresses": ("SharingControl", "Addresses that need m signatures out of n keys.", "a safe deposit box that needs two of three keyholders"),
    "hot wallet": ("CustodyHistory", "A wallet whose keys sit on an online machine.", "the cash in your pocket, handy but easy to lose"),
    "Survivability": ("Survivability", "Funds and access that outlive failure, loss or the death of the owner.", "a lifeboat that still floats after a leak"),
    "estate planning": ("Survivability", "Arranging in advance who can reach the coins after you, and when.", "writing a will that names the heir and the waiting time"),
}
