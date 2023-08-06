import unittest

from pyaes.AES import cbc_encrypt, cbc_decrypt
from pyaes.AES import cfb_stream, ofb_stream, ctr_stream
from pyaes.AES import ecb_encrypt, ecb_decrypt
from pyaes.AES import pcbc_encrypt, pcbc_decrypt


class TestECB(unittest.TestCase):

    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ecb_encrypt(self.plaintext, self.password, 128, salt=self.salt)

        new_plaintext = ecb_decrypt(ciphertext, self.password, 128, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ecb_encrypt(self.plaintext, self.password, 192, salt=self.salt)

        new_plaintext = ecb_decrypt(ciphertext, self.password, 192, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ecb_encrypt(self.plaintext, self.password, 256, salt=self.salt)

        new_plaintext = ecb_decrypt(ciphertext, self.password, 256, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)


class TestCBC(unittest.TestCase):
    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'
        self.iv = b'this is a bad IV'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cbc_encrypt(self.plaintext, self.password, 128, iv=self.iv, salt=self.salt)

        new_plaintext = cbc_decrypt(ciphertext, self.password, 128, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cbc_encrypt(self.plaintext, self.password, 192, iv=self.iv, salt=self.salt)

        new_plaintext = cbc_decrypt(ciphertext, self.password, 192, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cbc_encrypt(self.plaintext, self.password, 256, iv=self.iv, salt=self.salt)

        new_plaintext = cbc_decrypt(ciphertext, self.password, 256, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)


class TestPCBC(unittest.TestCase):
    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'
        self.iv = b'this is a bad IV'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = pcbc_encrypt(self.plaintext, self.password, 128, iv=self.iv, salt=self.salt)

        new_plaintext = pcbc_decrypt(ciphertext, self.password, 128, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = pcbc_encrypt(self.plaintext, self.password, 192, iv=self.iv, salt=self.salt)

        new_plaintext = pcbc_decrypt(ciphertext, self.password, 192, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = pcbc_encrypt(self.plaintext, self.password, 256, iv=self.iv, salt=self.salt)

        new_plaintext = pcbc_decrypt(ciphertext, self.password, 256, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext)


class TestCFB(unittest.TestCase):
    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'
        self.iv = b'this is a bad IV'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cfb_stream(self.plaintext, self.password, 128, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = cfb_stream(ciphertext, self.password, 128, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cfb_stream(self.plaintext, self.password, 192, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = cfb_stream(ciphertext, self.password, 192, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = cfb_stream(self.plaintext, self.password, 256, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = cfb_stream(ciphertext, self.password, 256, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))


class TestOFB(unittest.TestCase):
    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'
        self.iv = b'this is a bad IV'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ofb_stream(self.plaintext, self.password, 128, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ofb_stream(ciphertext, self.password, 128, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ofb_stream(self.plaintext, self.password, 192, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ofb_stream(ciphertext, self.password, 192, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ofb_stream(self.plaintext, self.password, 256, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ofb_stream(ciphertext, self.password, 256, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))


class TestCTR(unittest.TestCase):
    def setUp(self):
        self.plaintext = b'Hello, world!'
        self.password = b'test key please ignore'
        self.salt = b'No salt please'
        self.iv = b'this is a bad IV'

    def test_128_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ctr_stream(self.plaintext, self.password, 128, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ctr_stream(ciphertext, self.password, 128, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_192_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ctr_stream(self.plaintext, self.password, 192, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ctr_stream(ciphertext, self.password, 192, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

    def test_256_base(self):
        # Test for reversibility of encryption

        ciphertext, *_ = ctr_stream(self.plaintext, self.password, 256, iv=self.iv, salt=self.salt)

        new_plaintext, *_ = ctr_stream(ciphertext, self.password, 256, iv=self.iv, salt=self.salt)

        self.assertEqual(self.plaintext, new_plaintext.strip(b'\x00'))

if __name__ == '__main__':
    AES_Suite = unittest.TestSuite()

    AES_Suite.addTest(TestECB())
    AES_Suite.addTest(TestCBC())
    AES_Suite.addTest(TestPCBC())
    AES_Suite.addTest(TestCFB())
    AES_Suite.addTest(TestOFB())
    AES_Suite.addTest(TestCTR())

    AES_Suite.run(unittest.TestResult())
