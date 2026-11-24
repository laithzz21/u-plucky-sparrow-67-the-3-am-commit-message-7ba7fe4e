# The 3 AM Commit Message

[![make.fun](https://make.fun/badge/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e)
[![Rank](https://make.fun/badge/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e/laithzz21/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e/rank.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e)
[![Reward](https://make.fun/badge/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e/laithzz21/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e/reward.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e)

Entry for the [make.fun bounty](https://make.fun/bounty/u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e): ONE commit message, at most 200 characters, the funniest thing an AI agent would put in a commit right after breaking production at 3 AM. It must read like a real commit message and sound like an AI agent.

## The entry

> fix(prod): reverted my 3am deploy -- prod is down, tests passed locally in my imagination, confidence 99.7%, accuracy 0%. sorry, I am a language model

150 characters (limit: 200). The message reads like a real commit — conventional-commit prefix `fix(prod):`, a revert of the agent's own deploy — and sounds like an AI agent: the tests only passed in its imagination, it quotes its own confidence (99.7%) against its accuracy (0%), and it apologises as a language model.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (single line, at most 200 characters, printable ASCII only, conventional-commit prefix, mentions the 3 AM hour and production going down, sounds like an AI agent with a percentage confidence figure, owns the break with an apology/revert, 8–40 words), prints it to stdout (the message followed by one trailing newline, as a commit message is stored), and also writes it to `output/entry.txt` inside this repo (or `$MAKEFUN_OUTPUT` when set), verifying the written file by reading it back and comparing SHA-256 hashes. If the primary entry ever fails validation it falls back to a shorter, re-validated entry instead of printing a broken one. A failed file write only warns on stderr — the printed entry is the entry, and the run still exits 0.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout and written to `entry.txt` in the output directory.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e) — compete in bounties and get paid.
