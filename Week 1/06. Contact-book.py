import json
import csv
import tkinter as tk
from tkinter import ttk, messagebox

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("900x600")
        
        # Initialize contacts
        self.contacts = self.load_contacts()
        
        # Configure styles
        self.configure_styles()
        
        # Build UI
        self.create_widgets()
        
        # Auto-save when closing window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 10), rowheight=25)
        self.style.configure("TButton", font=('Arial', 10), padding=5)
        self.style.configure("TLabel", font=('Arial', 10))
        self.style.configure("TEntry", font=('Arial', 10))
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button panel
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Add Contact", command=self.show_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Contact", command=self.show_edit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        
        # Search panel
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_contacts)
        
        # Contacts table
        self.tree = ttk.Treeview(main_frame, columns=("Name", "Phone", "Email"), show="headings")
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Phone", text="Phone", anchor=tk.W)
        self.tree.heading("Email", text="Email", anchor=tk.W)
        
        self.tree.column("Name", width=200)
        self.tree.column("Phone", width=150)
        self.tree.column("Email", width=250)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load data
        self.update_contacts_table()
    
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as file:
                contacts = json.load(file)
                # Convert old format if needed
                for name, details in contacts.items():
                    if isinstance(details, str):
                        contacts[name] = {"phone": details, "email": ""}
                return contacts
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file, indent=4)
    
    def update_contacts_table(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts to table
        for name, details in sorted(self.contacts.items()):
            self.tree.insert("", tk.END, values=(name, details["phone"], details["email"]))
    
    def show_add_dialog(self):
        self.contact_dialog("Add New Contact", self.add_contact)
    
    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit")
            return
        
        name = self.tree.item(selected[0])["values"][0]
        self.contact_dialog("Edit Contact", self.update_contact, name)
    
    def contact_dialog(self, title, save_callback, name=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # Form fields
        ttk.Label(dialog, text="Name:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Phone:").pack()
        phone_entry = ttk.Entry(dialog)
        phone_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Email:").pack()
        email_entry = ttk.Entry(dialog)
        email_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Pre-fill for edit mode
        if name:
            name_entry.insert(0, name)
            name_entry.config(state="readonly")
            phone_entry.insert(0, self.contacts[name]["phone"])
            email_entry.insert(0, self.contacts[name]["email"])
        
        # Save button
        ttk.Button(
            dialog, 
            text="Save", 
            command=lambda: self.save_contact_data(
                dialog, 
                name_entry.get().strip(), 
                phone_entry.get().strip(), 
                email_entry.get().strip(), 
                save_callback
            )
        ).pack(pady=10)
    
    def save_contact_data(self, dialog, name, phone, email, callback):
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        if not phone and not email:
            messagebox.showerror("Error", "At least phone or email is required!")
            return
        
        callback(name, phone, email)
        dialog.destroy()
        self.update_contacts_table()
    
    def add_contact(self, name, phone, email):
        if name in self.contacts:
            messagebox.showerror("Error", f"Contact '{name}' already exists!")
            return
        
        self.contacts[name] = {"phone": phone, "email": email}
        messagebox.showinfo("Success", "Contact added successfully!")
    
    def update_contact(self, name, phone, email):
        self.contacts[name] = {"phone": phone, "email": email}
        messagebox.showinfo("Success", "Contact updated successfully!")
    
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return
        
        name = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", f"Delete contact '{name}'?"):
            del self.contacts[name]
            self.update_contacts_table()
            messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def search_contacts(self, event=None):
        query = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if (query in values[0].lower() or 
                query in values[1].lower() or 
                query in values[2].lower()):
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)
    
    def export_to_csv(self):
        try:
            with open("contacts.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Phone", "Email"])
                for name, details in self.contacts.items():
                    writer.writerow([name, details["phone"], details["email"]])
            messagebox.showinfo("Success", "Contacts exported to contacts.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def on_close(self):
        self.save_contacts()
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
