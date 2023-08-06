"""Basic cryptographic functions to aid in key management for the user.
"""
from random import choice
from hashlib import sha256
from os import environ
from random import Random
from sys import maxsize
import string
import struct
import nacl.bindings

from aries_cloudagent.wallet.crypto import (create_keypair, seed_to_did, bytes_to_b58, validate_seed,
                                            sign_message, bytes_to_b64, b64_to_bytes, verify_signed_message,
                                            random_seed, b58_to_bytes)

from datacustodian.settings import app_specs


def anon_crypt_message(message: bytes, pk: bytes) -> bytes:
    """Apply anon_crypt to a binary message.

    Args:
        message: The message to encrypt
        pk: The verkey to encrypt the message for

    Returns:
        The anon encrypted message
    """
    _pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(pk)
    enc_message = nacl.bindings.crypto_box_seal(message, _pk)
    return enc_message


def anon_decrypt_message(enc_message: bytes, pk: bytes, sk: bytes) -> bytes:
    """Apply anon_decrypt to a binary message.

    Args:
        enc_message: The encrypted message
        pk: public key that the message was encrypted for.
        sk: private key that the message was encrypted for.

    Returns:
        The decrypted message
    """
    _pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(pk)
    _sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(sk)

    message = nacl.bindings.crypto_box_seal_open(enc_message, _pk, _sk)
    return message


def create_did(seed: bytes):
    """Creates a DID and verkey from the given seed.

    Args:
        seed (bytes): the secret seed to use in generating the verkey.

    Returns:
        tuple: `(did, verkey)`.
    """
    seed = validate_seed(seed)
    verkey, _ = create_keypair(seed)
    did = bytes_to_b58(verkey[:16])
    return did, bytes_to_b58(verkey)


def keypath_to_salt(keypath: str) -> bytes:
    """Converts a keypath into the salt to use in a derivation algorithm.

    Args:
         keypath (str): the string keypath to convert to salt.
    """
    try:
        parts = map(int, keypath.split('/')[1:])
        seed = sum(p*10**i for i, p in enumerate(parts))
    except:
        seed = 0
    r = Random(seed).randrange(maxsize)
    return sha256(str(r).encode("ascii")).digest()

def get_master_seed(agent) -> bytes:
    """Retrieves the master encryption key seed from the application specifications and environment variables.

    Args:
        agent (str): name of the agent to retrieve a master seed for.
    """
    envar = app_specs["dlt"]["agents"][agent]["wallet"]["seed"]
    envseed = environ[envar]
    return validate_seed(f"{envseed:0>32}")

def verify_signature(signature, verkey):
    """Verifies a signature cryptographically.

    Args:
        agent (str): name of the agent whose master key should be used.
        signature (str): base-64 encoded signature that should be verified.
        verkey (str): public key to use in verifying the signature.
    """
    s, v = b64_to_bytes(signature), b64_to_bytes(verkey)
    return verify_signed_message(s, v)

def sign(message, sk=None, agent=None, seed=None, context=None, keypath=None):
    """Signs the specified message using a derived key based on the master key of `agent`.

    Args:
        message (str): text to sign using the agent's derived key.
        sk (bytes): secret key to use for signing. If not specified, then
            `agent`, `context` and `keypath` should be specified so that the key
            can get derived dynamically.
        agent (str): name of the agent whose master key should be used.
        seed (bytes): if specified, use this as the seed to derive other
            keys from; otherwise, use the master seed.
        context (str): context identifier to use when creating the derived key.
        keypath (str): derivation key path, a `/`-separated path of integer
            numbers representing a hierarchical path to derived keys for.
    """
    if sk is None:
        vk, pk, sk = derived_keypair(agent, context, keypath)
    bmsg = message.encode("UTF-8")
    return bytes_to_b64(sign_message(bmsg, sk))

def derived_keypair(agent, seed=None, context=None, keypath=None):
    """Returns new derived keypair using the specified agent's master key.

    Args:
        agent (str): name of the configured agent to use.
        seed (bytes): if specified, use this as the seed to derive other
            keys from; otherwise, use the master seed.
        context (str): unique context to use in deriving the key.
        keypath (str): derivation key path, a `/`-separated path of integer
            numbers representing a hierarchical path to derived keys for.

    Returns:
        tuple: `(vk, public key, secret key)` where `vk` is base64-encoded
        version of the public key, and the other two keys are `bytes`.
    """
    # Create a new seed using HKDF and the agent's master seed.
    if seed is None:
        master = get_master_seed(agent)
        mp, ms = create_keypair(master)
    else:
        mp, ms = create_keypair(seed)

    salt = keypath_to_salt(keypath)
    ctxt = context.encode("ascii")
    seed = hkdf(ms, salt, ctxt)
    pk, sk = create_keypair(seed)
    return (bytes_to_b64(pk), pk, sk)

def hkdf(master: bytes, salt: bytes, context: bytes, key_len: int = 32, num_keys: int = 1):
    """Derive one or more keys from a master secret using the HMAC-based KDF defined in RFC5869_.

    ..note:: HKDF is a key derivation method approved by NIST in `SP 800 56C`__. This code was adapted from
        :mod:`pycryptodome`.

    Args:
     master (byte string):
        The unguessable value used by the KDF to generate the other keys.
        It must be a high-entropy secret, though not necessarily uniform.
        It must not be a password.
     salt (byte string):
        A non-secret, reusable value that strengthens the randomness of the
        extraction step. Ideally, it is as long as the digest size of the chosen hash.
     key_len (integer):
        The length in bytes of every derived key.
     num_keys (integer):
        The number of keys to derive. Every key is :data:`key_len` bytes long.
     context (byte string):
        Optional identifier describing what the keys are used for.

    Return:
        A byte string or a list of byte strings.
    .. _RFC5869: http://tools.ietf.org/html/rfc5869
    .. __: http://csrc.nist.gov/publications/nistpubs/800-56C/SP-800-56C.pdf
    """
    assert num_keys < 255
    if context is None:
        context = b""
    output_len = key_len * num_keys
    prk = sha256(salt+master).digest()

    t, current = [b""],  b""
    n, tlen = 1, 0
    while tlen < output_len:
        m = sha256()
        m.update(prk + current + context + struct.pack('B', n))
        current = m.digest()
        t.append(current)
        tlen += m.digest_size
        n += 1

    derived_output = b"".join(t)
    if num_keys == 1:
        return derived_output[:key_len]
    kol = [derived_output[idx:idx + key_len] for idx in range(0, output_len, key_len)]
    return list(kol[:num_keys])


def otp_gen_key(text):
    """Generates a random encryption key that is the same length as `text`.

    Args:
        text (str): text that you want to encrypt using OTP.
    """
    return "".join(choice(string.printable) for _ in text)


def otp_encrypt(text, key):
    """Encrypts `text` using the given OTP `key`.

    Args:
        text (str): text to encrypt using OTP.
        key (str): OTP key to encrypt with; must have the same length as `text`.
    """
    assert len(text) == len(key)
    return "".join(chr(ord(i) ^ ord(j)) for (i, j) in zip(text, key))


def otp_decrypt(ciphertext, key):
    """Decrypts the OTP cipher that was generated with `key`.

    Args:
        ciphertext (str): output of the :func:`otp_encrypt`.
        key (str): same key passed to :func:`otp_encrypt` to perform the
            encryption.
    """
    return otp_encrypt(ciphertext, key)
