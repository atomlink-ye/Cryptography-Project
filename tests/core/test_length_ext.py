from core.length_ext import (
    SimpleMDHasher,
    compute_tag,
    forge_length_extension,
)


def test_length_extension_forgery_matches_real_digest():
    hasher = SimpleMDHasher()
    secret = b"hidden"
    original = b"amount=100"
    append = b"&admin=true"

    digest = compute_tag(secret, original, hasher=hasher)
    result = forge_length_extension(
        original_digest=digest,
        original_message=original,
        append_message=append,
        key_length_guess=len(secret),
        hasher=hasher,
    )

    real_digest = compute_tag(secret, result.forged_message, hasher=hasher)
    assert result.forged_digest == real_digest
    assert result.forged_message.startswith(original)
    assert result.key_length_guess == len(secret)


def test_glue_padding_alignment():
    message_length = 15
    padding = SimpleMDHasher.glue_padding(message_length)
    assert padding.startswith(b"\x80")
    assert (message_length + len(padding)) % SimpleMDHasher.block_size == 0
