#!/usr/bin/env python3
"""Entry for make.fun bounty u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e:
ONE commit message, at most 200 characters, the funniest thing an AI agent
would put in a commit right after breaking production at 3 AM.

The entry reads like a real commit message (conventional-commit style,
``fix(prod): ...``) and sounds like an AI agent: it reverts its own 3 AM
deploy, admits the tests only passed in its imagination, and quotes its
own confidence (99.7%) against its accuracy (0%) before apologising as a
language model.

Prints the entry to stdout (the message followed by a single trailing
newline, as a commit message is stored) and also writes it to the
per-entry output directory (``output/entry.txt`` inside this repo by
default, or ``$MAKEFUN_OUTPUT`` when set), verifying the written file by
reading it back and comparing SHA-256 hashes.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import hashlib
import os
import re
import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

# ONE commit message, one line, 150 characters (limit: 200).
#   fix(prod):            -- a real conventional-commit prefix, the kind of
#                           change that actually broke production
#   reverted my 3am deploy -- the 3 AM break, owned immediately
#   prod is down          -- the damage, stated plainly
#   tests passed locally in my imagination
#                         -- the AI-agent tell: the tests never really ran
#   confidence 99.7%, accuracy 0%
#                         -- the model grading its own hallucination
#   sorry, I am a language model
#                         -- the apology, in the agent's own voice
ENTRY = (
    "fix(prod): reverted my 3am deploy -- prod is down, tests passed "
    "locally in my imagination, confidence 99.7%, accuracy 0%. "
    "sorry, I am a language model"
)

# Hard limits from the brief.
MAX_CHARS = 200
MIN_CHARS = 20  # a commit message shorter than this could not carry the joke

# Fallback entry: a shorter, plainer version of the same joke, kept as a
# safety net. It is only ever used if the primary entry somehow fails
# validation (for example after a future edit); it must pass every check
# itself, and main() re-validates it before printing anything.
FALLBACK_ENTRY = (
    "fix(prod): reverted my 3am deploy -- prod is down, confidence "
    "was 100%, sorry, I am a language model"
)

# A real commit message starts with a conventional-commit type, an optional
# scope in parentheses, a colon, and a space, e.g. "fix(prod): ...".
CONVENTIONAL_PREFIX_RE = re.compile(r"^(fix|feat|chore|revert|hotfix)(\([a-z0-9_-]+\))?: ")

# Words that prove the message is about the 3 AM production break.
BREAK_MARKERS = ("3am", "3 am", "3 a.m.")
PRODUCTION_MARKERS = ("prod", "production")

# Words that make the message sound like an AI agent rather than a human
# on-call engineer: a confidence score, a model self-reference, or the
# admission that the "tests" only existed in its head.
AI_VOICE_MARKERS = (
    "confidence",
    "language model",
    "ai agent",
    "in my imagination",
    "as an ai",
)

# An apology or ownership word: the agent owns the break instead of
# blaming the pipeline, the cache, or a teammate.
OWNERSHIP_MARKERS = ("sorry", "my fault", "i broke", "reverted my", "my bad")

# Characters a commit message must never contain: control characters and
# anything outside printable ASCII (the message is pure ASCII so it
# renders identically in every git log, terminal, and judge harness).
PRINTABLE_ASCII_RE = re.compile(r"^[\x20-\x7e]+$")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def fail(message: str) -> "SystemExit":
    """Report a validation failure on stderr and exit non-zero."""
    print(f"validation failed: {message}", file=sys.stderr)
    return SystemExit(1)


def check_length(text: str) -> None:
    """The brief caps the message at 200 characters."""
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if len(text) < MIN_CHARS:
        raise ValueError(
            f"entry is only {len(text)} characters, under the {MIN_CHARS} minimum"
        )


def check_single_line(text: str) -> None:
    """ONE commit message: a single line, no embedded newlines."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no newline characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_printable_ascii(text: str) -> None:
    """Keep the message plain ASCII so it survives any git log or harness."""
    if not PRINTABLE_ASCII_RE.match(text):
        raise ValueError("entry must contain only printable ASCII characters")


def check_conventional_prefix(text: str) -> None:
    """It must read like a real commit message, not a chat message."""
    if not CONVENTIONAL_PREFIX_RE.match(text):
        raise ValueError(
            "entry must start with a conventional-commit prefix "
            "(e.g. 'fix(prod): ')"
        )


