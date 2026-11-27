# Learning Log

## Day 1: Project setup

- Built: project folder, git repo, Python venv, .gitignore, requirements.txt, SSH connection to GitHub, first push
- Why: a venv isolates dependencies from system Python; .gitignore keeps generated files and test secrets out of the repo; SSH uses a key pair so no secret travels over the network

### Confusing / went wrong
- "Author identity unknown": git stamps every commit with a name and email and won't guess them
- "not a git repository": I was running git outside the project folder; use pwd to check
- GH007 push rejected: GitHub blocks pushes that expose a private email. Fixed with the noreply address and `git commit --amend --reset-author`. Rewriting history is only safe before the commits are shared.

### Concepts learned
- What `python3 -m venv .venv` does
- SSH: private key stays on my machine, public key goes to GitHub
- Host fingerprint check on first connection protects against impersonation

### Next
- cipher module: passphrase -> key (KDF), then AES-GCM encrypt/decrypt




## Day 2: Key derivation (KDF)

- Built: `cryptique/kdf.py` with `generate_salt()` and `derive_key()` using scrypt
- Why: a passphrase is a weak secret, so it can't be used as an encryption key directly. A KDF turns it into a 256-bit key and makes every guess expensive for an attacker.

### Concepts learned
- **KDF:** I pay the cost once (about 0.22 s). An attacker pays it for every guess.
- **Salt:** random, stored openly next to the encrypted data. It makes keys unique per file, so cracking work and precomputed tables can't be reused. It is not secret, and it doesn't fix a weak or reused passphrase.
- **scrypt is memory-hard** (about 32 MB per guess), which blunts GPU attacks.
- **Experiment results:** same salt + same passphrase gives the same key. A different salt gives a different key. That's why the salt must be stored with the file.
- **Speed gap:** SHA-256 did about 1,206,695 guesses/sec versus scrypt at about 4.5/sec, roughly 268,000x slower for the attacker.

### Confusing / went wrong
- I thought the salt had to be secret. Wrong: the attacker can see it. The secret is the passphrase.
- I first thought we could "change the encryption" while an attacker was guessing. Wrong: theft is offline, so protection has to be built into the file in advance.
- Unsure where to put `__init__.py`: the repo folder holds project files, and the code goes in a `cryptique/` package folder inside it.
- SSH warning "REMOTE HOST IDENTIFICATION HAS CHANGED": the host key for that IP differed from the saved one. Verify the fingerprint on the real machine before removing the old entry with `ssh-keygen -R`.
- Learned that an SSH private key without a passphrase is usable by anyone who copies it. Can add one with `ssh-keygen -p`.

### Next
- AES-GCM encryption in the cipher module. Open question: why do we need both a salt and a nonce?





## Day 3: AES-GCM encryption (cipher module)

- Built: `cryptique/cipher.py` with `encrypt()`, `decrypt()`, `encrypt_file()` and `decrypt_file()`
- File format: `[salt 16 bytes][nonce 12 bytes][ciphertext + 16-byte tag]`, so every encrypted file adds 44 bytes of overhead

### Concepts learned
- **Salt vs nonce:** the salt feeds the KDF (before the key exists) and makes the key unique per file. The nonce feeds AES-GCM (after the key exists) and makes each encryption unique. Neither is secret. Reusing a nonce with the same key breaks GCM.
- **Authenticated encryption:** the tag is computed from the key, nonce and ciphertext. Any change to the data makes verification fail, and GCM returns nothing instead of garbage. This is why GCM beats plain AES-CBC.
- **Experiments:** round trip works. Wrong passphrase is rejected. A flipped bit in the salt, nonce, ciphertext or tag is rejected every time.
- Wrong passphrase and tampered data give the same error. GCM can't tell them apart, and the tool shouldn't pretend it can.
- Reading and writing files as raw bytes, because encrypted data isn't text.
- Use `getpass` for passphrases so they don't show on screen or land in shell history. Keep test secrets in /tmp, outside the repo.

### Confusing / went wrong
- I tried to explain tamper detection by saying the length or salt changed, but the length never changed. The real reason is that the tag is recomputed and no longer matches.
- Wasn't sure what "CLI" meant at first: it's a thin layer over the same functions, so the tool can be run from the terminal.

### Next
- Build the CLI: argparse subcommands, hidden passphrase prompt, friendly errors, pyproject.toml so `cryptique` works as a command
