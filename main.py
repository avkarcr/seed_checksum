from itertools import permutations
import hashlib

WORDLIST_FILE = "bip39_wordlist.txt"


def load_wordlist():
    with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
        return [w.strip() for w in f.readlines()]


def mnemonic_to_bits(mnemonic, wordlist):
    bits = ""
    for word in mnemonic:
        if word not in wordlist:
            raise ValueError(f"Word not in BIP39 list: {word}")
        idx = wordlist.index(word)
        bits += format(idx, "011b")
    return bits


def check_bip39_checksum(mnemonic):
    wordlist = load_wordlist()

    if len(mnemonic) != 12:
        raise ValueError("Only 12-word mnemonics supported")

    bits = mnemonic_to_bits(mnemonic, wordlist)

    entropy_bits = bits[:128]
    checksum_bits = bits[128:]

    entropy = int(entropy_bits, 2).to_bytes(16, byteorder="big")
    hash_bits = format(int(hashlib.sha256(entropy).hexdigest(), 16), "0256b")

    return checksum_bits == hash_bits[:4]

with open(".seed", "r", encoding="utf-8") as f:
    for line in f:
        words = line.strip().split()
        break

counter = 0
found = 0
for w in permutations(words):
    counter = counter + 1
    # print("Analysing phrase:", counter, " - found", found, end=" ")
    try:
        if check_bip39_checksum(w):
            found = found + 1
            print("✅ found: ", found)
            with open("found.txt", "a", encoding="utf-8") as f:
                f.write(" ".join(w) + "\n")
        else:
            print("❌")
    except Exception as e:
        print("Error:", e)
