from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

class EncryptionManager:
    def __init__(self, private_key):
        salt = b'some_salt_value'
        # Derive encryption key from the private key
        self.key = PBKDF2(private_key, salt, dkLen=32)

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return cipher.nonce, ciphertext, tag

    def decrypt(self, nonce, ciphertext, tag):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
