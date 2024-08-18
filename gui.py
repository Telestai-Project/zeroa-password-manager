import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog  # Import simpledialog for user input
from bip39_manager import BIP39Manager, PasswordVault  # Import the BIP39Manager and PasswordVault

class ZeroaPasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeroa Password Manager")  # Main window title

        # Set Telestai logo as app icon
        self.set_app_icon()

        self.bip39_manager = BIP39Manager()
        self.password_vault = None  # Will be set once the encryption key is derived

        # GUI Elements
        self.setup_ui()

    def set_app_icon(self):
        # Load the telestai.png image and set it as the icon
        try:
            self.icon_image = tk.PhotoImage(file="telestai.png")
            self.root.iconphoto(False, self.icon_image)
        except Exception as e:
            print(f"Error loading icon: {e}")

    def setup_ui(self):
        # Seed Phrase Options
        self.seed_frame = tk.LabelFrame(self.root, text="BIP-39 Seed Phrase Options")
        self.seed_frame.grid(row=0, column=0, padx=10, pady=10)

        self.generate_button = tk.Button(self.seed_frame, text="Generate New Seed Phrase", command=self.generate_seed_phrase)
        self.generate_button.grid(row=0, column=0, padx=10, pady=5)

        self.use_existing_button = tk.Button(self.seed_frame, text="Use Existing Seed Phrase", command=self.use_existing_seed)
        self.use_existing_button.grid(row=1, column=0, padx=10, pady=5)

        # Warning to the user
        self.warning_label = tk.Label(self.root, text="WARNING: Your seed phrase cannot be recovered. Store it securely.")
        self.warning_label.grid(row=2, column=0, padx=10, pady=10)

    def generate_seed_phrase(self):
        seed_phrase = self.bip39_manager.generate_seed_phrase()
        messagebox.showinfo("New Seed Phrase", f"Your new seed phrase is:\n\n{seed_phrase}\n\nPlease store it securely.", title="Seed Phrase Generated")

        # Derive the encryption key and prepare the vault
        self.setup_vault_with_seed(seed_phrase)

    def use_existing_seed(self):
        seed_phrase = self.get_seed_phrase_from_user()
        if seed_phrase:
            self.bip39_manager.use_existing_seed(seed_phrase)
            self.setup_vault_with_seed(seed_phrase)

    def get_seed_phrase_from_user(self):
        seed_phrase = simpledialog.askstring("Enter Seed Phrase", "Please enter your BIP-39 seed phrase:", title="Enter Seed Phrase")  # Use simpledialog with a title
        if seed_phrase:
            return seed_phrase.strip()
        return None

    def setup_vault_with_seed(self, seed_phrase):
        # Derive the encryption key and initialize the password vault
        encryption_key = self.bip39_manager.derive_key_from_seed()
        self.password_vault = PasswordVault(encryption_key)
        messagebox.showinfo("Encryption Setup", "Your password vault is now secured with the seed phrase.", title="Vault Secured")

        # Proceed to the password management interface
        self.show_password_manager()

    def show_password_manager(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Label the new password manager window
        self.root.title("Zeroa Password Manager - Manage Passwords")

        # Password Management Frame
        self.pwd_frame = tk.LabelFrame(self.root, text="Password Management")
        self.pwd_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.pwd_frame, text="Label:").grid(row=0, column=0, padx=5, pady=5)
        self.pwd_label = tk.Entry(self.pwd_frame)
        self.pwd_label.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.pwd_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.pwd_password = tk.Entry(self.pwd_frame, show="*")
        self.pwd_password.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.pwd_frame, text="Add Password", command=self.add_password).grid(row=2, column=0, columnspan=2, pady=10)

        # Password List Frame
        self.pwd_list_frame = tk.LabelFrame(self.root, text="Stored Passwords")
        self.pwd_list_frame.grid(row=1, column=0, padx=10, pady=10)

        self.pwd_list = tk.Listbox(self.pwd_list_frame)
        self.pwd_list.grid(row=0, column=0)

        tk.Button(self.pwd_list_frame, text="View Password", command=self.view_password).grid(row=1, column=0)
        tk.Button(self.pwd_list_frame, text="Delete Password", command=self.delete_password).grid(row=2, column=0)

        self.load_passwords()

    def add_password(self):
        label = self.pwd_label.get()
        password = self.pwd_password.get()

        if not label or not password:
            messagebox.showerror("Error", "Please fill in both fields.", title="Error")
            return

        self.password_vault.store_password(label, password)
        self.pwd_list.insert(tk.END, label)
        messagebox.showinfo("Success", f"Password for {label} stored successfully!", title="Success")

    def view_password(self):
        selected_label = self.pwd_list.get(tk.ACTIVE)
        if not selected_label:
            messagebox.showerror("Error", "Please select a password to view.", title="Error")
            return

        decrypted_password = self.password_vault.retrieve_password(selected_label)
        if decrypted_password:
            messagebox.showinfo("Password", f"The password for {selected_label} is: {decrypted_password}", title="View Password")
        else:
            messagebox.showerror("Error", "Failed to retrieve the password.", title="Error")

    def delete_password(self):
        selected_label = self.pwd_list.get(tk.ACTIVE)
        if not selected_label:
            messagebox.showerror("Error", "Please select a password to delete.", title="Error")
            return

        # Remove password from password manager
        self.password_vault.delete_password(selected_label)
        # Remove the selected label from the listbox
        self.pwd_list.delete(tk.ACTIVE)
        messagebox.showinfo("Success", f"Password for {selected_label} deleted successfully!", title="Success")

    def load_passwords(self):
        passwords = self.password_vault.load_passwords()
        for label in passwords:
            self.pwd_list.insert(tk.END, label)

if __name__ == "__main__":
    # Set className to ZeroaPasswordManager to change how the OS recognizes the app
    root = tk.Tk(className="Zeroa Password Manager")  # Change the window class name
    app = ZeroaPasswordManagerGUI(root)
    root.mainloop()

