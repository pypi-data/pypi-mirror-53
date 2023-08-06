# pyaes

## Description

This is my attempt to implement the AES encryption algorithm in Python 3.7.

This is my first real project that has taken a while to study and understand the mathematics behind the scenes in how it operates and also my first project uploaded to Github so that I can learn how to properly use version control software as well.



End goal is to be used in the creation of a password manager system.


## Installation

Package can be installed with pip via:

pip install ech2901-pyaes

## Simple Use Case
import pyaes.AES as aes

ciphertext, salt = aes.ecb_encrypt(b'test', b'password')

plaintext = aes.ecb_decrypt(ciphertext, b'password', salt=salt)