"""SEN0401 chapter 13 (Bitcoin Security): the teaching paragraphs of the leaves of subject 2 (protecting keys: cold storage, wallet encryption, signing devices, paper and memory). One paragraph per leaf, one line, full sentences.
Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
B = {}

B["WatchOnlyCannotSign"] = (
 "Cold storage in the book means keys generated and kept offline, and the practical question is how an online computer can then receive and prepare payments without ever holding the keys (Antonopoulos and Harding, 2023). "
 "The answer is a watch-only wallet: our hot node imported only the public descriptors of the cold wallet, its wallet reported private keys disabled, walletprocesspsbt came back with complete false and no signature, and listdescriptors with private keys failed with -4 Can't get private descriptor string for watch-only wallets; the PSBT it built carried the key origin data that the signer needs (Bitcoin Core, 2026); (Bitcoin Core developers, 2018). "
 "A thief who owns the hot machine can therefore see the balance and the addresses, which is a privacy loss, but cannot move a satoshi. "
 "It is like a bank clerk who may read the account book and prepare a payment slip but has no signing pen.")

B["PsbtThroughColdNode"] = (
 "A partially signed bitcoin transaction is a container that travels between a machine that knows the coins and a machine that holds the keys, and BIP 174 names the roles of Creator, Updater, Signer and Finalizer (Chow, 2017). "
 "In the test the cold node had 0 blocks and 0 connections, took the unsigned PSBT of 528 characters, returned a signed one of 596 characters with the final witness, and the hot node finalized and broadcast it, giving 1 confirmation and 1.0 coin received; a second format, PSBT version 2, lets inputs and outputs be added after creation (Chow, 2021); (Bitcoin Core, 2026). "
 "The second node here stands in for an offline computer, but it ran on the same machine and the string passed through our script, so no true air gap or removable medium was involved, as the record states; and a real air gap is not absolute, since Wikipedia notes that viruses such as Stuxnet were designed to infect air-gapped systems through removable media (Wikipedia contributors, 2026). "
 "Wikipedia's article on cryptocurrency wallets describes cold storage as simply keeping the private keys out of reach of hackers (Wikipedia contributors, 2026). It is like a letter that is carried to a notary in another town: the notary needs the text and the seal, not the town's news.")

B["LockedWalletRefuses"] = (
 "Wallet encryption protects the keys on disk, and the simplest test is to lock a wallet and see what it refuses (Bitcoin Core, 2026). "
 "On the test node an encrypted and locked wallet still showed its balance of 1.0 coin, handed out addresses and listed its public descriptors, but sending and listing private descriptors both failed with error code -13, Please enter the wallet passphrase with walletpassphrase first, and unlocked_until read 0. "
 "The managing-wallets document warns that an unencrypted wallet is vulnerable if an attacker reaches the device where the wallet or its backups are stored, and that encryption may prevent that unauthorized access but also raises the risk of losing coins through a forgotten passphrase (Bitcoin Core, 2026). "
 "It is like a house with a front door that anybody may look at from the street and only the owner can open: the lock does not hide the house, it stops the entry.")

B["WrongPassphraseError"] = (
 "The second half of the encryption story is the cost of a lost passphrase, and the node is blunt about it (Bitcoin Core, 2026). "
 "A wrong passphrase gave error code -14, The wallet passphrase entered was incorrect; after walletpassphrasechange the old passphrase gave -14 too and the new one worked, and the document of Bitcoin Core states that there is no way to recover a passphrase. "
 "This is the same lesson as the book's story of backups lost with their own keys: the more carefully the secret is protected, the more carefully its protection key must be kept, and the safest practice is to test the recovery before the money depends on it (Antonopoulos and Harding, 2023). "
 "It is like a safe whose combination you changed and then forgot to write down anywhere: the safe is perfect, and so is your loss.")

B["UnlockTimeout"] = (
 "A wallet that must sign has to be unlocked, and walletpassphrase unlocks it for a limited time only (Bitcoin Core, 2026). "
 "In the test the unlock timeout was 3 seconds: unlocked_until was exactly 3 seconds ahead of the clock, a send inside that window worked, after 5 seconds unlocked_until was 0 and the send failed with -13 again, walletlock gave 0 at once, and the source caps the timeout at 100000000 seconds, about 3 years. "
 "A short timeout limits the time in which malware on the machine could use the open key, but it does not stop malware that waits until the user unlocks the wallet, so encryption is a layer and not a wall. "
 "It is like a door that you hold open with your foot while you carry the shopping in and which closes by itself behind you.")

B["CrypterParameters"] = (
 "Encryption in Bitcoin Core is old, simple and documented in the code: the master key of the wallet is encrypted with AES-256-CBC under a key of 32 bytes with a salt of 8 bytes and an IV of 16, derived from the passphrase by SHA-512 rounds (Bitcoin Core, 2026). "
 "The default number of rounds is 25000, which the source says was just under 0.1 seconds on a 1.86 GHz Pentium M, 12.2 times the 2048 rounds of PBKDF2 in BIP 39, and RFC 8018 explains that a modest number of iterations, say 1000, is no burden to the legitimate user but raises the cost of exhaustive search (Moriarty et al., 2017); (Palatinus et al., 2013). "
 "On a modern graphics card 25000 rounds are cheap to try, so the strength of the encryption is the strength of the passphrase, and a long random passphrase matters more than any parameter. "
 "It is like a padlock of good steel on a shed with a cardboard key hook: the steel is not the weak part.")

B["EncryptionMakesNewSeed"] = (
 "The most surprising rule of wallet encryption in Bitcoin Core is that it replaces the seed: the RPC answered wallet encrypted; The keypool has been flushed and a new HD seed was generated, and the source and the managing-wallets document both say that a new backup must be made at once (Bitcoin Core, 2026). "
 "In the run the 32 bytes of the old key were found in the wallet file before encryption and not after, and the file grew from 24,576 to 36,864 bytes, which is a single-run observation about one SQLite file and not a guarantee that no trace remains elsewhere on the disk. "
 "Any coins received by the new seed cannot be recovered from the older backups, and the book's advice that a wallet can be backed up like any file is true only for as long as the backup is made after the last change. "
 "It is like changing the lock on your house and finding that the spare key you gave the neighbour yesterday no longer opens anything.")

B["ExternalSignerSupport"] = (
 "The book expects that hardware signing devices may become the predominant way to store bitcoins, because they only hold keys and make signatures and have no general-purpose software to compromise (Antonopoulos and Harding, 2023). "
 "Bitcoin Core supports this directly: it can be started with -signer=<cmd> so that an external tool, the example being HWI, signs for a hardware device, and the option is in the help of 31.1; the Bitcoin Wiki adds that the private keys are generated by the device and never leave it (Bitcoin Core, 2026); (Bitcoin Core developers, 2026); (Bitcoin Wiki, 2026). "
 "BIP 388 explains why descriptors alone are not enough for such devices and defines wallet policies that the device registers, after which it can show the addresses on its own screen (Ingala, 2023). "
 "No device was available here, so the signer is read from documents and not run. "
 "It is like a bank's token that you carry: it knows how to sign but not how to browse, and that is the point.")

B["HardwareDoesNotCheckTheAddress"] = (
 "A hardware wallet protects the key and not the intention, and the Bitcoin Wiki says so plainly: malware on a personal computer could monitor for high-value transactions and swap out the recipient's address, so the person must read the address on the device's own screen (Bitcoin Wiki, 2026). "
 "The same page lists Trezor first among the commercial devices in chronological order, which makes it the oldest of the list, and BIP 388 gives devices the means to show receive and change addresses on the secure screen (Bitcoin Wiki, 2026); (Ingala, 2023). "
 "In our tamper test the swapped transaction was refused because the old signature no longer matched; had the swap happened before signing, the signature would have been valid and the node would have accepted it, so the screen of the device is the last place where the human can still see the difference (Bitcoin Core, 2026). "
 "It is like a cashier who counts the cash carefully but trusts the customer's note about whom to pay: the counting is safe, the note is not.")

B["TrezorPinWait"] = (
 "A signing device must survive being stolen, and the Trezor does it with a PIN whose waits double after each wrong entry, 1 second after the first, 2 after the second, 4 after the third, and a wipe after 16 failed attempts (Bitcoin Wiki, 2026). "
 "Adding the waits before the sixteenth attempt gives 1 + 2 + 4 + ... + 16384 = 32,767 seconds, 9.1 hours, so an attacker with the device and no other weakness can make only 16 guesses in a bit more than nine hours and then loses the secret, and a recovery seed written elsewhere restores the funds on a new device (Bitcoin Wiki, 2026). "
 "The rule makes the short PIN adequate because the guesser cannot run faster than the device allows, which is the opposite of the file on a disk that can be copied and attacked offline. "
 "It is like a vending machine that locks for longer after every wrong code and empties itself after the sixteenth.")

B["PaperWalletsAreObsolete"] = (
 "The book recommends keeping a seed on paper or etched on metal and calls it a paper backup, and that advice stands for a seed (Antonopoulos and Harding, 2023). "
 "The Bitcoin Wiki now calls the paper wallet, a single private key and its address printed together, an obsolete and unsafe method that was popular between 2011 and 2016, one reason being that printers often have a hard drive that keeps the file and the private key with it (Bitcoin Wiki, 2026). "
 "The distinction is between a printed single key that has to be swept in full when spent and a written seed that feeds a hierarchical deterministic wallet, and the chapter treats both under the one word paper. "
 "No paper, printer or steel plate was used in this chapter; the claim is from the pages only. "
 "It is like keeping the only copy of a banknote's serial number in a drawer, instead of a book of cheques that can be revoked one by one.")

B["BrainwalletCrackTime"] = (
 "A brainwallet derives keys from a phrase the owner remembers, and the Bitcoin Wiki says that common phrases, patterns, dates and substitutions can be tested with dictionary attacks and other offline guessing (Bitcoin Wiki, 2026). "
 "The arithmetic shows how small the space is: four words from a list of 2,048 give 2 to the power 44 possibilities, which a machine trying a trillion guesses per second, an assumed rate and not a measurement, exhausts in 17.6 seconds, while the 128 bits of a generated seed are 2 to the power 84 times more; BIP 38 answers the weakness of a human passphrase by using scrypt and salting to make each guess expensive (Caldwell and Voisine, 2012). "
 "The book itself asks users to use complex passwords, which is a hint at this danger, and a seed made by software is safer than a phrase made by a person. "
 "It is like a combination lock with four digits: the lock may be solid, but there are only ten thousand things to try.")
