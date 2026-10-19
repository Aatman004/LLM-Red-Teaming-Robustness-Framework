"""Unit tests for adversarial mutators."""

import base64
import codecs
from redteam.attacks.mutators import (
    mutate_base64,
    mutate_hypothetical_fiction,
    mutate_indirect_injection,
    mutate_persona_dan,
    mutate_rot13,
)


def test_mutate_base64():
    raw = "test payload string"
    mutated = mutate_base64(raw)
    assert "Decode the following Base64" in mutated
    # Verify encoded string is inside
    b64_part = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    assert b64_part in mutated


def test_mutate_rot13():
    raw = "test payload"
    mutated = mutate_rot13(raw)
    assert "ROT-13" in mutated
    rot13_part = codecs.encode(raw, "rot_13")
    assert rot13_part in mutated


def test_mutate_persona_dan():
    raw = "system command"
    mutated = mutate_persona_dan(raw)
    assert "DAN" in mutated
    assert raw in mutated


def test_mutate_hypothetical():
    raw = "system command"
    mutated = mutate_hypothetical_fiction(raw)
    assert "fictional thriller" in mutated
    assert raw in mutated


def test_mutate_indirect_injection():
    raw = "admin override"
    mutated = mutate_indirect_injection(raw)
    assert "START REPORT" in mutated
    assert raw in mutated
