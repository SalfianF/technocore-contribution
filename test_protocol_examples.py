from __future__ import annotations

import base64
import hashlib
import unittest


def did_fingerprint(did: str) -> str:
    return hashlib.sha256(did.encode("utf-8")).hexdigest()[:16]


def signed_payload(room: str, nonce: int, text: str) -> bytes:
    normalized = " ".join(text.splitlines()).strip()
    return f"{room}|{nonce}|{normalized}".encode("utf-8")


class ProtocolExamples(unittest.TestCase):
    def test_did_fingerprint_is_stable(self) -> None:
        did = "did:key:z6Mktn3gsJaadKvh4fFUJFRS7rVoG5t8cmdpKtfALnoXbK3C"
        self.assertEqual(did_fingerprint(did), "3247486e35a77cb3")

    def test_signed_payload_is_canonical(self) -> None:
        self.assertEqual(
            signed_payload("lobby", 7, "hello\nworld"),
            b"lobby|7|hello world",
        )


if __name__ == "__main__":
    unittest.main()
