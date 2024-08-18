import json
import os
from encryption import EncryptionManager

class PasswordManager:
    def __init__(self, private_key):
        self.file_path = "passwords.json"
        self.encryption_manager = EncryptionManager(private_key)

    def store_password(self, label, password):
        # Encrypt the password
        nonce, ciphertext, tag = self.encryption_manager.encrypt(password)
        data = {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "tag": tag.hex(),
        }

        # Load existing passwords and add the new password
        passwords = self.load_passwords()
        passwords[label] = data
        self.save_passwords(passwords)

    def load_passwords(self):
        # If the passwords file doesn't exist, return an empty dictionary
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, 'r') as f:
                data = f.read().strip()
                if not data:  # If the file is empty
                    return {}
                return json.loads(data)  # Attempt to load the JSON data
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is not found or contains invalid JSON, return an empty dictionary
            return {}

    def save_passwords(self, passwords):
        # Save the passwords to the JSON file
        with open(self.file_path, 'w') as f:
            json.dump(passwords, f)

    def delete_password(self, label):
        passwords = self.load_passwords()
        if label in passwords:
            del passwords[label]
            self.save_passwords(passwords)

    def retrieve_password(self, label):
        passwords = self.load_passwords()
        if label in passwords:
            data = passwords[label]
            nonce = bytes.fromhex(data["nonce"])
            ciphertext = bytes.fromhex(data["ciphertext"])
            tag = bytes.fromhex(data["tag"])
            return self.encryption_manager.decrypt(nonce, ciphertext, tag)
        return None
