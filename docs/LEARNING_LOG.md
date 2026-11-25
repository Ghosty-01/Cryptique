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
