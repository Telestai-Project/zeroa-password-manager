from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum
from Crypto.Cipher import AES
import json
import os

class BIP39Manager:
    def __init__(self):
        self.seed_phrase = None
        self.encryption_key = None

    # Generate a new BIP-39 seed phrase
    def generate_seed_phrase(self):
        # Correct value for 12-word mnemonic
        self.seed_phrase = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        return self.seed_phrase

    # Use an existing seed phrase
    def use_existing_seed(self, seed_phrase):
        self.seed_phrase = seed_phrase
        return self.seed_phrase

    # Derive the encryption key from the provided seed phrase
    def derive_key_from_seed(self, seed_phrase):
        self.seed_phrase = seed_phrase
        seed_bytes = Bip39SeedGenerator(self.seed_phrase).Generate()
        self.encryption_key = seed_bytes[:32]  # Use the first 32 bytes for AES encryption
        return self.encryption_key

class PasswordVault:
    def __init__(self, encryption_key):
        self.file_path = "passwords.json"
        self.encryption_key = encryption_key

    # Encrypt the password vault
    def encrypt_password_vault(self, password_vault):
        cipher = AES.new(self.encryption_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(password_vault).encode('utf-8'))
        return cipher.nonce, ciphertext, tag

    # Decrypt the password vault
    def decrypt_password_vault(self, nonce, ciphertext, tag):
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8'))

    # Save the encrypted password vault to file
    def save_encrypted_vault(self, nonce, ciphertext, tag):
        vault_data = {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "tag": tag.hex(),
        }
        with open(self.file_path, 'w') as f:
            json.dump(vault_data, f)

    # Load the encrypted password vault from file
    def load_encrypted_vault(self):
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, 'r') as f:
            try:
                data = json.load(f)
                if "nonce" not in data or "ciphertext" not in data or "tag" not in data:
                    raise KeyError("Missing required fields in password file")
                nonce = bytes.fromhex(data["nonce"])
                ciphertext = bytes.fromhex(data["ciphertext"])
                tag = bytes.fromhex(data["tag"])
                return nonce, ciphertext, tag
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Failed to load or parse the vault: {e}")
                return None

    # Load passwords from the encrypted vault file
    def load_passwords(self):
        encrypted_vault = self.load_encrypted_vault()
        if encrypted_vault:
            nonce, ciphertext, tag = encrypted_vault
            try:
                decrypted_vault = self.decrypt_password_vault(nonce, ciphertext, tag)
                return decrypted_vault
            except Exception as e:
                print(f"Failed to decrypt vault: {e}")
                return {}
        return {}

    # Store a password in the vault
    def store_password(self, label, password):
        passwords = self.load_passwords()
        passwords[label] = password
        nonce, ciphertext, tag = self.encrypt_password_vault(passwords)
        self.save_encrypted_vault(nonce, ciphertext, tag)

    # Retrieve a password from the vault
    def retrieve_password(self, label):
        passwords = self.load_passwords()
        return passwords.get(label, None)

    # Delete a password from the vault
    def delete_password(self, label):
        passwords = self.load_passwords()
        if label in passwords:
            del passwords[label]
            nonce, ciphertext, tag = self.encrypt_password_vault(passwords)
            self.save_encrypted_vault(nonce, ciphertext, tag)
