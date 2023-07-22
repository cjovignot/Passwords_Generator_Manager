import os
import json
import random
import string
import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk

import qrcode
from dotenv import load_dotenv

load_dotenv()


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        ctk.deactivate_automatic_dpi_awareness()

        # Password data
        self.passwords = {}
        self.load_data()

        # GUI Widgets
        entry_font = ctk.CTkFont(family='Roboto', size=20)
        button_font = ctk.CTkFont(family='Roboto', size=20)

        self.website_name_entry = ctk.CTkEntry(self, placeholder_text="Website Name", font=entry_font, height=40)
        self.website_name_entry.grid(row=0, column=0, padx=10, pady=10)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", font=entry_font, height=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", font=entry_font, height=40)
        self.password_entry.grid(row=0, column=2, padx=10, pady=10)

        self.generate_password_button = ctk.CTkButton(
            self, text="Generate Password", command=self.generate_password, font=button_font, height=40
        )
        self.generate_password_button.grid(row=0, column=3, padx=10, pady=10)
        self.save_button = ctk.CTkButton(
            self, text="Save", command=self.save_password, font=button_font, height=40
        )
        self.save_button.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(
            self, text="Delete", command=self.delete_password, font=button_font, height=40
        )
        self.delete_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Update the window size to fit all widgets
        self.update_idletasks()

        # Search widgets
        self.create_search_widgets()

        # Text boxes to display selected password details
        self.create_text_boxes()  # Add this line to create the text boxes


    def create_text_boxes(self):
        """
        Create the text boxes to display the selected password details.
        """
        font_entry = ctk.CTkFont(family='Roboto', size=20)

        self.selected_website_label = ctk.CTkLabel(self, text="Selected Website:", font=font_entry)
        self.selected_website_label.grid(row=5, column=0, padx=10, pady=10)
        self.selected_website_entry = ctk.CTkEntry(self, font=font_entry, state=tk.DISABLED
                                                #    , fg_color="black"
                                                   )
        self.selected_website_entry.grid(row=5, column=1, padx=10, pady=10)

        self.selected_email_label = ctk.CTkLabel(self, text="Email:", font=font_entry)
        self.selected_email_label.grid(row=5, column=2, padx=10, pady=10)
        self.selected_email_entry = ctk.CTkEntry(self, font=font_entry, state=tk.DISABLED
                                                #  , fg_color="black"
                                                 )
        self.selected_email_entry.grid(row=5, column=3, padx=10, pady=10)

        self.selected_password_label = ctk.CTkLabel(self, text="Password:", font=font_entry)
        self.selected_password_label.grid(row=5, column=4, padx=10, pady=10)
        self.selected_password_entry = ctk.CTkEntry(self, font=font_entry, state=tk.DISABLED
                                                    # , fg_color="black"
                                                    )
        self.selected_password_entry.grid(row=5, column=5, padx=10, pady=10)


    def create_search_widgets(self):
        """
        Create the search widgets.
        """
        font_entry = ctk.CTkFont(family='Roboto', size=20)
        button_entry = ctk.CTkFont(family='Roboto', size=20)

        self.website_search_entry = ctk.CTkEntry(
            self, placeholder_text="Search Website", font=font_entry, height=40
        )
        self.website_search_entry.grid(row=4, column=0, padx=10, pady=10)
        self.email_search_entry = ctk.CTkEntry(
            self, placeholder_text="Search Email", font=font_entry, height=40
        )
        self.email_search_entry.grid(row=4, column=1, padx=10, pady=10)
        self.search_button = ctk.CTkButton(
            self, text="Search", command=self.search_password, font=font_entry, height=40
        )
        self.search_button.grid(row=4, column=2, padx=10, pady=10)
        self.clear_search_button = ctk.CTkButton(
            self, text="Clear Search", command=self.clear_search_fields, font=button_entry, height=40
        )
        self.clear_search_button.grid(row=4, column=3, padx=10, pady=10)

    def search_password(self):
        """
        Search for passwords associated with the entered website and email.
        """
        website_to_search = self.website_search_entry.get()
        email_to_search = self.email_search_entry.get()

        if website_to_search and email_to_search:
            for website, data in self.passwords.items():
                if data["email"] == email_to_search:
                    if website == website_to_search:
                        print(email_to_search)
                        print(data["password"])

                        # Display the matching data in the text boxes
                        self.selected_website_entry.insert(0, website)
                        self.selected_email_entry.insert(0, email_to_search)
                        self.selected_password_entry.insert(0, data["password"])
                        break


    def clear_search_fields(self):
        """
        Clear the search fields and display all passwords.
        """
        self.website_search_entry.delete(0, tk.END)
        self.email_search_entry.delete(0, tk.END)


    def generate_password(self):
        """
        Generate a random password excluding quotes and display it in the password entry field.
        """
        characters = string.ascii_letters + string.digits + string.punctuation.replace('"', "")
        password = "".join(random.choice(characters) for _ in range(16))
        self.password_entry.delete(0, tk.END)  # Clear any existing text
        self.password_entry.insert(0, password)

    def save_password(self):
        """
        Save the password data to the passwords dictionary.
        """
        website_name = self.website_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if website_name and email and password:
            self.passwords[website_name] = {"email": email, "password": password}
            self.clear_entry_fields()
            self.save_data()

    def delete_password(self):
        """
        Delete the selected password from the passwords dictionary.
        """
        selected_website = self.get_selected_website()
        if selected_website:
            del self.passwords[selected_website]
            self.clear_entry_fields()
            self.save_data()

    def show_selected_password(self, event):
        """
        Display the selected password details in the entry fields.
        """
        selected_website = self.get_selected_website()
        if selected_website:
            password_data = self.passwords[selected_website]
            self.selected_website_entry.set(selected_website)
            self.selected_email_entry.set(password_data["email"])
            self.selected_password_entry.set(password_data["password"])

    def get_selected_website(self):
        """
        Get the selected website from the password listbox.
        """
        selected_index = self.password_listbox.curselection()
        if selected_index:
            return self.password_listbox.get(selected_index[0])
        return None


    def clear_entry_fields(self):
        """
        Clear the entry fields.
        """
        self.website_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def load_data(self):
        """
        Load password data from a JSON file.
        """
        try:
            with open("passwordsTK.json", "r") as file:
                self.passwords = json.load(file)
        except FileNotFoundError:
            self.passwords = {}

    def save_data(self):
        """
        Save the password data to a JSON file.
        """
        with open("passwordsTK.json", "w") as file:
            json.dump(self.passwords, file)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
