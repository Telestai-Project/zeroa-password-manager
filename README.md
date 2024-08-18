# Zeroa Password Manager

**Zeroa** is an **open-source**, **experimental password manager** that allows users to encrypt and decrypt their password vault using a BIP-39 seed phrase from any blockchain wallet (e.g., Bitcoin, Ethereum). This project explores a decentralized, cryptographic approach to password management, providing an innovative solution for securing your vault with blockchain-derived seed phrases.

---

## ⚠️ Experimental Status

Zeroa is currently in the **experimental phase** and **not ready for production use**. We are actively developing the core features, and the security model is still evolving. **We invite crypto developers, cryptographers, and blockchain enthusiasts** to join us in refining and enhancing this project.

> **Note:** This password manager is actively being produced by **Telestai**.

---

## 🚀 Features

- **BIP-39 Seed Encryption**: Encrypt and decrypt your password vault using any BIP-39 compatible seed phrase.
- **Simple Local Storage**: Passwords are securely encrypted and stored locally on your device.
- **Minimal UI**: Intuitive user interface for adding, viewing, and deleting passwords.
- **Blockchain Focused**: Built with crypto enthusiasts in mind, leveraging the blockchain ecosystem for encryption.
- **Open-Source**: Fully open for anyone to contribute and improve.

### Coming Soon:
- **Cross-Device Password Recovery**: We're working on enabling secure password vault restoration using your seed phrase across multiple devices. This is a key feature in progress, and we invite contributions from the community.

---

## 💰 Bounty Program

We're launching a **Bounty Program** to attract contributions from developers passionate about blockchain, cryptography, and decentralized applications!

### Current Bounties:
- **Cross-Device Vault Recovery**: Help implement secure, decentralized password recovery across devices.
- **UI/UX Improvements**: Improve the user interface and user experience of the Zeroa Password Manager.
- **Blockchain Integrations**: Explore using other blockchain networks for storing encrypted vaults.
- **Security Audits**: Conduct a security audit of the encryption and storage mechanism to identify vulnerabilities.

Interested? Start contributing, and you may receive a **bounty reward** based on the complexity and importance of your contribution.

---

## 🛠️ Installation

To install and run Zeroa locally:

```bash
# Clone the repository
git clone https://github.com/Telestai-Project/zeroa-password-manager.git

# Navigate to the project directory
cd zeroa-password-manager

# Install the required dependencies
pip install -r requirements.txt

# Run the application
python3 gui.py
```

### Requirements

- Python 3.6+
- BIP-39 (via `bip-utils`)
- Tkinter (for the GUI)
- pycryptodome (for AES encryption)

---

## 🤝 Contributions

We welcome contributions from developers of all experience levels! Whether you want to help build features, audit security, or provide feedback, we'd love to have you on board.

### How to Contribute

1. **Fork the repository**: Click the "Fork" button on the top right of this GitHub page to create your own copy of the repository.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/Telestai-Project/zeroa-password-manager.git
   cd zeroa-password-manager
   ```
3. **Create a new branch** for your changes:
   ```bash
   git checkout -b your-feature-branch
   ```
4. **Make your changes**, then commit and push them:
   ```bash
   git commit -m "Add feature"
   git push origin your-feature-branch
   ```
5. **Submit a pull request**: Once you're happy with your changes, submit a PR back to the main repository. We'll review it and discuss any feedback.

### Community

- **Join our Discord**: For questions, feedback, or to claim a bounty, join our [Discord community](https://discord.gg/VmFXfHnZE5). This is the best place to connect with the team and other contributors.

---

## 📄 License

Zeroa is licensed under the [MIT License](LICENSE), making it freely available for anyone to use, modify, and distribute.

---

We encourage anyone interested in blockchain technology, cryptography, or password management to contribute to Zeroa and help shape the future of decentralized password security!