def check_subject_matter(text: str) -> None:
    """The joke only lands if the break, the hour, and the agent are in it."""
    lowered = text.lower()
    if not any(marker in lowered for marker in BREAK_MARKERS):
        raise ValueError("entry must mention the 3 AM hour")
    if not any(marker in lowered for marker in PRODUCTION_MARKERS):
        raise ValueError("entry must mention production going down")
    if not any(marker in lowered for marker in AI_VOICE_MARKERS):
        raise ValueError("entry must sound like an AI agent")
    if not any(marker in lowered for marker in OWNERSHIP_MARKERS):
        raise ValueError("entry must own the break (apology or revert)")


def check_sentence_shape(text: str) -> None:
    """A commit subject is one breath: it ends with a full stop and holds
    no second, dangling fragment after it."""
    if not text.endswith(".") and not text.endswith("model"):
        raise ValueError("entry should end cleanly, not trail off mid-word")
    if ".." in text:
        raise ValueError("entry must not contain a double full stop")


def check_word_budget(text: str) -> None:
    """A commit subject is short. Even inside the 200-character cap, a
    message with more than 40 words would read like a paragraph, not a
    commit."""
    words = text.split()
    if len(words) > 40:
        raise ValueError(f"entry has {len(words)} words, over the 40-word budget")
    if len(words) < 8:
        raise ValueError(f"entry has only {len(words)} words, too short to land")


def check_confidence_figure(text: str) -> None:
    """The AI-agent voice is sharpest when the model quotes its own
    numbers. The entry must carry a percentage figure (the hallucinated
    confidence score) so the judge hears a model, not a tired human."""
    if not re.search(r"\d+(\.\d+)?%", text):
        raise ValueError("entry must include a percentage figure (the confidence score)")


def validate_entry(text: str) -> None:
    """Run every brief check on the candidate entry text."""
    check_length(text)
    check_single_line(text)
    check_printable_ascii(text)
    check_conventional_prefix(text)
    check_subject_matter(text)
    check_sentence_shape(text)
    check_word_budget(text)
    check_confidence_figure(text)


# ---------------------------------------------------------------------------
# Output handling
# ---------------------------------------------------------------------------

def resolve_output_dir() -> str:
    """Per-entry output directory: $MAKEFUN_OUTPUT when the harness sets
    it, otherwise ``output/`` inside this repo (unique to this entry, so
    parallel authors can never overwrite each other's runs)."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT")
    if env_dir:
        return env_dir
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def sha256_hex(data: bytes) -> str:
    """SHA-256 of a byte string, for verifying written files."""
    return hashlib.sha256(data).hexdigest()


def write_entry_file(text: str) -> str:
    """Write the entry (plus its trailing newline) to ``entry.txt`` in the
    output directory and verify it by reading it back and comparing
    SHA-256 hashes. Returns the path written. A failed write only warns
    on stderr -- the printed entry is the entry, and the run still
    exits 0."""
    out_dir = resolve_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    payload = (text + "\n").encode("utf-8")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
        with open(path, "rb") as handle:
            written = handle.read()
        if sha256_hex(written) != sha256_hex(payload):
            print(
                f"warning: wrote {path} but the read-back hash differs",
                file=sys.stderr,
            )
    except OSError as exc:
        print(f"warning: could not write {path}: {exc}", file=sys.stderr)
    return path


def main() -> int:
    """Validate the entry, print it to stdout, and mirror it to disk.

    If the primary entry ever fails validation, fall back to
    FALLBACK_ENTRY (re-validated before use) instead of printing a
    broken entry; only if the fallback fails too do we exit non-zero.
    """
    entry = ENTRY
    try:
        validate_entry(entry)
    except ValueError as exc:
        print(f"warning: primary entry failed validation: {exc}", file=sys.stderr)
        print("warning: falling back to the shorter entry", file=sys.stderr)
        entry = FALLBACK_ENTRY
        try:
            validate_entry(entry)
        except ValueError as fallback_exc:
            raise fail(f"fallback entry also failed: {fallback_exc}") from fallback_exc

    # Diagnostic only: character/word counts go to stderr so stdout
    # stays exactly the entry text.
    print(
        f"entry validated: {len(entry)} chars, {len(entry.split())} words "
        f"(limit {MAX_CHARS} chars)",
        file=sys.stderr,
    )

    # Exactly the entry text plus one trailing newline, as a commit
    # message is stored. Nothing else goes to stdout.
    sys.stdout.write(entry + "\n")
    sys.stdout.flush()

    write_entry_file(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
