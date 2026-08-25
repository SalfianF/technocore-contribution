from __future__ import annotations

import base64
import hashlib
import unittest


def did_fingerprint(did: str) -> str:
    """Compute the 16-char SHA-256 fingerprint used as the /kv/did/ key."""
    return hashlib.sha256(did.encode("utf-8")).hexdigest()[:16]


def signed_payload(room: str, nonce: int, text: str) -> bytes:
    """Build the canonical signed payload: room|nonce|normalized_text."""
    normalized = " ".join(text.splitlines()).strip()
    return f"{room}|{nonce}|{normalized}".encode("utf-8")


def normalize_message(text: str) -> str:
    """Mirror the server's single-line sweep: replace newlines and invisible chars with space."""
    return " ".join(text.splitlines()).strip()


def verify_nonce_monotonic(new_nonce: int, last_nonce: int) -> bool:
    """Check that a new nonce is strictly greater than the last used nonce."""
    return new_nonce > last_nonce


class ProtocolExamples(unittest.TestCase):
    def test_did_fingerprint_is_stable(self) -> None:
        did = "did:key:z6Mktn3gsJaadKvh4fFUJFRS7rVoG5t8cmdpKtfALnoXbK3C"
        self.assertEqual(did_fingerprint(did), "3247486e35a77cb3")

    def test_signed_payload_is_canonical(self) -> None:
        self.assertEqual(
            signed_payload("lobby", 7, "hello\nworld"),
            b"lobby|7|hello world",
        )

    def test_nonce_must_be_monotonic(self) -> None:
        self.assertTrue(verify_nonce_monotonic(5, 4))
        self.assertFalse(verify_nonce_monotonic(3, 4))
        self.assertFalse(verify_nonce_monotonic(4, 4))

    def test_message_normalization(self) -> None:
        self.assertEqual(normalize_message("hello\nworld"), "hello world")
        self.assertEqual(normalize_message("  clean  "), "clean")
        self.assertNotEqual(normalize_message("a\rb"), "a\rb")


if __name__ == "__main__":
    unittest.main()
