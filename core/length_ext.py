"""Length-extension demonstrator using a toy Merkle–Damgård hash."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


BLOCK_SIZE = 64
MASK32 = 0xFFFFFFFF
IV = (0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210)


def _rotl(value: int, amount: int) -> int:
    amount &= 31
    return ((value << amount) | (value >> (32 - amount))) & MASK32


def _compress(state: Tuple[int, int, int, int], block: bytes) -> Tuple[int, int, int, int]:
    a, b, c, d = state
    words = [int.from_bytes(block[i : i + 4], "little") for i in range(0, BLOCK_SIZE, 4)]
    for index, word in enumerate(words):
        mix = _rotl(word ^ (a + index), (index % 16) + 1)
        a = (a + mix) & MASK32
        b = (b ^ a ^ _rotl(word, index % 5 + 1)) & MASK32
        c = (c + _rotl(b, (index % 7) + 2) + word) & MASK32
        d = (d ^ c ^ index) & MASK32
        # simple permutation similar to MD-style register rotation
        a, b, c, d = b, c, d, a
    return a, b, c, d


class SimpleMDHasher:
    """A minimal Merkle–Damgård hash exposing internal state control."""

    block_size = BLOCK_SIZE
    digest_size = 16

    def __init__(self, state: Tuple[int, int, int, int] | None = None, processed_bytes: int = 0):
        self._state = list(state or IV)
        self._processed = processed_bytes
        self._buffer = bytearray()

    def copy(self) -> "SimpleMDHasher":
        clone = SimpleMDHasher(tuple(self._state), self._processed)
        clone._buffer = self._buffer.copy()
        return clone

    @staticmethod
    def glue_padding(message_length: int) -> bytes:
        """Return Merkle–Damgård style padding for ``message_length`` bytes."""

        bit_length = (message_length * 8) & 0xFFFFFFFFFFFFFFFF
        padding = b"\x80"
        remainder = (message_length + 1) % BLOCK_SIZE
        pad_len = (BLOCK_SIZE - 8 - remainder) % BLOCK_SIZE
        padding += b"\x00" * pad_len
        padding += bit_length.to_bytes(8, "big")
        return padding

    def update(self, data: bytes) -> None:
        if not data:
            return
        self._buffer.extend(data)
        while len(self._buffer) >= BLOCK_SIZE:
            block = bytes(self._buffer[:BLOCK_SIZE])
            self._state = list(_compress(tuple(self._state), block))
            del self._buffer[:BLOCK_SIZE]
            self._processed += BLOCK_SIZE

    def _apply_padding(self) -> None:
        padding = self.glue_padding(self._processed + len(self._buffer))
        self.update(padding)

    def digest(self) -> bytes:
        clone = self.copy()
        clone._apply_padding()
        return clone._state_to_bytes()

    def hexdigest(self) -> str:
        return self.digest().hex()

    def _state_to_bytes(self) -> bytes:
        return b"".join(value.to_bytes(4, "little") for value in self._state)

    def state_from_digest(self, digest: bytes | str) -> None:
        """Overwrite the internal registers using a given digest value."""

        if isinstance(digest, str):
            digest_bytes = bytes.fromhex(digest)
        else:
            digest_bytes = digest
        if len(digest_bytes) != self.digest_size:
            raise ValueError("digest length mismatch for SimpleMDHasher")
        values = [int.from_bytes(digest_bytes[i : i + 4], "little") for i in range(0, self.digest_size, 4)]
        self._state = values
        # Reset buffers; the caller is responsible for updating processed length.
        self._buffer.clear()

    def set_processed_length(self, total_length: int) -> None:
        """Set the total number of bytes that have already been hashed."""

        if total_length < 0:
            raise ValueError("processed length cannot be negative")
        self._processed = total_length
        self._buffer.clear()


@dataclass
class LengthExtensionResult:
    forged_message: bytes
    forged_digest: str
    glue_padding: bytes
    key_length_guess: int


def compute_tag(key: bytes, message: bytes, *, hasher: SimpleMDHasher | None = None) -> str:
    """Compute the MAC style tag for ``key || message`` using ``SimpleMDHasher``."""

    hasher = hasher.copy() if hasher else SimpleMDHasher()
    hasher.update(key + message)
    return hasher.hexdigest()


def forge_length_extension(
    *,
    original_digest: str | bytes,
    original_message: bytes,
    append_message: bytes,
    key_length_guess: int,
    hasher: SimpleMDHasher | None = None,
) -> LengthExtensionResult:
    """Perform a length-extension forgery using the toy hash implementation."""

    if key_length_guess < 0:
        raise ValueError("key_length_guess must be non-negative")

    hasher = hasher.copy() if hasher else SimpleMDHasher()
    hasher.state_from_digest(original_digest)

    total_processed = key_length_guess + len(original_message)
    glue_padding = SimpleMDHasher.glue_padding(total_processed)
    hasher.set_processed_length(total_processed + len(glue_padding))
    hasher.update(append_message)
    forged_digest = hasher.hexdigest()
    forged_message = original_message + glue_padding + append_message

    return LengthExtensionResult(
        forged_message=forged_message,
        forged_digest=forged_digest,
        glue_padding=glue_padding,
        key_length_guess=key_length_guess,
    )


__all__ = [
    "SimpleMDHasher",
    "LengthExtensionResult",
    "compute_tag",
    "forge_length_extension",
]
