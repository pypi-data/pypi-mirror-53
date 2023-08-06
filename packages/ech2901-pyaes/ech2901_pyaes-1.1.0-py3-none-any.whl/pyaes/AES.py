# Import base encryption and decryption functions
# Import pbkdf2_hmac to generage passwords of a fixed size based on inputs
from functools import wraps
from hashlib import pbkdf2_hmac as phash
# Import urandom to get cryptographically secure random bytes
from os import urandom

from pyaes.AESCore import encrypt_128, encrypt_192, encrypt_256, decrypt_128, decrypt_192, decrypt_256
# Import Finite(Galois) Field class
# This handles most of the math operated on values
from pyaes.Field import GF
# Import key generation function
# Generates the key schedule for a given AES size (128, 192, 256) and loops over the schedule repeatedly
# So that the keys can be used for each block of plaintext
from pyaes.Key import iter_key


# TODO finish commenting code
# TODO Create other block cipher operating modes

def encrypt_decorator():
    def func_wrapper(func):
        @wraps(func)
        def wrapper(plaintext, password, size, *, iv=None, salt=None):

            plaintext = [GF(i) for i in plaintext]
            while len(plaintext) % 16 != 0:
                # Pad at end of plaintext to make sure it always has blocks with 16 bytes of data
                plaintext.append(GF(0))
            # Add a list of list objects that represent 16 byte blocks of data
            blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]

            if salt is None:
                salt = urandom(64)

            key = iter_key([GF(i) for i in phash('sha256', password, salt, 1_000_000, size / 8)], size)

            if iv is None:
                iv = [GF(i) for i in urandom(16)]
            elif len(iv) != 16:
                raise ValueError
            else:
                iv = [GF(i) for i in iv]


            if size == 128:
                enc_func = encrypt_128
            elif size == 192:
                enc_func = encrypt_192
            elif size == 256:
                enc_func = encrypt_256
            else:
                raise ValueError

            enc_blocks, *outputs = func(blocks, key, salt, iv, enc_func)

            out = ''
            for block in enc_blocks:
                for item in block:
                    out = out + str(item)

            return (bytes.fromhex(out), *outputs)

        return wrapper
    return func_wrapper


def decrypt_decorator(*, req_iv=True, reverse=True):
    def func_wrapper(func):
        @wraps(func)
        def wrapper(ciphertext, password, size, *, iv=None, salt=None):

            if len(ciphertext) % 16 != 0:
                # Ciphertext must always have blocks with 16 bytes of data
                raise ValueError
            ciphertext = [GF(i) for i in ciphertext]
            # Add a list of list objects that represent 16 byte blocks of data
            blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

            key = iter_key([GF(i) for i in phash('sha256', password, salt, 1_000_000, size / 8)], size, reverse=reverse)

            if req_iv:
                if iv is None or len(iv) != 16:
                    raise ValueError
                else:
                    iv = [GF(i) for i in iv]

            # Determine which AES key size we will decrypt in
            # or raise a Value Error if it's not a useable size
            if size == 128:
                dec_func = decrypt_128
            elif size == 192:
                dec_func = decrypt_192
            elif size == 256:
                dec_func = decrypt_256
            else:
                raise ValueError

            dec_blocks = func(blocks, key, iv, dec_func)

            out = ''
            for block in dec_blocks:
                for item in block:
                    # For every item of every block convert to a string and append to an output string
                    if item.int == 0:
                        continue
                    out = out + str(item)

            return bytes.fromhex(out)

        return wrapper
    return func_wrapper


@encrypt_decorator()
def ecb_encrypt(blocks, key, salt, iv, enc_func):
    """
    Encrypt plaintext with the Electronic Code Book mode of operation

    :param plaintext: bytes
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param salt:  bytes=None (not required)
    :return: ciphertext: bytes, salt: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """

    for index, block in enumerate(blocks):
        blocks[index] = enc_func(block, key)
    return blocks, salt


@decrypt_decorator(req_iv=False)
def ecb_decrypt(blocks, key, _, dec_func):
    """
    Decrypt ciphertext with the Electronic Code Book mode of operation

    :param ciphertext: bytes
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param salt: bytes
    :return: plaintext: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """

    # blocks, key, _, dec_func = parser(ciphertext=ciphertext, password=password, size=size, salt=salt, reverse=True)

    for index, block in enumerate(blocks):
        # Encrypt each block with the key schedule
        blocks[index] = dec_func(block, key)

    return blocks


@encrypt_decorator()
def cbc_encrypt(blocks, key, salt, iv, enc_func):
    """
    Encrypt plaintext with the Cipher Block Chaining mode of operation

    :param plaintext: bytes
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param iv: bytes (not required but if supplied must be 16 bytes)
    :param salt: bytes (not required
    :return: ciphertext: bytes, iv: bytes, salt: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """


    xor_iv = iv.copy()

    for index, block in enumerate(blocks):
        block = [b_item ^ iv_item for b_item, iv_item in zip(block, xor_iv)]
        # Get the new iv ready and encrypt this block with the key schedule
        xor_iv = enc_func(block, key)
        # New iv is the encrypted block
        blocks[index] = xor_iv

    return blocks, iv, salt


