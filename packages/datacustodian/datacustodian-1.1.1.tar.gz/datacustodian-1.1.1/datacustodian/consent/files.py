"""Functions for handling the sharding, encryption, and sharing of files that
are authorized by verifiable credentials.
"""
from io import BufferedWriter
import random
from operator import itemgetter

from datacustodian.db import databases
from datacustodian.crypto import derived_keypair, anon_crypt_message, anon_decrypt_message
from datacustodian.ipfs import agent, cluster

def serve(cid) -> bytes:
    """Serves the file with the specified CID by collecting the encrypted shards
    and putting them back together.

    Args:
        cid (str): IPFS CID of the *unencrypted*, original file collection.
    """
    if cid not in databases.acl.db:
        return None

    with databases.acl[cid] as doc:
        shards = doc.get("shards", {})
        seed = b64_to_bytes(doc["seed"])

    if len(shards) == 0:
        return None

    result = BufferedWriter()
    for _cid, item in sorted(shards.items(), key=lambda i: i[1]["i"]):
        keypath = f"/1/{item['i']}"
        vk, pk, sk = derived_keypair(seed, cid, keypath)
        encrypted = agent.block.get(_cid)
        s = result.write(anon_decrypt_message(encrypted, pk, sk))
        assert s == item["size"]

    result.seek(0)
    return result

def _add_ipfs_block(seed, cid, block, i):
    """Adds the specified block of bytes to IPFS *as a block*.

    Args:
        block (bytes): raw bytes to add; note that they will be encrypted before
            being stored.
        i (int): integer order of this block in the file.
    """
    keypath = f"/1/{i}"
    vk, pk, sk = derived_keypair(seed, cid, keypath)
    encrypted = anon_crypt_message(block, pk)
    return client.block.put(encrypted)

def shard(cid, block_size=512*1024):
    """Shards the contents of the specified CID using the *unencrypted* version,
    then the shards are encrypted and stored in IPFS. Knowledge of how to rebuild
    the file is contained in the `acl` database.

    Args:
        cid (str): the CID of the object to shard, encrypt and store as encrypted
            blocks in IPFS.
    """
    # Get the unique random seed and initialize the shards container.
    with databases.acl[cid] as doc:
        if "shards" not in doc:
            doc["shards"] = {}
        seed = b64_to_bytes(doc["seed"])

    size = agent.object.stat(cid)["CumulativeSize"]
    indices = list(range(0, size, block_size))
    rands = list(range(len(indices)))
    random.shuffle(rands)
    steps = sorted(zip(indices, rands), key=itemgetter(1))

    for offset, index in steps:
        if index == len(indices) - 1:
            block = agent.cat(cid, offset=offset)
        else:
            block = agent.cat(cid, offset=offset, length=block_size)

        r = _add_ipfs_block(block, index)

        with databases.acl[cid] as doc:
            doc["shards"][r["Key"]] = {
                "i": count,
                "size": r["Size"]
            }
