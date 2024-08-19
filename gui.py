from ttkthemes import ThemedTk  # For using custom themes with Tkinter
from tkinter import ttk, messagebox, StringVar, PhotoImage
import tkinter as tk  # Switch to tk for more styling flexibility
from bip39_manager import BIP39Manager, PasswordVault  # custom classes for managing encryption and storage

class ZeroaPasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeroa Password Manager")
        self.style = ttk.Style()
        self.style.theme_use('arc')
        self.root.configure(bg="#f5f6f7")  # Set a unified light background color
        self.bip39_manager = BIP39Manager()
        self.password_vault = None

        self.bip39_word_list = self.load_bip39_words()  # Load BIP-39 word list from local file

        self.set_app_icon()
        self.setup_ui()

    def load_bip39_words(self):
        """Load the BIP-39 word list from the local file."""
        with open('bip39_wordlist.txt', 'r') as f:
            return [word.strip() for word in f.readlines()]

    def set_app_icon(self):
        # Load the telestai.png image and set it as the icon
        try:
            self.icon_image = PhotoImage(file="telestai.png")
            self.root.iconphoto(False, self.icon_image)
        except Exception as e:
            print(f"Error loading icon: {e}")

    def setup_ui(self):
        # Add padding, modern fonts, and space elements for a clean layout
        try:
            self.logo_image = PhotoImage(file="telestai.png")
            self.logo_label = ttk.Label(self.root, image=self.logo_image, background="#f5f6f7")
            self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Seed Phrase Options Frame
        self.seed_frame = ttk.LabelFrame(self.root, text="BIP-39 Seed Phrase Options", padding=(10, 10))
        self.seed_frame.grid(row=1, column=0, padx=20, pady=20)

        self.generate_button = ttk.Button(self.seed_frame, text="Generate New Seed Phrase", command=self.generate_seed_phrase)
        self.generate_button.grid(row=0, column=0, padx=10, pady=10)

        self.use_existing_button = ttk.Button(self.seed_frame, text="Use Existing Seed Phrase", command=self.use_existing_seed)
        self.use_existing_button.grid(row=1, column=0, padx=10, pady=10)

        # Warning to the user
        self.warning_label = ttk.Label(self.root, text="WARNING: Your seed phrase cannot be recovered. Store it securely.",
                                       foreground="red", background="#f5f6f7")
        self.warning_label.grid(row=2, column=0, padx=20, pady=10)

    def generate_seed_phrase(self):
        # Generate the seed phrase using the bip39_manager
        seed_phrase = self.bip39_manager.generate_seed_phrase()

        # Show the seed phrase in a messagebox
        messagebox.showinfo("Seed Phrase Generated", f"Your new seed phrase is:\n\n{seed_phrase}\n\nPlease store it securely.")

        # Derive the encryption key and prepare the vault
        self.setup_vault_with_seed(seed_phrase)

    def use_existing_seed(self):
        self.create_seed_entry_ui()  # Call to open the seed phrase input interface

    def create_seed_entry_ui(self):
        """Create a user-friendly UI for entering BIP-39 seed phrases."""
        # Clear the previous widgets
        for widget in self.root.winfo_children():
            widget.grid_forget()

        self.root.title("Enter BIP-39 Seed Phrase")

        # Create input fields for the 12-word BIP-39 seed phrase
        self.seed_phrase_vars = [StringVar() for _ in range(12)]
        self.seed_entry_frame = ttk.Frame(self.root, padding=(20, 20))
        self.seed_entry_frame.grid(row=0, column=0, padx=20, pady=20)

        ttk.Label(self.seed_entry_frame, text="Enter your 12-word BIP-39 seed phrase:").grid(row=0, column=0, columnspan=6, pady=10)

        # Create the entry fields using tk.Entry for text color change
        self.entries = []
        for i in range(12):
            entry = tk.Entry(self.seed_entry_frame, textvariable=self.seed_phrase_vars[i], width=10, font=("Arial", 12))
            entry.grid(row=(i // 6) + 1, column=i % 6, padx=5, pady=5)
            self.entries.append(entry)
            self.seed_phrase_vars[i].trace("w", lambda *args, idx=i: self.validate_word(idx))

        # Submit button to process the seed phrase
        ttk.Button(self.seed_entry_frame, text="Submit Seed Phrase", command=self.submit_seed_phrase).grid(row=3, column=0, columnspan=6, pady=10)

    def validate_word(self, idx):
        """Validate each word as it is entered and change text color based on validity."""
        word = self.seed_phrase_vars[idx].get().strip().lower()
        entry_widget = self.entries[idx]

        # Check if the word is in the BIP-39 word list
        if word in self.bip39_word_list:
            entry_widget.config(fg="green")  # Green text for valid words
        else:
            entry_widget.config(fg="red")  # Red text for invalid words

    def submit_seed_phrase(self):
        """Process the entered seed phrase."""
        seed_phrase = " ".join(var.get().strip() for var in self.seed_phrase_vars)

        # Validate before setting up the vault
        if not self.validate_seed_phrase(seed_phrase):
            messagebox.showerror("Invalid Seed", "Please enter a valid BIP-39 seed phrase.")
            return

        self.setup_vault_with_seed(seed_phrase)

    def validate_seed_phrase(self, seed_phrase):
        """Validate the entered seed phrase (check word count and validity)."""
        words = seed_phrase.split()
        return len(words) == 12 and all(word in self.bip39_word_list for word in words)

    def setup_vault_with_seed(self, seed_phrase):
        try:
            # Derive the encryption key and initialize the password vault
            encryption_key = self.bip39_manager.derive_key_from_seed(seed_phrase)  # Pass the seed
            self.password_vault = PasswordVault(encryption_key)

            # Show the encryption setup message
            messagebox.showinfo("Vault Secured", "Your password vault is now secured with the seed phrase.")

            # Proceed to the password management interface
            self.show_password_manager()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup vault: {e}")

    def show_password_manager(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Label the new password manager window
        self.root.title("Zeroa Password Manager - Manage Passwords")

        # Password Management Frame
        self.pwd_frame = ttk.LabelFrame(self.root, text="Password Management", padding=(10, 10))
        self.pwd_frame.grid(row=0, column=0, padx=20, pady=20)

        ttk.Label(self.pwd_frame, text="Label:").grid(row=0, column=0, padx=10, pady=10)
        self.pwd_label = ttk.Entry(self.pwd_frame)
        self.pwd_label.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.pwd_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.pwd_password = ttk.Entry(self.pwd_frame, show="*")
        self.pwd_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.pwd_frame, text="Add Password", command=self.add_password).grid(row=2, column=0, columnspan=2, pady=10)

        # Password List Frame
        self.pwd_list_frame = ttk.LabelFrame(self.root, text="Stored Passwords", padding=(10, 10))
        self.pwd_list_frame.grid(row=1, column=0, padx=20, pady=20)

        self.pwd_list = ttk.Treeview(self.pwd_list_frame)  # Use Treeview for a better password list display
        self.pwd_list.grid(row=0, column=0)

        ttk.Button(self.pwd_list_frame, text="View Password", command=self.view_password).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.pwd_list_frame, text="Delete Password", command=self.delete_password).grid(row=2, column=0, padx=10, pady=10)

        self.load_passwords()

    def add_password(self):
        label = self.pwd_label.get()
        password = self.pwd_password.get()

        if not label or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        self.password_vault.store_password(label, password)
        self.pwd_list.insert("", "end", text=label)

        # Show success message
        messagebox.showinfo("Success", f"Password for {label} stored successfully!")

    def view_password(self):
        selected_item = self.pwd_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a password to view.")
            return

        selected_label = self.pwd_list.item(selected_item, "text")
        decrypted_password = self.password_vault.retrieve_password(selected_label)
        if decrypted_password:
            messagebox.showinfo("View Password", f"The password for {selected_label} is: {decrypted_password}")
        else:
            messagebox.showerror("Error", "Failed to retrieve the password.")

    def delete_password(self):
        selected_item = self.pwd_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a password to delete.")
            return

        selected_label = self.pwd_list.item(selected_item, "text")
        self.password_vault.delete_password(selected_label)
        self.pwd_list.delete(selected_item)

        # Show success message
        messagebox.showinfo("Success", f"Password for {selected_label} deleted successfully!")

    def load_passwords(self):
        passwords = self.password_vault.load_passwords()
        for label in passwords:
            self.pwd_list.insert("", "end", text=label)


if __name__ == "__main__":
    root = ThemedTk(theme="arc", className="Zeroa Password Manager")
    app = ZeroaPasswordManagerGUI(root)
    root.mainloop()