@decrypt_decorator()
def cbc_decrypt(blocks, key, xor_iv, dec_func):
    """
    Decrypt ciphertext with the Cipher Block Chaining mode of operation

    :param ciphertext: bytes
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param iv: bytes
    :param salt: bytes
    :return: plaintext: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """

    for index, block in enumerate(blocks):
        # Get the new iv ready
        next_iv = block
        # Decrypt the block
        block = dec_func(block, key)
        # Save decrypted block by xor-ing with iv
        blocks[index] = [b_item ^ iv_item for b_item, iv_item in zip(block, xor_iv)]
        # Assign new iv
        xor_iv = next_iv

    return blocks


@encrypt_decorator()
def pcbc_encrypt(blocks, key, salt, iv, enc_func):
    """
    Encrypt plaintext using the Propagating Cipher Block Chaining
    mode of operation. Slightly more complex mode than CBC.

    :param plaintext: bytes
    :param password: bytes
    :param size: int (Must be either 128, 192, or 256)
    :param iv: bytes (not required but if supplied must be 16 bytes)
    :param salt: bytes (Can be omitted)
    :return: ciphertext: bytes, iv: bytes, salt: bytes
    """

    xor_iv = iv.copy()

    for index, block in enumerate(blocks):
        # Get the new iv ready
        new_iv = block

        for i in range(16):
            block[i] = block[i] ^ xor_iv[i]
        # Encrypt each block with the key schedule
        block = enc_func(block, key)

        # Save encrypted block
        blocks[index] = block

        for i in range(16):
            # xor each byte of the encrypted block with each byte of the unencrypted block
            # This creates the new iv for the next block
            xor_iv[i] = new_iv[i] ^ block[i]

    return blocks, iv, salt


@decrypt_decorator()
def pcbc_decrypt(blocks, key, xor_iv, dec_func):
    """
    Encrypt plaintext using the Propagating Cipher Block Chaining
    mode of operation.

    :param ciphertext: bytes
    :param password: bytes
    :param size: int (Must be either 128, 192, or 256)
    :param iv: bytes (Must be 16 bytes of data)
    :param salt: bytes
    :return: ciphertext: bytes, iv: bytes, salt: bytes
    """

    for index, block in enumerate(blocks):

        # Get the new iv ready
        new_iv = block

        # Encrypt each block with the key schedule
        block = dec_func(block, key)

        for i in range(16):
            block[i] = block[i] ^ xor_iv[i]

        # Save decrypted block
        blocks[index] = block

        for i in range(16):
            # xor each byte of the encrypted block with each byte of the unencrypted block
            # This creates the new iv for the next block
            xor_iv[i] = new_iv[i] ^ block[i]

    return blocks


@encrypt_decorator()
def cfb_stream(blocks, key, salt, iv, func):
    """
    Encrypt and decrypt data with the Cipher Block Chaining mode of operation

    :param state: bytes for encryption; str for decryption
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param iv: bytes (not required if encrypting but if supplied must be 16 bytes)
    :param salt: bytes (not required if encrypting)
    :return: if encrypting: ciphertext: bytes, iv: bytes, salt: bytes
    :return: if decrypting: plaintext: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """

    enc_iv = iv.copy()

    for index, block in enumerate(blocks):
        for i, p_item, c_item in zip(range(16), block, func(enc_iv, key)):
            block[i] = p_item ^ c_item

        enc_iv = block
        blocks[index] = block

    return blocks, iv, salt


@encrypt_decorator()
def ofb_stream(blocks, key, salt, iv, func):
    """
    Encrypt and decrypt data with the Cipher Block Chaining mode of operation

    :param state: bytes for encryption; str for decryption
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param iv: bytes (not required if encrypting but if supplied must be 16 bytes)
    :param salt: bytes (not required if encrypting)
    :return: if encrypting: ciphertext: bytes, iv: bytes, salt: bytes
    :return: if decrypting: plaintext: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """


    xor_iv = iv.copy()
    for index, block in enumerate(blocks):
        xor_iv = func(xor_iv, key)
        for i in range(16):
            block[i] = block[i] ^ xor_iv[i]
        blocks[index] = block

    return blocks, salt, iv


@encrypt_decorator()
def ctr_stream(blocks, key, salt, iv, func):
    """
    Encrypt and decrypt data with the Cipher Block Chaining mode of operation

    :param state: bytes for encryption; str for decryption
    :param password: bytes
    :param size: int (must be either 128, 192, or 256)
    :param iv: bytes (not required if encrypting but if supplied must be 16 bytes)
    :param salt: bytes (not required if encrypting)
    :return: if encrypting: ciphertext: bytes, iv: bytes, salt: bytes
    :return: if decrypting: plaintext: bytes
    :raise: ValueError: if size is not either 128, 192, or 256
    """

    xor_iv = iv.copy()

    for index, block in enumerate(blocks):
        ctr_iv = [GF(i) ^ x_item for i, x_item in zip(index.to_bytes(16, 'big'), xor_iv)]
        blocks[index] = [b_item ^ ctr_item for b_item, ctr_item in zip(block, func(ctr_iv, key))]

    return blocks, salt, iv


if __name__ == '__main__':
    pass
